#!/usr/bin/env python3

'''Set of tests, specifically for the JACK to VM (the compiler's front end)
    currentTest
    currentBookTest
    testLexer -- test for tokenizer
    testParse
    extendedTestToken
    extendedTestParse

'''
## TO-DO:
# - Make runnable from Bash, i.e. interface that by runs a default test and lets you choose other tests.
# - Remove (soon-to-be) redundant log feature from `extendedTestParse'. Leave in as commented out code.

import main_loop as main

###############################################################################
#### T  ###### E ###### S ###### T ###### S ###################################
###############################################################################
################ T  ###### E ###### S ###### T ###### S #######################
###############################################################################
############################ T  ###### E ###### S ###### T ###### S ###########
###############################################################################
def currentTest():
    '''This is the default test suite. It sees whether book projects AND a ton of classroom projects (which I've not re-found the link to, yet) will compile.
    If it successfully compiles every file, tokenization and parsing have (ostensibly) worked, as has code output. Warnings are normal, as the compiler is over-zealous.
    If it freezes, it's (probably) because something's wrong with the compiler.'''
    import time
    tic = time.clock()
    a = './tests/test_code0/ArrayTest'
    # b = './tests/test_code0/ExpressionlessSquare'
    c = './tests/test_code0/Square'
    a1 = './tests/test_code0/Extras_(Non_Project)/BeerTanks'
    b1 = './tests/test_code0/Extras_(Non_Project)/Binge'
    c1 = './tests/test_code0/Extras_(Non_Project)/Darts'
    d = './tests/test_code0/Extras_(Non_Project)/hangman'
    e = './tests/test_code0/Extras_(Non_Project)/LePacMan'
    f = './tests/test_code0/Extras_(Non_Project)/LunarLander2'
    g = './tests/test_code0/Extras_(Non_Project)/Maze'
    h = './tests/test_code0/Extras_(Non_Project)/Maze3d'
    i = './tests/test_code0/Extras_(Non_Project)/Pong'
    j = './tests/test_code0/Extras_(Non_Project)/Schizophrenia'
    k = './tests/test_code0/Extras_(Non_Project)/ShapeSwap'
    l = './tests/test_code0/Extras_(Non_Project)/Simon'
    m = './tests/test_code0/Extras_(Non_Project)/SlotMachineGame'
    n = './tests/test_code0/Extras_(Non_Project)/SnakeLike'
    o = './tests/test_code0/Extras_(Non_Project)/SpaceInvaders'
#    p = './tests/test_code0/Extras_(Non_Project)/TicJackToe/src'
#   /\ won't work because it contains escaped characters (e.g. \" to represent a quote), which is
#   outside the language spec
    q = './tests/test_code0/Extras_(Non_Project)/WormsRock2'   
    testpaths = [a, c, a1, b1, c1, d, e, f, g, h, i, j, k, l, m, n, o, q]
    # testpaths = [a, b, c, a1, b1, c1, d, e, f, g, h, i, j, k, l, m, n, o, q]
    for path in testpaths:
        main.mainloop(path)
    toc = time.clock()
    print('===========================================================')
    print("Compilation took %s seconds." % (toc - tic))


def currentBookTest():
    '''Tests the most \"difficult\"-to-compile book projects. If it finishes without error, the compiler's (ostensibly) successfully outputted the proper .vm files'''
    import time
    tic = time.clock()
    a = './tests/test_code1/Average'
    b = './tests/test_code1/ComplexArrays'
    c = './tests/test_code1/ConvertToBin'
    d = './tests/test_code1/Pong'
    e = './tests/test_code1/Seven'
    f = './tests/test_code1/Square'
    testpaths = [a, b, c, d, e, f]
    for path in testpaths:
        main.mainloop(path)
    toc = time.clock()
    print('===========================================================')
    print("Compilation took %s seconds." % (toc - tic))

def testLexer():# unit test for tokenizer
    import subprocess
    a = './tests/test_code0/ArrayTest'
    b = './tests/test_code0/ExpressionlessSquare'
    c = './tests/test_code0/Square'
    testpaths = [a, b, c]
    filelist = []
    for path in testpaths:
#        filelist_, path = main.fileorpathparser(path)
        filelist_ = main.fileorpathparser(path)
        filelist = filelist + filelist_
    for filename in filelist:
        main.mainloop(filename, outputmode='tokens')
    print('===========================================================')
    print('Diff results will appear, below each file. If none appear, everything worked.')
#    batch = './tests/tokentestscript.bat'  # Windows test script
    batch = './tests/tokentestscript.bash'  # Windows test script
    subprocess.call(batch)

def testParse():
# unit test for parser
    import subprocess
    a = './tests/test_code0/ArrayTest'
    b = './tests/test_code0/ExpressionlessSquare'
    c = './tests/test_code0/Square'
    testpaths = [a, b, c]
    filelist = []
    for path in testpaths:
#        filelist_, path = main.fileorpathparser(path)
        filelist_ = main.fileorpathparser(path)
        filelist = filelist + filelist_
    for filename in filelist:
        main.mainloop(filename, outputmode='parse_tree')
    print('===========================================================')
    print('Diff results will appear, below each file. If none appear, everything worked.')
#    batch = './tests/parsetestscript.bat'  # Windows test script
    batch = './tests/parsetestscript.bash'
    subprocess.call(batch)

