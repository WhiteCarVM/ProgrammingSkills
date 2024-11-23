import argparse
import shlex
import socket
import subprocess
import textwrap

def parser():
    """
        This function is using as a help menu
    """
    
    args = argparse.ArgumentParser(
    prog="MyNetCat",
    description='This is my netcat',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''Examples:
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l #connect to target and listen
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l -c # connect to target and use command shell
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -l -u=test.txt #connect to target and upload file "test.txt"
            python3 mynetcat.py -t 8.8.8.8 -p 4444 -e="cat /etc/passwd" # connect to target and execute command "cat /etc/passwd"
    '''))

    
    args.add_argument('-c', '--comand', action='store_true', help='use command shell')
    args.add_argument('-e', '--execute', help='execute specified command')
    args.add_argument('-l', '--listen', action='store_true', help='listen')
    args.add_argument('-p', '--port', type=int, default=10000, help="target port to connection")
    args.add_argument('-t', '--target', help='target IP address to connection')
    args.add_argument('-u', '--upload', help='upload file to target')

    return args.parse_args()

def execute(command):
    """
        This function is using for executing commands on target
    """
    
    command = command.strip()
    if not command:
        return
    results = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)

    return results.decode(encoding='utf-8')

if __name__ == "__main__":
    args = parser()