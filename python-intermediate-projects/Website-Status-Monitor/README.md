# Website Status Monitor

Project 04 — Python Intermediate Projects. A sequential CLI monitor for authorized HTTP(S) websites.

## Setup
Extract the archive and open a terminal in this directory. Python 3.10+ is required; no external dependencies.

Windows: `py main.py --help`

Kali Linux: `python3 main.py --help`

## Commands
Use `py` on Windows or `python3` on Kali in place of `python` if needed.

```bash
python main.py check https://example.com
python main.py monitor https://example.com --interval 60 --count 5
python main.py history
python main.py summary
python main.py export report.csv
python -m unittest discover -s tests -v
```

Use only websites you own or have permission to monitor. Monitoring is sequential, finite by default, and intervals are at least 30 seconds. Ctrl+C stops monitoring. History is stored in `data/history.jsonl`; use `--data PATH` before the command to override it. Avoid URLs containing secrets. HTTP errors and network failures count as unsuccessful checks; this does not prove a server is offline. Response time measures time to response headers including redirects, not full page load. Availability percentage is the proportion of successful samples, not continuous uptime. Tests mock network responses; no live endpoint is required.

## About the developer
Part of the Python Intermediate Projects collection by Krushna Kale. [GitHub](https://github.com/krushnakaale).
