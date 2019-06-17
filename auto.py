import subprocess
import argparse
import time
import pexpect

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
dialog = pexpect.spawn('git push -u origin master')
dialog.expect('''Username for 'https://github.com': ''')
dialog.sendline(login)
dialog.expect('''Password for 'https://Denis-Gerashchenko@github.com': ''')
dialog.sendline(password)




