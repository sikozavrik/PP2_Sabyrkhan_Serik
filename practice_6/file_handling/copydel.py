import os
import shutil

path = "sample.txt"
backup_path = "backup.txt"

if os.path.exists(path):
    shutil.copy(path, backup_path)
    print("Backup created")

if os.path.exists(path):
    print("Exists:", os.path.exists(path))
    print("Readable:", os.access(path, os.R_OK))
    print("Writable:", os.access(path, os.W_OK))
    print("Executable:", os.access(path, os.X_OK))

    directory, filename = os.path.split(path)
    print("Directory:", directory)
    print("Filename:", filename)

if os.path.exists(backup_path) and os.access(backup_path, os.W_OK):
    os.remove(backup_path)
    print("File deleted successfully")