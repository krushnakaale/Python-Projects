import json
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from datetime import date
from uuid import uuid4
import tempfile
import os

def money(value):
    try:
        n = Decimal(str(value))
        if not n.is_finite() or n <= 0 or n > Decimal('1000000000000') or n != n.quantize(Decimal('.01')):
            raise ValueError
        return format(n, '.2f')
    except (InvalidOperation, ValueError):
        raise ValueError('Enter a positive amount with at most two decimal places.')

def month_key(value):
    if len(value) != 7 or date.fromisoformat(value + '-01').isoformat()[:7] != value:
        raise ValueError('Use YYYY-MM for month.')
    return value

class Tracker:
    def __init__(self, path):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {'transactions': [], 'budgets': {}}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=self.path.parent, delete=False) as f:
            name = f.name
            json.dump(self.data, f, indent=2)
        try:
            os.replace(name, self.path)
        finally:
            Path(name).unlink(missing_ok=True)

    def record(self, kind, amount, category, day, note='', transaction_id=None):
        if kind not in ('income', 'expense') or not category.strip():
            raise ValueError('Invalid transaction type or category.')
        row = dict(id=transaction_id or uuid4().hex, kind=kind, amount=money(amount), category=category.strip(), date=date.fromisoformat(day).isoformat(), note=note)
        if transaction_id:
            rows = self.data['transactions']
            index = next((i for i,r in enumerate(rows) if r['id']==transaction_id), None)
            if index is None: raise ValueError('Transaction not found.')
            rows[index] = row
        else:
            self.data['transactions'].append(row)
        self.save()
        return row

    def delete(self, transaction_id):
        rows = self.data['transactions']
        remaining = [r for r in rows if r['id'] != transaction_id]
        if len(rows)==len(remaining): raise ValueError('Transaction not found.')
        self.data['transactions'] = remaining
        self.save()

    def rows(self, month=None):
        if month: month_key(month)
        return sorted((r for r in self.data['transactions'] if not month or r['date'].startswith(month)), key=lambda r:r['date'])

    def budget(self, month, amount):
        self.data['budgets'][month_key(month)] = money(amount)
        self.save()

    def summary(self, month):
        totals = {'income': Decimal(0), 'expense': Decimal(0)}
        categories = {}
        for r in self.rows(month):
            n = Decimal(r['amount'])
            totals[r['kind']] += n
            if r['kind']=='expense': categories[r['category']] = categories.get(r['category'], Decimal(0))+n
        budget = self.data['budgets'].get(month)
        return totals, categories, Decimal(budget) if budget else None

    def export(self, path, month=None):
        rows = self.rows(month)
        with open(path, 'x', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id','kind','amount','category','date','note'])
            writer.writeheader()
            for row in rows:
                writer.writerow({k: "'"+v if k in ('category','note') and v.lstrip().startswith(('=','+','-','@')) else v for k,v in row.items()})
