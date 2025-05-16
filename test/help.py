#!/usr/bin/env python3
# Check for undocumented functions
# T J Atherton May 2025

import subprocess
import re 
import colored
from colored import stylize

morphocmd = "morpho6"

# Calls the morpho terminal application and perform a help query by piping into stdin
def morphoHelp(query):
    result = subprocess.run(["echo ? "+query+" | "+morphocmd], shell=True, capture_output=True, text=True)
    return result.stdout

# Check if a help query failed
def checkResult(result):
    return re.search("No help found for",result)==None

# Identify methods provided by a morpho class by using introspection
def morphoMethods(clss):
    cmd = "print " + clss + ".respondsto()"
    result = subprocess.run(["echo \""+cmd+"\" | "+morphocmd ], shell=True, capture_output=True, text=True)
    out = result.stdout
    if (re.search("Error",out)==None): # Check the query succeeded
        return [item.strip() for item in out.strip("[]\n").split(",")] # Separate into list
    return [] 


classes = [ "Array", "List", "String", "System", "Tuple" ]

results = []

print("--Begin testing---------------------")

for clss in classes: 
    methods = morphoMethods(clss)
    for m in methods: 
        query = clss + "."+m
        success=checkResult(morphoHelp(query))
        results.append([query, success])

countSuccess = 0

for r in results:
    success = ( stylize("Passed",colored.fg("green")) if r[1] else stylize("Failed",colored.fg("red")))
    print(r[0] + ":" + success)
    if r[1]: countSuccess+=1
    
print("--End testing-----------------------")
print(countSuccess, 'out of', len(results), 'tests passed.')
