import sys

from compiler_error import CompilerError
import globalVars
from . import vars
from . import back_end as BE

def checkReturn(token):
    '''Provides some limited error checking for return statements. Doesn't do much type checking--simply makes sure that constructors, void functions, and value-returning functions all do what they should.

    Jack's very, very lax typing is kept intact. Type checking could be added, but would require more effort when expressions are involved. Since the only platform we're compiling to treats everything as a 16-bit word, there's at least no impedance mismatch'''
    if vars.parsenum == 2:
        value = token.value

        *NULL, funct_role, returnsType  = BE.functionsInfo.lookupSubroutineInfo(vars.currentClass, vars.currentFunction)

        if funct_role == 'constructor':
            if value != 'this':
                error_middle = ' -- NOT `%s\'' % value 
                if value == ';':
                    error_middle = ''
                raise CompilerError('`%s\' is a constructor and should return `this\'%s. Line %s, %s' % (vars.currentFunction, error_middle, token.line, globalVars.inputFileName))

        elif returnsType == 'void':
            if value != ';':
                raise CompilerError('`%s\' is a void function, and so mustn\'t return a value. It does. Line %s, %s' % (vars.currentFunction, token.line, globalVars.inputFileName))

        else:
            if value == ';':
                raise CompilerError('`%s\' isn\'t a void function, and so it must return a value. Line %s, %s' % (vars.currentFunction, token.line, globalVars.inputFileName))


def checkDotlessFunctionCall(subroutinetoken, callerexpectsreturnval):
    '''This checks whether dotless function calls (i.e. ones of the form `do function()\' or `let thing = function()\' return value when they should (and don't when they should not) AND makes sure we don't issue meaningless method calls.'''

    *NULL, calledfunct, calledreturns = BE.functionsInfo.\
                                        lookupSubroutineInfo(vars.currentClass, subroutinetoken)
    *NULL, callingfunct, NULL = BE.functionsInfo.lookupSubroutineInfo(vars.currentClass, vars.currentFunction)

    if calledfunct == 'method' and callingfunct == 'function':
        raise CompilerError('Argument less method calls cannot be made from within functions. Method calls must be of the form `OBJECT.method(), or else we have no object to work on`. Line %s, %s' % (subroutinetoken.line, globalVars.inputFileName))

    if callerexpectsreturnval == True:
        if calledreturns == 'void':
            print("WARNING: Call to `%s\' expects a return value, but subroutine is of type void. Line %s, %s" % (subroutinetoken.value, subroutinetoken.line, globalVars.inputFileName), file=sys.stderr)
    else:
        if calledreturns != 'void':
            print("WARNING: Function `%s\' is value returning, but that value is ignored. Line %s, %s" % (subroutinetoken.value, subroutinetoken.line, globalVars.inputFileName), file=sys.stderr)
            # raise RuntimeError("Called function `%s\' %s a return value. It %s. Line %s, %s" % (functname, msg[0], msg[1], getattr(subroutinetoken, 'line'), globalVars.inputFileName))
    return calledfunct
