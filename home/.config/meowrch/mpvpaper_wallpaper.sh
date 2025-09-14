#!/bin/bash

VIDEO_PATH="$1"
MONITOR="eDP-1"
PID_FILE="/tmp/mpvpaper_wallpaper.pid"

# Останавливаем предыдущий процесс mpvpaper
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    kill "$OLD_PID" 2>/dev/null
    rm -f "$PID_FILE"
fi

# Останавливаем swww daemon если он запущен
pkill swww-daemon 2>/dev/null

# Запускаем mpvpaper в фоне
mpvpaper -f -o "no-audio loop" "$MONITOR" "$VIDEO_PATH" &

# Сохраняем PID процесса
echo $! > "$PID_FILE"





