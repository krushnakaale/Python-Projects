"""Command-line interface."""
import argparse
import logging
from pathlib import Path

from .core import duplicates, organize, undo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="smart-file-organizer", description="Safely organize files by type.")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed logging")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("organize", "duplicates", "undo"):
        command = subparsers.add_parser(name)
        command.add_argument("path", type=Path, help="Folder to process")
        if name != "duplicates":
            command.add_argument("--dry-run", action="store_true", help="Preview without changing files")
        if name != "undo":
            command.add_argument("--recursive", action="store_true", help="Include nested folders")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        if args.command == "organize":
            result = organize(args.path, dry_run=args.dry_run, recursive=args.recursive)
            print("PREVIEW (no files changed)" if result["dry_run"] else "ORGANIZATION COMPLETE")
            for move in result["moves"]:
                print(f"  {move['from']} -> {move['to']}")
            print(f"Total: {len(result['moves'])} file(s)")
            if result["journal"]:
                print(f"Undo journal: {result['journal']}")
        elif args.command == "duplicates":
            groups = duplicates(args.path, recursive=args.recursive)
            for index, group in enumerate(groups, 1):
                print(f"Group {index}: " + ", ".join(group))
            print(f"Duplicate groups: {len(groups)} (nothing deleted)")
        else:
            result = undo(args.path, dry_run=args.dry_run)
            print("UNDO PREVIEW" if result["dry_run"] else "UNDO COMPLETE")
            for move in result["moves"]:
                print(f"  {move['to']} -> {move['from']}")
            print(f"Restored: {len(result['moves'])} file(s)")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
