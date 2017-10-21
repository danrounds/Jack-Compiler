import collections
import sys

from compiler_error import CompilerError
import globalVars
# import JackStdLib


def initialize_globals(linking, parsenum):
    global functionsInfo, varTable, output, STRONGLINKING
    global uniqueIfIdentifier, uniqueWhileIdentifier
    functionsInfo = classAndFunctionsHash()
    varTable = variableTable()

    STRONGLINKING = linking # this is vestigial and represents an attempt to allow for
    # compiling .jack files separately with later "linking""

    uniqueIfIdentifier = uniqueWhileIdentifier  = -1
    defineParseNumber(parsenum)
    output = Output()

global currentClass, currentFunction
# These are state variables. They reflect the file, class, and function we're currently in the middle
def setCurrentClass(classtoken):
    global currentClass
    currentClass = classtoken.value
def setCurrentFunction(functiontoken):
    global currentFunction
    currentFunction = functiontoken.value



global parsenum
def defineParseNumber(n):
    '''This defines a global variable which the compiler uses to generate our hash tables (parse # 1)\
OR to output code (parse # 2) OR to output XML tokens or parse tree (parse # 0)'''
    global parsenum
    parsenum = n



global uniqueIfIdentifier, uniqueWhileIdentifier # Integers
class IfWhileIdentifiers():
    '''Used to provide unique IDs for ifs/whiles in code output'''
    def updateIfID():
        global uniqueIfIdentifier
        uniqueIfIdentifier += 1
        return str(uniqueIfIdentifier)
    def updateWhileID():
        global uniqueWhileIdentifier
        uniqueWhileIdentifier += 1
        return str(uniqueWhileIdentifier)



