import dbus
import dbus.service
import json
import logging
import os
import psutil
import re
import subprocess
import sys

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import gi
from gi.repository import GLib

logging.basicConfig(level=logging.INFO)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MAPPING_SCRIPT_PATH = DIR_PATH + '/mapping_scripts/'
CONFIG_FILE_PATH = DIR_PATH + '/app_mapping.json'

OPATH = '/org/schorsch/mousekeymapper'
IFACE = 'org.schorsch.mousekeymapper'
BUS_NAME = 'org.schorsch.mousekeymapper'

CURRENT_MAPPING = ''

class Mouse_Remapper(dbus.service.Object):

    def __init__(self):
        bus = dbus.SessionBus()
        bus.request_name(BUS_NAME)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)
        self.shortcut_watchdog = Shortcut_Watchdog()
        with open(CONFIG_FILE_PATH, 'r') as configfile:
            self.config = json.load(configfile)
        logging.debug(f'Mouse_Remapper initialized...')

    @dbus.service.method(dbus_interface=IFACE + '.LoadMapping', in_signature='si', out_signature='')
    def LoadMapping(self, window_title, pid):
        logging.debug(f'DBus message received, checking mappings...')
        mapping_script = self.find_match(window_title, pid)
        if not mapping_script:
            logging.debug(f'no match found for {window_title=} or {pid=}')
            mapping_script = [ app for app in self.config if app['match-type'] == '__DEFAULT__' ][0]['mapping-script']
        global CURRENT_MAPPING
        if mapping_script == CURRENT_MAPPING:
            return
        if self.shortcut_watchdog.global_shortcut_active():
            self.shortcut_watchdog.defer_mapping(mapping_script)
            return
        run_mapping(mapping_script)

    def find_match(self, window_title, pid):
        for config in [config for config in self.config if config['match-type'] != '__DEFAULT__' ]:
            match config['match-type']:
                case 'window-title':
                    logging.debug(f'trying to match {window_title=} to {config=}')
                    all_patterns_match = True
                    for pattern in config['match-patterns']:
                        if not re.match(pattern, window_title):
                            all_patterns_match = False
                            break
                    if all_patterns_match:
                        return config['mapping-script']
                    continue
                case 'cmdline':
                    cmdline = psutil.Process(pid).cmdline()
                    logging.debug(f'trying to match {cmdline=} to {config=}')
                    for pattern in config['match-patterns']:
                        pattern_matches_any_arg = False
                        for arg in cmdline:
                            if re.match(pattern, arg):
                                pattern_matches_any_arg = True
                                break
                        if not pattern_matches_any_arg:
                            break
                    if not pattern_matches_any_arg:
                        continue
                    return config['mapping-script']



class Shortcut_Watchdog:

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

    def defer_mapping(self, mapping_script):
        self.pending_mapping_script = mapping_script

def run_mapping(mapping_script):
    global CURRENT_MAPPING
    subprocess.call(args=MAPPING_SCRIPT_PATH + mapping_script, shell=True)
    CURRENT_MAPPING = mapping_script
    logging.info(f'Mapping {mapping_script} loaded...')

if __name__ == '__main__':
    a = Mouse_Remapper()
    loop = GLib.MainLoop()
    loop.run()
