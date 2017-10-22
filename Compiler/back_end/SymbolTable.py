import collections
import sys

from compiler_error import CompilerError
import globalVars
from . import vars


funct_info = collections.namedtuple('funct_info', ['k_params', 'n_vars', 'funct_type', 'returnsType'])
# /\ the "value" part of the key:value in our classDOTfunctions table. Used for code output and error-checking.
#
# -`n_vars` is the number of local variables declared in a given function, i.e. `var int name1, ... n'
# -`k_params` is the number of variables declared in a function prototype/declaration
# -`funct_type`, used to ensure that:
#     * `constructor`s return `this` (parseReturnStatement),
#     * `this` is not used in `function`s,
#     * `functions` don't call `methods` without passing an object (i.e OBJECT.method)
#     * `methods` do a `push pointer 0` before the other arguments are pushed and before `call Class.Function k`
#     * `call Class.Function k` has the right number of arguments (i.e. accounts for the `this` in method calls)
# -`returnsType` is used to make sure `void` functions don't return a value, and that non-voids return one.
#    In theory, it could be used to introduce strong typing into Jack.
global functionsInfo
class classAndFunctionsHash():
    def __init__(self):
        self.table = {'Math^max': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'), 'Array^new': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='Array'), 'Memory^deAlloc': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'String^dispose': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'), 'String^backSpace': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'), 'Math^sqrt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'), 'Math^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Keyboard^readChar': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'), 'Array^dispose': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'), 'Math^min': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'), 'String^setCharAt': funct_info(k_params='3', n_vars='x', funct_type='method', returnsType='void'), 'Memory^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Memory^peek': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'), 'Screen^drawRectangle': funct_info(k_params='4', n_vars='x', funct_type='function', returnsType='void'), 'Output^printChar': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'Keyboard^readInt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'), 'String^length': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='int'), 'Sys^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Math^multiply': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'), 'Sys^error': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'Sys^wait': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'Output^backSpace': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Memory^poke': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'), 'Sys^halt': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'String^new': funct_info(k_params='1', n_vars='x', funct_type='constructor', returnsType='String'), 'Output^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Math^abs': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='int'), 'String^eraseLastChar': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='void'), 'Output^printInt': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'Screen^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Output^println': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'Screen^drawCircle': funct_info(k_params='3', n_vars='x', funct_type='function', returnsType='void'), 'Math^divide': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='int'), 'Screen^drawPixel': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'), 'Output^moveCursor': funct_info(k_params='2', n_vars='x', funct_type='function', returnsType='void'), 'Keyboard^keyPressed': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'), 'Screen^setColor': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'Memory^alloc': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='Array'), 'Screen^drawLine': funct_info(k_params='4', n_vars='x', funct_type='function', returnsType='void'), 'String^newLine': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'), 'String^appendChar': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='String'), 'Output^printString': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='void'), 'Keyboard^init': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'String^charAt': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='char'), 'Keyboard^readLine': funct_info(k_params='1', n_vars='x', funct_type='function', returnsType='String'), 'String^doubleQuote': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='char'), 'Screen^clearScreen': funct_info(k_params='0', n_vars='x', funct_type='function', returnsType='void'), 'String^setInt': funct_info(k_params='2', n_vars='x', funct_type='method', returnsType='void'), 'String^intValue': funct_info(k_params='1', n_vars='x', funct_type='method', returnsType='int')}


    def init_k_params(self):
        # k_params_declrd  is the number of parameters (arguments) declared in a function header/prototype
        if vars.currentFnType in ('constructor', 'function'):  #  Constructors and functions operate on k arguments
            self.k_params_declrd = 0
        else:
            self.k_params_declrd = 1                      # ... Methods, on k+1.

    def increment_k_params(self):
        if vars.parsenum == 1:
            self.k_params_declrd += 1

    def codifyField_N(self):
        '''This creates a key in our class/function lookup table which will us how many fields our Class defines/object has. It will tell us how much\
memory to allocate for our objects'''
        if vars.parsenum == 1:
            self.table[vars.currentClass+'$$N_FIELDS'] = varTable.fieldVarN

    def getField_N(self):
        '''Returns the number of field variables the requested object type (i.e. class) has, so that we allocate enough memory for them'''
        return self.table[vars.currentClass+'$$N_FIELDS']

    def addFunction(self, returnsType, token):
        if vars.parsenum == 1:
            key = vars.currentClass+'^'+vars.currentFunction
            totalLocalVars = varTable.localVarN
            params_vars_pair = funct_info(self.k_params_declrd, totalLocalVars, vars.currentFnType, returnsType)
            if key in self.table:
                raise CompilerError("Subroutine `%s' has already been declared. Line %s, %s" % (vars.currentFunction, token.line, globalVars.inputFileName))
            self.table[key] = params_vars_pair

    def lookupSubroutineInfo(self, class_, subroutinetoken):
        '''This is a utility function, and is used to evaluate semantics, tell us about our current context (based on our position in the \
parse), and give us info for code output.

`subroutinetoken', in the header, is a misnomer. Sometimes, we'll be calling this with a string, in its place.

The instance in which we do this where it /might/ not have a value is `SubroutineCall_WithDot_B\', and it also crashes our exception handler.
That's good, because we want the exception handled /there/, and the proper error message output.

Returns a 'funct_info' (named) tuple :: (k_params, n_vars, funct_type, returnsType)'''
        try:
            if type(subroutinetoken) is not str:
                function = subroutinetoken.value
                return self.table[class_+'^'+function]
            else:
                function = subroutinetoken
                if class_+'^'+function in self.table:
                    return self.table[class_+'^'+function]
                classdotfunction = function.replace('.', '^')
                return self.table[classdotfunction]
        except:
            raise CompilerError("`%s': Function does not exist. Line %s, %s" % (function, subroutinetoken.line, globalVars.inputFileName))


