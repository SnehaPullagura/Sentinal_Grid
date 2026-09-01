import os

def w(path, code):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

def run():
    print("--> Building Phase 1 files...")