class Output():
    '''Outputs XML or code, depending on the parse number'''
    def __init__(self):
        if parsenum == 0:
            self.code = Output.null
        elif parsenum == 1:
            self.outt = self.startt = self.endt = Output.null
            self.code = Output.null

    def defineOutputValues(self, output_file_name):
        global uniqueIfIdentifier, uniqueWhileIdentifier
        if parsenum == 1:
            return
        else:
            self.global_file_out = open(output_file_name, 'w')

        if parsenum == 2:
            self.code = self.codeoutput
            uniqueIfIdentifier = uniqueWhileIdentifier = -1

    def closeFile(self):
        if parsenum == 1:
            pass
        else:
            self.global_file_out.close()


    # XML output
    def outt(self, token):
        if parsenum == 0:
            val, tag = token.value, token.typ
            if   val == '<': val = '&lt;'
            elif val == '>': val = '&gt;'
            elif val == '&': val = '&amp;'
            self.global_file_out.write("<%s> %s </%s>\n" % (tag, val, tag))
    def startt(self, tag):
        if parsenum == 0:
            self.global_file_out.write("<%s>\n" % tag)
    def endt(self, tag):
        if parsenum == 0:
            self.global_file_out.write("</%s>\n" % tag)

    # Code output
    def codeoutput(self, line_of_code):
        self.global_file_out.write(line_of_code + '\n')

    ###
    def null(*args, **kwargs):
        pass


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
        if self.functTyp in ('constructor', 'function'):  #  Constructors and functions operate on k arguments
            self.k_params_declrd = 0
        else:
            self.k_params_declrd = 1                      # ... Methods, on k+1.

    def increment_k_params(self):
        if parsenum == 1:
            self.k_params_declrd += 1

    def defFunctTyp(self, token):
        self.functTyp = token.value
        return self.functTyp

    def codifyField_N(self):
        '''This creates a key in our class/function lookup table which will us how many fields our Class defines/object has. It will tell us how much\
memory to allocate for our objects'''
        if parsenum == 1:
            self.table[currentClass+'$$N_FIELDS'] = varTable.fieldVarN

    def getField_N(self):
        '''Returns the number of field variables the requested object type (i.e. class) has, so that we allocate enough memory for them'''
        return self.table[currentClass+'$$N_FIELDS']

    def addFunction(self, returnsType, token):
        if parsenum == 1:
            key = currentClass+'^'+currentFunction
            totalLocalVars = varTable.localVarN
            params_vars_pair = funct_info(self.k_params_declrd, totalLocalVars, self.functTyp, returnsType)
            if key in self.table:
                raise CompilerError("Subroutine `%s' has already been declared. Line %s, %s" % (currentFunction, token.line, globalVars.inputFileName))
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
# Associated with a key, formatted 'currentClass^currentFunction^varName' or currentClass+'^'+varName
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
        if parsenum == 1:
            self.fieldVarN = self.staticVarN = 0

    def resetVarCounter(self):
        if parsenum == 1:
            if functionsInfo.functTyp == 'method':
                self.localVarN = 1
            else:
                self.localVarN = 0

    def setInDeclaration(self, boolean):
        if parsenum == 1:
            self.inDeclaration = boolean

    def addVariable(self, token, _type, _kind, scope):
        '''Adds a variable to either our class-level variable table (classScope) or our function-level one (functScope). \
Included is information for `Type\' (int, char, boolean, void, and arbitrary types); `_kind` (field, static, local, argument); \
and the variable number, which is used for relative addressing'''
        if parsenum == 1:

            variableName = token.value
            classkey = currentClass+'^'+variableName

            # Checks whether our local variable has already been declared as class-level variables
            #  or function parameters. Issues appropriate warning, if they have, then adds the variable
            #  and typing, scope, and position (variable number) to our function scope hash table.
            if scope == 'function':
                key = currentClass+'^'+currentFunction+'^'+variableName
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
                key = currentClass+'^'+variableName
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
        if parsenum == 2:
            variableName = variableToken.value
            try:
                key = currentClass+'^'+currentFunction+'^'+variableName
                if key in self.functScope:
                    base = self.functScope[key]
                else:
                    key = currentClass+'^'+variableName
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
        if parsenum == 1:
            try:
                if currentClass not in self.list_of_extended_types:
                    self.list_of_extended_types.append(currentClass)
            except:
                pass

    def checkTypeExistence(self, token, subroutineDeclaration=False):
        '''This checks whether a declared type actually exists in the files we're compiling OR the Jack Standard Library'''
        if parsenum == 2:
            type_ = token.value
            if type_ == 'void':
                if not subroutineDeclaration:
                    raise CompilerError('`void\' only makes sense as a subroutine return value. Line %s, %s' % (token.line, globalVars.inputFileName))
            elif type_ not in ('int', 'char', 'boolean', 'Array', 'String'):
                if type_ not in self.list_of_extended_types:
                    raise CompilerError('Unknown type `%s\', line %s, %s' % (token.value, token.line, globalVars.inputFileName))

    def checkClassExistence(self, token):
        '''This checks whether a called class name exists, so that Class.subroutine() actually calls code that exists'''
        if parsenum == 2:
            Class = token.value
            if Class not in ('Array', 'Keyboard', 'Math', 'Memory', 'Output', 'Screen', 'String', 'Sys'):
                if Class not in self.list_of_extended_types:
                    raise CompilerError('Class `%s\' doesn\'t seem to exist. Line %s, %s' % (token.value, token.line, globalVars.inputFileName))




global n_curlies, max_curlies   # << for insane if/else "stack", to determine 
global functionRtnsStack, codeHasTerminated  # whether a function might return
class DoesFunctionReturnStack():
    '''This uses a heuristic that I dreamt up on my own (at the height of compiler-writing insanity, no less), to \
determine whether functions seem likely to return, OR whether we end up with sections of dead code. I'm sure I could \
reconstruct the heuristic I had in mind, but the code is unobtrusive, more or less does what it should (very few false \
positives), and won't halt compilation.

If anything, it yields /potentially/ useful warnings.

I also find it kind of charming. It could be removed without penalty (but it won't be).'''

    unreachableTriggered = False
    def stackvars_init():
        if parsenum == 2:
            global n_curlies, max_curlies
            n_curlies = max_curlies = 0
    def stackvars_incr():
        if parsenum == 2:
            global n_curlies, max_curlies
            n_curlies += 1
            if n_curlies > max_curlies:
                max_curlies = n_curlies
    def stackvars_decr():
        if parsenum == 2:
            global n_curlies
            n_curlies -= 1
    
    def stack_init():
        if parsenum == 2:
            global functionRtnsStack
            functionRtnsStack = ""
    def stack_addIfStmnt():
        if parsenum == 2:
            global functionRtnsStack
            functionRtnsStack = functionRtnsStack + 'if'+str(n_curlies)
    def stack_addElseStmnt():
        if parsenum == 2:
            global functionRtnsStack
            functionRtnsStack = functionRtnsStack + 'else'+str(n_curlies)
    def stack_addReturnStmnt():
        if parsenum == 2:
            global functionRtnsStack
            functionRtnsStack = functionRtnsStack + 'return'+str(n_curlies)
            
    ############### These three functions are used as each statement is parsed,
    ############### to see whether there seems to be unreachable code
    def warning_test_init():
        global codeHasTerminated
        codeHasTerminated = False
    def warning_reduc():
        if parsenum == 2:
