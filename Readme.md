# Scuffed Auto Mouse Key Remapping with Kwin and DBus
This is the result of ~~a~~ several spontaneous 6h pre-weekend crunches. It's pretty scuffed but hey, it works so far (not that I've tested it for more than ~~5~~ 120 minutes as of writing this).  
If this acutally ends up working mid to long term, consider my mind thoroughly boggled that it took this long to produce something like this.  
Though to be fair, scope of application is a bit narrow, seeing as this is very KDE specific.  

## Working Principle
1. 'kwin-auto-mouse-remapper-dbus-service.py' runs as a systemd service using 'kwin-auto-mouse-remapper.service'
2. This python script loads 'app_mapping.json' which contains the rules about which window gets which mapping script. simple.
2. 'kwin_window_title_sender' runs in the background as a KWin script. This connects to the workspace.windowActivated signal and with every window focus change reports the title of the active window and the PID of the responsible process to the DBus service 'org.schorsch.mousekeymapper' provided by 'kwin-auto-mouse-remapper-dbus-service.py'
3. 'kwin-auto-mouse-remapper-dbus-service.py' then decides based on the received window title / PID and the rules in app_mapping.json which script to run from the 'mapping_scripts' folder. This folder can contain arbitrary shell scripts (YOLO), but I filled them with something like this:  
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
To set the Plasma Extra Mouse Buttons. This is equvalent to mapping the extra mouse buttons in the Plasma Settings.

## Configuration
The 'app_mapping.json' config file must consist of a json list of dicts. See an example below.  
There has to be one entry with the "match-type" "\__DEFAULT__", this is the mapping that applies if no other match is found.  
Currently there are two kinds of "match-type": "window-title" and "cmdline". Both take one or more patterns using regex notation (matching is done with the python *re* package) to match against the reported active window.  
**All specified patterns have to match** (AND logic).  
### Matching Window Titles
Since apps are generally free to change their window titles freely, matching that can be finicky, but under the hood it's probably a good bit faster. Also since a window title change generally doesn't correspond to a focus change, depending on the timing a mapping might not get applied as expected.  
Example: Elite Dangerous comes with a launcher and when using gamescope to run the game, the main game "takes over" the launcher window and my mapping doesn't get applied when the game starts proper unless I match the Launcher title, which would break if I ever alt-tabbed out and back into the game, so it's not ideal.  
For this reason we can also match by "cmdline".
### Matching "cmdline"
If a matching rule using match-type "cmdline" is specified we use the PID supplied by the KWin script together with [psutil](https://pypi.org/project/psutil/) to get the cmdline property of the process object.  
This info can be as simple as just the binary path or as convoluted as
```json
['gamescope', '-H', '600', '--hdr-enabled', '-r', '240', '--', '/home/schorsch/.local/share/Steam/ubuntu12_32/steam-launch-wrapper',
'--', '/home/schorsch/.local/share/Steam/ubuntu12_32/reaper', 'SteamLaunch', 'AppId=359320', '--',
'/home/schorsch/.local/share/Steam/steamapps/common/SteamLinuxRuntime_sniper/_v2-entry-point', '--verb=waitforexitandrun', '--',
'/home/schorsch/.local/share/Steam/steamapps/common/Proton Hotfix/proton', 'waitforexitandrun',
'/home/schorsch/.local/share/Steam/steamapps/common/Elite Dangerous/EDLaunch.exe', '/Steam', '/novr']

```
Doesn't that look like fun...  
Problem here is how to determine what's the actual application name we're interested in, so I figure just narrow it down as much as possible so it *probably* doesn't match something I dont want.  
Here the multiple matching patterns really shine. Each pattern gets sequentially applied to each item in this list and for the config to match, each pattern has to match with at least one item.  
In my example I use the patterns ".\*proton$" and ".\*EDLaunch.exe$". I figure if these patterns both occur in my command line I'm *probably* looking at the actual game window of Elite Dangerous. And if not I can always narrow it down further with more or better patterns.  

A full valid 'app_mapping.json' could be:  
```json
[
    {
        "match-type": "__DEFAULT__",
        "match-patterns": [],
        "mapping-script": "keybind_desktop.sh"
    },
    {
        "match-type": "window-title",
        "match-patterns": ["ARMORED CORE™ VI FIRES OF RUBICON™"],
        "mapping-script": "keybind_armored_core_6.sh"
    },
    {
        "match-type": "cmdline",
        "match-patterns": [".*proton$", ".*EDLaunch.exe$"],
        "mapping-script": "keybind_elite_dangerous.sh"
    }
]
```
And of course both 'keybind_desktop.sh', "keybind_armored_core_6.sh" and 'keybind_elite_dangerous.sh' need to be present in the 'mapping_scripts' folder and be executable.


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
9. Use Piper or equivalent to set your Gamerbuttons™ to something generic to avoid conflicting inputs
10. Done  

See the documentation above on how to configure which window should trigger which script. Don't forget to `systemctl --user restart kwin-auto-mouse-remapper` after changing the config so it gets reloaded.  

## DISCLAIMER
This service can just run arbitrary scripts. Make sure you have backups of your data for when your 'friend' smuggles some ransomware in there.  
In any case I take no responsibility for any consequences that may result from proper or improper use of the information contained in this repository.  
I just thought it would be nice to have this publicly documented.

## Thanks
- [JoGr@Stackoverflow](https://stackoverflow.com/questions/34482691/register-a-hello-world-dbus-service-object-and-method-using-python) for the HelloWorld python-dbus example
- *You*, should you decide to contribute to the [KWin Scripting API documentation](https://develop.kde.org/docs/plasma/kwin/) (because lord knows, it needs it)

## Changes
### 17.05.2025
Added an additional DBus listener so the script can wait until any global hotkeys are released before loading a new mapping. Previously there was an issue that when for example switching to a matching window on a different virtual desktop using Ctrl+Meta+ArrowKey the Ctrl+Meta keys would get stuck.

### 19.05.2025
Added more advanced matching features

## To Do
- ~~Offer more options for matching, maybe via regex pattern or process name~~
