import sys

import globalVars

global nCurlies, maxCurlies   # << for insane if/else "stack", to determine
global functionRtnsStack, codeHasTerminated  # whether a function might return


def setParseNum(_parseNum):
    global parseNum
    parseNum = _parseNum


"""
This uses a heuristic that I dreamt up on my own (at the height of compiler
-writing insanity, no less), to determine whether functions seem likely to
return, OR whether we end up with sections of dead code. I'm sure I could
reconstruct the heuristic I had in mind, but the code is unobtrusive, more or
less does what it should (very few false positives), and won't halt
compilation.

If anything, it yields /potentially/ useful warnings.

I also find it kind of charming. It could be removed without penalty (but it
won't be).
"""

unreachableTriggered = False


def stackVarsInit():
    if parseNum == 2:
        global nCurlies, maxCurlies
        nCurlies = maxCurlies = 0


def stackVarsIncr():
    if parseNum == 2:
        global nCurlies, maxCurlies
        nCurlies += 1
        if nCurlies > maxCurlies:
            maxCurlies = nCurlies


def stackVarsDecr():
    if parseNum == 2:
        global nCurlies
        nCurlies -= 1


def stackInit():
    if parseNum == 2:
        global functionRtnsStack
        functionRtnsStack = ""


def stackAddIfStmnt():
    if parseNum == 2:
        global functionRtnsStack
        functionRtnsStack = functionRtnsStack + 'if'+str(nCurlies)


def stackAddElseStmnt():
    if parseNum == 2:
        global functionRtnsStack
        functionRtnsStack = functionRtnsStack + 'else'+str(nCurlies)


def stackAddReturnStmnt():
    if parseNum == 2:
        global functionRtnsStack
        functionRtnsStack = functionRtnsStack + 'return'+str(nCurlies)


# These three functions are used as each statement is parsed,
# to see whether there seems to be unreachable code
def warningTestInit():
    global codeHasTerminated
    codeHasTerminated = False


def warningReduc():
    if parseNum == 2:
        reduction()
        if functionRtnsStack[-7:] == 'return2':
            global codeHasTerminated
            codeHasTerminated = True


def IFissueWarning(token):
    global unreachableTriggered
    # \/ added the parseNum == 2 as a hail Mary
    if parseNum == 2:
        if codeHasTerminated is True and not unreachableTriggered:
            print("Warning: Unreachable code. Line %s, %s" % (token.line, globalVars.inputFileName), file=sys.stderr)
            unreachableTriggered = True
            ###############


def codeCheck(token):
    if parseNum == 2:
        if functionRtnsStack[-7:] not in ('return2', ''):
            old = None
            while old != functionRtnsStack:
                old = functionRtnsStack
                reduction()
        if 'return2' not in functionRtnsStack:
            print("Warning: Function might not return. Make sure your if/elses are mutually exclusive.  Line %s, %s" % (token.line, globalVars.inputFileName), file=sys.stderr)


def reduction():
    global functionRtnsStack
    for i in range(1, maxCurlies):
        str_ = 'if'+str(i)+'return'+str(i+1)
        if str_ + str_ in functionRtnsStack:
            functionRtnsStack = functionRtnsStack.replace(str_+str_, str_)

    for i in range(1, maxCurlies):
        str_ = 'if'+str(i)+'return'+str(i+1)+'else'+str(i)+'return'+str(i+1)
        if str_ in functionRtnsStack:
            functionRtnsStack = functionRtnsStack.replace(str_, 'return'+str(i))

    for i in range(1, maxCurlies):
        str_ = 'if'+str(i)+'return'+str(i)
        if str_ in functionRtnsStack:
            functionRtnsStack = functionRtnsStack.replace(str_, 'return'+str(i))


def reduction2(test, max):
    for i in range(1, max):
        string = 'if'+str(i)+'return'+str(i+1)
        if string+string in test:
            test = test.replace(string+string, string)
    for i in range(1, max):
        string = 'if'+str(i)+'return'+str(i+1)+'else'+str(i)+'return'+str(i+1)
        if string in test:
            test = test.replace(string, 'return'+str(i))
    for i in range(1, max):
        string = 'if'+str(i)+'return'+str(i)
        if string in test:
            test = test.replace(string, 'return'+str(i))
    return(test)
