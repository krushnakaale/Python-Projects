import csv
import json
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit


def check(url, timeout=10):
    parsed = urlsplit(url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Provide an HTTP(S) URL without credentials.')
    start = time.monotonic()
    code, error = None, ''
    try:
        with urlopen(Request(url, headers={'User-Agent': 'EducationalWebsiteMonitor/1.0'}), timeout=timeout) as response:
            code = response.status
    except HTTPError as exc:
        code, error = exc.code, str(exc.reason)
        exc.close()
    except (URLError, OSError) as exc:
        error = str(exc)
    return dict(timestamp=datetime.now(timezone.utc).isoformat(), url=url,
                status=code, available=code is not None and 200 <= code < 400,
                response_ms=round((time.monotonic()-start)*1000, 2), error=error)


def record(path, result):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(result)+'\n')


def history(path):
    if not path.exists():
        return []
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def summary(rows):
    counts = {}
    for row in rows:
        total, up = counts.get(row['url'], (0, 0))
        counts[row['url']] = (total+1, up+int(row['available']))
    return {url: (total, round(100*up/total, 2)) for url, (total, up) in counts.items()}


def export(rows, path):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp','url','status','available','response_ms','error'])
        writer.writeheader()
        writer.writerows(rows)
