# import collections

# funct_info = collections.namedtuple('funct_info', ['k_params', 'n_vars', 'funct_type', 'returnsType'])

# JackStandardLibraryPrototypes = {
#     'Array^new': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='Array'),\
#     'Array^dispose': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'),\
#     'Keyboard^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Keyboard^keyPressed': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#     'Keyboard^readChar': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#     'Keyboard^readInt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#     'Keyboard^readLine': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='String'),\
#     'Math^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Math^abs': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#     'Math^divide': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#     'Math^max': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#     'Math^min': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#     'Math^multiply': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#     'Math^sqrt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#     'Memory^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Memory^alloc': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='Array'),\
#     'Memory^deAlloc': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#     'Memory^peek': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#     'Memory^poke': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^backSpace': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^moveCursor': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^printChar': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^printInt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^println': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Output^printString': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^clearScreen': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^drawCircle': funct_info(k_params='3', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^drawLine': funct_info(k_params='4', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^drawPixel': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^drawRectangle': funct_info(k_params='4', n_vars='x', funct_type='function', returnsType='void'),\
#     'Screen^setColor': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#     'String^new': funct_info(k_params='1', n_vars='x', funct_type='constructor', returnsType='String'),\
#     'String^appendChar': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='String'),\
#     'String^charAt': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='char'),\
#     'String^dispose': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'),\
#     'String^doubleQuote': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#     'String^eraseLastChar': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'),\
#     'String^length': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='int'),\
#     'String^newLine': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#     'String^backSpace': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#     'String^intValue': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='int'),\
#     'String^setCharAt': funct_info(k_params='3', n_vars='x', funct_type='method', returnsType='void'),\
#     'String^setInt': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='void'),\
#     'Sys^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Sys^error': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#     'Sys^halt': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#     'Sys^wait': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
# }


# JackStandardLibraryPrototypes = {
#     'Array':{'new': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='Array'),\
#             'dispose': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void')},\

#     'Keyboard':{'init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#                 'keyPressed': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#                 'readChar': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#                 'readInt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#                 'readLine': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='String')},\

#     'Math':{'init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#             'abs': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#             'divide': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#             'max': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#             'min': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#             'multiply': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'),\
#             'sqrt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int')},\

#     'Memory':{'init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#               'alloc': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='Array'),\
#               'deAlloc': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#               'peek': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'),\
#               'poke': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void')},\

#     'Output':{'init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#               'backSpace': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#               'moveCursor': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'),\
#               'printChar': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#               'printInt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#               'println': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#               'printString': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void')},\

#     'Screen':{'init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#               'clearScreen': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#               'drawCircle': funct_info(k_params='3', n_vars='x', funct_type='function', returnsType='void'),\
#               'drawLine': funct_info(k_params='4', n_vars='x', funct_type='function', returnsType='void'),\
#               'drawPixel': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'),\
#               'drawRectangle': funct_info(k_params='4', n_vars='x', funct_type='function', returnsType='void'),\
#               'setColor': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void')},\

#     'String':{'new': funct_info(k_params='1', n_vars='x', funct_type='constructor', returnsType='String'),\
#               'appendChar': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='String'),\
#               'charAt': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='char'),\
#               'dispose': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'),\
#               'doubleQuote': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#               'eraseLastChar': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'),\
#               'length': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='int'),\
#               'newLine': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#               'backSpace': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'),\
#               'intValue': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='int'),\
#               'setCharAt': funct_info(k_params='3', n_vars='x', funct_type='method', returnsType='void'),\
#               'setInt': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='void')},\

#     'Sys':{'init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#            'error': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'),\
#            'halt': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'),\
#            'wait': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void')},\
# }
