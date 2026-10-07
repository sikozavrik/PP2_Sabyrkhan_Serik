import os

os.makedirs("parent/child/sub", exist_ok=True)
print("Created nested directories")

items = os.listdir(".")
print("All items:", items)

dirs = [i for i in items if os.path.isdir(i)]
files = [i for i in items if os.path.isfile(i)]

print("Directories only:", dirs)
print("Files only:", files)