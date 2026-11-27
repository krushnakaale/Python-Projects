import argparse
import sqlite3
from contextlib import closing
from .core import Library

def main():
    p=argparse.ArgumentParser(description='Library Management System')
    p.add_argument('--db',default='library.db')
    sub=p.add_subparsers(dest='command',required=True)
    specs={'add-book':[('title',str),('author',str),('copies',int)],'update-book':[('id',int),('title',str),('author',str),('copies',int)],'delete-book':[('id',int)],'add-member':[('name',str)],'update-member':[('id',int),('name',str)],'delete-member':[('id',int)],'issue':[('book',int),('member',int)],'return':[('id',int)],'books':[],'members':[],'loans':[],'overdue':[],'stats':[]}
    for cmd,fields in specs.items():
        s=sub.add_parser(cmd)
        for name,typ in fields: s.add_argument(name,type=typ)
        if cmd=='books': s.add_argument('--search',default='')
        if cmd=='issue': s.add_argument('--days',type=int,default=14)
    a=p.parse_args()
    try:
        with closing(Library(a.db)) as lib:
            cmd=a.command
            if cmd=='books': result=lib.books(a.search)
            elif cmd=='overdue': result=lib.loans(True)
            elif cmd=='return': result=lib.return_book(a.id)
            elif cmd=='issue': result=lib.issue(a.book,a.member,a.days)
            else: result=getattr(lib,cmd.replace('-','_'))(*(getattr(a,n) for n,_ in specs[cmd]))
            if isinstance(result,list):
                for row in result: print(' | '.join(f'{k}: {v}' for k,v in row.items()))
                if not result: print('No records found.')
            elif isinstance(result,dict):
                for k,v in result.items(): print(f'{k}: {v}')
            else: print('Success.' if result is None else f'Success. ID: {result}')
        return 0
    except (ValueError,sqlite3.Error) as e:
        print(f'Error: {e}')
        return 1
