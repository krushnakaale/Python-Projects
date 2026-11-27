# Library Management System
A Python 3.10+ CLI application with SQLite persistence, book and member CRUD, loan tracking, overdue reports and statistics.

## Getting started
From the repository root, open `intermediate/library-management-system`. On Windows use `py main.py --help`; on Kali Linux use `python3 main.py --help`. No dependencies are required. Replace `python` below with `py` or `python3` as appropriate.

```sh
python main.py add-book "Python Basics" "Demo Author" 2
python main.py add-member "Demo Member"
python main.py books --search Python
python main.py issue 1 1 --days 14
python main.py loans
python main.py overdue
python main.py return 1
python main.py stats
python main.py update-book 1 "Python Basics" "Demo Author" 3
python main.py update-member 1 "Demo Reader"
python main.py members
python main.py --help
```
IDs above assume a fresh database. Use `--db demo.db` before the subcommand to select a separate database. Delete commands are `delete-book ID` and `delete-member ID`; records referenced by any loan are protected to preserve history. Due dates use local calendar dates; no fines or login system are implemented. Back up the database before modifying important records.

## Architecture
`main.py` launches `library_system/cli.py`; `library_system/core.py` contains the Library class and parameterized SQLite operations. `tests/` contains isolated in-memory tests.

## Tests
```sh
python -m unittest discover -s tests -v
```

## About the developer
Part of the Python Intermediate Projects collection, focused on practical Python programming, modular design and testing.
