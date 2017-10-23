#!/usr/bin/env python3

"""
Info:
CLI for the Jack language compiler.

Stages:
  1.    Jack=>VM
  1.a. *optimizer(VM code)
  2.    VM code=>Hack Assembly
  3.    Hack Assembly=>Hack Machine Code)
*not implemented, yet

Possible modifications:
- A backend that outputs machine code in other formats (x86/64, ARM, MIPS, etc)
"""
import sys, os, glob
import argparse
import tempfile
global stdout

basePath = os.path.dirname(sys.argv[0])
for path in ['/Compiler', '/Virtual Machine', '/Assembler']:
    sys.path.insert(0, basePath + path)

import main_loop as compiler
from compiler_error import CompilerError
import VM
import HACK_rewrite as assembler


def main():
    """
    JackCC.

    Takes a Jack language file or files as input and outputs VM intermediary
    code, Hack Assembly code, or Hack machine code (the default). Command line
    flags will change the nature of our STDOUT and STDERR messages, what we're
    outputting, the name of our output file, etc.
    """

    args = defineCLIParser()    # define our CLI flags, etc

    compilerInput, tmpDir, vmInput, vmFilename, vmOutDir, asmInput,\
        asmFilename, asmOutDir, finalOutputFile, finalOutputDir = setOutputVaribles(args)
    # /\ set up all the variables we'll need to compiler output

    try:
        # Our compiler (i.e. Jack to VM) is the only stage we should really
        # expect to fail, as lexical, parse, and semantic errors will halt
        # compilation. This makes sure execution halts gracefully, instead of
        # issuing a massive stack trace
        compiler.mainloop(compilerInput, custom_out_dir=tmpDir, vmfinaloutput=args.verbose, \
                          warnings=not(args.mutewarn))
    except (CompilerError) as E:
        print('\n' + str(E)[1:-1])
        MUTE(args)              # User probably doesn't care we're deleting
        cleanUp(tmpDir)         # temp files--hence the MUTE/UNMUTE
        UNMUTE(args)            # .
        print('\nCompilation unsuccessful. Compilation halted.')
        exit(1)

    # Our other modules /shouldn't/ crash, because we're assuming our compiler
    # stage is outputting correct VM code, our VM is outputting correct Hack
    # Assembly, etc.
    MUTE(args)  # If verbose output flag is set (args.verbose=True), this will do nothing
    VM.vmtoassembly(vmInput, outputfile=vmFilename, custom_out_dir=vmOutDir)
    assembler.assembler(asmInput, asmFilename, asmOutDir)

    cleanUp(tmpDir)
    UNMUTE(args)  # if verbose output flag is set (args.verbose=True), this will do nothing

    if args.assembly or args.hack:
        print('Output: {}'.format(os.path.join(finalOutputDir, os.path.basename(finalOutputFile))))


def defineCLIParser():
    """
    Defines the arguments and flags for the JackCC CLI (and their relevant
    `help' entries).
    """
    description = """
    Jack language to Hack machine code compiler. Compiles Jack language to Hack
    machine code. Jack, Hack, and the intermediary VM language we compile to
    ("through") are all specified in Elements of Computing Systems [2005]."""

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('INFILEORPATH', help='Path to a .jack file OR a directory with multiple .jack files', type=str)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-V', '--VM', action='store_true', default=False, help='Output is tECS VM intermediary language')
    group.add_argument('-A', '--assembly', action='store_true', default=False, help='Output is Hack Assembly')
    group.add_argument('-H', '--hack', action='store_true', default=True, help='Output is Hack machine code')

    parser.add_argument('-o', '--outfile', default='', type=str)
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Gives us the full STDOUT \
    output, from the compiler\'s separate stages')
    parser.add_argument('-m', '--mutewarn', action='store_true', default=False, help='Mute warnings (not implemented)')

    return parser.parse_args()


def setOutputVaribles(args):
    """
    This hideous function is in charge of defining all the variables we'll need
    for the different stages of the compiler's output
    """

    compilerInput = args.INFILEORPATH
    finalOutputFile = args.outfile

    # Here, we set out final output directory, which'll mean different things,
    # depending on the type of output we want:
    if compilerInput.endswith('.jack'):
        contingentFinalDir = os.path.dirname(compilerInput)
        if not contingentFinalDir:
            contingentFinalDir = './'
    else:
        contingentFinalDir = compilerInput

    if finalOutputFile:
        finalOutputDir = os.path.dirname(finalOutputFile)
        if not finalOutputDir:
            finalOutputDir = './'
    else:
        finalOutputDir = contingentFinalDir

    # Output options -- {VM, assembly, hack (machine code)}
    if args.VM:
        # VM intermediary code output settings
        args.hack = False
        args.verbose = True
        tmpDir = vmInput = vmOutDir = vmFilename = asmInput = asmOutDir = asmFilename = None
        VM.vmtoassembly = assembler.assembler = null
        if finalOutputFile:
            print('WARNING: Custom file names don\'t work with VM output. Flag ignored.\n', file=sys.stderr)

    else:  # Sets up variables relevant to Assembly and HACK output

        ##############################################################
        finalOutputFile = os.path.basename(finalOutputFile)
        tmpDir = tempfile.mkdtemp()
        vmInput = os.path.join(tmpDir, os.path.basename(compilerInput))

        if vmInput.endswith('.jack'):
            vmInput = vmInput[:-5] + '.vm'

        # Normalizes input. Without it, os.path.basename gets confused by directory suffixes
        #  that don't end in '/'
        if not os.path.isdir(vmInput):
            vmInput = os.path.split(vmInput)[0]
        ##############################################################

        if args.assembly:
            # Assembly output settings
            args.hack = False
            asmInput = asmOutDir = asmFilename = None
            # assembler.HACK_rewrite.assembler = null
            assembler.assembler = null

            if finalOutputFile:
                vmFilename = finalOutputFile
                vmOutDir = finalOutputDir
            else:
                vmOutDir = contingentFinalDir
                finalOutputFile = vmFilename = 'whatever.asm'

        else:
            # HACK machine code output settings
            vmFilename = 'whatever.asm'
            vmOutDir = tmpDir
            asmInput = os.path.join(tmpDir, vmFilename)

            if finalOutputFile:
                asmFilename = finalOutputFile
                asmOutDir = finalOutputDir
            else:
                asmOutDir = contingentFinalDir
                # finalOutputFile = asmFilename = 'a.hack'
                finalOutputFile = asmFilename = 'a.comparison'

    return compilerInput, tmpDir, vmInput, vmFilename, vmOutDir, \
        asmInput, asmFilename, asmOutDir, finalOutputFile, finalOutputDir


def MUTE(args):
    """
    Mutes STDOUT, because potentially no one cares about all the intermediary
    files that go into a compiled product
    """
    global stdout
    if not args.verbose:
        stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return stdout


def UNMUTE(args):
    """Restores STDOUT"""
    if not args.verbose:
        sys.stdout = stdout


def cleanUp(tmpDirectory):
    """Gets rid of all the temp files we use during compilation"""
    if not tmpDirectory:
        pass
    else:
        print('Cleaning up tmp files: ', end='')
        for f in glob.glob(os.path.join(tmpDirectory, '*')):
            print('{} '.format(f), end='')
            os.remove(f)
        print('\nRemoving {}\n'.format(tmpDirectory))
        os.rmdir(tmpDirectory)


def null(*args, **kwargs):
    pass


if __name__ == '__main__':
    main()
