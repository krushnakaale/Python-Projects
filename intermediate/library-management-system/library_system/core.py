import sqlite3
from datetime import date, timedelta
from contextlib import closing

class Library:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL, copies INTEGER NOT NULL CHECK(copies>0));
        CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS loans(id INTEGER PRIMARY KEY, book_id INTEGER REFERENCES books(id), member_id INTEGER REFERENCES members(id), issued TEXT NOT NULL, due TEXT NOT NULL, returned TEXT);''')
    def close(self): self.db.close()
    def rows(self, sql, args=()): return [dict(r) for r in self.db.execute(sql,args)]
    def write(self, sql, args):
        with self.db:
            cur=self.db.execute(sql,args)
            return cur.lastrowid,cur.rowcount
    @staticmethod
    def clean(value):
        if not value.strip(): raise ValueError('Text cannot be empty')
        return value.strip()
    def add_book(self,title,author,copies=1):
        if copies<1: raise ValueError('Copies must be positive')
        return self.write('INSERT INTO books(title,author,copies) VALUES(?,?,?)',(self.clean(title),self.clean(author),copies))[0]
    def books(self,query=''):
        return self.rows('''SELECT b.*, copies-(SELECT count(*) FROM loans WHERE book_id=b.id AND returned IS NULL) AS available FROM books b WHERE title LIKE ? OR author LIKE ? ORDER BY id''',('%'+query+'%','%'+query+'%'))
    def update_book(self,id,title,author,copies):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            active=self.db.execute('SELECT count(*) FROM loans WHERE book_id=? AND returned IS NULL',(id,)).fetchone()[0]
            if copies<max(1,active): raise ValueError('Copies below active loans or one')
            if not self.db.execute('UPDATE books SET title=?,author=?,copies=? WHERE id=?',(self.clean(title),self.clean(author),copies,id)).rowcount: raise ValueError('Book not found')
    def delete_book(self,id):
        if not self.write('DELETE FROM books WHERE id=?',(id,))[1]: raise ValueError('Book not found')
    def add_member(self,name): return self.write('INSERT INTO members(name) VALUES(?)',(self.clean(name),))[0]
    def members(self): return self.rows('SELECT * FROM members ORDER BY id')
    def update_member(self,id,name):
        if not self.write('UPDATE members SET name=? WHERE id=?',(self.clean(name),id))[1]: raise ValueError('Member not found')
    def delete_member(self,id):
        if not self.write('DELETE FROM members WHERE id=?',(id,))[1]: raise ValueError('Member not found')
    def issue(self,book,member,days=14):
        if not 1<=days<=365: raise ValueError('Days must be 1–365')
        today=date.today()
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            row=self.db.execute('SELECT copies-(SELECT count(*) FROM loans WHERE book_id=? AND returned IS NULL) FROM books WHERE id=?',(book,book)).fetchone()
            if not row or row[0]<=0: raise ValueError('Book unavailable')
            return self.db.execute('INSERT INTO loans(book_id,member_id,issued,due) VALUES(?,?,?,?)',(book,member,today.isoformat(),(today+timedelta(days=days)).isoformat())).lastrowid
    def return_book(self,id):
        if not self.write('UPDATE loans SET returned=? WHERE id=? AND returned IS NULL',(date.today().isoformat(),id))[1]: raise ValueError('Active loan not found')
    def loans(self,overdue=False):
        return self.rows('SELECT * FROM loans'+(' WHERE returned IS NULL AND due<?' if overdue else '')+' ORDER BY id',(date.today().isoformat(),) if overdue else ())
    def stats(self):
        return self.rows('SELECT (SELECT count(*) FROM books) AS titles,(SELECT coalesce(sum(copies),0) FROM books) AS copies,(SELECT count(*) FROM members) AS members,(SELECT count(*) FROM loans WHERE returned IS NULL) AS active_loans')[0]
