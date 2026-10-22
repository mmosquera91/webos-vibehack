#!/usr/bin/env python3
"""Make the Home button open the launcher instead of LG's home.

webOS does not let an app replace Home, or even see which app is in front, so this runs on
another always-on device on the same network (a Mac, a Raspberry Pi, a phone in Termux). It
watches the foreground app over the TV's remote-control service and, the moment LG's home
appears, launches the launcher on top. LG's home shows for about half a second.

Press Home twice within ESCAPE_SECONDS to stay on LG's home (for its menus).

    python3 home-watch.py 192.168.1.50

Needs: pip install websockets. Pair once first (sync-apps.py does it).
"""
import asyncio
import json
import os
import sys
import time

import lgtv

LAUNCHER = "com.gathin.tvhome"
LG_HOME = "com.webos.app.home"
ESCAPE_SECONDS = 4.0   # second Home press within this window (after the bounce window) = stay on LG home
BOUNCE_SECONDS = 1.8   # LG home reappearing this soon after our launch = focus bounce, relaunch
MAX_BOUNCES = 2
LAUNCH_DELAY = 0.6


def log(*args):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *args, flush=True)


async def watch(host):
    ws = await lgtv.session(host, ping_interval=10, ping_timeout=10)
    log("connected to", host)
    last_redirect = 0.0
    bounces = 0
    try:
        await ws.send(json.dumps({"type": "subscribe", "id": "fg",
                                  "uri": "ssap://com.webos.applicationManager/getForegroundAppInfo",
                                  "payload": {}}))
        async for raw in ws:
            msg = json.loads(raw)
            if msg.get("id") != "fg":
                continue
            app = msg.get("payload", {}).get("appId")
            if os.environ.get("HW_DEBUG"):
                log("fg:", app, json.dumps(msg.get("payload", {}))[:200])
            if app != LG_HOME:
                continue
            now = time.monotonic()
            since = now - last_redirect
            # webOS 6 (UP77): LG home grabs focus back ~1 s after our launch. Treat that as a
            # bounce and relaunch, not as a second Home press.
            if since < BOUNCE_SECONDS and bounces < MAX_BOUNCES:
                bounces += 1
                await asyncio.sleep(LAUNCH_DELAY)
                await ws.send(json.dumps({"type": "request", "id": "launch", "uri": "ssap://system.launcher/launch",
                                          "payload": {"id": LAUNCHER}}))
                last_redirect = time.monotonic()
                log(f"LG home bounced back -> launcher again ({bounces})")
                continue
            if since < ESCAPE_SECONDS:
                log("Home pressed twice: staying on LG home")
                last_redirect = 0.0
                continue
            bounces = 0
            # Let LG home finish its own launch first, so it doesn't steal focus back.
            await asyncio.sleep(LAUNCH_DELAY)
            await ws.send(json.dumps({"type": "request", "id": "launch", "uri": "ssap://system.launcher/launch",
                                      "payload": {"id": LAUNCHER}}))
            last_redirect = time.monotonic()
            log("LG home -> launcher")
    finally:
        await ws.close()


async def main(host):
    delay = 5
    while True:
        try:
            await watch(host)
            delay = 5
        except (OSError, asyncio.TimeoutError, lgtv.websockets.WebSocketException) as e:
            # TV off, in standby or off the network: keep trying, but back off.
            log("not connected:", type(e).__name__, e)
            delay = min(delay * 2, 20)
        await asyncio.sleep(delay)


if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TV_HOST")
    if not host:
        sys.exit("usage: home-watch.py <TV IP>")
    try:
        asyncio.run(main(host))
    except KeyboardInterrupt:
        pass
