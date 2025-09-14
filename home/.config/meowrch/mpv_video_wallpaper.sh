#!/bin/bash

VIDEO_PATH="$1"
PID_FILE="/tmp/mpv_wallpaper.pid"

# Останавливаем предыдущий процесс mpv
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    kill "$OLD_PID" 2>/dev/null
    rm -f "$PID_FILE"
fi

# Запускаем mpv в фоне для воспроизведения видеообоев
mpv \
    --really-quiet \
    --no-audio \
    --loop \
    --fullscreen \
    --no-border \
    --no-input-default-bindings \
    --no-input-vo-keyboard \
    --no-input-terminal \
    --vo=wlshm \
    "$VIDEO_PATH" &

# Сохраняем PID процесса
echo $! > "$PID_FILE"
