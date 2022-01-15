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
import logging as log
import os
from os.path import exists

  
# importing
sys.path.append('../Pydis')
from Pydis.Pydis import *

def run(str):
    os.system(str)
    
def deldatabasefile():
    try:
        os.remove(".pydisstore.json")
    except FileNotFoundError as _:
        pass
    

pythonstr = "python3 Pydis/Pydis.py"

class TestPipe(unittest.TestCase):
    
    def test_pipe(self):
        deldatabasefile()
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


        
         
        
    
if __name__ == '__main__':
    unittest.main()
