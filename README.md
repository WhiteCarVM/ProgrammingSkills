# PortScanner
Многопоточный сканер портов, написанный на языке программирования python. Он способен проводить сканирование нескольких IP-адресов, диапозона IP дресов на наличие открытых портов.
Пользователь сам выбирает порты, количество потоков и тип сканирования (доступно TCP и UDP). Есть возможность сохранения результатов сканирования и запуска нового.

![Image alt](https://github.com/WhiteCarVM/ProgrammingSkills/blob/main/pictures_to_readme/main_window.png)

### Использование
На устройстве должен быть установлен python3 и достаточное количесво свободной памяти.

Для начала необходимо кланировать репозиторий:

        git clone https://github.com/WhiteCarVM/ProgrammingSkills.git

Далее переходим в нужную директорию:

        cd Python/PortScanner/

Делаем устанивщик исполняемым файлом:

        chmod u+x installer.sh

Запускаем установку (потребуются права суперпользователя):

        sudo ./installer.sh

Приложение готово к работе !!! 

Запуск: 

        /path/to/application/portscanner

### Дополнительные сведения

Поле ввода IP-адреса принимает на вход данные следующего типа:

1. IP-адрес, например, 127.0.0.1

2. Несколько IP-адресов, например, 192.168.1.1,192.168.1.2

3. Диапазон IP-адресов, например, 192.168.1.1-24

4. CIDR запись IP-адресов, например, 192.168.1.0/24

Поле ввода порта принимает на вход данные следующего типа:

1. Целое число, например, 45

2. Несколько портов, например, 21,22

3. Диапазон чисел, например, 1-81

# MyNetCat

### Общие сведения

Консольный сетевой инструмент, написанный на языке программирования python, аналог инструмента netcat, но с меньшим числом функций. 
Он может работать либо в режиме прослушевателя, то есть принимает соединения и выполняет необходимые команды, либо в одном из следующих режимов: 
подключение, выполнение команд или какой-то определенной команды, загрузка файлов.

![Image alt](https://github.com/WhiteCarVM/ProgrammingSkills/blob/main/pictures_to_readme/mynetcat_main.png)

### Использование

Для начала необходимо убедиться, на устройстве установлен python3.

	python3 --version

Далее клонируем репозиторий:

	git clone https://github.com/WhiteCarVM/ProgrammingSkills.git

Переходим в папку с проектом:

	cd Python/MyNetCat

Запускаем инструмент:

	python3 mynetcat.py -t <IP address> -p <port> <options>

Перед началом использования рекомендую почитать меню помощи:

	python3 mynetcat.py -h

### Пример использзования

![Image alt](https://github.com/WhiteCarVM/ProgrammingSkills/blob/main/pictures_to_readme/mynetcat_example.png)

В примере выше в левой части терминала я запускаю сервер на прослушивание входящих соединений и выполнение команды "head /etc/passwd". 
В правой части терминала я подключаю клиента к серверу, клиент получает результат работы команды.

### Дополнительные сведения

Инструмент находится на стадии тестирования и доработки. При обнаружении ошибок просьба сообщить.

# NetworkSniffer