#            functionRtnsStack = reduction(functionRtnsStack, n_curlies)
            DoesFunctionReturnStack.reduction()
            if functionRtnsStack[-7:] == 'return2':
                global codeHasTerminated
                codeHasTerminated = True
    def IFissue_warning(token):
        ## \/ added the parsenum == 2 as a hail Mary
        if parsenum == 2:
            if codeHasTerminated == True and not DoesFunctionReturnStack.unreachableTriggered:
                print("Warning: Unreachable code. Line %s, %s" % (token.line, globalVars.inputFileName), file=sys.stderr)
                DoesFunctionReturnStack.unreachableTriggered = True
    ###############
    
    def codecheck(token):
        if parsenum == 2:
            if functionRtnsStack[-7:] not in ('return2', ''):
                old = None
                while old != functionRtnsStack:
                    old = functionRtnsStack
                    DoesFunctionReturnStack.reduction()
            if 'return2' not in functionRtnsStack:
                print("Warning: Function might not return. Make sure your if/elses are are mutually exclusive.  Line %s, %s" % (token.line, globalVars.inputFileName), file=sys.stderr)
    def reduction():
        global functionRtnsStack
        for i in range(1, max_curlies):
            string = 'if'+str(i)+'return'+str(i+1)
            if string+string in functionRtnsStack:
                functionRtnsStack = functionRtnsStack.replace(string+string, string)

        for i in range(1, max_curlies):
            string = 'if'+str(i)+'return'+str(i+1)+'else'+str(i)+'return'+str(i+1)
            if string in functionRtnsStack:
                functionRtnsStack = functionRtnsStack.replace(string, 'return'+str(i))

        for i in range(1, max_curlies):
            string = 'if'+str(i)+'return'+str(i)
            if string in functionRtnsStack:
                functionRtnsStack = functionRtnsStack.replace(string, 'return'+str(i))

    def reduction2(test, max):
        for i in range(1, max):
            string = 'if'+str(i)+'return'+str(i+1)
            if string+string in test:
                test = test.replace(string+string, string)
        for i in range(1, max):
            string = 'if'+str(i)+'return'+str(i+1)+'else'+str(i)+'return'+str(i+1)
            if string in test:
                test = test.replace(string, 'return'+str(i))
        for i in range(1, max):
            string = 'if'+str(i)+'return'+str(i)
            if string in test:
                test = test.replace(string, 'return'+str(i))
        return(test)






class Semantics():
    def checkReturn(token):
        '''Provides some limited error checking for return statements. Doesn't do much type checking--simply makes sure that constructors, void functions, and value-returning functions all do what they should.

Jack's very, very lax typing is kept intact. Type checking could be added, but would require more effort when expressions are involved. Since the only platform we're compiling to treats everything as a 16-bit word, there's at least no impedance mismatch'''
        if parsenum == 2:
            value = token.value

            *NULL, funct_role, returnsType  = functionsInfo.lookupSubroutineInfo(currentClass, currentFunction)

            if funct_role == 'constructor':
                if value != 'this':
                    error_middle = ' -- NOT `%s\'' % value 
                    if value == ';':
                        error_middle = ''
                    raise CompilerError('`%s\' is a constructor and should return `this\'%s. Line %s, %s' % (currentFunction, error_middle, token.line, globalVars.inputFileName))

            elif returnsType == 'void':
                if value != ';':
                    raise CompilerError('`%s\' is a void function, and so mustn\'t return a value. It does. Line %s, %s' % (currentFunction, token.line, globalVars.inputFileName))

            else:
                if value == ';':
                    raise CompilerError('`%s\' isn\'t a void function, and so it must return a value. Line %s, %s' % (currentFunction, token.line, globalVars.inputFileName))


    def checkDotlessFunctionCall(subroutinetoken, callerexpectsreturnval):
        '''This checks whether dotless function calls (i.e. ones of the form `do function()\' or `let thing = function()\' return value when they should (and don't when they should not) AND makes sure we don't issue meaningless method calls.'''

        *NULL, calledfunct, calledreturns = functionsInfo.\
                                            lookupSubroutineInfo(currentClass, subroutinetoken)
        *NULL, callingfunct, NULL = functionsInfo.lookupSubroutineInfo(currentClass, currentFunction)
       
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




