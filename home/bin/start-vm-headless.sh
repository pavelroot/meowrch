#!/bin/bash

# Получаем список всех виртуальных машин
VMS=$(VBoxManage list vms | grep -o '"[^"]*"' | tr -d '"')

if [ -z "$VMS" ]; then
    notify-send "VirtualBox" "Не найдено виртуальных машин"
    exit 1
fi

# Выбираем VM через dmenu (если установлен) или zenity
if command -v dmenu >/dev/null 2>&1; then
    SELECTED_VM=$(echo "$VMS" | dmenu -p "Выберите VM для запуска:")
elif command -v zenity >/dev/null 2>&1; then
    SELECTED_VM=$(echo "$VMS" | zenity --list --title="Выберите VM" --text="Выберите виртуальную машину для запуска:" --column="Имя VM")
else
    echo "Доступные VM:"
    echo "$VMS"
    read -p "Введите имя VM: " SELECTED_VM
fi

if [ -n "$SELECTED_VM" ]; then
    echo "Запускаем VM: $SELECTED_VM"
    VBoxManage startvm "$SELECTED_VM" --type headless
    notify-send "VirtualBox" "VM '$SELECTED_VM' запущена в headless режиме"
else
    notify-send "VirtualBox" "VM не выбрана"
fi
