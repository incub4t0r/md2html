from os import path
import os
import markdown
import hashlib
import json
markdownFolder = 'markdown'

ROOT = path.dirname(path.realpath(__file__))
MDROOT = path.join(ROOT, markdownFolder)
OUTPAGES = path.join(path.join(ROOT, 'static'), 'pages')
genHash = {}
storedHash = {}


def generate_file_md5(rootdir, filename):
    m = hashlib.md5()
    with open(os.path.join(rootdir, filename), "rb") as f:
        while True:
            buf = f.read(8192)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def checkChange(filename):
    try:
        return storedHash[filename] != generate_file_md5(MDROOT, filename)
    except:
        return True


def genHTML(filename):
    with open(path.join(MDROOT, filename), 'r') as f:
        text = f.read()
        html = markdown.markdown(
            text, extensions=['tables', 'toc', 'codehilite', 'fenced_code'])
    with open(path.join(OUTPAGES, f"{filename[:-3]}.html"), 'w') as f:
        f.write(html)


def convert(folder):
    for file in os.listdir(folder):
        if file.endswith(".md"):
            genHash[file] = str(generate_file_md5(MDROOT, file))
            if checkChange(file):
                print(f"{file} changed, generating new html...")
                genHTML(file)


def readHashes():
    try:
        with open(path.join(ROOT, 'hashes.txt'), 'r') as f:
            readHash = f.read()
            readHash = json.loads(readHash)
        return readHash
    except:
        print("hashes not found, regenerating all pages...")
        return {}


def storeHashes():
    with open(path.join(ROOT, 'hashes.txt'), 'w') as f:
        json.dump(genHash, f)


storedHash = readHashes()
convert(markdownFolder)
storeHashes()
