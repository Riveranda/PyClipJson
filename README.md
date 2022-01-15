### Examples

command | pydis                     Saves output of command to key 0
command | pydis 2                   Saves output of command to key 2

pydis -s or pydis s                 Saves output of clipboard to key 0
pydis -s 2                          Saves output of clipboard to key 2
Keys are by default numerals, but can be anything specified.
We will use 2 dictionaries, numerical keys go in one, otherwise in the other. 

pydis -f "filepath"|key "25:65"     Saves lines 25-65 from the file at "filepath"

pydis -m 3 4                        Swaps the contents of 3 and 4

pydis -c 
pydis -c 2                          Copies contents of 2 to clipboard
pydis -c 2 -d                       Copies contents of 2 to clipboard, then deletes.

pydis -p                            Prints the database
pydis -p 2                          Prints the contents of 2

pydis -clear                        Wipes database

pydis -d 0                          Deleted 0

pydis -ck 3 4                       Copies contents of 3 to 4 and then deletes 3




