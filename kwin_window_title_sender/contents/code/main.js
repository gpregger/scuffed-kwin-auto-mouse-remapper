function sendWindowTitle(window) {
    callDBus('org.schorsch.mousekeymapper',
             '/org/schorsch/mousekeymapper',
             'org.schorsch.mousekeymapper.LoadMapping',
             'LoadMapping',
             window.caption)
}

workspace.windowActivated.connect(sendWindowTitle);

