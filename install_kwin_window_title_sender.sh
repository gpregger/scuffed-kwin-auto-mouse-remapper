#!/usr/bin/bash

kpackagetool6 --type=KWin/Script -i kwin_window_title_sender/
kcmshell6 kcm_kwin_scripts > /dev/null 2>&1 &

echo 'Please enable the "Mouse Mapping Window Title Sender" Kwin Script'
