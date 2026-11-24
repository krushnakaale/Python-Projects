import argparse
from datetime import date
from .core import Tracker

def main():
    p = argparse.ArgumentParser(description='Personal Expense Tracker (INR)')
    p.add_argument('--data', default='data/transactions.json')
    sub = p.add_subparsers(dest='command', required=True)
    for cmd in ('add','update'):
        a = sub.add_parser(cmd)
        if cmd=='update': a.add_argument('id')
        a.add_argument('kind', choices=['income','expense'])
        a.add_argument('amount')
        a.add_argument('category')
        a.add_argument('--date', default=date.today().isoformat())
        a.add_argument('--note', default='')
    sub.add_parser('delete').add_argument('id')
    for cmd in ('list','summary','export'):
        a = sub.add_parser(cmd)
        a.add_argument('--month', default=date.today().isoformat()[:7] if cmd=='summary' else None)
        if cmd=='export': a.add_argument('output')
    a = sub.add_parser('budget'); a.add_argument('month'); a.add_argument('amount')
    args = p.parse_args()
    try:
        t = Tracker(args.data)
        if args.command in ('add','update'):
            r=t.record(args.kind,args.amount,args.category,args.date,args.note,getattr(args,'id',None)); print('Saved:',r['id'])
        elif args.command=='delete': t.delete(args.id); print('Deleted.')
        elif args.command=='list':
            for r in t.rows(args.month): print(r['id'],r['date'],r['kind'],r['amount'],r['category'],r['note'])
        elif args.command=='budget': t.budget(args.month,args.amount); print('Budget saved.')
        elif args.command=='export': t.export(args.output,args.month); print('CSV exported.')
        else:
            totals,categories,budget=t.summary(args.month)
            print(f'Month: {args.month}')
            print(f"Income: INR {totals['income']:.2f}\nExpenses: INR {totals['expense']:.2f}\nBalance: INR {totals['income']-totals['expense']:.2f}")
            for k,v in sorted(categories.items()): print(f'{k}: INR {v:.2f}')
            if budget is not None:
                print(f'Budget remaining: INR {budget-totals["expense"]:.2f}')
                if totals['expense']>budget: print('WARNING: Budget exceeded!')
        return 0
    except (ValueError,OSError,KeyError,TypeError) as e:
        print(f'Error: {e}'); return 1
