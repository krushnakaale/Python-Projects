# Secure Password Vault

An intermediate Python CLI project demonstrating authenticated encryption, password-based key derivation, local persistence and automated testing. Use dummy credentials only; this is not an audited password manager.

## Setup

From the repository root, open `intermediate/secure-password-vault`.

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --help
```

Kali Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py --help
```

Use the virtual environment Python for the commands below. If venv is missing on Kali, install the distribution's python3-venv package.

## Commands

```bash
python main.py init
python main.py add demo
python main.py list
python main.py search demo
python main.py show demo
python main.py update demo
python main.py delete demo
python main.py verify
python main.py generate --length 32
```

The default vault is `.demo-password-vault.json` in your home directory. To select another file, put `--vault PATH` before the subcommand. Passwords are prompted without echo. Show and generate can expose passwords in terminal scrollback.

## Design

Scrypt derives a 32-byte key from the master password and a random 16-byte salt. Fernet encrypts and authenticates the JSON payload. The salt and format version are public. Updates use atomic replacement. There is no password recovery. Back up the encrypted file; do not commit it. Use one process at a time. Windows permissions inherit from the parent directory. This project does not protect against malware, memory inspection, weak master passwords or concurrent writes.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project layout

- `main.py`: entry point
- `password_vault/core.py`: encryption and storage
- `password_vault/cli.py`: command parsing and prompts
- `tests/`: unit tests
- `examples/`: sample output
