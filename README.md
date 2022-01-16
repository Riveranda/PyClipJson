### Examples

command | pyclip                     Saves output of command to key 0
command | pyclip 2                   Saves output of command to key 2

pyclip -s or pyclip s                 Saves output of clipboard to key 0
pyclip -s 2                          Saves output of clipboard to key 2
Keys are by default numerals, but can be anything specified.
We will use 2 dictionaries, numerical keys go in one, otherwise in the other. 

pyclip -f "filepath"|key "25:65"     Saves lines 25-65 from the file at "filepath"

pyclip -m 3 4                        Swaps the contents of 3 and 4

pyclip -c 
pyclip -c 2                          Copies contents of 2 to clipboard
pyclip -c 2 -d                       Copies contents of 2 to clipboard, then deletes.

pyclip -p                            Prints the database
pyclip -p 2                          Prints the contents of 2

pyclip -clear                        Wipes database

pyclip -d 0                          Deleted 0

pyclip -ck 3 4                       Copies contents of 3 to 4 and then deletes 3




