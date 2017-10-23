# Interpreter section (unessential code):

from processVmInstructions import VM, processArithmeticLogic, processPushPop,\
    processProgramFlow, processFunctionCmds, writeBootstrap

def VMinterpreter():
    """
    An `interpreter' for tECS VM commands. Doesn't execute VM commands, but
    outputs their Hack translation. Gives some insight into the translation,
    itself. Some syntactically-invalid commands will print, because I don't
    want to pollute the logic of the translator.
    """
    while True:
        try:
            thing = input('Type a VM command, `bootstrap`, OR type `h` for help or `q` to quit: ')
            print()
            printVMcmd(thing)
        except EOFError:
            print('BYE')
            break
        except Exception as e:
            print(e)
            print('\nSomething went wrong. Conversion halted.')
            break


def printVMcmd(command):
    """
    ======================================================================================
    Commands:
    arithmetic/logical ops:      add, sub, neg, eq, gt, lt, and, or, not

    stack operations:            push LOCATION n, pop LOCATION m,  e.g.,
                                        `push local 0', `pop local 3',
                                        `push argument 0',`pop argument 0',
                                        `push temp 0', `pop temp 1'

    program flow commands:       label VARIABLE, goto VARIABLE, if-goto VARIABLE
    structured programming:      function NAME n, call NAME k, return
    ======================================================================================
    Labeled Memory Locations:       argument, local, this, pointer 0 (`this'),
                                    pointer 1 (`that'), temp 0/1/2/3/4/5/6/7
    ======================================================================================
    """

    import Output
    import processVmInstructions
    global file_
    file_ = Output.Output(None)
    processVmInstructions.initialize(file_)

    globallyuniqueNUM = linenum = 0
    moduleprefix = 'interpreter'
    command = command.split()

    if command == []:
        OP = ''
    else:
        OP = command[0]

    if OP in VM.arithlogicoperations:
        processArithmeticLogic(command, linenum, globallyuniqueNUM)
    elif OP in VM.memoryoperations and len(command) == 3:
        processPushPop(command, moduleprefix)
    elif OP in VM.programflowcommands:
        processProgramFlow(command, moduleprefix)
    elif OP in VM.functioncallcommands:
        if len(command) == 1 and command[0] != 'return':
            command.append('function')
            command.append('0')
        processFunctionCmds(command, globallyuniqueNUM)
    elif OP == 'bootstrap':
        writeBootstrap()
    elif OP == 'h':
        print(VMinterpreter.__doc__ + '\n' + printVMcmd.__doc__)
    elif OP == 'q':
        raise EOFError          # sloppy exit
    else:
        print('Malformed command, I guess. Try again!')

    print('\n'+str(file_.N_INSTRUCTIONS)+' instructions')
