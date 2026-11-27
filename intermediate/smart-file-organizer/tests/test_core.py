import tempfile
import unittest
from pathlib import Path

from smart_file_organizer.core import category_for, duplicates, organize, undo


class FileOrganizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_categories(self):
        self.assertEqual(category_for(Path("PHOTO.JPG")), "Images")
        self.assertEqual(category_for(Path("file.unknown")), "Others")

    def test_dry_run_does_not_move(self):
        (self.root / "photo.jpg").write_bytes(b"image")
        result = organize(self.root, dry_run=True)
        self.assertEqual(len(result["moves"]), 1)
        self.assertTrue((self.root / "photo.jpg").exists())
        self.assertFalse((self.root / "Images").exists())

    def test_organize_and_undo(self):
        (self.root / "notes.txt").write_text("hello")
        organize(self.root)
        self.assertTrue((self.root / "Documents" / "notes.txt").exists())
        undo(self.root)
        self.assertTrue((self.root / "notes.txt").exists())
        self.assertFalse((self.root / "Documents" / "notes.txt").exists())

    def test_collision_uses_new_filename(self):
        (self.root / "Images").mkdir()
        (self.root / "Images" / "pic.png").write_bytes(b"old")
        (self.root / "pic.png").write_bytes(b"new")
        organize(self.root)
        self.assertEqual((self.root / "Images" / "pic.png").read_bytes(), b"old")
        self.assertEqual((self.root / "Images" / "pic_1.png").read_bytes(), b"new")

    def test_duplicates_by_content(self):
        (self.root / "a.txt").write_bytes(b"same")
        (self.root / "b.txt").write_bytes(b"same")
        (self.root / "c.txt").write_bytes(b"different")
        self.assertEqual(duplicates(self.root), [["a.txt", "b.txt"]])

    def test_recursive_and_undo(self):
        nested = self.root / "nested"
        nested.mkdir()
        (nested / "a.pdf").write_bytes(b"pdf")
        organize(self.root, recursive=True)
        self.assertTrue((self.root / "Documents" / "a.pdf").exists())
        undo(self.root)
        self.assertTrue((nested / "a.pdf").exists())

    def test_undo_refuses_conflict(self):
        (self.root / "x.txt").write_text("original")
        organize(self.root)
        (self.root / "x.txt").write_text("new")
        with self.assertRaises(ValueError):
            undo(self.root)
        self.assertEqual((self.root / "x.txt").read_text(), "new")

    def test_skip_symlink(self):
        target = self.root / "actual.txt"
        target.write_text("data")
        link = self.root / "linked.txt"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        organize(self.root)
        self.assertTrue(link.is_symlink())


if __name__ == "__main__":
    unittest.main()
