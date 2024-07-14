#!/usr/bin/env python3
# Automated testing for memory leaks in Morpho
# Chaitanya Joshi, 2024
#
# Each unit test is run using valgrind and the valgrind log file is
# analyzed for errors
#
# import necessary modules
import os, glob, sys
import regex as rx
from functools import reduce
import operator
import colored
from colored import stylize

VALGRIND_FILE = "valgrind.log"

# define what command to use to invoke the interpreter
command = "valgrind --leak-check=full --log-file=" + VALGRIND_FILE + " morpho6"

# define the file extension to test
ext = 'morpho'

# We reduce any errors to this value
err = '@error'

# We reduce any stacktrace lines to this values
stk = '@stacktrace'

# Removes control characters
def remove_control_characters(str):
    return rx.sub(r'\x1b[^m]*m', '', str.rstrip())

# Simplify error reports
def simplify_errors(str):
    # this monster regex extraxts NAME from error messages of the form error ... 'NAME'
    return rx.sub('.*[E|e]rror[ :]*\'([A-z;a-z]*)\'.*', err+'[\\1]', str.rstrip())

# Simplify stacktrace
def simplify_stacktrace(str):
    return rx.sub(r'.*at line.*', stk, str.rstrip())

# Find an expected value
def findvalue(str):
    return rx.findall(r'// expect: ?(.*)', str)

# Find an expected error
def finderror(str):
    #return rx.findall(r'\/\/ expect ?(.*) error', str)
    return rx.findall(r'.*[E|e]rror[ :].*?(.*)', str)

# Find an expected error
def iserror(str):
    #return rx.findall(r'\/\/ expect ?(.*) error', str)
    test=rx.findall(r'@error.*', str)
    return len(test)>0

# Find an expected error
def isin(str):
    #return rx.findall(r'\/\/ expect ?(.*) error', str)
    test=rx.findall(r'.*in .*', str)
    return len(test)>0

# Remove elements from a list
def remove(list, remove_list):
    test_list = list
    for i in remove_list:
        try:
            test_list.remove(i)
        except ValueError:
            pass
    return test_list

# Find what is expected
def findexpected(str):
    out = finderror(str) # is it an error?
    if (out!=[]):
        out = [simplify_errors(str)] # if so, simplify it
    else:
        out = findvalue(str) # or something else?
    return out

# Works out what we expect from the input file
def getexpect(filepath):
    # Load the file
    file_object = open(filepath, 'r')
    lines = file_object.readlines()
    file_object.close()
    #Find any expected values over all lines
    if (lines != []):
        out = list(map(findexpected, lines))
        out = reduce(operator.concat, out)
    else:
        out = []
    return out

# Gets the output generated
def getoutput(filepath):
    # Load the file
    file_object = open(filepath, 'r')
    lines = file_object.readlines()
    file_object.close()
    # remove all control characters
    lines = list(map(remove_control_characters, lines))
    # Convert errors to our universal error code
    lines = list(map(simplify_errors, lines))
    # Identify stack trace lines
    lines = list(map(simplify_stacktrace, lines))
    for i in range(len(lines)-1):
        if (iserror(lines[i])):
            if (isin(lines[i+1])):
                lines[i+1]=stk
    # and remove them
    return list(filter(lambda x: x!=stk, lines))

# Test a file
def valgrind_test(file,testLog,CI):
    ret = 0
    if not CI:
        print(file+":", end=" ")


    # Create a temporary file in the same directory
    tmp = file + '.out'

    #Get the expected output
    expected=getexpect(file)

    # Run the test
    os.system(command + ' ' +file + ' > ' + tmp)

    # For the valgrind test, we don't care about the output from Morpho, only the log file.
    # The only thing we need to check is whether the test ran successfully.
    if not os.path.exists(tmp):
        # We couldn't run the test
        # Print a message
        if not CI:
            print(stylize("Failed",colored.fg("red")))
            print("  Could not run the test")
        else:
            print("\n::error file = {",file,"}::{",file," Failed}")
            #also print to the test log
            print(file+":", end=" ",file = testLog)
            print("Failed. Could not run the test", file = testLog)
            print("\n",file = testLog)

        return ret

    # If the test was run with valgrind, check the log file for memory leaks
    num_memory_errors = 0
    if os.path.exists(VALGRIND_FILE):
        # Check if there were any errors
        with open(VALGRIND_FILE, 'r') as f:
            for line in f.readlines():
                if 'ERROR SUMMARY' not in line:
                    continue # Wait until we get to the summary
                errors = rx.findall(r'ERROR SUMMARY: (\d+) errors', line)
                num_memory_errors = int(errors[0])
                if num_memory_errors == 0: # No memory errors!
                    ret = 1
                    if not CI:
                        print(file+":", end=" ")
                        print(stylize("Passed",colored.fg("green")))
                else:
                    if not CI:
                        print(stylize("Failed",colored.fg("red")))
                        print(num_memory_errors, " Memory errors found.")
                    else:
                        print("\n::error file = {",file,"}::{",file," Failed}")

        if num_memory_errors == 0:
            # Delete the valgrind log
            os.system('rm ' + VALGRIND_FILE)
            return ret
        # If there were memory errors, print the valgrind log
        #also print the valgrind log to the test log
        print(file+":", end=" ",file = testLog)
        print("Failed", file = testLog)
        print(num_memory_errors, " Memory errors found.", file = testLog)
        print("\n",file = testLog)
        print("Valgrind output:\n", file = testLog)
        # Add the valgrind log to the test log
        with open(VALGRIND_FILE, 'r') as f:
            for line in f.readlines():
                print(line, file = testLog)

        # Delete the valgrind log
        os.system('rm ' + VALGRIND_FILE)
        return ret
    else: # No valgrind log was created
        if not CI:
            print(stylize("Failed",colored.fg("red")))
            print("  Could not find valgrind log")
        else:
            print("\n::error file = {",file,"}::{",file," Failed}")
            print(file+":", end=" ",file = testLog)
            print("Failed. Could not find valgrind log", file = testLog)
            print("\n",file = testLog)
        return ret



print('--Begin testing---------------------')

# open a test log
# write failures to log
success=0 # number of successful tests
total=0   # total number of tests
failedTestsFileName = "FailedValgrindTests.log"

# look for a command line arguement that says
# this is being run for continous integration
CI = False
# Also look for a command line argument that says this is being run with multiple threads
MT = False

for arg in sys.argv:
    if arg == '-c': # if the argument is -c, then we are running in CI mode
        CI = True
    if arg == '-m': # if the argument is -m, then we are running in multi-thread mode
        MT = True
        failedTestsFileName = "FailedTestsValgrindMultiThreaded.log"
        command += " -w4"
        print("Running tests with 4 threads")

files=glob.glob('**/**.'+ext, recursive=True)
with open(failedTestsFileName,'w') as testLog:

    for f in files:
        # print(f)
        success+=valgrind_test(f,testLog,CI)
        total+=1

# if (not CI) and (not success == total):
#     os.system("emacs FailedTests.txt &")

print('--End testing-----------------------')
print(success, 'out of', total, 'tests passed.')
if CI and success<total:
    exit(-1)
