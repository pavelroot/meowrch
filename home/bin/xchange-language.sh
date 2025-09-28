#!/bin/bash

CURRENT_LAYOUT=$(xset -q|grep LED| awk '{ print $10 }')
setxkbmap -layout us,ru -option "altwin:swap_alt_win,grp:win_space_toggle"
