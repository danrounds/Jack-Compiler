from CompilerError import CompilerError
import globalVars


def initializeHashTables(_variableTable, _classAndFunctionsHash):
    global functionsInfo, varTable
    varTable = _variableTable
    functionsInfo = _classAndFunctionsHash


def setGlobals(_parseNum=None, _currentClass=None, _currentFn=None,
               _currentFnType=None):
    global parseNum, currentClass, currentFn, currentFnType
    if _parseNum is not None:
        parseNum = _parseNum
    elif _currentClass:
        currentClass = _currentClass
    elif _currentFn:
        currentFn = _currentFn
    elif _currentFnType:
        currentFnType = _currentFnType


def defineOutput(_output):
    global output
    output = _output


"""
This is where all the code output logic is stored. Each section is called
directly from its relevant parse stage:
"""


def SubroutineDeclaration(token):
    if parseNum == 2:
        currentFnContext = functionsInfo.getCurrentFnContext()
        shouldReturnType = currentFnContext.returnsType
        num = currentFnContext.nVars

        # The function declaration, itself:
        output.code('function %s.%s %s' %
                    (currentClass, currentFn, num))

        # If we're dealing with a constructor, we've got to allocate memory,
        # and put the reference to our new object in the right memory location
        if currentFnType == 'constructor':
            if currentClass == shouldReturnType:
                memtoalloc = functionsInfo.getFieldN()
                output.code('push constant '+str(memtoalloc))
                output.code('call Memory.alloc 1')
                # ^ Leaves the address of our allocated object @ top of stack
                output.code('pop pointer 0')
                # ^ Puts &NEW_OBJECT in pointer 0 (`@THIS', in Hack Assembly)
            else:
                raise CompilerError('A constructor\'s return type must be the '
                                    'class type, Line %s, %s' %
                                    (token.line, globalVars.inputFileName))

        # If we're dealing with a method, we have to pop pointer to the object
        # upon which our method operates
        elif currentFnType == 'method':
            # `argument 0` is the object called by the method. This pops it
            # into pointer 0, so that `this n` VM commands work.
            output.code('push argument 0')
            output.code('pop pointer 0')


def LetStatement_ARRAY_BASE(variableToken):
    if parseNum == 2:
        NULL, kind, n = varTable.lookupVariable(variableToken)
        output.code('push %s %s' % (kind, n))
        output.code('add')
        # ^ adds variable *(kind n) to the prior stack value (an expression)


def LetStatement(array, variableToken):
    # I THINK This is where you could optimize code for array indexing
    # knowable at compile time
    if parseNum == 2:
        NULL, kind, n = varTable.lookupVariable(variableToken)
        if array is True:
            output.code('pop temp 0')
            output.code('pop pointer 1')
            output.code('push temp 0')
            output.code('pop that 0')
        else:
            output.code('pop %s %s' % (kind, n))


def IfStatement_IF(n):
    output.code('if-goto IF_TRUE'+n)  # pops the result of conditional in
    output.code('goto IF_FALSE'+n)    # the If statement. If True, jumps
    output.code('label IF_TRUE'+n)    # to IF_TRUE+n.


# \/ These two functions run (output) if the parser finds an `else`##
def IfStatement_ELSE_A(n):
    output.code('goto IF_END'+n)
    output.code('label IF_FALSE'+n)


def IfStatement_ELSE_B(n):
    output.code('label IF_END'+n)
# /\ These two functions run (output) if the parser finds an `else`##


# \/ This gets output only if we don't have an `else`
def IfStatement_NOELSE(n=''):
    output.code('label IF_FALSE'+n)


def WhileStatement_1(n):
    output.code('label WHILE_EXP'+n)


def WhileStatement_2(n):
    output.code('not')  # The expression is NOT-ed, and if it then equals
    output.code('if-goto WHILE_END'+n)  # zero, the jump is made to END


def WhileStatement_3(n):
    output.code('goto WHILE_EXP'+n)
    output.code('label WHILE_END'+n)


def DoStatementNULLPOP():
    # This can be removed, so long as you remove the corresponding code in
    # `ReturnStatementVoid'. It could also be left in if the idiom of calling
    # function-returning values but ignoring the return value is considered
    # useful.
    output.code('pop temp 0')


def ReturnStatementVoidPrep(token):
    if parseNum == 2:
        if functionsInfo.getCurrentFnContext().returnsType == 'void':
            output.code('push constant 0')
        # /\ If you deleted the code that automatically pops the result of a
        # `do`, then this code would be unnecessary, since the compiler /could/
        # restrict `do` calls for non-void functions.


def ReturnStatementOutput():
    output.code("return")


