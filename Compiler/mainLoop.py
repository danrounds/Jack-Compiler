"""
Jack to `intermediate VM representation' portion of a full-compiler (to Hack
machine code).

Turns spec-compliant Jack code to spec-compliant tECS VM code.

Jack is a structured programming language with a context-free grammar,
approaching LL(0).

It's C-esque, but /very/ weakly typed, and without spec-defined
order-of-operations. Ultimately everything in Jack is a 16 bit word. The
language is flexible enough that that could be easily changed, but standard
spec Jack is all 16-bit words, with code idioms reflecting that fact (i.e. weak
typing is central).

Jack comes equipped with a relatively full standard library (featuring I/O
abstrations, math subroutines, heap memory allocation, a string library, etc)
and uses objects and a bit of OO semantics to extend its type system, similarly
to how C uses structs.

Jack effectively has no run-time system (at least not in the Object Oriented,
scripting, or dynamic-language senses), and so is not truly object-oriented.
Things like dynamic dispatch are /no-go/.

It also has really...unique truth semantics (e.g. in if/while statements)
"""

from CompilerError import CompilerError
from lexer import lexer
from parser import parser
import backEnd as backEnd
import globalVars


def mainloop(in_pathorfile='./tests/test_code0/Square/Square.jack',
             outputMode='code', stronglinking='False', customOutDir=None,
             vmfinaloutput=True, warnings=True):

    """
    Parses a Jack file, generating either (1) code, (2) an XML parse tree,
    (3) XML tokenization.

    XML output was left intact, because tECS has an array of tests based on
    tokens and parse tree output, and that helps us know this thing's working.

    `mainloop()`:

    1. Parses either a single file or all the .jack files pointed to by a given
    directory path [files sussed out via `fileorpathparser()`]
    2a. Calls the output stage  [`.initialize_globals()`] to set parse number
    2b. Calls the output stage  [`.initialize_globals()`] to set up hash tables
    3. Outputs one of the following:
        I.  Code:
               a. PARSE ONE: Populates `varTable' and `functionsInfo', which
                  gives us the information we need for error checks and code
                  output in...
               b. PARSE TWO: Does semantic checks and outputs code
            Output is of the form *.vm

        II. XML Parse Tree: Single parse, outputs an XML representation of a
            parse tree. Output is of the form * + _.xml

        III.XML Tokens: Cycles through Jack tokens, one at a time. Proves to us
            our tokenizer works. Output is of the form * + T_.xml

    The parse can be thought of as going through text files, one at a time,
    moving left-to-right, top-to-bottom. State variables (denoting the current
    input file, currentClass, currentFn) are maintained and are
    referenced in code output to resolve variable/function references.
    """

    fileList = fileOrPathParser(in_pathorfile)

    if outputMode == 'code':  # `Code output' OR `code output into temp files'
        outputCode(fileList, stronglinking, customOutDir, vmfinaloutput)

    elif outputMode == 'parseTree':  # Outputs XML parse tree (for testing)
        outputParseTree(fileList)

    elif outputMode == 'tokens':  # Tokenizer -- outputs XML token "tree"
        outputTokens(fileList)

    print()


