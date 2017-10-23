import collections

functInfo = collections.namedtuple('functInfo', [
    'k_params', 'n_vars', 'funct_type', 'returnsType'
])
# ^ the "value" part of the key:value in our class.functions table. Used for
# code output and error-checking.
#
# -`n_vars` is the number of local variables declared in a given function, i.e.
#  `var int name1, ... n'
# -`k_params` is the number of variables declared in a function prototype/
#   declaration
# -`funct_type`, used to ensure that:
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
        'Math^max': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='int'),
        'Array^new': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='Array'),
        'Memory^deAlloc': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'String^dispose': functInfo(k_params='1', n_vars='x', funct_type='method', returnsType='void'),
        'String^backSpace': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='char'),
        'Math^sqrt': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='int'),
        'Math^init': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Keyboard^readChar': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='char'),
        'Array^dispose': functInfo(k_params='1', n_vars='x', funct_type='method', returnsType='void'),
        'Math^min': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='int'),
        'String^setCharAt': functInfo(k_params='3', n_vars='x', funct_type='method', returnsType='void'),
        'Memory^init': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Memory^peek': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='int'),
        'Screen^drawRectangle': functInfo(k_params='4', n_vars='x', funct_type='function', returnsType='void'),
        'Output^printChar': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'Keyboard^readInt': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='int'),
        'String^length': functInfo(k_params='1', n_vars='x', funct_type='method', returnsType='int'),
        'Sys^init': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Math^multiply': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='int'),
        'Sys^error': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'Sys^wait': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'Output^backSpace': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Memory^poke': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='void'),
        'Sys^halt': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'String^new': functInfo(k_params='1', n_vars='x', funct_type='constructor', returnsType='String'),
        'Output^init': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Math^abs': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='int'),
        'String^eraseLastChar': functInfo(k_params='1', n_vars='x', funct_type='method', returnsType='void'),
        'Output^printInt': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'Screen^init': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Output^println': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'Screen^drawCircle': functInfo(k_params='3', n_vars='x', funct_type='function', returnsType='void'),
        'Math^divide': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='int'),
        'Screen^drawPixel': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='void'),
        'Output^moveCursor': functInfo(k_params='2', n_vars='x', funct_type='function', returnsType='void'),
        'Keyboard^keyPressed': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='char'),
        'Screen^setColor': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'Memory^alloc': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='Array'),
        'Screen^drawLine': functInfo(k_params='4', n_vars='x', funct_type='function', returnsType='void'),
        'String^newLine': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='char'),
        'String^appendChar': functInfo(k_params='2', n_vars='x', funct_type='method', returnsType='String'),
        'Output^printString': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='void'),
        'Keyboard^init': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'String^charAt': functInfo(k_params='2', n_vars='x', funct_type='method', returnsType='char'),
        'Keyboard^readLine': functInfo(k_params='1', n_vars='x', funct_type='function', returnsType='String'),
        'String^doubleQuote': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='char'),
        'Screen^clearScreen': functInfo(k_params='0', n_vars='x', funct_type='function', returnsType='void'),
        'String^setInt': functInfo(k_params='2', n_vars='x', funct_type='method', returnsType='void'),
        'String^intValue': functInfo(k_params='1', n_vars='x', funct_type='method', returnsType='int')
    }
