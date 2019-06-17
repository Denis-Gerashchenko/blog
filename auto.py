import subprocess
import argparse

my_parser = argparse.ArgumentParser(prog='autopush', description='List the content of a folder')

my_parser.add_argument('Message',
                       metavar='message',
                       type=str,
                       help='the commit message')

my_parser.add_argument('Password',
                       metavar='message',
                       type=str,
                       help='the password')

args = my_parser.parse_args()
message = args.Message
password = args.Password
login = 'Denis-Gerashchenko'

encoded_login = bytes(login, 'utf-8')
encoded_password = bytes(password, 'utf-8')

subprocess.call(['git', 'add', '-A'])
subprocess.call(['git', 'commit', '-m', f'{message}'])
proc = subprocess.Popen(['git', 'push', '-u', 'origin', 'master'], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
proc.stdin.write(encoded_login)
proc.stdin.write(encoded_password)




