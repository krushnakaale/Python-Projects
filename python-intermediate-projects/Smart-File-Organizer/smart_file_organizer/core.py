"""File classification, organization, duplicate inspection, and undo."""
from __future__ import annotations

import hashlib
import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

LOG = logging.getLogger(__name__)
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".json", ".xml"},
}


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    return next((name for name, extensions in CATEGORIES.items() if suffix in extensions), "Others")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_directory(directory: Path) -> Path:
    directory = directory.expanduser().resolve()
    if not directory.is_dir():
        raise ValueError(f"Directory does not exist: {directory}")
    return directory


def _unique_target(destination: Path, reserved: set[Path]) -> Path:
    candidate = destination
    counter = 1
    while candidate.exists() or candidate in reserved:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
        counter += 1
    reserved.add(candidate)
    return candidate


def organize(source: Path, *, dry_run: bool = False, recursive: bool = False) -> dict:
    """Organize files into category directories inside source.

    Only regular non-symlink files are processed. In recursive mode, pre-existing
    category directories and the internal state directory are excluded.
    """
    source = _check_directory(source)
    state = source / ".sfo_state"
    category_names = set(CATEGORIES) | {"Others"}
    iterator = source.rglob("*") if recursive else source.iterdir()
    files = []
    for path in iterator:
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(source)
        if relative.parts[0] == ".sfo_state" or relative.parts[0] in category_names:
            continue
        files.append(path)
    files.sort(key=lambda p: str(p.relative_to(source)).casefold())
    reserved: set[Path] = set()
    moves = []
    for path in files:
        target = _unique_target(source / category_for(path) / path.name, reserved)
        moves.append({"from": str(path.relative_to(source)), "to": str(target.relative_to(source))})
    if dry_run or not moves:
        return {"dry_run": dry_run, "moves": moves, "journal": None}

    # Keep a record of successfully completed moves, including partial runs.
    state.mkdir(exist_ok=True)
    journal = state / f"operation-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{uuid4().hex[:8]}.json"
    record = {"version": 1, "source": str(source), "created_utc": datetime.now(timezone.utc).isoformat(), "moves": [], "undone": False}
    _write_json_atomic(journal, record)
    try:
        for move in moves:
            original = source / move["from"]
            target = source / move["to"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(original), str(target))
            record["moves"].append(move)
            _write_json_atomic(journal, record)
            LOG.info("Moved %s -> %s", original, target)
    except (OSError, shutil.Error):
        LOG.exception("Operation interrupted; completed moves are recorded in %s", journal)
        raise
    return {"dry_run": False, "moves": record["moves"], "journal": str(journal)}


def _write_json_atomic(path: Path, value: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def duplicates(source: Path, *, recursive: bool = False) -> list[list[str]]:
    """Return groups of identical files, without deleting or modifying anything."""
    source = _check_directory(source)
    iterator = source.rglob("*") if recursive else source.iterdir()
    by_size: dict[int, list[Path]] = {}
    for path in iterator:
        if not path.is_file() or path.is_symlink() or ".sfo_state" in path.relative_to(source).parts:
            continue
        by_size.setdefault(path.stat().st_size, []).append(path)
    groups: list[list[str]] = []
    for candidates in by_size.values():
        if len(candidates) < 2:
            continue
        by_hash: dict[str, list[Path]] = {}
        for path in candidates:
            by_hash.setdefault(sha256(path), []).append(path)
        for matches in by_hash.values():
            if len(matches) > 1:
                groups.append(sorted(str(p.relative_to(source)) for p in matches))
    return sorted(groups, key=lambda group: group[0])


def undo(source: Path, *, dry_run: bool = False) -> dict:
    """Undo the latest unfinished operation without overwriting existing files."""
    source = _check_directory(source)
    state = source / ".sfo_state"
    journals = sorted(state.glob("operation-*.json"), reverse=True) if state.is_dir() else []
    record = None
    journal = None
    for candidate in journals:
        data = json.loads(candidate.read_text(encoding="utf-8"))
        if data.get("source") == str(source) and not data.get("undone"):
            record, journal = data, candidate
            break
    if record is None or journal is None:
        raise ValueError("No organization operation available to undo")
    moves = list(reversed(record["moves"]))
    # Validate all targets before modifying anything; no clobbering or symlink paths.
    for move in moves:
        original = source / move["from"]
        current = source / move["to"]
        if original.exists() or original.is_symlink() or not current.is_file() or current.is_symlink():
            raise ValueError(f"Cannot safely undo {move['to']}: source missing or destination occupied")
        for parent in (original.parent, current.parent):
            if parent != source and any(p.is_symlink() for p in [parent, *list(parent.parents)[:len(parent.relative_to(source).parts)-1]]):
                raise ValueError("Cannot undo through symlinked directories")
    if dry_run:
        return {"dry_run": True, "moves": moves, "journal": str(journal)}
    # Update journal after every reversal so an interrupted undo can resume.
    for move in moves:
        original, current = source / move["from"], source / move["to"]
        original.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(current), str(original))
        record["moves"].remove(move)
        _write_json_atomic(journal, record)
        LOG.info("Restored %s -> %s", current, original)
    record["undone"] = True
    _write_json_atomic(journal, record)
    return {"dry_run": False, "moves": moves, "journal": str(journal)}
