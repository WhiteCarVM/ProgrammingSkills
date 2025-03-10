#!/bin/bash

# Начало скрипта
echo -e "Скрипт для сбора информации об системе. Расчитан на использование против дистрибутивов linux.\n"
echo "  Скрипт собирает следующую информацию:"
echo "1. Информация о системе: ядро, архитектура, процессор, жесткий диск, запущенные процессы"
echo "2. Информация о сети: сетевые интерфейсы, таблица маршрутизации, arp-таблица, сетевые подключения, открытые порты и запущенные сервисы."
echo "3. Пользователи и группы: история действий, права и файлы пользователей, ключи и пароли"
echo "4. Доступное ПО: полезное для пивотинга и эскалации привилегий программное обеспечение"
echo "5. Файлы и резервные копии: файлы, содержащие полезную информацию, резервные копии недоступных для чтения файлов"
echo -e "\nСоздатель: WhiteCar"
echo -e "-------------------------------------------------------------------------------------------------------------------\n"

# Часть 1: Информация о системе
echo "Часть 1: Информация о системе"
echo -e "\n1) Ядро: $(uname -s)"
echo "Релиз: $(uname -r)"
echo "Версия: $(uname -v)"
echo "Архитектура: $(uname -m)"
echo "Операционная система: $(uname -o)"

# Информация о процессоре
echo -e "\n2) Процессор"
echo "Производитель: $(lscpu | grep 'Vendor ID:' | cut -d : -f 2 | awk '{$1=$1; print}')"
echo "Модель: $(lscpu | grep 'Model name:' | cut -d : -f 2 | awk '{$1=$1; print}')"
echo "Семейство: $(lscpu | grep 'CPU family:' | cut -d : -f 2 | awk '{$1=$1; print}')"
CPUs=$(lscpu | grep 'CPU(s):' | cut -d : -f 2 | awk '{$1=$1; print}')
echo "Количество логических процессоров: $(echo $CPUs | cut -d ' ' -f 1)"
echo "Гиперпоточность: $(lscpu | grep 'Thread(s) per core:' | cut -d : -f 2 | awk '{$1=$1; print}') ядра"
echo "Минимальная частота: $(lscpu | grep 'CPU min MHz:' | cut -d : -f 2 | awk '{$1=$1; print}') MHz"
echo "Максимальная частота: $(lscpu | grep 'CPU max MHz:' | cut -d : -f 2 | awk '{$1=$1; print}') MHz"

# Информация о жестких дисках
echo -e "\n3) Жесткие диски"
echo "Диски и их размеры:"
disks=$(lsblk -x TYPE | grep disk | cut -d ' ' -f 1)
for i in $disks;
do
  echo $i
done

# ОТФИЛЬТРОВАТЬ БЕСПОЛЕЗНУЮ ИНФОРМАЦИЮ
echo -e "\n4) Процессы"
ps -aux
echo -e "\n-------------------------------------------------------------------------------------------------------------------\n"

# Часть 2: Информация о сети
echo "Часть 2: Информация о сети"
echo -e "\n1) Сетевые интерфейсы:\n"
ifconfig
echo -e "\n2) Таблица маршрутизации:\n"
route -nve
echo -e "\n3) Arp-таблица:\n"
arp -en
echo -e "\n4) Сетевые подключения:\n"
netstat -ano

# Открытые порты и запущенные сервисы
echo -e "\n5) Открытые порты и запущенные сервисы:\n"
touch /tmp/ports.py
echo -e "import socket\n" >> /tmp/ports.py
echo "counter = 1" >> /tmp/ports.py
echo "for port in range(1, 65536):" >> /tmp/ports.py
echo "        try:" >> /tmp/ports.py
echo "                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)" >> /tmp/ports.py
echo "                sock.connect(('127.0.0.1', port))" >> /tmp/ports.py
echo "                service = socket.getservbyport(port, \"tcp\")" >> /tmp/ports.py
echo "                print(f'{counter}) {str(port)}\ttcp\t{service}')" >> /tmp/ports.py
echo "                counter += 1" >> /tmp/ports.py
echo "                sock.close()" >> /tmp/ports.py
echo "        except:" >> /tmp/ports.py
echo "                pass" >> /tmp/ports.py
echo -e "\nfor port in range(1, 65536):" >> /tmp/ports.py
echo "        try:" >> /tmp/ports.py
echo "                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)" >> /tmp/ports.py
echo "                sock.connect(('127.0.0.1', port))" >> /tmp/ports.py
echo "                service = socket.getservbyport(port, \"udp\")" >> /tmp/ports.py
echo "                print(f'{counter}) {str(port)}\tudp\t{service}')" >> /tmp/ports.py
echo "                counter += 1" >> /tmp/ports.py
echo "                sock.close()" >> /tmp/ports.py
echo "        except:" >> /tmp/ports.py
echo "                pass" >> /tmp/ports.py

if [[ -e /usr/bin/python3 ]];
then
  python3 /tmp/ports.py
elif [[ -e /usr/bin/python2 ]];
then
  python2 /tmp/ports.py
fi

rm -rf /tmp/ports.py
echo -e "\n-------------------------------------------------------------------------------------------------------------------"

# Часть 3: Пользователи и группы
echo -e "\nЧасть 3: Пользователи и группы"
echo -e "\n1) Пользователи:"
home_grep=$(ls /home/)
users=()
users+=root

# Сбор пользователей
for user in $home_grep;
do
  users+=("$user")
  #echo $user
done

for user in "${users[@]}";
do
  current=$(whoami)
  if [[ $user != $current ]];
  then
    echo -e "\n$user"
  else
    echo -e "\n$user -- текущий пользователь"
  fi
  echo $(id "$user")
done
echo -e "\n-------------------------------------------------------------------------------------------------------------------"

# Часть 4: Доступное ПО
echo -e "\nЧасть 4: Доступное ПО"
echo -e "\nУстановленные пакеты:"
dpkg --get-selections | grep -v deinstall
echo -e "\n-------------------------------------------------------------------------------------------------------------------"

# Часть 5: Файлы и резервные копии (пример с /etc)
echo -e "\nЧасть 5: Файлы и резервные копии"
echo "Резервные копии /etc (если доступны):"
tar -cvzf /tmp/etc_backup.tar.gz /etc
echo -e "\n-------------------------------------------------------------------------------------------------------------------"
echo "Завершено!"