class CodeProcess():
    '''This is where all the code output logic is stored. Each section is called directly from its \
relevant parse stage.'''

    def SubroutineDeclaration(token):
        if parsenum == 2:
            currentFunctionContext = functionsInfo.table[currentClass+'^'+currentFunction]
            shouldReturnType = currentFunctionContext.returnsType
            num = currentFunctionContext.n_vars

            # The function declaration, itself:
            output.code('function %s.%s %s' % (currentClass, currentFunction, num))

            # If we're dealing with a constructor, we've got to allocate memory and 
            if functionsInfo.functTyp == 'constructor':
                if currentClass == shouldReturnType:
                    memtoalloc = functionsInfo.getField_N()
                    output.code('push constant '+str(memtoalloc))
                    output.code('call Memory.alloc 1')  # Leaves the address of our allocated object @ the top of the stack
                    output.code('pop pointer 0')        # Puts &NEW_OBJECT in pointer 0 (`@THIS', in Hack Assembly)
                else:
                    raise CompilerError("A constructor's return type must be the class type, Line %s, %s" % (token.line, globalVars.inputFileName))

            # If we're dealing with a method, we have to pop pointer to the object upon which our method operates
            elif functionsInfo.functTyp == 'method':
                output.code('push argument 0')   # argument 0 is the object called by the method. This pops it into pointer 0, so that
                output.code('pop pointer 0')     # `this n` VM commands work.


    def LetStatement_ARRAY_BASE(variableToken):
        if parsenum == 2:
            NULL, kind, n = varTable.lookupVariable(variableToken)
            output.code('push %s %s' % (kind, n))
            output.code('add')  # adds variable *(kind n) to the prior stack value (an expression)

    def LetStatement(array, variableToken):
        # I THINK This is where you could optimize code for array indexing knowable at compile time
        if parsenum == 2:
            NULL, kind, n = varTable.lookupVariable(variableToken)
            if array == True:
                output.code('pop temp 0')
                output.code('pop pointer 1')
                output.code('push temp 0')
                output.code('pop that 0')
            else:
                output.code('pop %s %s' % (kind, n))


    def IfStatement_IF(n):
        output.code('if-goto IF_TRUE'+n) # pops the result of conditional in
        output.code('goto IF_FALSE'+n)   # the If statement. If True, jumps
        output.code('label IF_TRUE'+n)   # to IF_TRUE+n.
    ## \/ These two functions run (output) if the parser finds an `else`##
    def IfStatement_ELSE_A(n):                                             #
        output.code('goto IF_END'+n)                                #
        output.code('label IF_FALSE'+n)                             #
    def IfStatement_ELSE_B(n):                                              #
        output.code('label IF_END'+n)                               #
    ## /\ These two functions run (output) if the parser finds an `else`##

    ## \/ This gets output only if we don't have an `else`
    def IfStatement_NOELSE(n):
        output.code('label IF_FALSE'+n)


    def WhileStatement_1(n):
        output.code('label WHILE_EXP'+n)
    def WhileStatement_2(n):
        output.code('not') # The expression is NOT-ed, and if it then equals
        output.code('if-goto WHILE_END'+n) # zero, the jump is made to END
    def WhileStatement_3(n):
        output.code('goto WHILE_EXP'+n)
        output.code('label WHILE_END'+n)

    def DoStatementNULLPOP():
        # This can be removed, so long as you remove the corresponding code in `ReturnStatementVoid'
        # It could also be left in if the idiom of calling function-returning values but ignoring the
        #  function were considered useful.
        output.code('pop temp 0')


    def ReturnStatementVoidPrep(token):
        if parsenum == 2:
            key = currentClass+'^'+currentFunction
            if functionsInfo.table[key].returnsType == 'void':
                output.code('push constant 0')
            # /\ If you deleted the code that automatically pops the result of a `do`, then this code would be
            #  unnecessary, since the compiler /could/ restrict `do` calls for non-void functions.
    def ReturnStatementOutput():
        output.code("return")


    # ops = {"+":'add', "-":'sub', "&":'and', "|":'or', "<":'lt', ">":'gt', "=":'eq', "*":"call Math.multiply 2",
    #        "/":"call Math.divide 2",}
    def ExpressionOP(op):
        ## Tried this as a "jump" into the dictionary above, instead of loads of sequential logic,
        #   but it offered no performance improvements
        if parsenum == 2:
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
        if parsenum == 2:
            string = token.value
            output.code("push constant %s" % len(string))
            output.code("call String.new 1")
            for c in string:
                output.code("push constant %s" % ord(c))
                output.code("call String.appendChar 2")

    def TermKEYWORD(token):
        if parsenum == 2:
            keyword = token.value
            if keyword == 'true':
                output.code("push constant 1")
                output.code('neg')
            elif keyword == 'false':
                output.code("push constant 0")
            elif keyword == 'null':
                output.code("push constant 0")
            elif keyword == 'this':
                currentContext = functionsInfo.table[currentClass+'^'+currentFunction]
                if currentContext.funct_type != 'function':
                    output.code("push pointer 0")
                else:
                    raise CompilerError('`this\' cannot be used in a function. Line %s, %s' % (token.line, globalVars.inputFileName))

    # def TermARRAY(variableName):
    def TermARRAY(variableToken):
        if parsenum == 2:
            NULL, kind,  n = varTable.lookupVariable(variableToken)
            output.code('push %s %s' % (kind, n))
            output.code('add')
            output.code('pop pointer 1')
            output.code('push that 0')

    def TermUNARYOP(op):
        if parsenum == 2:
            if op.value == '~':
                output.code('not')
            else:
                output.code('neg')

    def TermVARNAME(variableToken):
        if parsenum == 2:
            NULL, kind, n = varTable.lookupVariable(variableToken)
            output.code('push %s %s' % (kind, n))


    def SubroutineCall_NoDot_A(subroutinetoken, callerexpectsreturnval):
        '''Parses a subroutine call without an argument or preceding class name, i.e. `subroutineName(arguments)`
            i.e. a `function' call (if it's not, in fact, a syntax error)'''
        if parsenum == 2:
            calledfunrole = Semantics.checkDotlessFunctionCall(subroutinetoken, callerexpectsreturnval)

            if calledfunrole == 'method':
                output.code('push pointer 0')

    def SubroutineCall_NoDot_B(subroutinetoken, numberofparams):
        '''Second part of our logic/error-checking for method-less/Class-less subroutine calls\ni.e., in the language of Jack, "function" call'''
        if parsenum == 2:

            k, NULL, proceduretype, NULL = functionsInfo.lookupSubroutineInfo(currentClass, subroutinetoken)
            if proceduretype == 'method': numberofparams += 1

            if numberofparams != k:
                raise CompilerError('Function `%s\' takes %s arguments. Number given: %s. Line %s, %s' % (subroutinetoken.value, k, numberofparams, subroutinetoken.line, globalVars.inputFileName))
            else:
                output.code('call %s.%s %s' % (currentClass, subroutinetoken.value, numberofparams))


    def SubroutineCall_WithDot_A(subroutinetoken, classORobject):
        '''`object.method()` or `class.subroutine()`'''

        methodcall = function = None
        if parsenum == 2:

            ## \/ this checks to see whether what we have is `var.method()`, as opposed to a `class.function()` call
            try:
                Class, kind, n = varTable.lookupVariable(classORobject)
                methodcall = True
                output.code('push %s %s' % (kind, n))
            except:
                varTable.checkClassExistence(classORobject)
                Class = classORobject.value
                methodcall = False

            function = '%s.%s' % (Class, subroutinetoken.value)

        return methodcall, function

    def SubroutineCall_WithDot_B(subroutinetoken, function, n_exprs_in_call):
        '''2nd part of output logic for `object.method()\' or `class.subroutine()\`'''

        if parsenum == 2:
            try:
                expectedparams, *NULL = functionsInfo.lookupSubroutineInfo('', function)
                if int(n_exprs_in_call) != int(expectedparams):
                    raise CompilerError('Function `%s\' takes %s argument(s). Number given: %s. Line %s, %s' % (function, expectedparams, n_exprs_in_call, subroutinetoken.line, globalVars.inputFileName))

            except AttributeError:
                raise CompilerError("Call to `%s\': Class/object does not exist or subroutine doesn't (or both). Line %s, %s" % (function, subroutinetoken.line, globalVars.inputFileName))
                # if STRONGLINKING == True:
                #     ...

            output.code('call %s %s' % (function, n_exprs_in_call))


