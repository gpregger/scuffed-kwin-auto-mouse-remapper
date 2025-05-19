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

kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton1 "Key,Q" --notify         # Left Shoulder
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton2 "Key,Q" --notify         # Left Shoulder
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton4 "Key,Ctrl+L" --notify    # Expansion Bay
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton5 "Key,E" --notify         # Right Shoulder
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton6 "Key,E" --notify         # Right Shoulder
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton7 "Key,Ctrl+L" --notify    # Expansion Bay
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton8 "Key,C" --notify         # Heal
kwriteconfig6 --file kcminputrc --group ButtonRebinds --group Mouse --key ExtraButton9 "Key,V" --notify         # Scan
