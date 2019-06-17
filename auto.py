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
subprocess.call(['git', 'add', '-A'])
subprocess.call(['git', 'commit', '-m', f'{message}'])
proc = subprocess.Popen(['git', 'push', '-u', 'origin', 'master'], stdin=subprocess.PIPE)
proc.communicate(f'{login:b}')
proc.communicate(f'{password:b}')


