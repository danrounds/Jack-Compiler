
class VM():
    arithlogicoperations = ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not')
    memoryoperations     = ('push', 'pop')
    programflowcommands  = ('label', 'goto', 'if-goto')
    functioncallcommands = ('function', 'call', 'return')

    nopointnostaticDict  = {'argument':'ARG', 'local':'LCL', 'this':'THIS', 'that':'THAT'}
    pointerandtempDict   = {'pointer':  {'0':'THIS',  '1':'THAT'}, \
                            'temp':     {'0':'R5',    '1':'R6',   '2':'R7',   '3':'R8',
                                         '4':'R9',    '5':'R10',  '6':'R11',  '7':'R12'}}


def initialize(_file):
    # \/ This is the variable we use for all output. Instance of `Output`
    global file_
    file_ = _file


def processVmInstruction(line, moduleprefix, linenum, globallyuniqueNUM):
    try:
        OP = line[0]
        if OP in VM.arithlogicoperations:
            processArithmeticLogic(line, linenum, globallyuniqueNUM)

        elif OP in VM.memoryoperations and len(line) == 3:
            if not processPushPop(line, moduleprefix):
                raise

        elif OP in VM.programflowcommands:
            processProgramFlow(line, moduleprefix)

        elif OP in VM.functioncallcommands:
            processFunctionCmds(line, globallyuniqueNUM)

        elif OP == '': pass

        else:
            raise
    except:
            raise RuntimeError('Line %s. Something went wrong. '
                               'Conversion halted.' % linenum)


def writeBootstrap():
    """
    Writes the bootstrap code that:
    - initializes SP, LCL, and ARG to the right values
    - calls Sys.init (part of Jack Standard Library):
        ++Pushes Sys.init's return address onto the stack, i.e.,
            `@RTN_ADR_Sys.init`
        ++Pushes 0s onto the stack where a normal function call would push
            LCL, ARG, THIS, and THAT
        ++Writes the goto Sys.init statement
        ++Writes the return address token, i.e. `(RTN_ADR_Sys.init)`
    """

    file_.out('@256\nD=A\n@SP\nM=D\n@LCL\nM=D\n')         # SP=256; LCL = SP

    # \/ call Sys.init--{Memory,Math,Output,Keyboard,Screen,String,Main}.init
    #                     + Sys.halt--in that order)
    file_.out('@RTN_ADR_Sys.init\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n') # push Sys.init's return address
    for i in range(4):
        # Pushes zeros on the stack (just in case system start-up doesn't
        # default to zeros
        file_.out('@SP\nA=M\nM=0\n@SP\nM=M+1\n')
    file_.out('@256\nD=A\n@ARG\nM=D\n')           # ARG = SP-n-5
    file_.out('@Sys.init\n0;JMP\n')               # `goto Sys.init'
    file_.out('(RTN_ADR_Sys.init)\n')             # (return-address)


