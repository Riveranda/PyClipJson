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

import unittest
import sys
import os
from os.path import exists

if __name__ != "__main__":
    from Pydis import *
else:
    sys.path.append('../Pydis')
    from Pydis.Pydis import *
    
def deldatabasefile():
    try:
        os.remove(".pydisstore.json")
    except FileNotFoundError as _:
        pass
    

pythonstr = "python3 Pydis/Pydis.py"

def systemexcecute(str):
    os.system(str)
class TestPipe(unittest.TestCase):
    
    def test_pipe(self):
        deldatabasefile()
        print("NAME: " + __name__)
        os.system("echo \"test1\" | " + pythonstr)
        self.assertTrue(exists(FILENAME))

        os.system("echo \"test2\" | " + pythonstr + " 2")  
        json = readFromFile()
        self.assertTrue("0" in json["numerals"])      
        self.assertEqual("test1\n", json["numerals"]["0"])
        self.assertTrue("2" in json["numerals"])
        self.assertEqual("test2\n", json["numerals"]["2"])
    
    def test_pipe_custom_key(self):
        deldatabasefile()
        os.system("echo \"test1\" | " + pythonstr + " mykey")
        json = readFromFile()
        self.assertTrue("mykey" in json["custom"])   
        self.assertEqual("test1\n", json["custom"]["mykey"])
        
    
    def test_pipe_overrite(self):
        deldatabasefile()
        os.system("echo \"test1\" | " + pythonstr + " mykey")
        os.system("echo \"test2\" | " + pythonstr + " mykey")
        json = readFromFile()
        self.assertEqual(json["custom"]["mykey"], "test2\n")
    
class TestCopy(unittest.TestCase):
    
    def test_copy(self):
        deldatabasefile()
        os.system("echo \"test1\" | " + pythonstr + " mykey")
        os.system(pythonstr + " -c mykey")
    
    def test_copy_delete(self):
        deldatabasefile()
        os.system("echo \"test1\" | " + pythonstr + " mykey")
        os.system(pythonstr + " -c mykey -d")
        json = readFromFile()
        self.assertFalse("mykey" in json["custom"])
        self.assertFalse("mykey" in json["lastkey"])

class TestClear(unittest.TestCase):
    
    def test_clear(self):
        deldatabasefile()
        os.system("echo \"test1\" | " + pythonstr)
        os.system(pythonstr + " -clear")
        json = readFromFile()
        self.assertEqual({"numerals": {}, "custom": {}, "lastkey" : []}, json)     
        
class TestMove(unittest.TestCase):
    
    def test_move(self):
        deldatabasefile()
        os.system("echo \"test1\" | " + pythonstr)
        os.system("echo \"test2\" | " + pythonstr)
        os.system(pythonstr + " -m 1 0")
        json = readFromFile()
        self.assertTrue("0" in json["numerals"])
        self.assertTrue("1" in json["numerals"])
        self.assertEqual(json["numerals"]["0"], "test2\n")
        self.assertEqual(json["numerals"]["1"], "test1\n")
        

class TestFile(unittest.TestCase):
    
    def test_file_save(self):
        contents = None
        with open("testfile.txt") as file:
            contents = file.read()
        deldatabasefile()
        os.system(pythonstr + " -f \"testfile.txt\"")
        json = readFromFile()
        self.assertTrue("0" in json["numerals"])
        self.assertEqual(contents, json["numerals"]["0"])
    
    def test_file_custom_key(self):
        contents = None
        with open("testfile.txt") as file:
            contents = file.read()
        deldatabasefile()
        os.system(pythonstr + " -f \"testfile.txt\" 1")
        json = readFromFile()
        self.assertTrue("1" in json["numerals"])
        self.assertEqual(contents, json["numerals"]["1"])
    
    def test_file_readrange(self):
        contents = None
        string = ""
        with open("testfile.txt") as file:
            contents = file.readlines()[0:6]
        for s in contents:
            string += s
        deldatabasefile()
        os.system(pythonstr + " -f \"testfile.txt\" 1 0:5")
        json = readFromFile()
        self.assertTrue("1" in json["numerals"])
        self.assertEquals(string, json["numerals"]["1"])


if __name__ == '__main__':
    unittest.main()
