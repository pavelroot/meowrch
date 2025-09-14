
#!/bin/bash

# Маппинг номеров на названия (ваши настройки)
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

# Функция переименования всех рабочих столов
rename_all_workspaces() {
    # Получаем список всех рабочих столов
    workspaces=$(hyprctl workspaces -j | jq -r '.[] | "\(.id)"')
    
    # Переименовываем каждый рабочий стол
    while IFS= read -r workspace_id; do
        if [ -n "$workspace_id" ]; then
            custom_name="${workspace_names[$workspace_id]}"
            if [ -n "$custom_name" ]; then
                # Переименовываем workspace
                hyprctl dispatch renameworkspace "$workspace_id" "$custom_name"
                echo "Переименован workspace $workspace_id в '$custom_name'"
            fi
        fi
    done <<< "$workspaces"
}

# Функция переименования текущего рабочего стола
rename_current_workspace() {
    # Получаем текущий рабочий стол
    current_ws=$(hyprctl activeworkspace -j | jq -r '.id')
    
    if [ -n "$current_ws" ]; then
        custom_name="${workspace_names[$current_ws]}"
        if [ -n "$custom_name" ]; then
            # Переименовываем текущий workspace
            hyprctl dispatch renameworkspace "$current_ws" "$custom_name"
            echo "Переименован текущий workspace $current_ws в '$custom_name'"
        fi
    fi
}

# Функция переименования конкретного workspace
rename_specific_workspace() {
    workspace_id=$1
    if [ -n "$workspace_id" ]; then
        custom_name="${workspace_names[$workspace_id]}"
        if [ -n "$custom_name" ]; then
            # Переименовываем указанный workspace
            hyprctl dispatch renameworkspace "$workspace_id" "$custom_name"
            echo "Переименован workspace $workspace_id в '$custom_name'"
        fi
    fi
}

# Обработка аргументов
case "${1:-}" in
    "all")
        rename_all_workspaces
        ;;
    "current")
        rename_current_workspace
        ;;
    [1-9]|10)
        rename_specific_workspace "$1"
        ;;
    *)
        rename_current_workspace
        ;;
esac