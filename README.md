# 🐍 Python Projects Repository

<p align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python Logo" width="80" height="80"/>
</p>

<p align="center">
  <em>A curated collection of practical Python projects — from beginner-friendly terminal applications to modular, production-ready CLI tools.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
  <img src="https://img.shields.io/github/license/krushnakaale/Python-Projects?style=for-the-badge&color=green" alt="License"/>
  <img src="https://img.shields.io/github/repo-size/krushnakaale/Python-Projects?style=for-the-badge&color=orange" alt="Repo Size"/>
  <img src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg?style=for-the-badge" alt="Maintained"/>
</p>

---

## 📌 Repository Overview

Welcome to the **Python-Projects** repository! This repository is organized by skill level to showcase clean code practices, algorithmic thinking, and modular software architecture in Python. 

Whether you are looking for simple terminal exercises or intermediate-level modular applications with automated unit tests, this repository has hands-on examples built primarily using Python's standard library.

---

## 📂 Repository Structure

```text
Python-Projects/
│
├── python-mini-projects/                 # 🚀 Beginner-friendly terminal projects
│   ├── calculator.py                    # Multi-operation CLI calculator
│   ├── numGuessGame.py                  # Number guessing game with hints
│   ├── passGenerator.py                 # Customizable secure password generator
│   ├── rockPaperScissior.py             # Best-of-5 Rock Paper Scissors game
│   ├── toDo.py                          # Terminal To-Do list with JSON persistence
│   └── README.md                        # Documentation for mini projects
│
├── python-intermediate-projects/         # ⚡ Modular, robust intermediate projects
│   ├── Smart-File-Organizer/            # Cross-platform CLI file organizer
│   │   ├── smart_file_organizer/        # Core business logic & CLI module
│   │   ├── tests/                       # Automated unit test suite
│   │   ├── examples/                    # Sample output demonstrations
│   │   ├── main.py                      # Main entry point
│   │   └── README.md                    # Detailed documentation & safety guide
│   │
│   ├── Personal-Expense-Tracker/        # Income, expense & budget manager CLI in INR
│   │   ├── expense_tracker/             # CLI & core logic with Decimal precision
│   │   ├── tests/                       # Automated unit test suite
│   │   ├── examples/                    # Sample outputs & CSV reports
│   │   ├── main.py                      # Main entry point
│   │   └── README.md                    # Documentation & CLI usage guide
│   │
│   ├── Secure-Password-Vault/           # Encrypted local password manager with Scrypt & Fernet
│   │   ├── password_vault/              # Encryption engine & interactive CLI
│   │   ├── tests/                       # Automated unit test suite
│   │   ├── examples/                    # Sample outputs
│   │   ├── main.py                      # Main entry point
│   │   └── README.md                    # Security design & command reference
│   │
│   └── Website-Status-Monitor/          # HTTP(S) availability & latency monitor with CSV export
│       ├── website_monitor/             # Sequential monitoring engine & CLI
│       ├── tests/                       # Automated unit test suite with mock endpoints
│       ├── examples/                    # Sample outputs
│       ├── main.py                      # Main entry point
│       └── README.md                    # Monitoring guide & safety reference
│
└── README.md                            # Main repository guide (this file)
```

---

## 🚀 Projects Showcase

### 1. Beginner Level: `python-mini-projects`
> Focused on core programming foundations: loops, conditional logic, functions, OOP, and JSON file persistence using **zero external dependencies**.

| # | Project | Description | Core Concepts |
|---|---|---|---|
| 1 | **Simple Calculator** | Continuous command-line calculator with input validation | Functions, arithmetic logic, loops |
| 2 | **Number Guessing Game** | Interactive guessing game with scoring and hints | `random`, conditionals, state tracking |
| 3 | **Rock-Paper-Scissors** | Play 5-round matches against computer AI | Random choices, comparison algorithms |
| 4 | **Password Generator** | Generates strong passwords with customizable complexity | `string`, `random`, password strength evaluation |
| 5 | **To-Do List Manager** | CRUD task manager with persistent JSON storage | File I/O, `json`, OOP, task lifecycle |

---

### 2. Intermediate Level: `python-intermediate-projects`
> Focused on software architecture, clean CLI design, SHA-256 data hashing, test automation, and state management.

| # | Project | Description | Core Concepts |
|---|---|---|---|
| 1 | **Smart File Organizer** | Safe file categorization, duplicate detection & undo journal | `argparse`, `pathlib`, SHA-256, transaction journaling |
| 2 | **Personal Expense Tracker** | Income, expense & budget management CLI with CSV export | `decimal.Decimal`, financial math, JSON store, `csv` |
| 3 | **Secure Password Vault** | Encrypted credentials vault with Scrypt & Fernet | `cryptography`, Scrypt KDF, Fernet AES, `getpass` |
| 4 | **Website Status Monitor** | Sequential HTTP(S) health checker & uptime tracker | `urllib`, HTTP status, JSONL log, CSV report |

#### 📁 **Smart File Organizer** (`Smart-File-Organizer/`)
A cross-platform CLI tool that cleans up cluttered directories safely and intelligently.
- **Categorization:** Automatically sorts files into `Images`, `Documents`, `Spreadsheets`, `Presentations`, `Videos`, `Audio`, `Archives`, `Code`, and `Others`.
- **Duplicate Detection:** Computes **SHA-256** checksums (grouped by size) to find duplicate files without deleting anything automatically.
- **Safety First (`--dry-run`):** Preview planned moves before touching files.
- **Collision Protection:** Never overwrites existing destination files (appends `_1`, `_2`).
- **Undo System:** Keeps an operation journal (`.sfo_state/`) to revert file movements anytime.
- **Unit Tested:** Complete test coverage using Python's built-in `unittest` framework.