def processArithmeticLogic(line, linenum, gID):
    """
    Receives `line' (list of VM tokens); line[0] is ostensibly a VM operator.
    Writes the relevant assembly to the output file
    """
    # This function is /definitely/ a candidate for replacement with a
    # dictionary that returns the relevant string for each operator. E.g.,
    # {'add':'@SP\nAM=M1...', ..., 'eq':'SP...@EQTRUE%s\n', etc}
    # UPDATE: tried this, and it offered no performance update and somewhat
    # obfuscated the code
    if len(line) != 1:
        print('Line %s. Warning: Arithmetic and Logical operations on the '
              'stack don\'t take arguments. Make sure you know what your code '
              'does\n' & linenum, file=sys.stderr)
    line = line[0]
    if line == 'add':
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M+D\n@SP\nM=M+1\n')
    elif line == 'sub':
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M-D\n@SP\nM=M+1\n')
    elif line == 'neg':
        file_.out('@SP\nAM=M-1\nM=!M\nM=M+1\n@SP\nM=M+1\n')
    elif line == 'eq':
        gID = str(gID)
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@EQTRUE'+gID+'\nD;')
        file_.out('JEQ\nD=0\n@ENDEQ'+gID+'\n0;JMP\n(EQTRUE'+gID+')\nD=-1\n')
        file_.out('(ENDEQ'+gID+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
    elif line == 'gt':
        gID = str(gID)
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@GTTRUE'+gID+'\nD;')
        file_.out('JGT\nD=0\n@ENDGT'+gID+'\n0;JMP\n(GTTRUE'+gID+')\nD=-1\n')
        file_.out('(ENDGT'+gID+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
    elif line == 'lt':
        gID = str(gID)
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@LTTRUE'+gID+'\nD;')
        file_.out('JLT\nD=0\n@ENDLT'+gID+'\n0;JMP\n(LTTRUE'+gID+')\nD=-1\n')
        file_.out('(ENDLT'+gID+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
    elif line == 'and':
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M&D\n@SP\nM=M+1\n')
    elif line == 'or':
        file_.out('@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M|D\n@SP\nM=M+1\n')
    else:  # 'not'
        file_.out('@SP\nAM=M-1\nM=!M\n@SP\nM=M+1\n')


def processPushPop(line, module):
    """
    Receives a line (as a list) with a push/pop operation in it; writes the
    relevant assembly to the output file
    """
    operator, location, offset = line[0], line[1], line[2]
    if operator == 'push':
        if location in ['argument', 'local', 'this', 'that']:
            area = VM.nopointnostaticDict[location]
            if offset == '0':
                file_.out('@'+area+'\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            else:
                file_.out('@'+offset+'\nD=A\n@'+area+'\nA=M+D\nD=M\n@SP\n')
                file_.out('A=M\nM=D\n@SP\nM=M+1\n')
        elif location == 'constant':
            file_.out('@'+offset+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        else:
            if location == 'static':
                area = module + '.' + offset
            elif location in ['pointer', 'temp']:
                try:
                    area = VM.pointerandtempDict[location][offset]
                except:
                    return False
            else:
                return False
            file_.out('@'+area+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')

    elif operator == 'pop':
        if location in ['argument', 'local', 'this', 'that']:
            # No memory-bounding checks
            area = VM.nopointnostaticDict[location]
            if offset == '0':
                file_.out('@SP\nAM=M-1\nD=M\n@'+area+'\nA=M\nM=D\n')
            else:
                file_.out('@'+offset+'\nD=A\n@'+area+'\nD=M+D\n@R13\nM=D\n')
                file_.out('@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n')
        else:
            if location == 'static':
                area = module + '.' + offset
            elif location in ['pointer', 'temp']:
                try:  # <<< out of memory range will trigger exception
                    area = VM.pointerandtempDict[location][offset]
                except:
                    return False
            else:
                return False
            file_.out('@SP\nAM=M-1\nD=M\n@'+area+'\nM=D\n')
    return True


def processProgramFlow(line, module):
    """Processes a VM `line' prefixed by `goto', `label', and `if-goto'"""
    if len(line) != 2:
        print('%s commands accept one argument, or your label name contains a '
              'space.' % line[0], file=sys.stderr)
    else:
        #  Implementation of the command `label /label/` -> functionName$label
        #  assumes compiler has generated unique (/correct) names for labels.
        command, label = line[0], line[1]
        if command == 'label':
            file_.out('('+module+'$'+label+')\n')
        elif command == 'goto':
            file_.out('@'+module+'$'+label+'\n0;JMP\n')
        else:  # 'if-goto'
            file_.out('@SP\nAM=M-1\nD=M\n@'+module+'$'+label+'\nD;JNE\n')


def processFunctionCmds(line, gID):
    """
    Accepts `line' (list of VM tokens), parses it, writes assembly for one of
    the following:
    (1) 'call' -- defines return address, saves function state on the
        stack, writes return token (i.e. a goto destination)
    (2) 'function' definition -- goto token and variable initialization
    (3) 'return' -- pops return value onto the stack, restores state of
        calling function.
    ####### See pg. 163 of tElements of Computing Systems for details#########
    """
    if len(line) == 3:
        operation, function, n_lcl_vars = line[0], line[1], line[2]
    else:
        operation = line[0]
        if len(line) != 1:
            raise SyntaxError('Seems your invocation of `%s` wasn\'t '
                              'syntactically correct' % (operation), file=sys.stderr)

    if operation == 'call':
    # The assembly here:
    # (1) Saves the state of the calling function, by pushing @return_address, LCL, ARG, THIS, and
    #      THAT onto the stack
    # (2) Changes the value of ARG so that it points below all the state-save values pushed above
    #      (ARG = SP-n-5), n=number of funct arguments
    # (3) Points LCL to the top of the stack, where the called function will put its local variables
    # (4) Writes a jump to the function
    # (5) Defines a return address by pushing an assembly label [i.e. "(returnadr)"] at end of assembly output

    # Afterwards, stack looks as follows:
    #    +-------------------------------+
    #    |      argument 0               |  <= ARG; function(arg1, arg2, argN-1);
    #    |      argument 1               |      Calling function has pushed arguments onto the stack.
    #    |        ...                    |      They reside here, right before saved context info (\/)
    #    |      argument n-1             |      These `push's happened just before `call f n' was issued
    #    +-------------------------------+
    #    |     return_address            |  <= NONE of the registers point here. This is simply the place 
    #    |       saved LCL               |      the prior context gets saved. VM code (& by extension Jack
    #    |       saved ARG               |      code compiled to VM) will NOT interact with this, EXCEPT
    #    |       saved THIS              |      for `return', which puts these values into their proper 
    #    |       saved THAT              |      registers and JMPs to `return_address'
    #    +-------------------------------+
    #    |       local 0                 |  <= LCL; these are the local variables of the function we've
    #    |       local 1                 |      now entered or about to enter (depending on perspective).
    #    |        ...                    |      The function in question will begin by pushing the 
    #    |       local k-1               |      initial values into these variables.
    #    +-------------------------------+
    #    |                               |  <= SP; initial place the SP points, after entering a function
    #    +-------------------------------+      (and after variables are initialized)

        #### \/ precall push \/ ##########################################
        returnadr = "RTN_ADR_"+function+str(gID)                         # << Pushes return address
        file_.out("@"+returnadr+"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")   #    onto the stack
        for label in ['LCL','ARG','THIS','THAT']:
            # Pushes values contained in LCL (RAM[1]), ARG (RAM[2]), THIS (RAM[3], THAT (RAM[4]) onto
            #  the stack, where a `return` can later unpack them.
            file_.out('@'+label+'\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        #### /\ precall push /\ #########################################

        # ARG=SP-n-5, i.e. points ARG to the 0th argument. Function arguments are pushed before a `call`
        #  is initiated \/
        nplus5 = str(int(n_lcl_vars) + 5)
        file_.out('@SP\nD=M\n@'+nplus5+'\nD=D-A\n@ARG\nM=D\n')

        file_.out('@SP\nD=M\n@LCL\nM=D\n')         # LCL = SP;
        file_.out('@'+function+'\n0;JMP\n')        # Goto `function'
        file_.out('('+returnadr+')\n')	            # Writes return address

    elif operation == 'function':
    # (1) writes a label for the function destination, i.e. "(function_name)"
    # (2) initializes variables by pushing 'n' varibles onto the stack, where
    #      n = number of local variables'''
        file_.out('('+function+')\n')                     # (function_name)
        for i in range(int(n_lcl_vars)):
            file_.out('@SP\nA=M\nM=0\n@SP\nM=M+1\n')      # pushes n zeros

    else:
    # == 'return'
    # (1) puts the return address into R14 (temp register)
    # (2) pops the return value of the function to the memory location pointed
    #     to by ARG, i.e. SP-n-5, i.e. the value that SP had before pushing
    #     its n function arguments.
    # (3) puts the stack pointer right above the returned value (i.e. ARG+1)
    # (4) puts the state-save values that the calling function put on the stack
    #     back into THAT, THIS, ARG, and LCL
    # (5) JMPs to the return address (defined by the writing of the function
    #     call)'''
        file_.out('@LCL\nD=M\n@R13\nM=D\n')                 # FRAME = LCL
        file_.out('@R13\nD=M\n@5\nA=D-A\nD=M\n@R14\nM=D\n') # RET = *(FRAME-5)
        file_.out('@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n')     # *ARG = pop()
        file_.out('@ARG\nD=M+1\n@SP\nM=D\n')                # SP = ARG+1
        for l in ['THAT', 'THIS', 'ARG', 'LCL']:            # /THAT, THIS, ARG,
            file_.out('@R13\nAM=M-1\nD=M\n@'+l+'\nM=D\n')   # \LCL=*(FRAME-[n+1])
        file_.out('@R14\nA=M\n0;JMP\n')                     # @return-address;JMP
