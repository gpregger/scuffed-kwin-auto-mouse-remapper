function sendWindowTitle(window) {
    callDBus('org.schorsch.mousekeymapper',
             '/org/schorsch/mousekeymapper',
             'org.schorsch.mousekeymapper.LoadMapping',
             'LoadMapping',
             window.caption,
             window.pid)
}

workspace.windowActivated.connect(sendWindowTitle);

