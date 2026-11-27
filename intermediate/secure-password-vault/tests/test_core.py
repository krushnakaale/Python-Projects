import tempfile
import unittest
from pathlib import Path
from password_vault.core import Vault, generate_password


class VaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'vault.json'
        self.master = 'demo-master-12345'
        self.vault = Vault.create(self.path, self.master)

    def test_roundtrip(self):
        self.vault.put('demo', 'user', 'dummy-secret')
        self.assertEqual(Vault.open(self.path, self.master).entries['demo']['password'], 'dummy-secret')

    def test_wrong_password(self):
        with self.assertRaises(ValueError):
            Vault.open(self.path, 'wrong')

    def test_encrypted(self):
        self.vault.put('demo', 'user', 'dummy-secret')
        self.assertNotIn('dummy-secret', self.path.read_text())

    def test_update(self):
        self.vault.put('demo', 'user', 'old')
        self.vault.put('demo', 'user', 'new', True)
        self.assertEqual(Vault.open(self.path, self.master).entries['demo']['password'], 'new')

    def test_delete(self):
        self.vault.put('demo', 'user', 'old')
        self.vault.delete('demo')
        self.assertEqual(Vault.open(self.path, self.master).entries, {})

    def test_search(self):
        self.vault.put('Demo', 'user', 'old')
        self.assertEqual(self.vault.search('dem'), ['Demo'])

    def test_no_overwrite(self):
        with self.assertRaises(FileExistsError):
            Vault.create(self.path, self.master)

    def test_generator(self):
        self.assertEqual(len(generate_password(32)), 32)
        with self.assertRaises(ValueError):
            generate_password(4)
