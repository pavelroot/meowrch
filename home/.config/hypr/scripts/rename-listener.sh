#!/bin/bash

# Путь к вашему скрипту для переименования
RENAME_SCRIPT="$HOME/.config/hypr/scripts/rename-workspaces.sh"

# Используем socat для прослушивания событий Hyprland
socat -u UNIX-CONNECT:/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - | while read -r line; do
    # Проверяем, является ли событие "openwindow"
    if [[ $line == "openwindow>>"* ]]; then
        # Парсим строку, чтобы получить адрес и класс окна
        # Пример строки: openwindow>>0x12345678,Discord,discord,Discord
        IFS=',' read -r event type window_address window_class _ <<< "$line"

        # Удаляем символ возврата каретки и лишние пробелы
        window_class=$(echo "$window_class" | tr -d '\r')

        # Проверяем, что это окно Discord
        if [[ "$window_class" == "discord" ]]; then
            echo "Найдено окно Discord с адресом: $window_address"

            # Запрашиваем у Hyprland, на каком рабочем столе находится это окно
            workspace_id=$(hyprctl -j clients | jq -r --arg addr "$window_address" '.[] | select(.address == $addr) | .workspace.id')

            # Если удалось получить ID рабочего стола
            if [ -n "$workspace_id" ]; then
                echo "Окно Discord находится на рабочем столе: $workspace_id"

                # Запускаем ваш скрипт-переименователь с найденным ID
                "$RENAME_SCRIPT" "$workspace_id"
                echo "Скрипт переименования выполнен."
            else
                echo "Не удалось получить ID рабочего стола для Discord."
            fi
        fi
    fi
done