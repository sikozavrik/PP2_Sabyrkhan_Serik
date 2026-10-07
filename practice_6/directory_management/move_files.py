import os
import shutil

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            print("Found python file:", os.path.join(root, file))

os.makedirs("destination", exist_ok=True)

if os.path.exists("sample.txt"):
    shutil.copy("sample.txt", "destination/sample.txt")
    print("File copied to destination folder")