#!/usr/bin/env python3

'''A SERIES OF TESTS FOR THE `tECS VM LANGUAGE TO HACK ASSEMBLY TRANSLATOR.'
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Output isn't compared to anything; we're just seeing if the translator can convert a large set of files, without crashing.

Other tests exist elsewhere (they came with the book), however automating them is not entirely straightforward.

Completion without obvious error messages should be treated as success.'''


from VM import *
import time

################################################################################
################################################################################
################################################################################
################################################################################
def testscriptbootstrap():
    '''Test script for the VM tests that require bootstrap code; files from book'''
    tic = time.clock()
    a = ['./tests/control/FunctionCalls/FibonacciElement', 'FibonacciElement']
    b = ['./tests/control/FunctionCalls/StaticsTest', 'StaticsTest']
    test = [a,b]
    for i in test:
        vmtoassembly(i[0],i[1])
    toc = time.clock()
    print("DONE. Time to complete: %s" % (toc - tic))

def testscript():
    '''Test script for VM tests that don't require the bootstrap code; files from the book'''
    tic = time.clock()
    a = ['./tests/arithmetic/MemoryAccess/BasicTest/', 'BasicTest']
    b = ['./tests/arithmetic/MemoryAccess/PointerTest/', 'PointerTest']
    c = ['./tests/arithmetic/MemoryAccess/StaticTest/', 'StaticTest']
    d = ['./tests/arithmetic/StackArithmetic/SimpleAdd/', 'SimpleAdd']
    e = ['./tests/arithmetic/StackArithmetic/StackTest', 'StackTest']
    f = ['./tests/control/ProgramFlow/BasicLoop/', 'BasicLoop']
    g = ['./tests/control/ProgramFlow/FibonacciSeries/', 'FibonacciSeries']
    h = ['./tests/control/FunctionCalls/SimpleFunction/', 'SimpleFunction']

    test = [a,b,c,d,e,f,g,h]
    for i in test:
        vmtoassembly(bootstrap=False, pathorfile=i[0], outputfile=i[1])
    toc = time.clock()
    print("DONE. Time to complete: %s" % (toc - tic))

def nonbooktest():
    '''Test script for the VM tests that require bootstrap code; code is a large collection of games from a 2011 class'''
    tic = time.clock()
    a1 = '../Compiler/tests/test_code0/Extras_(Non_Project)/BeerTanks/'
    b1 = '../Compiler/tests/test_code0/Extras_(Non_Project)/Binge/'
    c1 = '../Compiler/tests/test_code0/Extras_(Non_Project)/Darts/'
    d  = '../Compiler/tests/test_code0/Extras_(Non_Project)/hangman/'
    e  = '../Compiler/tests/test_code0/Extras_(Non_Project)/LePacMan/'
    f  = '../Compiler/tests/test_code0/Extras_(Non_Project)/LunarLander2/'
    g  = '../Compiler/tests/test_code0/Extras_(Non_Project)/Maze/'
    h  = '../Compiler/tests/test_code0/Extras_(Non_Project)/Maze3d/'
    i  = '../Compiler/tests/test_code0/Extras_(Non_Project)/Pong/'
    j  = '../Compiler/tests/test_code0/Extras_(Non_Project)/Schizophrenia/'
    k  = '../Compiler/tests/test_code0/Extras_(Non_Project)/ShapeSwap/'
    l  = '../Compiler/tests/test_code0/Extras_(Non_Project)/Simon/'
    m  = '../Compiler/tests/test_code0/Extras_(Non_Project)/SlotMachineGame/'
    n  = '../Compiler/tests/test_code0/Extras_(Non_Project)/SnakeLike/'
    o  = '../Compiler/tests/test_code0/Extras_(Non_Project)/SpaceInvaders/'
    q  = '../Compiler/tests/test_code0/Extras_(Non_Project)/WormsRock2/'

    test = [a1,b1,c1,d,e,f,g,h,i,j,k,l,m,n,o,q]
    for i in test:
        vmtoassembly(i)
    toc = time.clock()
    print("DONE. Time to complete %s" % (toc - tic))

if __name__ == '__main__':
    print(__doc__ + '\n\n')
    input("Press ENTER to continue")
    testscriptbootstrap()
    input("Press ENTER for next test")
    testscript()
    input("Press ENTER for next test")
    nonbooktest()