var_info = collections.namedtuple('var_info', ['TYPE', 'KIND', 'N'])
# /\ Tuple that forms the basis of the varTable
# Associated with a key, formatted 'vars.currentClass^vars.currentFunction^varName' or vars.currentClass+'^'+varName
#                                  (for function and class scopes, respectively)
global varTable
class variableTable():
    def __init__(self):
        self.functScope = {}
        self.classScope = {}
        self.list_of_extended_types = []

        self.localVarN = self.fieldVarN = self.staticVarN = None
        self.inDeclaration = None

    def resetFieldStaticCount(self):
        if vars.parsenum == 1:
            self.fieldVarN = self.staticVarN = 0

    def resetVarCounter(self):
        if vars.parsenum == 1:
            if vars.currentFnType == 'method':
                self.localVarN = 1
            else:
                self.localVarN = 0

    def setInDeclaration(self, boolean):
        if vars.parsenum == 1:
            self.inDeclaration = boolean

    def addVariable(self, token, _type, _kind, scope):
        '''Adds a variable to either our class-level variable table (classScope) or our function-level one (functScope). \
Included is information for `Type\' (int, char, boolean, void, and arbitrary types); `_kind` (field, static, local, argument); \
and the variable number, which is used for relative addressing'''
        if vars.parsenum == 1:

            variableName = token.value
            classkey = vars.currentClass+'^'+variableName

            # Checks whether our local variable has already been declared as class-level variables
            #  or function parameters. Issues appropriate warning, if they have, then adds the variable
            #  and typing, scope, and position (variable number) to our function scope hash table.
            if scope == 'function':
                key = vars.currentClass+'^'+vars.currentFunction+'^'+variableName
                if classkey in self.classScope:
                    kind1 = self.classScope[classkey].KIND
                    kind2 = _kind
                    line = token.line
                    if kind2 == 'var': kind2 = 'local'
                    print("WARNING: Duplicate variable names. %s\'s scope is overridden by %s\'s. Line %s, %s. Variable name: `%s\'" % (kind1, kind2, line, globalVars.inputFileName, variableName), file=sys.stderr)

                if key in self.functScope:
                    line = token.line
                    print("WARNING: Local variable declaration overrides argument -- Line %s, %s; variable name, `%s\'" % (line, globalVars.inputFileName, variableName), file=sys.stderr)
                self.functScope[key] = var_info(_type, _kind, self.localVarN)
                self.localVarN += 1

            #
            else: # == 'class'
                key = vars.currentClass+'^'+variableName
                if key in self.classScope:
                    raise CompilerError("Duplicate class-level variable name: `%s\'. Line %s, %s" % (variableName, line, globalVars.inputFileName))
                if _kind == 'field':
                    self.classScope[key] = var_info(_type, _kind, self.fieldVarN)
                    self.fieldVarN += 1
                else: # _kind == 'static':
                    self.classScope[key] = var_info(_type, _kind, self.staticVarN)
                    self.staticVarN += 1


    def lookupVariable(self, variableToken):
        kind = n = None
        if vars.parsenum == 2:
            variableName = variableToken.value
            try:
                key = vars.currentClass+'^'+vars.currentFunction+'^'+variableName
                if key in self.functScope:
                    base = self.functScope[key]
                else:
                    key = vars.currentClass+'^'+variableName
                    base = self.classScope[key]

                kind = base.KIND
                if kind == 'field': kind = 'this'
                elif kind == 'var': kind = 'local'

                n = base.N
                type_ = base.TYPE

            except:
                # raise ValueError("Variable `%s' not found. Line %s, %s" % (variableName, variableToken.line, globalVars.inputFileName))
                raise CompilerError("Variable `%s' not found. Line %s, %s" % (variableName, variableToken.line, globalVars.inputFileName))
        return type_, kind,  n

    def addToAvailableTypes(self):
        '''We're keeping a list of the types (i.e. defined classes) available in our compiled files, so that type declarations are meaningful'''
        if vars.parsenum == 1:
            try:
                if vars.currentClass not in self.list_of_extended_types:
                    self.list_of_extended_types.append(vars.currentClass)
            except:
                pass

    def checkTypeExistence(self, token, subroutineDeclaration=False):
        '''This checks whether a declared type actually exists in the files we're compiling OR the Jack Standard Library'''
        if vars.parsenum == 2:
            type_ = token.value
            if type_ == 'void':
                if not subroutineDeclaration:
                    raise CompilerError('`void\' only makes sense as a subroutine return value. Line %s, %s' % (token.line, globalVars.inputFileName))
            elif type_ not in ('int', 'char', 'boolean', 'Array', 'String'):
                if type_ not in self.list_of_extended_types:
                    raise CompilerError('Unknown type `%s\', line %s, %s' % (token.value, token.line, globalVars.inputFileName))

    def checkClassExistence(self, token):
        '''This checks whether a called class name exists, so that Class.subroutine() actually calls code that exists'''
        if vars.parsenum == 2:
            Class = token.value
            if Class not in ('Array', 'Keyboard', 'Math', 'Memory', 'Output', 'Screen', 'String', 'Sys'):
                if Class not in self.list_of_extended_types:
                    raise CompilerError('Class `%s\' doesn\'t seem to exist. Line %s, %s' % (token.value, token.line, globalVars.inputFileName))


def initialize():
    global functionsInfo, varTable
    functionsInfo = classAndFunctionsHash()
    varTable = variableTable()
    return varTable, functionsInfo
