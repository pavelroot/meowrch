#!/bin/bash

# Скрипт для переименования рабочих столов в Hyprland
# Запускается при старте Hyprland

# Ждем немного, чтобы Hyprland полностью загрузился
sleep 2

# Переименовываем рабочие столы
hyprctl dispatch renameworkspace 1 Q
hyprctl dispatch renameworkspace 2 W
hyprctl dispatch renameworkspace 3 E
hyprctl dispatch renameworkspace 4 A
hyprctl dispatch renameworkspace 5 S
hyprctl dispatch renameworkspace 6 D
hyprctl dispatch renameworkspace 7 Z
hyprctl dispatch renameworkspace 8 X
hyprctl dispatch renameworkspace 9 C
hyprctl dispatch renameworkspace 10 V

