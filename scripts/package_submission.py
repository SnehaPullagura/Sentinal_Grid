import os
import sys
import zipfile

def package_submission_zip():
    zip_path = "sentinel_grid_submission.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)

    print(f"Creating submission zip: {zip_path}...")
    
    exclude_dirs = {"node_modules", ".pytest_cache", "dist", "build", "__pycache__", ".venv", "venv", ".vite"}
    exclude_files = {"sentinel_grid_submission.zip", "sentinel_grid.db", ".DS_Store", "Thumbs.db"}

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file in exclude_files:
                    continue
                fpath = os.path.join(root, file)
                rel_path = os.path.relpath(fpath, ".")
                zipf.write(fpath, rel_path)
                file_count += 1

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"Submission zip created successfully with {file_count} files ({size_mb:.2f} MB).")
    return zip_path

if __name__ == "__main__":
    package_submission_zip()
