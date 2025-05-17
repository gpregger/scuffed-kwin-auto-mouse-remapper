# Scuffed Auto Mouse Key Remapping with Kwin and DBus
This is the result of a spontaneous 6h pre-weekend crunch trying to somewhat replicate the Logitech G Hub functionality of having per application mouse profiles.  
It's pretty scuffed but hey, it works so far (not that I've tested it for more than 5 minutes as of writing this).  
If this acutally ends up working mid to long term, consider my mind somewhat boggled that it took this long to produce something like this.  
Though to be fair, scope of application is a bit narrow, seeing as this is very KDE specific.  

## Working Principle
1. 'kwin-auto-mouse-remapper-dbus-service.py' runs as a systemd service using 'kwin-auto-mouse-remapper.service'
2. This python script loads 'app_mapping.json' which contains the rules about which window gets which mapping script. simple.
2. 'kwin_window_title_sender' runs in the background as a KWin script. This connects to the workspace.windowActivated signal and with every window focus change reports the title of the active window to the DBus service 'org.schorsch.mousekeymapper' provided by 'kwin-auto-mouse-remapper-dbus-service.py'
3. 'kwin-auto-mouse-remapper-dbus-service.py' then decides based on the received window title which script to run from the 'mapping_scripts' folder. This folder can contain arbitrary shell scripts (YOLO), but I filled them with something like this:  
```bash
#!/usr/bin/bash
# keybind_elite_dangerous.sh

kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton1 "Key,X" --notify             # Throttle to 0
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton2 "Key,U" --notify             # Deploy / Retract Hardpoints
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton4 "Key,J" --notify             # Toggle Frame Shift Drive
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton5 "Key,T" --notify             # Select Target Ahead
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton6 "Key,N" --notify             # Cycle Next Fire Group
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton7 "Key,Z" --notify             # Toggle Flight Assist
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton8 "Key,L" --notify             # Landing Gear
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton9 "Key,Home" --notify          # Cargo Scoop
```
Along with this rule in 'app_mapping.json':  
```json
    {
        "window-title": "Elite - Dangerous (CLIENT)",
        "mapping-script": "keybind_elite_dangerous.sh"
    }

```
which automagically configures the extra buttons on my mouse for Elite Dangrous as if you'd set them in the Plasma System settings. Seems pretty reliable. More reliable than Piper in any case, fucking rat-shit...  
Well to be fair you do need Piper to set all your Gamerbuttons to something generic first. But that's a one and done kinda deal.  

Also make sure there is a "\_\_DEFAULT__" 'app' in the 'app_mapping.json', this is the mapping that applies if no other match is found. A valid 'app_mapping.json' would be:  
```json
[
    {
        "window-title": "__DEFAULT__",
        "mapping-script": "keybind_desktop.sh"
    },
    {
        "window-title": "Elite - Dangerous (CLIENT)",
        "mapping-script": "keybind_elite_dangerous.sh"
    }
]
```
And of course both 'keybind_desktop.sh' and 'keybind_elite_dangerous.sh' need to be present in the 'mapping_scripts' folder and be executable.

## Installation
0. Clone the repo to where you're ok for it to stay
1. Open the repo folder in a terminal
2. Create a python venv, eg `python -m venv .venv` and enable the venv, eg `source .venv/bin/activate`
3. Install required python packages `pip install -r requirements.txt`
4. Adjust the 'ExecStart' path in the kwin-auto-mouse-remapper.service systemd unit file. It needs to point to the python executable from your venv followed by the path to kwin-auto-mouse-remapper-dbus-service.py. eg `ExecStart=/home/coolname/scripts/scuffed-kwin-auto-mouse-remapper/.venv/bin/python /home/coolname/scripts/scuffed-kwin-auto-mouse-remapper/win-auto-mouse-remapper-dbus-service.py`
5. Install the service file by copying to /usr/lib/systemd/user/: `sudo cp kwin-auto-mouse-remapper.service /usr/lib/systemd/user/`
6. Enable the new service: `systemctl --user enable --now kwin-auto-mouse-remapper`
7. Sanity check that the service is running: `systemctl --user status kwin-auto-mouse-remapper`
8. Install and enable the KWin script, either via the provided install script or via Plasma System Settings GUI
9. Done  

See the documentation above on how to configure which window should trigger which script. Don't forget to `systemctl --user restart kwin-auto-mouse-remapper` after changing the config so it gets reloaded.  

## DISCLAIMER
This service can just run arbitrary scripts. Make sure you have backups of your data for when your 'friend' smuggles some ransomware in there.  
In any case I take no responsibility for any consequences that may result from proper or improper use of the information contained in this repository.  
I just thought it would be nice to have this publicly documented.

## Thanks
- [JoGr@Stackoverflow](https://stackoverflow.com/questions/34482691/register-a-hello-world-dbus-service-object-and-method-using-python) for the HelloWorld python-dbus example
- *You*, should you decide to contribute to the [KWin Scripting API documentation](https://develop.kde.org/docs/plasma/kwin/) (because lord knows, it needs it)
