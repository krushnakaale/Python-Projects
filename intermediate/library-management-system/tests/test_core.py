import unittest
import sqlite3
from library_system.core import Library

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.lib=Library(':memory:')
        self.addCleanup(self.lib.close)
        self.book=self.lib.add_book('Python','Author')
        self.member=self.lib.add_member('Demo')
    def test_search(self): self.assertEqual(len(self.lib.books('Python')),1)
    def test_issue(self):
        self.lib.issue(self.book,self.member)
        self.assertEqual(self.lib.books()[0]['available'],0)
    def test_unavailable(self):
        self.lib.issue(self.book,self.member)
        with self.assertRaises(ValueError): self.lib.issue(self.book,self.member)
    def test_return(self):
        self.lib.return_book(self.lib.issue(self.book,self.member))
        self.assertEqual(self.lib.books()[0]['available'],1)
    def test_invalid_member(self):
        with self.assertRaises(sqlite3.IntegrityError): self.lib.issue(self.book,999)
    def test_update(self):
        self.lib.update_book(self.book,'New','Author',2)
        self.assertEqual(self.lib.books()[0]['copies'],2)
    def test_delete(self):
        self.lib.delete_book(self.book)
        self.assertEqual(self.lib.books(),[])
    def test_overdue(self):
        loan=self.lib.issue(self.book,self.member)
        self.lib.write('UPDATE loans SET due=? WHERE id=?',('2000-01-01',loan))
        self.assertEqual(len(self.lib.loans(True)),1)
    def test_stats(self): self.assertEqual(self.lib.stats()['members'],1)
    def test_history_protection(self):
        self.lib.return_book(self.lib.issue(self.book,self.member))
        with self.assertRaises(sqlite3.IntegrityError): self.lib.delete_book(self.book)
