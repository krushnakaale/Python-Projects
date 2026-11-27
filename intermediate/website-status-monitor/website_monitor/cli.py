import argparse
import logging
import time
from pathlib import Path
from .core import check, record, history, summary, export


def main():
    p = argparse.ArgumentParser(description='Website Status Monitor')
    p.add_argument('--data', type=Path, default=Path('data/history.jsonl'))
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('check', 'monitor'):
        cmd = sub.add_parser(name)
        cmd.add_argument('urls', nargs='+')
        cmd.add_argument('--timeout', type=float, default=10)
        if name == 'monitor':
            cmd.add_argument('--interval', type=int, default=60)
            cmd.add_argument('--count', type=int, default=5)
    sub.add_parser('history')
    sub.add_parser('summary')
    sub.add_parser('export').add_argument('output', type=Path)
    a = p.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    try:
        if a.command in ('check', 'monitor'):
            count, interval = getattr(a, 'count', 1), getattr(a, 'interval', 60)
            if not 0 < a.timeout <= 120 or count < 1 or interval < 30:
                p.error('Timeout must be 0–120 seconds (exclusive of 0), count positive, interval at least 30 seconds.')
            for i in range(count):
                for url in dict.fromkeys(a.urls):
                    row = check(url, a.timeout)
                    record(a.data, row)
                    logging.info('%s | %s | HTTP %s | %.2f ms', url, 'UP' if row['available'] else 'UNAVAILABLE', row['status'], row['response_ms'])
                if i+1 < count:
                    time.sleep(interval)
        elif a.command == 'history':
            for row in history(a.data):
                print(row)
        elif a.command == 'summary':
            for url, (total, percent) in summary(history(a.data)).items():
                print(f'{url}: {percent:.2f}% successful checks ({total} samples)')
        else:
            export(history(a.data), a.output)
            print(f'Exported to {a.output}')
    except KeyboardInterrupt:
        print('\nMonitoring stopped.')
    except (ValueError, OSError) as exc:
        p.exit(1, f'Error: {exc}\n')
