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
MAXKEYMEMSIZE = 20

class InvalidKeyException(Exception):
    def __init__(self):
        self.message = "The passed key is invalid."
        super().__init__(self.message)

class InvalidArgumentException(Exception):
    def __init__(self):
        self.message = "Invalid key."
        super().__init__(self.message)

def subcat(key):
    return "numerals" if str.isdigit(key) else "custom"


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
        JSON_OBJECT[subcat(finalkey)][finalkey] = data
        if len(JSON_OBJECT["lastkey"]) == 0 or JSON_OBJECT["lastkey"][-1] != finalkey:
            JSON_OBJECT["lastkey"].append(finalkey)
        print("WRITING DATA TO " + finalkey)
        json.dump(JSON_OBJECT, file, indent=4)
        
def writeObjToFile(JSON_OBJECT):
    with open(FILENAME, 'w') as file:
        json.dump(JSON_OBJECT, file, indent=4)
   
        
def save(args):
    pass

def file(args):
    if len(args) > 2:
        contents, key = None, None
        filepath = args[2].strip()        
        with open(filepath, "r") as file:
            
            def readrange(arg):
                split = arg.split(":")
                range = [int(i) for i in split]
                string = ""
                if(len(range)) > 2 or len(range) == 0:
                    raise InvalidArgumentException
                if len(range) == 1:
                    range.append(range[1])
                for s in file.readlines()[range[0]:range[1] + 1]:
                    string += s
                return string
        
            if len(args) == 3:
                contents = file.read()
            elif len(args) == 4:
                if(':' in args[3]):
                    contents = readrange(args[3])
                else:
                    key = args[3].strip()
                    contents = file.read()
            elif len(args) == 5:
                key = args[3].strip()
                if(':' in args[4]):
                    contents = readrange(args[4])
                
            writeToFile(contents, key)
    else:
        raise InvalidArgumentException
        
def move(args):
    if(len(args) == 4):
        key1, key2 = args[2].strip(), args[3].strip()
        subcat1, subcat2 = subcat(key1), subcat(key2)
        JSON_OBJECT = readFromFile()
        if key1 in JSON_OBJECT[subcat1] and key2 in JSON_OBJECT[subcat2]:
            data1 = JSON_OBJECT[subcat1][key1]
            JSON_OBJECT[subcat1][key1] = JSON_OBJECT[subcat2][key2]
            JSON_OBJECT[subcat2][key2] = data1
            writeObjToFile(JSON_OBJECT)
        else:
            raise InvalidKeyException
    else:
        raise InvalidArgumentException

def copy(args):
    JSON_OBJECT = readFromFile()
    key = None
    if len(args) > 2:
        key = args[2].strip()
    elif len(JSON_OBJECT["lastkey"]) != 0:
        key = JSON_OBJECT["lastkey"][-1]
    else:
        raise InvalidKeyException
    subcat1 = subcat(key)
    if key in JSON_OBJECT[subcat1]:
        pyperclipcopy(JSON_OBJECT[subcat1][key])
        delete = True if len(args) == 4 and args[3].lower().strip() == '-d' else False
        if delete:
            del JSON_OBJECT[subcat1][key]
            if key in JSON_OBJECT["lastkey"]:
                JSON_OBJECT["lastkey"] = JSON_OBJECT["lastkey"][1:] if len(JSON_OBJECT["lastkey"]) > 0 else []
            writeObjToFile(JSON_OBJECT)
    else:
        raise InvalidKeyException
    
      

def printdb(args):
    pass

def clear(args):
    JSON_OBJECT = {"numerals": {}, "custom": {}, "lastkey" : []}
    writeObjToFile(JSON_OBJECT)

def delete(args):
    if(len(args) == 3):
        key = args[2].trim()
        JSON_OBJECT = readFromFile()
        if(str.isdigit(key)):
            del JSON_OBJECT["numerals"][key] 
        else:
            del JSON_OBJECT["custom"][key]
        writeObjToFile(JSON_OBJECT)

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
    
if __name__ == '__main__':
    main()