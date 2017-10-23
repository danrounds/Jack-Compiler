import sys

from compiler_error import CompilerError
import globalVars
from . import vars


def checkReturn(token):
    """
    Provides some limited error checking for return statements. Doesn't do much
    type checking--simply makes sure that constructors, void functions, and
    value-returning functions all do what they should.

    Jack's very, very lax typing is kept intact. Type checking could be added,
    but would require more effort when expressions are involved. Since the only
    platform we're compiling to treats everything as a 16-bit word, there's at
    least no impedance mismatch
    """

    if vars.parsenum == 2:
        value = token.value

        *NULL, functRole, returnsType = functionsInfo.getCurrentFnContext()

        if functRole == 'constructor':
            errorMiddle = ''
            if value != 'this':
                errorMiddle = '. Found: `%s`' % value
                raise CompilerError('`%s` is a constructor and should return '
                                    '`this`%s. Line %s, %s' %
                                    (vars.currentFunction, errorMiddle,
                                     token.line, globalVars.inputFileName))

        elif returnsType == 'void':
            if value != ';':
                raise CompilerError('`%s` is a void function, and so mustn\`t'
                                    'return a value. It does. Line %s, %s' %
                                    (vars.currentFunction, token.line,
                                     globalVars.inputFileName))

        else:
            if value == ';':
                raise CompilerError('`%s` isn`t a void function, and so must '
                                    'return a value. Line %s, %s' %
                                    (vars.currentFunction, token.line,
                                     globalVars.inputFileName))


def checkDotlessFunctionCall(subroutinetoken, callerexpectsreturnval):
    """
    This checks whether dotless function calls (i.e. ones of the form
    `do function()` or `let thing = function()` return value when they should
    (and don\'t when they should not) AND makes sure we don't issue meaningless
    method calls.
    """

    if vars.parsenum != 2:
        return

    *NULL, calledfunct, calledreturns = functionsInfo.lookupFn(subroutinetoken)

    *NULL, callingfunct, NULL = functionsInfo.getCurrentFnContext()

    if calledfunct == 'method' and callingfunct == 'function':
        raise CompilerError('Argument-less method calls cannot be made from '
                            'within functions. Method calls must be of the '
                            'form `OBJECT.method(), or else we have no object '
                            'to work on`. Line %s, %s' %
                            (subroutinetoken.line, globalVars.inputFileName))

    if callerexpectsreturnval is True:
        if calledreturns == 'void':
            print('WARNING: Call to `%s` expects return value, but subroutine '
                  'is of type void. Line %s, %s' %
                  (subroutinetoken.value, subroutinetoken.line,
                   globalVars.inputFileName), file=sys.stderr)

    else:
        if calledreturns != 'void':
            print('WARNING: Function `%s` is value-returning, but that value '
                  'is ignored. Line %s, %s' %
                  (subroutinetoken.value, subroutinetoken.line,
                   globalVars.inputFileName), file=sys.stderr)

    return calledfunct


def initialize(_functionsInfo):
    global functionsInfo
    functionsInfo = _functionsInfo
