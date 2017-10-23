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
                                    (vars.currentFn, errorMiddle,
                                     token.line, globalVars.inputFileName))

        elif returnsType == 'void':
            if value != ';':
                raise CompilerError('`%s` is a void function, and so mustn\`t'
                                    'return a value. It does. Line %s, %s' %
                                    (vars.currentFn, token.line,
                                     globalVars.inputFileName))

        else:
            if value == ';':
                raise CompilerError('`%s` isn`t a void function, and so must '
                                    'return a value. Line %s, %s' %
                                    (vars.currentFn, token.line,
                                     globalVars.inputFileName))


def checkDotlessFunctionCall(subroutineToken, callerExpectsReturnval):
    """
    This checks whether dotless function calls (i.e. ones of the form
    `do function()` or `let thing = function()` return value when they should
    (and don\'t when they should not) AND makes sure we don't issue meaningless
    method calls.
    """

    if vars.parsenum != 2:
        return

    *NULL, calledFunct, calledReturns = functionsInfo.lookupFn(subroutineToken)

    *NULL, callingfunct, NULL = functionsInfo.getCurrentFnContext()

    if calledFunct == 'method' and callingfunct == 'function':
        raise CompilerError('Argument-less method calls cannot be made from '
                            'within functions. Method calls must be of the '
                            'form `OBJECT.method(), or else we have no object '
                            'to work on`. Line %s, %s' %
                            (subroutineToken.line, globalVars.inputFileName))

    if callerExpectsReturnval is True:
        if calledReturns == 'void':
            print('WARNING: Call to `%s` expects return value, but subroutine '
                  'is of type void. Line %s, %s' %
                  (subroutineToken.value, subroutineToken.line,
                   globalVars.inputFileName), file=sys.stderr)

    else:
        if calledReturns != 'void':
            print('WARNING: Function `%s` is value-returning, but that value '
                  'is ignored. Line %s, %s' %
                  (subroutineToken.value, subroutineToken.line,
                   globalVars.inputFileName), file=sys.stderr)

    return calledFunct


def initialize(_functionsInfo):
    global functionsInfo
    functionsInfo = _functionsInfo
