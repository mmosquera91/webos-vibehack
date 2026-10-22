// Launcher configuration. Edit this file, then run webos-launcher/install.sh.
// App ids: run `python3 sync-apps.py --list` (or look in app/apps.js after a sync).
window.CONFIG = {
  // Apps pinned to the dock row at the bottom, in this order. Missing apps are skipped.
  dockApps: ['netflix', 'cdp-30', 'com.crunchyroll.webapp', 'youtube.leanback.v4'],

  // First apps of the grid, right below the dock, in this order. The rest follow alphabetically.
  gridFirst: ['com.disney.disneyplus-prod', 'amazon', 'org.jellyfin.webos'],

  // Apps never shown as tiles (inputs and Live TV are already in the Inputs menu).
  hiddenApps: [
    'com.gathin.tvhome',
    'com.webos.app.livetv',
    'com.webos.app.hdmi1', 'com.webos.app.hdmi2', 'com.webos.app.hdmi3', 'com.webos.app.hdmi4',
    // LG junk
    'com.webos.app.lgchannels', 'lgchannels.gip',
    'com.webos.app.sportsteamsettings',   // Sports Alert
    'com.webos.app.homeconnect',          // Home Dashboard
    'com.twin.app.gamingportal',          // LG Gaming Portal
    'com.playworks.app.fruitmatch',
    'com.blacknutbuystreamwopmlp.app',    // My Little Puppy
    'epoxyaisports',                      // LG Sports Playbook
    'webos.day',                          // LG Streaming Week
    'com.miniclip.eightballpool',
    'amazon.alexa.view',
    'shortcutcopilot',
    // Maintenance (still in LG's app list)
    'com.palmdts.devmode',
    'org.webosbrew.hbchannel',
    'com.pirate.refresh',
    // Old duplicate HBO Max (keep com.wbd.hbomax)
    'com.hbo.hbomax'
  ],

  // The Live TV app, offered at the end of the Inputs menu. Leave empty to omit.
  liveTvApp: 'com.webos.app.livetv',

  // Tiles per row in the grid; the dock always has this many slots.
  columns: 4
};