# ops = {"+":'add', "-":'sub', "&":'and', "|":'or', "<":'lt', ">":'gt', "=":'eq', "*":"call Math.multiply 2",
#        "/":"call Math.divide 2",}
def ExpressionOP(op):
    # Tried this as a "jump" into the dictionary above, instead of loads of
    # sequential logic, but it offered no performance improvements
    if parseNum == 2:
        if op == "+":    output.code('add')
        elif op == "-":  output.code('sub')
        elif op == "&":  output.code('and')
        elif op == "|":  output.code('or')
        elif op == "<":  output.code('lt')
        elif op == ">":  output.code('gt')
        elif op == "=":  output.code('eq')
        elif op == "*":  output.code("call Math.multiply 2")
        elif op == "/":  output.code("call Math.divide 2")
        # output.code(CodeProcess.ops[op])


def TermINTEGER(token):
    output.code("push constant " + token.value)


def TermSTRING(token):
    if parseNum == 2:
        string = token.value
        output.code("push constant %s" % len(string))
        output.code("call String.new 1")
        for c in string:
            output.code("push constant %s" % ord(c))
            output.code("call String.appendChar 2")


def TermKEYWORD(token):
    if parseNum == 2:
        keyword = token.value
        if keyword == 'true':
            output.code("push constant 1")
            output.code('neg')
        elif keyword == 'false':
            output.code("push constant 0")
        elif keyword == 'null':
            output.code("push constant 0")
        elif keyword == 'this':
            if functionsInfo.getCurrentFnContext().fnType != 'function':
                output.code("push pointer 0")
            else:
                raise CompilerError('`this\' cannot be used in a function. Line %s, %s' % (token.line, globalVars.inputFileName))


def TermARRAY(variableToken):
    if parseNum == 2:
        NULL, kind,  n = varTable.lookupVariable(variableToken)
        output.code('push %s %s' % (kind, n))
        output.code('add')
        output.code('pop pointer 1')
        output.code('push that 0')


def TermUNARYOP(op):
    if parseNum == 2:
        if op.value == '~':
            output.code('not')
        else:
            output.code('neg')


def TermVARNAME(variableToken):
    if parseNum == 2:
        NULL, kind, n = varTable.lookupVariable(variableToken)
        output.code('push %s %s' % (kind, n))


def SubroutineCall_NoDot_A(calledFnRole):
    """
    Parses a subroutine call without an argument or preceding class name, i.e.
    `subroutineName(arguments)` -- i.e. a `function' call (if it's not, in
    fact, a syntax error)
    """
    if calledFnRole == 'method':
        output.code('push pointer 0')


def SubroutineCall_NoDot_B(subroutineToken, numberOfParams):
    """
    Second part of our logic/error-checking for method-less/Class-less
    subroutine calls -- i.e., in the language of Jack, "function" call
    """
    if parseNum == 2:

        k, NULL, proceduretype, NULL = functionsInfo.lookupFn(subroutineToken)
        if proceduretype == 'method': numberOfParams += 1

        if numberOfParams != k:
            raise CompilerError('Function `%s\' takes %s arguments. Number '
                                'given: %s. Line %s, %s' %
                                (subroutineToken.value, k, numberOfParams,
                                 subroutineToken.line, globalVars.inputFileName))
        else:
            output.code('call %s.%s %s' % (currentClass, subroutineToken.value, numberOfParams))


def SubroutineCall_WithDot_A(subroutineToken, classOrObject):
    '''`object.method()` or `class.subroutine()`'''

    methodCall = function = None
    if parseNum == 2:

        # \/ this checks to see whether what we have is `var.method()`, as
        # opposed to a `class.function()` call
        try:
            Class, kind, n = varTable.lookupVariable(classOrObject)
            methodCall = True
            output.code('push %s %s' % (kind, n))
        except:
            varTable.checkClassExistence(classOrObject)
            Class = classOrObject.value
            methodCall = False

        function = '%s.%s' % (Class, subroutineToken.value)

    return methodCall, function


def SubroutineCall_WithDot_B(subroutineToken, fn, nExprsInCall):
    """Second part of output logic for `class.subroutine()`"""

    if parseNum == 2:
        try:
            expectedParams, *NULL = functionsInfo.lookupFn(fn)
            if int(nExprsInCall) != int(expectedParams):
                raise CompilerError('Function `%s` takes %s argument(s). '
                                    'Number given: %s. Line %s, %s' %
                                    (fn, expectedParams, nExprsInCall,
                                     subroutineToken.line, globalVars.inputFileName))

        except AttributeError:
            raise CompilerError('Call to `%s`: Class/object does not exist or '
                                'subroutine doesn\'t (or both). Line %s, %s' %
                                (fn, subroutineToken.line, globalVars.inputFileName))
            # if STRONGLINKING == True:
            #     ...

        output.code('call %s %s' % (fn, nExprsInCall))
