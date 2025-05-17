import dbus
import dbus.service
import subprocess
import json
import os
import sys

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import gi
from gi.repository import GLib

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MAPPING_SCRIPT_PATH = DIR_PATH + '/mapping_scripts/'

OPATH = '/org/schorsch/mousekeymapper'
IFACE = 'org.schorsch.mousekeymapper'
BUS_NAME = 'org.schorsch.mousekeymapper'

CURRENT_MAPPING = ''

with open(DIR_PATH + '/app_mapping.json', 'r') as configfile:
    CONFIG = json.load(configfile)

class MouseRemapper(dbus.service.Object):

    def __init__(self):
        bus = dbus.SessionBus()
        bus.request_name(BUS_NAME)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)
        self.shortcut_watchdog = ShortcutWatchdog()

    @dbus.service.method(dbus_interface=IFACE + '.LoadMapping',
                         in_signature='s', out_signature='')
    def LoadMapping(self, window_title):
        app = [ app for app in CONFIG if app['window-title'] == window_title ]
        if not app:
            mapping_script = [ app for app in CONFIG if app['window-title'] == '__DEFAULT__' ][0]['mapping-script']
        else:
            mapping_script = app[0]['mapping-script']
        global CURRENT_MAPPING
        if mapping_script == CURRENT_MAPPING:
            return
        if self.shortcut_watchdog.global_shortcut_active():
            self.shortcut_watchdog.wait_for_release(mapping_script)
            return
        run_mapping(mapping_script)

class ShortcutWatchdog:

    def __init__(self):
        listener_bus = dbus.SessionBus()
        listener_bus.add_signal_receiver(
            self.handle_active_global_shortcut,
            bus_name='org.kde.kglobalaccel',
            interface_keyword='interface',
            member_keyword='member',
            path_keyword='path',
            message_keyword='msg'
        )
        self.active_global_shortcuts = set()
        self.pending_mapping_script = ''

    def handle_active_global_shortcut(self, *args, **kwargs):
        if kwargs['member'] == 'globalShortcutPressed':
            self.active_global_shortcuts.add(args[1])
            return
        if kwargs['member'] == 'globalShortcutReleased':
            try:
                self.active_global_shortcuts.remove(args[1])
            except KeyError:
                pass
            if len(self.active_global_shortcuts) == 0 and self.pending_mapping_script:
                run_mapping(self.pending_mapping_script)
                self.pending_mapping_script = ''
            return

    def global_shortcut_active(self):
        return len(self.active_global_shortcuts) > 0

    def wait_for_release(self, mapping_script):
        self.pending_mapping_script = mapping_script

def run_mapping(mapping_script):
    global CURRENT_MAPPING
    subprocess.call(args=MAPPING_SCRIPT_PATH + mapping_script, shell=True)
    CURRENT_MAPPING = mapping_script
    print(f'Mapping {mapping_script} loaded...')
    sys.stdout.flush()

if __name__ == '__main__':
    a = MouseRemapper()
    loop = GLib.MainLoop()
    loop.run()
