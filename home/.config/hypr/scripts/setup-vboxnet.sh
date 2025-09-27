#!/bin/bash

# Скрипт для настройки vboxnet0 интерфейса VirtualBox
# Добавляет IP адрес и поднимает интерфейс

# Проверяем, существует ли интерфейс vboxnet0
if ip link show vboxnet0 >/dev/null 2>&1; then
    echo "Настройка vboxnet0 интерфейса..."
    
    # Добавляем IP адрес
    sudo ip addr add 192.168.56.1/24 dev vboxnet0 2>/dev/null || true
    
    # Поднимаем интерфейс
    sudo ip link set vboxnet0 up 2>/dev/null || true
    
    echo "vboxnet0 настроен успешно"
else
    echo "Интерфейс vboxnet0 не найден. Убедитесь, что VirtualBox запущен."
fi


