import os
import sys

def audit_codebase(root_dir="."):
    total_loc = 0
    blank_lines = 0
    comment_lines = 0
    code_lines = 0
    file_count = 0
    by_ext = {}
    by_dir = {}

    exclude_dirs = {".git", ".pytest_cache", "node_modules", "dist", "build", "__pycache__", ".venv", "venv"}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".html", ".css", ".md", ".toml", ".yml", ".yaml"}:
                fpath = os.path.join(root, f)
                file_count += 1
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        lines = fp.readlines()
                except Exception:
                    continue

                f_total = len(lines)
                f_blank = 0
                f_comment = 0
                f_code = 0

                for line in lines:
                    stripped = line.strip()
                    if not stripped:
                        f_blank += 1
                    elif stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                        f_comment += 1
                    else:
                        f_code += 1

                total_loc += f_total
                blank_lines += f_blank
                comment_lines += f_comment
                code_lines += f_code

                by_ext[ext] = by_ext.get(ext, 0) + f_code
                top_dir = root.split(os.sep)[1] if os.sep in root else "root"
                by_dir[top_dir] = by_dir.get(top_dir, 0) + f_code

    print("=================================================================")
    print("           SENTINEL GRID CODEBASE AUDIT & LOC REPORT             ")
    print("=================================================================")
    print(f"Total Source Files   : {file_count}")
    print(f"Total Lines (All)    : {total_loc:,}")
    print(f"Total Source Code LOC: {code_lines:,}")
    print(f"Comment Lines        : {comment_lines:,}")
    print(f"Blank Lines          : {blank_lines:,}")
    print("-----------------------------------------------------------------")
    print("Breakdown by File Extension (Pure Code LOC):")
    for ext, count in sorted(by_ext.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext:8s} : {count:6,d} LOC")
    print("-----------------------------------------------------------------")
    print("Breakdown by Subsystem Directory:")
    for d, count in sorted(by_dir.items(), key=lambda x: x[1], reverse=True):
        print(f"  {d:15s} : {count:6,d} LOC")
    print("=================================================================")
    return code_lines

if __name__ == "__main__":
    audit_codebase()
