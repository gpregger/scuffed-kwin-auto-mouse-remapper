#!/usr/bin/bash

# PLASMA:
#    _
#   | |     _____ _____ _____
#   |9|    /__7__|__6__|__5__\
#   |_|    \__4__|__2__|__1__/
#   | |
#   |8|
#   |_|
#
# LOGITECH:
#    ___
#   |   |     ______ ______ ______
#   |G11|    /__G9__|__G8__|__G7__\
#   |___|    \__G6__|__G5__|__G4__/
#   |   |
#   |G10|
#   |___|
#

kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton1 "Key,Back" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton2 "Key,Forward" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton4 "Key,Meta+Tab" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton5 "Key,Back" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton6 "Key,Forward" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton7 "Key,Meta+Tab" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton8 "Key,Meta+Ctrl+Right" --notify
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton9 "Key,Meta+Ctrl+Left" --notify