def extendedTestToken():
    import time
    tic = time.clock()
    a  = './tests/test_code0/Extras_(Non_Project)/BeerTanks'
    b  = './tests/test_code0/Extras_(Non_Project)/Binge'
    c  = './tests/test_code0/Extras_(Non_Project)/Darts'
    d  = './tests/test_code0/Extras_(Non_Project)/hangman'
    e  = './tests/test_code0/Extras_(Non_Project)/LePacMan'
    f  = './tests/test_code0/Extras_(Non_Project)/LunarLander2'
    g  = './tests/test_code0/Extras_(Non_Project)/Maze'
    h  = './tests/test_code0/Extras_(Non_Project)/Maze3d'
    i  = './tests/test_code0/Extras_(Non_Project)/Pong'
    j  = './tests/test_code0/Extras_(Non_Project)/Schizophrenia'
    k  = './tests/test_code0/Extras_(Non_Project)/ShapeSwap'
    l  = './tests/test_code0/Extras_(Non_Project)/Simon'
    m  = './tests/test_code0/Extras_(Non_Project)/SlotMachineGame'
    n  = './tests/test_code0/Extras_(Non_Project)/SnakeLike'
    o0 = './tests/test_code0/Extras_(Non_Project)/SpaceInvaders'
#    p  = './tests/test_code0/Extras_(Non_Project)/TicJackToe\src'
    q  = './tests/test_code0/Extras_(Non_Project)/WormsRock2'
#    testpaths = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o0, p, q]
    testpaths = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o0, q]
    filelist = []
    for path in testpaths:
        filelist_ = main.fileorpathparser(path)
        filelist = filelist + filelist_
    for filename in filelist:
        main.mainloop(filename, outputmode='tokens')
    toc = time.clock()
    print('===========================================================')
    print("%s files tokenized. Tokenizing took %s seconds." % (len(filelist), (toc - tic)))

#def extendedTestParse(log=False):
def extendedTestParse():
    '''Tests the output of the parser (and only the parser), by diff-ing output from other people's files/parser with the output of our parser.
    Errors on `TickJackToe' and `Maze3d' are to be expected, because the comparison files don't use XML `less-than'/`greater-than' symbols correctly, and `TicJackToe' was parsed with a non-spec-compliant parser that allows for escaped characters, e.g. quotation marks: \\\" == \"
    '''
    import subprocess
    import time
    tic = time.clock()
    a = './tests/test_code0/Extras_(Non_Project)/BeerTanks'
    b = './tests/test_code0/Extras_(Non_Project)/Binge'
    c = './tests/test_code0/Extras_(Non_Project)/Darts'
    d = './tests/test_code0/Extras_(Non_Project)/hangman'
    e = './tests/test_code0/Extras_(Non_Project)/LePacMan'
    f = './tests/test_code0/Extras_(Non_Project)/LunarLander2'
    g = './tests/test_code0/Extras_(Non_Project)/Maze'
    h = './tests/test_code0/Extras_(Non_Project)/Maze3d'
    i = './tests/test_code0/Extras_(Non_Project)/Pong'
    j = './tests/test_code0/Extras_(Non_Project)/Schizophrenia'
    k = './tests/test_code0/Extras_(Non_Project)/ShapeSwap'
    l = './tests/test_code0/Extras_(Non_Project)/Simon'
    m = './tests/test_code0/Extras_(Non_Project)/SlotMachineGame'
    n = './tests/test_code0/Extras_(Non_Project)/SnakeLike'
    o = './tests/test_code0/Extras_(Non_Project)/SpaceInvaders'
    # p = './tests/test_code0/Extras_(Non_Project)/TicJackToe/src'
    q = './tests/test_code0/Extras_(Non_Project)/WormsRock2'    
    # testpaths = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]
    testpaths = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, q]
    filelist = []
    for path in testpaths:
        filelist_ = main.fileorpathparser(path)
        filelist = filelist + filelist_
    for filename in filelist:
        main.mainloop(filename, outputmode='parse_tree')
    toc = time.clock()
    print("%s files compiled. Compilation took %s seconds.\n" % (len(filelist), (toc - tic)))
    print('Diff results between our files and reference files:\n')
    batch = './tests/parsetestscriptextended.bash'
    # print('Check shell window to see if the the files match the tests.')
#    batch = './tests/parsetestscriptextended.bat'  # Windows test script
    subprocess.call(batch)
    print('\nCheck `diff\' results, above. TicJackToe will have some disparities, but nothing else ought to.')

#     if log == False:
#         print('Check shell window to see if the the files match the tests.')
# #        batch = './tests/parsetestscriptextended.bat'  # Windows test script
#         batch = './tests/parsetestscriptextended.bash'
#         subprocess.call(batch)
#     else:
#         print("Generating log file...")
# #        batch = './tests/parsetestscriptextended2.bat'  # Windows test script
#         batch = './tests/parsetestscriptextended2.bash'
#         logfilename = 'extended_parse_log.txt'
#         log = open(logfilename, 'wt')
#         p = subprocess.Popen(batch,
#                          shell=True,
#                          bufsize=64,
#                          stdin=subprocess.PIPE,
#                          stderr=subprocess.PIPE,
#                          stdout=subprocess.PIPE)
#         for line in p.stdout:
#             log.write(str(line.rstrip()) + '\n')
#             p.stdout.flush()
#         print('DONE. Log file:', logfilename)

if __name__ == '__main__':
    currentTest()