#### 📁 **Personal Expense Tracker** (`Personal-Expense-Tracker/`)
A standard-library CLI application for tracking income, expenses, and monthly budgets in INR.
- **Accurate Financial Math:** Uses `decimal.Decimal` for exact monetary calculations without floating-point errors.
- **Budget Tracking:** Set monthly limits and monitor spending thresholds with warnings.
- **Monthly Summary:** Category-wise percentage breakdown of expenses and net balance calculation.
- **CSV Export:** Easily export monthly transaction statements to CSV spreadsheets.
- **Persistence:** Local JSON data store with full CRUD capabilities (Add, List, Update, Delete).
- **Unit Tested:** Automated unit test suite with temporary test storage isolation.

#### 📁 **Secure Password Vault** (`Secure-Password-Vault/`)
An encrypted local password vault demonstrating authenticated encryption and secure key derivation.
- **Strong Key Derivation:** Scrypt KDF derives a 32-byte cryptographic key using master password + 16-byte random salt.
- **Authenticated Encryption:** Fernet (AES-128 in CBC mode + HMAC-SHA256) ensures vault confidentiality and integrity.
- **Masked Password Prompts:** Uses `getpass` for hidden terminal input to prevent shoulder-surfing.
- **Cryptographic Password Generator:** Generates cryptographically secure, high-entropy passwords with custom length.
- **Atomic Storage:** Atomic file replacements prevent data corruption during unexpected interruptions.
- **Unit Tested:** Complete test suite covering encryption roundtrips, bad password handling, and entry lifecycle.

#### 📁 **Website Status Monitor** (`Website-Status-Monitor/`)
A standard-library CLI uptime monitor for checking availability and response times of HTTP(S) endpoints.
- **Health Checks & Latency:** Measures HTTP status codes and header response times in milliseconds (`ms`).
- **Sequential Monitoring:** Configurable periodic polling with custom intervals (`--interval`) and sample counts (`--count`).
- **Audit History:** Records timestamped checks locally in structured JSON Lines format (`data/history.jsonl`).
- **Uptime Analytics:** Computes overall availability percentages and total sample statistics.
- **CSV Reports:** Exports historical monitoring data into structured CSV spreadsheets for reporting.
- **Unit Tested:** Unit test suite with mock network responses ensuring reliability without live endpoints.

---

## 🛠️ Getting Started

### Prerequisites
- Python **3.10** or higher installed. Check version:
  ```bash
  python --version   # Windows / Linux / macOS
  ```

### Clone the Repository
```bash
git clone https://github.com/krushnakaale/Python-Projects.git
cd Python-Projects
```

---

## 💻 Running the Projects

### Running Mini Projects
Navigate to `python-mini-projects` or execute directly:
```bash
# Example: Run the To-Do List application
python python-mini-projects/toDo.py

# Example: Run the Password Generator
python python-mini-projects/passGenerator.py
```

### Running Intermediate Projects

#### 1. Smart File Organizer
```bash
cd python-intermediate-projects/Smart-File-Organizer

# View help and available subcommands
python main.py --help

# Preview organizing a folder (Dry Run - no files changed)
python main.py organize "C:\Users\<YourUser>\Downloads" --dry-run

# Run duplicate detection recursively
python main.py duplicates "C:\Users\<YourUser>\Downloads" --recursive

# Run automated tests
python -m unittest discover -s tests -v
```

#### 2. Personal Expense Tracker
```bash
cd python-intermediate-projects/Personal-Expense-Tracker

# Add income or expense
python main.py add income 5000 Salary --date 2026-11-01
python main.py add expense 250 Food --date 2026-11-02 --note "Lunch"

# Set a monthly budget and view monthly summary
python main.py budget 2026-11 2000
python main.py summary --month 2026-11

# Export monthly report to CSV
python main.py export report.csv --month 2026-11

# Run automated tests
python -m unittest discover -s tests -v
```

#### 3. Secure Password Vault
```bash
cd python-intermediate-projects/Secure-Password-Vault

# Install dependencies
pip install -r requirements.txt

# Initialize a new vault with master password
python main.py init

# Generate a strong 32-character password
python main.py generate --length 32

# Add an entry and list entries
python main.py add github
python main.py list

# Run automated tests
python -m unittest discover -s tests -v
```

#### 4. Website Status Monitor
```bash
cd python-intermediate-projects/Website-Status-Monitor

# Single health check for a website
python main.py check https://example.com

# Periodic monitoring (every 60s, 5 samples)
python main.py monitor https://example.com --interval 60 --count 5

# View check history and uptime summary
python main.py history
python main.py summary

# Export results to CSV
python main.py export report.csv

# Run automated tests
python -m unittest discover -s tests -v
```

---

## 👨‍💻 Developer Information

<div align="center">

### **Krushna Kale**
*Software Developer & Open Source Enthusiast*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/krushnakaale)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/krushnakaale/)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/krushnakaale/)

</div>

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project (`gh repo fork krushnakaale/Python-Projects` or via GitHub web)
2. Create your Feature Branch (`git checkout -b feature/NewProject`)
3. Commit your Changes (`git commit -m 'Add awesome new project'`)
4. Push to the Branch (`git push origin feature/NewProject`)
5. Open a Pull Request

---

## 📄 License

This repository is distributed under the **MIT License**. See individual project directories for specific licenses where applicable.
