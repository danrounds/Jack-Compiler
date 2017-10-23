def setParseNumber(n):
    """
    This defines a global variable which the compiler uses to generate our hash
    tables (parse # 1) OR to output code (parse # 2) OR to output XML tokens or
    parse tree (parse # 0)
    """

    global parsenum
    parsenum = n


def setCurrentClass(classtoken):
    """Sets the class that we're currently in the midst of parsing"""
    global currentClass
    currentClass = classtoken.value


def setCurrentFunction(functiontoken):
    """Sets the function that we're currently in the midst of parsing"""
    global currentFn
    currentFn = functiontoken.value


def setAndGetCurrentFnType(typeToken):
    """
    Sets the type (as in typing) of the fucking we're currently parsing.
    Returns string : the type in question
    """
    global currentFnType
    currentFnType = typeToken.value
    return currentFnType