def outputCode(fileList, stronglinking, customOutDir, vmfinaloutput):
    import os

    # Set parse n and set up SymbolTable/modules that depend on it
    backEnd.setGlobals(parseNum=1)
    vars_, classAndFns = backEnd.SymbolTable.initialize()
    backEnd.processCode.initializeHashTables(vars_, classAndFns)
    backEnd.returnSemantics.initialize(classAndFns)

    # Stub out our output (as in I/O) to do nothing on initial parse
    output = backEnd.SetupOutput('initial')
    backEnd.processCode.defineOutput(output)
    parser.initializeGlobals(output, classAndFns, vars_)
    print('Doing initial parse of:')

    # Initial parse; fleshes out hash-tables, so that we have relevant
    # typing/function prototype (&c) information, for the output stage \/
    for fileName in fileList:
        print(fileName)

        tokenGenerator = lexer(fileName)
        globalVars.defineGlobalInputFile(fileName)
        parser.parseClass(tokenGenerator)

    # Second parse + code output \/
    backEnd.setGlobals(parseNum=2)
    for fileName in fileList:
        if customOutDir:
            # We've specified a custom directory path for output.
            # Files are still INPUT_FILE_PREFIX.jack,
            base = os.path.basename(fileName)[:-5] + '.vm'
            outFileName = os.path.join(customOutDir, base)
        else:
            outFileName = fileName[:-5] + '.vm'

        globalVars.defineGlobalInputFile(fileName)

        tokenGenerator = lexer(fileName)
        # \/ Make output (I/O) object actually write out for 2nd parse
        output.defineOutputValues('codeOutput', outFileName)
        parser.parseClass(tokenGenerator)

        if vmfinaloutput is True:
            # \/ We only output file names if we're keeping output files. If
            # this is false, VM files are just a step toward full conversion
            # (i.e. we're using JackCC as a 1st stage for further processing)
            print('Output: %s' % outFileName)
        output.closeFile()


def outputParseTree(fileList):

    # Set parse n and set up SymbolTable/modules that depend on it
    backEnd.setGlobals(parseNum=0)
    vars_, classAndFns = backEnd.SymbolTable.initialize()
    backEnd.processCode.initializeHashTables(vars_, classAndFns)
    backEnd.returnSemantics.initialize(classAndFns)

    # Set up the `o` part of I/O
    output = backEnd.SetupOutput('test')
    backEnd.processCode.defineOutput(output)
    parser.initializeGlobals(output, classAndFns, vars_)


    # ...now for the `i`
    for fileName in fileList:
        print('Reading: %s' % fileName)
        outFileName = fileName[:-5] + '_.xml'
        globalVars.defineGlobalInputFile(fileName)
        output.defineOutputValues('test', outFileName)

        # Outputs parse tree in XML
        tokenGenerator = lexer(fileName)
        parser.parseClass(tokenGenerator)
        print('Parse tree output: %s' % outFileName)
        output.closeFile()


def outputTokens(fileList):

    # Set parse n and set up SymbolTable/modules that depend on it
    backEnd.setGlobals(parseNum=0)
    vars_, classAndFns = backEnd.SymbolTable.initialize()
    backEnd.processCode.initializeHashTables(vars_, classAndFns)
    backEnd.returnSemantics.initialize(classAndFns)

    # Set up the `o` part of I/O
    output = backEnd.SetupOutput('test')
    backEnd.processCode.defineOutput(output)
    parser.initializeGlobals(output, classAndFns, vars_)


    # ...now for the `i`
    for fileName in fileList:
        outFileName = fileName[:-5] + 'T_.xml'
        globalVars.defineGlobalInputFile(fileName)
        output.defineOutputValues('test', outFileName)
        print('Reading: %s' % fileName)

        # Outputs tokens in XML
        tokenGenerator = lexer(fileName)
        backEnd.processCode.output.startt('tokens')  # opening tag `<tokens>`
        for token in tokenGenerator:
            backEnd.processCode.output.outt(token)  # tokenizing + output
        backEnd.processCode.output.endt('tokens')  # closing tag `</tokens>`
        print('Tokenized output: %s' % outFileName)
        output.closeFile()


def fileOrPathParser(path):
    """
    Returns a list containing either the single .jack file pointed to or the
    .jack files in the specified directory
    """

    import os, glob
    try:
        if path.endswith('.jack'):
            files = [path]
        else:
            files = []  # enter'd nonsense
            for inFile in glob.glob(os.path.join(path, '*.jack')):
                files.append(inFile)
            if files == []:
                raise
    except RuntimeError:
        raise CompilerError("Badly formed file or path name, %s doesn't exist "
                            "or it doesn't point to .jack files" % path) \
                            from None
    return files
