import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from urllib.error import URLError, HTTPError
from website_monitor.core import check, record, history, summary, export

class Tests(unittest.TestCase):
    @patch('website_monitor.core.urlopen')
    def test_success(self, mock):
        mock.return_value.__enter__.return_value.status = 200
        self.assertTrue(check('https://example.com')['available'])
    @patch('website_monitor.core.urlopen', side_effect=URLError('offline'))
    def test_network_error(self, mock):
        self.assertFalse(check('https://example.com')['available'])
    @patch('website_monitor.core.urlopen', side_effect=HTTPError('https://example.com', 404, 'Not found', {}, None))
    def test_http_error(self, mock):
        self.assertEqual(check('https://example.com')['status'], 404)
    def test_invalid_url(self):
        with self.assertRaises(ValueError): check('file:///tmp/test')
    def test_history(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'history.jsonl'
            record(p, {'url':'x'})
            self.assertEqual(history(p), [{'url':'x'}])
    def test_missing_history(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(history(Path(d)/'missing'), [])
    def test_summary(self):
        self.assertEqual(summary([{'url':'x','available':True},{'url':'x','available':False}]), {'x':(2,50.0)})
    def test_export(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'report.csv'
            export([], p)
            self.assertIn('response_ms', p.read_text())
