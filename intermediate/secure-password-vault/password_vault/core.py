"""Encrypted storage for an educational, local-only vault."""
import base64
import json
import os
import secrets
import string
import tempfile
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_password(length=24):
    if not 16 <= length <= 256:
        raise ValueError('Length must be between 16 and 256.')
    return ''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*_-') for _ in range(length))


class Vault:
    def __init__(self, path, salt, password, entries):
        self.path = Path(path)
        self.salt = salt
        key = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1).derive(password.encode())
        self.cipher = Fernet(base64.urlsafe_b64encode(key))
        self.entries = entries

    @classmethod
    def create(cls, path, password):
        if len(password) < 12:
            raise ValueError('Use a master password of at least 12 characters.')
        vault = cls(path, os.urandom(16), password, {})
        vault.path.parent.mkdir(parents=True, exist_ok=True)
        with vault.path.open('xb') as f:
            f.write(vault.serialize())
        if os.name != 'nt':
            vault.path.chmod(0o600)
        return vault

    @classmethod
    def open(cls, path, password):
        raw = json.loads(Path(path).read_text(encoding='utf-8'))
        if raw['version'] != 1:
            raise ValueError('Unsupported vault version.')
        vault = cls(path, base64.b64decode(raw['salt'], validate=True), password, {})
        try:
            vault.entries = json.loads(vault.cipher.decrypt(raw['data'].encode()))
        except InvalidToken as exc:
            raise ValueError('Incorrect master password or damaged vault.') from exc
        return vault

    def serialize(self):
        token = self.cipher.encrypt(json.dumps(self.entries).encode()).decode()
        return json.dumps({'version': 1, 'salt': base64.b64encode(self.salt).decode(), 'data': token}).encode()

    def save(self):
        fd, name = tempfile.mkstemp(dir=self.path.parent)
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(self.serialize())
                f.flush()
                os.fsync(f.fileno())
            os.replace(name, self.path)
        finally:
            if os.path.exists(name):
                os.unlink(name)

    def put(self, name, username, password, update=False):
        if not name.strip() or not username.strip() or not password:
            raise ValueError('All fields are required.')
        if (name in self.entries) != update:
            raise ValueError('Entry already exists.' if not update else 'Entry not found.')
        self.entries[name] = {'username': username, 'password': password}
        self.save()

    def delete(self, name):
        if name not in self.entries:
            raise ValueError('Entry not found.')
        del self.entries[name]
        self.save()

    def search(self, query=''):
        return sorted(name for name in self.entries if query.casefold() in name.casefold())
