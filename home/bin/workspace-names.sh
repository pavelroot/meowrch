#!/bin/bash

# Получаем список рабочих столов
workspaces=$(hyprctl workspaces -j | jq -r '.[] | "\(.id) \(.name)"')

# Создаем маппинг номеров на названия
declare -A workspace_names
workspace_names[1]="Q"
workspace_names[2]="W"
workspace_names[3]="E"
workspace_names[4]="A"
workspace_names[5]="S"
workspace_names[6]="D"
workspace_names[7]="Z"
workspace_names[8]="X"
workspace_names[9]="C"
workspace_names[10]="V"

# Обрабатываем каждый рабочий стол
while IFS= read -r line; do
    if [ -n "$line" ]; then
        workspace_id=$(echo "$line" | cut -d' ' -f1)
        workspace_name=$(echo "$line" | cut -d' ' -f2-)
        
        # Получаем кастомное название
        custom_name="${workspace_names[$workspace_id]}"
        
        if [ -n "$custom_name" ]; then
            echo "$custom_name"
        else
            echo "$workspace_name"
        fi
    fi
done <<< "$workspaces"


