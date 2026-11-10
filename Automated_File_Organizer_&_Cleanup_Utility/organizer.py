import os
import shutil
from pathlib import Path

# Folder to organize. Change this to test on a smaller folder first.
TARGET_DIR = Path.home() / "Downloads"

# Extension -> category folder. Files with extensions not listed here are left untouched.
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".xlsx": "Documents", ".pptx": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos", ".avi": "Videos",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code", ".java": "Code",
}


def unique_destination(folder, filename):
    """Return a path inside `folder` that doesn't exist yet.

    Handles naming collisions: if 'report.pdf' already exists,
    the file is saved as 'report (1).pdf', 'report (2).pdf', etc.
    so nothing is ever overwritten.
    """
    dest = folder / filename
    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 1
    while dest.exists():
        dest = folder / f"{stem} ({counter}){suffix}"
        counter += 1
    return dest


def organize(target):
    moved = skipped = failed = 0

    # Read the directory into a list first, so the new category folders
    # created during the loop are not picked up by the scan.
    with os.scandir(target) as entries:
        files = [entry for entry in entries if entry.is_file()]

    for entry in files:
        # Never move this script itself if it sits inside the target folder.
        if entry.name == Path(__file__).name:
            continue

        category = EXTENSION_MAP.get(Path(entry.name).suffix.lower())
        if category is None:
            skipped += 1
            continue

        try:
            # Category folders are created only when needed.
            folder = target / category
            folder.mkdir(exist_ok=True)

            destination = unique_destination(folder, entry.name)
            shutil.move(entry.path, destination)
            moved += 1
            print(f"[MOVED]  {entry.name} -> {category}/{destination.name}")
        except PermissionError:
            # File is open in another program or access is denied.
            failed += 1
            print(f"[ERROR]  Permission denied: {entry.name}")
        except FileExistsError:
            failed += 1
            print(f"[ERROR]  File already exists: {entry.name}")

    # Execution summary
    print("\n" + "=" * 40)
    print("EXECUTION SUMMARY")
    print("=" * 40)
    print(f"Total files relocated : {moved}")
    print(f"Skipped (unknown type): {skipped}")
    print(f"Failed                : {failed}")
    print("=" * 40)


if __name__ == "__main__":
    if not TARGET_DIR.is_dir():
        print(f"Folder not found: {TARGET_DIR}")
    else:
        organize(TARGET_DIR)