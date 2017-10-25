import collections

functInfo = collections.namedtuple('functInfo', [
    'kParams', 'nVars', 'fnType', 'returnsType'
])
# ^ the "value" part of the key:value in our class.functions table. Used for
# code output and error-checking.
#
# -`kParams` is the number of variables declared in a function prototype/
#   declaration
# -`nVars` is the number of local variables declared in a given function, i.e.
#  `var int name1, ... n'
# -`fnType`, used to ensure that:
#     * `constructor`s return `this` (parseReturnStatement),
#     * `this` is not used in `function`s,
#     * `functions` don't call `methods` without passing an object
#        (i.e OBJECT.method)
#     * `methods` do a `push pointer 0` before the other arguments are pushed
#        and before `call Class.Function k`
#     * `call Class.Function k` has the right number of arguments (i.e.
#        accounts for the `this` in method calls)
# -`returnsType` is used to make sure `void` functions don't return a value,
#   and that non-voids return one.
#   In theory, it could be used to introduce strong typing into Jack.


def getJackStdLibrary():
    return {
        'Math^max': functInfo(kParams='2', nVars='x', fnType='function', returnsType='int'),
        'Array^new': functInfo(kParams='1', nVars='x', fnType='function', returnsType='Array'),
        'Memory^deAlloc': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'String^dispose': functInfo(kParams='1', nVars='x', fnType='method', returnsType='void'),
        'String^backSpace': functInfo(kParams='0', nVars='x', fnType='function', returnsType='char'),
        'Math^sqrt': functInfo(kParams='1', nVars='x', fnType='function', returnsType='int'),
        'Math^init': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Keyboard^readChar': functInfo(kParams='0', nVars='x', fnType='function', returnsType='char'),
        'Array^dispose': functInfo(kParams='1', nVars='x', fnType='method', returnsType='void'),
        'Math^min': functInfo(kParams='2', nVars='x', fnType='function', returnsType='int'),
        'String^setCharAt': functInfo(kParams='3', nVars='x', fnType='method', returnsType='void'),
        'Memory^init': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Memory^peek': functInfo(kParams='1', nVars='x', fnType='function', returnsType='int'),
        'Screen^drawRectangle': functInfo(kParams='4', nVars='x', fnType='function', returnsType='void'),
        'Output^printChar': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'Keyboard^readInt': functInfo(kParams='1', nVars='x', fnType='function', returnsType='int'),
        'String^length': functInfo(kParams='1', nVars='x', fnType='method', returnsType='int'),
        'Sys^init': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Math^multiply': functInfo(kParams='2', nVars='x', fnType='function', returnsType='int'),
        'Sys^error': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'Sys^wait': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'Output^backSpace': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Memory^poke': functInfo(kParams='2', nVars='x', fnType='function', returnsType='void'),
        'Sys^halt': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'String^new': functInfo(kParams='1', nVars='x', fnType='constructor', returnsType='String'),
        'Output^init': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Math^abs': functInfo(kParams='1', nVars='x', fnType='function', returnsType='int'),
        'String^eraseLastChar': functInfo(kParams='1', nVars='x', fnType='method', returnsType='void'),
        'Output^printInt': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'Screen^init': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Output^println': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'Screen^drawCircle': functInfo(kParams='3', nVars='x', fnType='function', returnsType='void'),
        'Math^divide': functInfo(kParams='2', nVars='x', fnType='function', returnsType='int'),
        'Screen^drawPixel': functInfo(kParams='2', nVars='x', fnType='function', returnsType='void'),
        'Output^moveCursor': functInfo(kParams='2', nVars='x', fnType='function', returnsType='void'),
        'Keyboard^keyPressed': functInfo(kParams='0', nVars='x', fnType='function', returnsType='char'),
        'Screen^setColor': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'Memory^alloc': functInfo(kParams='1', nVars='x', fnType='function', returnsType='Array'),
        'Screen^drawLine': functInfo(kParams='4', nVars='x', fnType='function', returnsType='void'),
        'String^newLine': functInfo(kParams='0', nVars='x', fnType='function', returnsType='char'),
        'String^appendChar': functInfo(kParams='2', nVars='x', fnType='method', returnsType='String'),
        'Output^printString': functInfo(kParams='1', nVars='x', fnType='function', returnsType='void'),
        'Keyboard^init': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'String^charAt': functInfo(kParams='2', nVars='x', fnType='method', returnsType='char'),
        'Keyboard^readLine': functInfo(kParams='1', nVars='x', fnType='function', returnsType='String'),
        'String^doubleQuote': functInfo(kParams='0', nVars='x', fnType='function', returnsType='char'),
        'Screen^clearScreen': functInfo(kParams='0', nVars='x', fnType='function', returnsType='void'),
        'String^setInt': functInfo(kParams='2', nVars='x', fnType='method', returnsType='void'),
        'String^intValue': functInfo(kParams='1', nVars='x', fnType='method', returnsType='int')
    }
