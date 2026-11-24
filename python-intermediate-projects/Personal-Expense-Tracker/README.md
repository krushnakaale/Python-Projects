# Personal Expense Tracker

A standard-library Python CLI for tracking income, expenses and monthly budgets in INR. Project 02 of the Python Intermediate Projects series.

## Setup
Install Python 3.10 or later, extract the project and open a terminal in its root. On Windows use `py`; on Kali Linux use `python3` in place of `py` below. No external dependencies are needed.

```sh
py main.py --help
py main.py add income 5000 Allowance --date 2026-11-01
py main.py add expense 250 Food --date 2026-11-02 --note Lunch
py main.py budget 2026-11 2000
py main.py list --month 2026-11
py main.py summary --month 2026-11
py main.py export report.csv --month 2026-11
py -m unittest discover -s tests -v
```

Use `update ID expense 300 Food --date 2026-11-02` or `delete ID` after `py main.py`, replacing ID with the full ID from `list`. Update replaces all fields. Delete is permanent. Use `--data demo.json` before the subcommand to select a separate data file.

## Design
`main.py` is the entry point; `expense_tracker/cli.py` handles arguments; `core.py` handles validation, Decimal arithmetic, JSON persistence and CSV export. Tests use temporary files.

Data is stored locally in `data/transactions.json`, in plaintext. Do not enter account numbers or secrets. Back up the data file, avoid concurrent instances and never commit personal records. CSV export refuses to overwrite existing files. Budgets are monthly expense limits; balance is monthly income minus expenses, not a bank balance.
