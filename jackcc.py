#!/usr/bin/env python3

'''Info: 
CLI for the Jack language compiler.

Stages:
  1.    Jack=>VM
  1.a. *optimizer(VM code)
  2.    VM code=>Hack Assembly
  3.    Hack Assembly=>Hack Machine Code)
*not implemented, yet

Possible modifications:
- A backend that outputs machine code in other formats (x86/64, ARM, MIPS, etc)
'''


import sys, os, glob
import argparse
import tempfile
global stdout

compilerPath = os.path.dirname(sys.argv[0]) + '/Compiler'
sys.path.insert(0, compilerPath)

import main_loop as compiler
from compiler_error import CompilerError

virtualMachine = __import__('Virtual Machine')
assembler = __import__('Assembler')


def main():
    '''JackCC.\n\nTakes a Jack language file or files as input and outputs VM intermediary code, Hack Assembly \
code, or Hack machine code (the default). Command line flags will change the nature of our STDOUT \
and STDERR messages, what we're outputting, the name of our output file, etc.'''

    args = defineCLIParser()    # define our CLI flags, etc

    compiler_input, tmpdir, VM_input, VM_filename, VM_out_dir, asm_input,\
        asm_filename, asm_out_dir, final_output_file, final_output_dir   = setOutputVaribles(args)
    ### /\ set up all the variables we'll need to compiler output

    try:
        # Our compiler (i.e. Jack to VM) is the only stage we should really expect to fail, as
        # lexical, parse, and semantic errors will halt compilation. This makes sure execution
        # halts gracefully, instead of issuing a massive stack trace
        compiler.mainloop(compiler_input, custom_out_dir=tmpdir, vmfinaloutput=args.verbose, \
                          warnings=not(args.mutewarn))
    except (CompilerError) as E:
        print('\n' + str(E)[1:-1])
        MUTE(args)              # User probably doesn't care we're deleting
        cleanUp(tmpdir)         # temp files--hence the MUTE/UNMUTE
        UNMUTE(args)            # .
        print('\nCompilation unsuccessful. Compilation halted.')
        exit(1)

    # Our other modules /shouldn't/ crash, because we're assuming our compiler stage
    # is outputting correct VM code, our VM is outputting correct Hack Assembly, etc.
    MUTE(args)   # if we've set the verbose output flag (args.verbose=True), this will do nothing
    virtualMachine.VM.vmtoassembly(VM_input, outputfile=VM_filename, custom_out_dir=VM_out_dir)
    assembler.HACK_rewrite.assembler(asm_input, asm_filename, asm_out_dir)

    cleanUp(tmpdir) 
    UNMUTE(args) # if we've set the verbose output flag (args.verbose=True), this will do nothing

    if args.assembly or args.hack:
        print('Output: {}'.format(os.path.join(final_output_dir, os.path.basename(final_output_file))))


def defineCLIParser():
    '''Defines the arguments and flags for the JackCC CLI (and their relevant `help' entries).'''
    parser = argparse.ArgumentParser(description="Jack language to Hack machine code compiler." \
                                     " Compiles Jack language to Hack machine code. Jack, Hack, and the" \
                                     " intermediary VM language we compile to (\"through\") are all" \
                                     " specified in Elements of Computing Systems [2005].")
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
    '''This hideous function is in charge of defining all the variables we'll need for the different stages of \
 the compiler's output'''

    compiler_input = args.INFILEORPATH
    final_output_file = args.outfile

    # Here, we set out final output directory, which'll mean something different
    # depending on the type of output we want
    if compiler_input.endswith('.jack'):
        contingent_final_dir = os.path.dirname(compiler_input)
        if not contingent_final_dir:
            contingent_final_dir = './'
    else:
        contingent_final_dir = compiler_input

    if final_output_file:
        final_output_dir = os.path.dirname(final_output_file)
        if not final_output_dir:
            final_output_dir = './'
    else:
        final_output_dir = contingent_final_dir


    ### Output options -- {VM, assembly, hack (machine code)}
    if args.VM:
        # VM intermediary code output settings
        args.hack = False
        args.verbose = True
        tmpdir = VM_input = VM_out_dir = VM_filename = asm_input = asm_out_dir = asm_filename = None
        virtualMachine.VM.vmtoassembly = assembler.HACK_rewrite.assembler = null
        if final_output_file:
            print('WARNING: Custom file names don\'t work with VM output. Flag ignored.\n', file=sys.stderr)


    else: # Sets up variables relevant to Assembly and HACK output

        ##############################################################
        final_output_file = os.path.basename(final_output_file)
        tmpdir = tempfile.mkdtemp()
        VM_input = os.path.join(tmpdir, os.path.basename(compiler_input))

        if VM_input.endswith('.jack'):
            VM_input = VM_input[:-5] + '.vm'

        # Normalizes input. Without it, os.path.basename gets confused by directory suffixes
        #  that don't end in '/'
        if not os.path.isdir(VM_input):
            VM_input = os.path.split(VM_input)[0]
        ##############################################################


        if args.assembly:
            # Assembly output settings
            args.hack = False
            asm_input = asm_out_dir = asm_filename = None
            assembler.HACK_rewrite.assembler = null

            if final_output_file:
                VM_filename = final_output_file
                VM_out_dir = final_output_dir
            else:
                VM_out_dir = contingent_final_dir
                final_output_file = VM_filename = 'whatever.asm'

        else:
            # HACK machine code output settings
            VM_filename = 'whatever.asm'
            VM_out_dir = tmpdir
            asm_input = os.path.join(tmpdir, VM_filename)

            if final_output_file:
                asm_filename = final_output_file
                asm_out_dir = final_output_dir
            else:
                asm_out_dir = contingent_final_dir
                # final_output_file = asm_filename = 'a.hack'
                final_output_file = asm_filename = 'a.comparison'

    return compiler_input, tmpdir, VM_input, VM_filename, VM_out_dir, \
        asm_input, asm_filename, asm_out_dir, final_output_file, final_output_dir



def MUTE(args):
    '''Mutes STDOUT, because potentially no one cares about all the intermediary
files that go into a compiled product'''
    global stdout
    if not args.verbose:
        stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        return stdout

def UNMUTE(args):
    '''Restores STDOUT'''
    if not args.verbose:
        sys.stdout = stdout

def cleanUp(tmpdirectory):
    '''Gets rid of all the temp files we use during compilation'''
    if not tmpdirectory:
        pass
    else:
        print('Cleaning up tmp files: ', end='')
        for f in glob.glob(os.path.join(tmpdirectory, '*')):
            print('{} '.format(f), end='')
            os.remove(f)
        print('\nRemoving {}\n'.format(tmpdirectory))
        os.rmdir(tmpdirectory)

def null(*args, **kwargs):
    pass

if __name__ == '__main__':
    main()
