import argparse
from getpass import getpass
from pathlib import Path
from .core import Vault, generate_password


def main():
    parser = argparse.ArgumentParser(description='Educational local password vault')
    parser.add_argument('--vault', type=Path, default=Path.home()/'.demo-password-vault.json')
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('init', 'list', 'verify'):
        sub.add_parser(command)
    for command in ('add', 'update', 'show', 'delete', 'search'):
        sub.add_parser(command).add_argument('name')
    sub.add_parser('generate').add_argument('--length', type=int, default=24)
    args = parser.parse_args()
    try:
        if args.command == 'generate':
            print(generate_password(args.length))
            return 0
        master = getpass('Master password: ')
        if args.command == 'init':
            if master != getpass('Confirm master password: '):
                raise ValueError('Passwords do not match.')
            Vault.create(args.vault, master)
            print('Vault created.')
            return 0
        vault = Vault.open(args.vault, master)
        if args.command in ('add', 'update'):
            vault.put(args.name, input('Username: '), getpass('Entry password: '), args.command == 'update')
            print('Entry saved.')
        elif args.command == 'delete':
            if input('Delete entry? [y/N]: ').lower() == 'y':
                vault.delete(args.name)
                print('Entry deleted.')
        elif args.command == 'show':
            entry = vault.entries.get(args.name)
            if entry is None:
                raise ValueError('Entry not found.')
            print('Username:', entry['username'])
            if input('Reveal password on screen? [y/N]: ').lower() == 'y':
                print('Password:', entry['password'])
        elif args.command == 'verify':
            print('Vault unlocked successfully.')
        else:
            print('\n'.join(vault.search(args.name if args.command == 'search' else '')) or 'No entries found.')
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('Error:', exc)
        return 1
    except (KeyboardInterrupt, EOFError):
        print('\nCancelled.')
        return 1
