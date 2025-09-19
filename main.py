import sys

filename = sys.argv[1]
print(filename)

with open(f"{filename}", "rb") as f:
    data = f.read()
