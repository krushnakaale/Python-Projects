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
│   └── Smart-File-Organizer/            # Cross-platform CLI file organizer
│       ├── smart_file_organizer/        # Core business logic & CLI module
│       ├── tests/                       # Automated unit test suite
│       ├── examples/                    # Sample output demonstrations
│       ├── main.py                      # Main entry point
│       └── README.md                    # Detailed documentation & safety guide
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

#### 📁 **Smart File Organizer** (`Smart-File-Organizer/`)
A cross-platform CLI tool that cleans up cluttered directories safely and intelligently.
- **Categorization:** Automatically sorts files into `Images`, `Documents`, `Spreadsheets`, `Presentations`, `Videos`, `Audio`, `Archives`, `Code`, and `Others`.
- **Duplicate Detection:** Computes **SHA-256** checksums (grouped by size) to find duplicate files without deleting anything automatically.
- **Safety First (`--dry-run`):** Preview planned moves before touching files.
- **Collision Protection:** Never overwrites existing destination files (appends `_1`, `_2`).
- **Undo System:** Keeps an operation journal (`.sfo_state/`) to revert file movements anytime.
- **Unit Tested:** Complete test coverage using Python's built-in `unittest` framework.

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

### Running Intermediate Projects (Smart File Organizer)
Navigate into the project directory:
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
