from . import doesFunctionReturn
from . import processCode
from . import returnSemantics
from . import SymbolTable


def setGlobals(parseNum=None, currentClass=None, currentFn=None,
               currentFnType=None):
    """
    Sets the intra-module global values for our backEnd modules.
        inputs:
            parseNum is a number,
            currentClass, currentFn, and currentFnType are tokens
    """
    if parseNum is not None:
        doesFunctionReturn.setParseNum(_parseNum=parseNum)
        processCode.setGlobals(_parseNum=parseNum)
        returnSemantics.setGlobals(_parseNum=parseNum)
        SymbolTable.setGlobals(_parseNum=parseNum)
    elif currentClass:
        currentClass = currentClass.value
        processCode.setGlobals(_currentClass=currentClass)
        SymbolTable.setGlobals(_currentClass=currentClass)
    elif currentFn:
        currentFn = currentFn.value
        processCode.setGlobals(_currentFn=currentFn)
        returnSemantics.setGlobals(_currentFn=currentFn)
        SymbolTable.setGlobals(_currentFn=currentFn)
    elif currentFnType:
        currentFnType = currentFnType.value
        processCode.setGlobals(_currentFnType=currentFnType)
        SymbolTable.setGlobals(_currentFnType=currentFnType)
