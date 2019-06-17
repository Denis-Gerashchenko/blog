import os
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
os.system('git add -A')
os.system(f'git commit -m "{message}"')
os.system('git push -u origin master')
os.system('Denis-Gerashchenko')
os.system(f'{password}')

