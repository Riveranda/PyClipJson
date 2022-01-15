# MIT License

# Copyright 2022 Timothy Bender

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sys import argv, stdin
try:
    import ujson as json
except ImportError:
    import json
    
from pyperclip import copy as pyperclipcopy

FILENAME = ".pydisstore.json"
MAXKEYMEMSIZE = 10

def readFromFile():
    JSON_OBJECT = {"numerals": {}, "custom": {}, "lastkey" : []}
    try:
        with open(FILENAME, "r+") as file:
            JSON_OBJECT = json.load(file) 
    except:
        pass
    return JSON_OBJECT 
        

def writeToFile(data, key):
    JSON_OBJECT = readFromFile()
    if len(JSON_OBJECT["lastkey"]) > MAXKEYMEMSIZE:
        JSON_OBJECT["lastkey"] = JSON_OBJECT["lastkey"][1:]
    def getKey():
        if key == None:
            intkey = 0
            while str(intkey) in JSON_OBJECT["numerals"]: 
                intkey += 1
            return str(intkey) 
        return str(key).strip()

    with open(FILENAME, 'w') as file:
        finalkey = getKey()
        JSON_OBJECT["numerals" if str.isdigit(finalkey) else "custom"][finalkey] = data
        if len(JSON_OBJECT["lastkey"]) == 0 or JSON_OBJECT["lastkey"][-1] != finalkey:
            JSON_OBJECT["lastkey"].append(finalkey)
        print("WRITING DATA TO " + finalkey)
        json.dump(JSON_OBJECT, file)
        
def writeObjToFile(JSON_OBJECT):
    with open(FILENAME, 'w') as file:
        json.dump(JSON_OBJECT, file)
   
        
def save(args):
    pass

def file(args):
    pass

def move(args):
    pass

def copy(args):
    JSON_OBJECT = readFromFile()
    key = JSON_OBJECT["lastkey"][-1]
    if len(args) > 2:
        key = args[2].strip()
    isint = str.isdigit(key)
    
    pyperclipcopy(JSON_OBJECT["numerals" if isint else "custom"][key])
    
    delete = True if len(args) == 4 and args[3].lower().strip() == '-d' else False
    if delete:
        del JSON_OBJECT["numerals" if isint else "custom"][key]
        if key in JSON_OBJECT["lastkey"]:
            JSON_OBJECT["lastkey"] = JSON_OBJECT["lastkey"][1:] if len(JSON_OBJECT["lastkey"]) > 0 else []
        writeObjToFile(JSON_OBJECT)
    
      

def printdb(args):
    pass

def clear(args):
    JSON_OBJECT = JSON_OBJECT = {"numerals": {}, "custom": {}, "lastkey" : []}
    writeObjToFile(JSON_OBJECT)

def delete(args):
    pass

def copykey(args):
    pass

def pipe(args):
    data = stdin.read()
    print(data)
    if len(args) == 2:
        writeToFile(data, args[1].strip())
    else:
        writeToFile(data, None)

    

FUNCTIONS = {
    "-s": save,
    "-f": file,
    "-m": move,
    "-c": copy,
    "-p": printdb,
    "-clear": clear,
    "-d": delete,
    "-ck": copykey
}

def main():
    if len(argv) < 2 or (len(argv) == 2 and '-' not in argv[1]):
        # command | pydis 
        # command | pydis mykey
        pipe(argv)
    else:
        # Fetch function from dictionary and execute
        arg = argv[1].lower().strip()
        func = FUNCTIONS[arg]
        func(argv)

def testmockmain(*args):
    a = [None]
    for item in args:
        a.append(item)
    if len(a) < 2 or (len(a) == 2 and '-' not in a[1]):
        # command | pydis 
        # command | pydis mykey
        pipe(a)
    else:
        # Fetch function from dictionary and execute
        arg = a[1].lower().strip()
        func = FUNCTIONS[arg]
        func(a)

    
if __name__ == '__main__':
    main()
    