import dbus
import dbus.service
import subprocess
import json
import os 

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

import gi
from gi.repository import GLib

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
MAPPING_SCRIPT_PATH = DIR_PATH + '/mapping_scripts/'

OPATH = '/org/schorsch/mousekeymapper'
IFACE = 'org.schorsch.mousekeymapper'
BUS_NAME = 'org.schorsch.mousekeymapper'

with open(DIR_PATH + '/app_mapping.json', 'r') as configfile:
    CONFIG = json.load(configfile)

class Example(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        bus.request_name(BUS_NAME)
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        dbus.service.Object.__init__(self, bus_name, OPATH)

    @dbus.service.method(dbus_interface=IFACE + '.LoadMapping',
                         in_signature='s', out_signature='')
    def LoadMapping(self, window_title):
        app = [ app for app in CONFIG if app['window-title'] == window_title ]
        if not app:
            mapping_script = [ app for app in CONFIG if app['window-title'] == '__DEFAULT__' ][0]['mapping-script']
        else:
            mapping_script = app[0]['mapping-script']
        subprocess.call(args=MAPPING_SCRIPT_PATH + mapping_script, shell=True)


if __name__ == '__main__':
    a = Example()
    loop = GLib.MainLoop()
    loop.run()
