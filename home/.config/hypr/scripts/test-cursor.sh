#!/bin/bash

# Скрипт для тестирования курсора в разных приложениях
echo "=== Тест курсора в Wayland ==="
echo "Текущие настройки курсора:"
echo "XCURSOR_THEME: $XCURSOR_THEME"
echo "XCURSOR_SIZE: $XCURSOR_SIZE"
echo ""

echo "=== Проверка переменных окружения ==="
echo "WAYLAND_DISPLAY: $WAYLAND_DISPLAY"
echo "XDG_CURRENT_DESKTOP: $XDG_CURRENT_DESKTOP"
echo ""

echo "=== Проверка настроек GNOME ==="
echo "GNOME cursor size: $(gsettings get org.gnome.desktop.interface cursor-size)"
echo ""

echo "=== Доступные курсоры ==="
ls /usr/share/icons/ | grep -i bibata | head -5
echo ""

echo "=== Информация о мониторах ==="
hyprctl monitors
echo ""

echo "=== Рекомендации ==="
echo "1. Перезапустите приложения для применения новых настроек"
echo "2. Если курсор все еще разный, попробуйте:"
echo "   - Установить одинаковый размер в GNOME настройках"
echo "   - Перезапустить Hyprland"
echo "   - Проверить настройки конкретных приложений"



