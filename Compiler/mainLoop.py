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
             outputmode='code', stronglinking='False', custom_out_dir=None,
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

    filelist = fileorpathparser(in_pathorfile)

    if outputmode == 'code':  # `Code output' OR `code output into temp files'
        outputCode(filelist, stronglinking, custom_out_dir, vmfinaloutput)

    elif outputmode == 'parse_tree':  # Outputs XML parse tree (for testing)
        outputParseTree(filelist)

    elif outputmode == 'tokens':  # Tokenizer -- outputs XML token "tree"
        outputTokens(filelist)

    print()


def outputCode(filelist, stronglinking, custom_out_dir, vmfinaloutput):
    import os

    # Set parse n and set up SymbolTable/modules that depend on it
    backEnd.setGlobals(parseNum=1)
    vars_, classAndFns = backEnd.SymbolTable.initialize()
    backEnd.processCode.initializeHashTables(vars_, classAndFns)
    backEnd.returnSemantics.initialize(classAndFns)

    # Stub out our output (as in I/O) to do nothing on initial parse
    output = backEnd.SetupOutput('initial')
    backEnd.processCode.defineOutput(output)
    parser.initializeTagOutput(output)
    print('Doing initial parse of:')

    # Initial parse; fleshes out hash-tables, so that we have relevant
    # typing/function prototype (&c) information, for the output stage \/
    for filename in filelist:
        print(filename)

        tokengenerator = lexer(filename)
        globalVars.defineGlobalInputFile(filename)
        parser.parseClass(tokengenerator)

    # Second parse + code output \/
    backEnd.setGlobals(parseNum=2)
    for filename in filelist:
        if custom_out_dir:
            # We've specified a custom directory path for output.
            # Files are still INPUT_FILE_PREFIX.jack,
            base = os.path.basename(filename)[:-5] + '.vm'
            outfilename = os.path.join(custom_out_dir, base)
        else:
            outfilename = filename[:-5] + '.vm'

        globalVars.defineGlobalInputFile(filename)

        tokengenerator = lexer(filename)
        # \/ Make output (I/O) object actually write out for 2nd parse
        output.defineOutputValues('codeOutput', outfilename)
        parser.parseClass(tokengenerator)

        if vmfinaloutput is True:
            # \/ We only output file names if we're keeping output files. If
            # this is false, VM files are just a step toward full conversion
            # (i.e. we're using JackCC as a 1st stage for further processing)
            print('Output: %s' % outfilename)
        output.closeFile()


def outputParseTree(filelist):

    # Set parse n and set up SymbolTable/modules that depend on it
    backEnd.setGlobals(parseNum=0)
    vars_, classAndFns = backEnd.SymbolTable.initialize()
    backEnd.processCode.initializeHashTables(vars_, classAndFns)
    backEnd.returnSemantics.initialize(classAndFns)

    # Set up the `o` part of I/O
    output = backEnd.SetupOutput('test')
    backEnd.processCode.defineOutput(output)
    parser.initializeTagOutput(output)

    # ...now for the `i`
    for filename in filelist:
        outfilename = filename[:-5] + '_.xml'
        globalVars.defineGlobalInputFile(filename)
        output.defineOutputValues('test', outfilename)
        parser.initializeTagOutput(output)

        # Outputs parse tree in XML
        tokengenerator = lexer(filename)
        parser.parseClass(tokengenerator)
        print('Output: %s\n' % outfilename)
        output.closeFile()


def outputTokens(filelist):

    # Set parse n and set up SymbolTable/modules that depend on it
    backEnd.setGlobals(parseNum=0)
    vars_, classAndFns = backEnd.SymbolTable.initialize()
    backEnd.processCode.initializeHashTables(vars_, classAndFns)
    backEnd.returnSemantics.initialize(classAndFns)

    # Set up the `o` part of I/O
    output = backEnd.SetupOutput('test')
    backEnd.processCode.defineOutput(output)
    parser.initializeTagOutput(output)

    # ...now for the `i`
    for filename in filelist:
        outfilename = filename[:-5] + 'T_.xml'
        # outfilename = filename[:-5] + '_COMPARE_T_.xml'
        globalVars.defineGlobalInputFile(filename)
        output.defineOutputValues('test', outfilename)
        print('Reading: %s' % filename)

        # Outputs tokens in XML
        tokengenerator = lexer(filename)
        backEnd.processCode.output.startt('tokens')  # opening tag `<tokens>`
        for token in tokengenerator:
            backEnd.processCode.output.outt(token)  # tokenizing + output
        backEnd.processCode.output.endt('tokens')  # closing tag `</tokens>`
        print('Output: %s' % outfilename)
        output.closeFile()


def fileorpathparser(path):
    '''
    Returns a list containing either the single .jack file pointed to or the
    .jack files in the specified directory
    '''

    import os; import glob
    try:
        if path.endswith('.jack'):
            files = [path]
        else:
            files = []  # enter'd nonsense
            for infile in glob.glob(os.path.join(path, '*.jack')):
                files.append(infile)
            if files == []:
                raise
    except RuntimeError:
        raise CompilerError("Badly formed file or path name, %s doesn't exist "
                            "or it doesn't point to .jack files" % path) \
                            from None
    return files
