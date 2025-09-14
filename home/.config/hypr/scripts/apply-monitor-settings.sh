#!/bin/bash

# Скрипт для применения настроек мониторов через wlr-randr
# Запускается при старте Hyprland

# Применяем настройки для eDP-1 (ваш основной монитор)
wlr-randr --output eDP-1 --mode 1920x1080@144Hz --transform 180 --scale 1.0

# Если есть другие мониторы, добавьте их здесь
# wlr-randr --output HDMI-A-1 --mode 1920x1080@60Hz --pos 1920,0
