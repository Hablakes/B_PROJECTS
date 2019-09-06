from pathlib import Path

entries = Path('my_directory/')
for entry in entries.iterdir():
    print(entry.name)
