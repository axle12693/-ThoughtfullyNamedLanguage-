
# Simple function to read a file
def readfile(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()


