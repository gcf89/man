#!/bin/bash

SIZE="--width=320 --height=240"
OPTS="--ellipsize"
PRINTER="BankPrinter"

# check if already added
lpstat -v | grep -q $PRINTER
if [[ $? -eq 0 ]]; then
    zenity $OPTS --warning \
        --text="Банковский принтер уже добавлен. Сперва необходимо выполнить его удаление из системы"
    exit 2
fi

# choose model: Olivetti/Epson
model=$(zenity $SIZE --list --radiolist \
    --title="Выберите модель принтера" \
    --column="" --column="Модель принтера" \
    "", "Olivetty" \
    "", "Epson"
    )

# wait for printer, add printer
TRY=15
DELAY=2
ITR=0
ISFOUND=0
case "$model" in
    "Olivetty")
        (
        while [[ $ITR -lt $TRY ]]; do
            lpinfo -v | grep -q '\busb://Unknown/Printer'
            if [[ $? -eq 0 ]]; then
                ISFOUND=1
                break
            fi
            ITR=$((ITR+1))
            echo $((ITR*100/$TRY)) # update zenity progress
            sleep $DELAY
        done

        if [[ $ISFOUND -eq 1 ]]; then
            lpadmin -p $PRINTER -E -v "usb://Unknown/Printer" -m "drv:///cupsfilters.drv/textonly.ppd" -o usb-unidir-default=true
        fi
        ) | zenity $SIZE --progress \
            --title="Поиск принтера" \
            --text="Выполняется поиск принтера..." \
            --percentage=0 \
            --auto-close \
            --time-remaining
        ;;
    "Epson")
        (
        while [[ $ITR -lt $TRY ]]; do
            lpinfo -v | grep -q '\busb://EPSON/TM-P2.01'
            if [[ $? -eq 0 ]]; then
                ISFOUND=1
                break
            fi
            ITR=$((ITR+1))
            echo $((ITR*100/$TRY)) # update zenity progress
            sleep $DELAY
        done

        if [[ $ISFOUND -eq 1 ]]; then
            lpadmin -p $PRINTER -E -v "usb://EPSON/TM-P2.01" -m "drv:///cupsfilters.drv/textonly.ppd" -o usb-unidir-default=true
        fi
        ) | zenity $SIZE --progress \
            --title="Поиск принтера" \
            --text="Выполняется поиск принтера..." \
            --percentage=0 \
            --auto-close \
            --time-remaining
        ;;
esac


# check if printer is added
lpstat -v | grep -q $PRINTER
if [[ $? -eq 0 ]]; then
    zenity $OPTS --info \
        --text="Принтер $model добавлен.\nВЫПОЛНИТЕ ПЕРЕЗАГРУЗКУ КОМПЬЮТЕРА!"
else
    zenity $OPTS --error \
        --text="Не удалось добавить притер $model.\nПерезагрузите компьютер и повторите попытку.\nИли обратитесь к администратору"
    exit 1
fi

