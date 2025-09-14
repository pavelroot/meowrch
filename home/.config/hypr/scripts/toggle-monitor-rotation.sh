#!/bin/bash

# Скрипт для переключения поворота монитора между 0° и 180°
# Проверяет текущий поворот и переключает на противоположный

# Получаем текущий поворот монитора eDP-1
current_transform=$(wlr-randr | grep -A 10 "eDP-1" | grep "Transform:" | awk '{print $2}')

echo "Текущий поворот: $current_transform"

# Переключаем поворот используя hyprctl keyword
if [ "$current_transform" = "180" ]; then
    echo "Поворачиваем на 0°"
    hyprctl keyword monitor eDP-1,preferred,auto,1,transform,0
    new_angle="0°"
else
    echo "Поворачиваем на 180°"
    hyprctl keyword monitor eDP-1,preferred,auto,1,transform,2
    new_angle="180°"
fi

# Показываем уведомление
notify-send "Поворот монитора" "Монитор повернут на $new_angle"
