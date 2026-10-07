try:
    with open("sample.txt", "r") as f:
        content = f.read()
        print("Content:")
        print(content)

    with open("sample.txt", "r") as f:
        lines = f.readlines()
        print("Line count:", len(lines))
except FileNotFoundError:
    print("File not found")