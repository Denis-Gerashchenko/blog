import subprocess
import argparse

my_parser = argparse.ArgumentParser(prog='autopush', description='List the content of a folder')

my_parser.add_argument('Message',
                       metavar='message',
                       type=str,
                       help='the commit message')


args = my_parser.parse_args()
message = args.Message

subprocess.call(['git', 'add', '-A'])
subprocess.call(['git', 'commit', '-m', f'{message}'])
subprocess.call(['git', 'push', '-u', 'origin', 'master'])