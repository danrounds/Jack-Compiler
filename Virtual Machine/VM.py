#!/usr/bin/env python3

"""
tECS-VM-to-HACK-Assembly Translator

Converts tECS-spec VM code to Hack Assembly code
tECS VM language, Hack Assembly, and the Hack architecture are all defined in
The Elements of Computing Systems [2005].

The virtual machine \"implemented\" here is a stack machine, featuring:
- Basic arithmetic and logical ops (add/sub, negation, [in]equality testing, &c)
- Basic stack operations (push/pop)
- A stack with logical variable segmentation (local and argument sections)
- Defined constructs for structured programming (function labels and calls,
  conditionals AND labeled-gotos and conditional jumps native that map directly
  to assembly)
- Special purpose registers (e.g. for handling implicit object references: `this`),
- General purpose registers (R5 through R12),

...basically a lot of niceties left undefined on the bare-bones, two-register
Hack architecture, which sets up structures that correspond very well to C-
style/"structured programming" language features.

The converter is non-optimizing, but the introduction of some extra
instructions could make the output much more time & space efficient..

The converter assumes correct VM code, generated by a compiler (NOT hand-
written). It generates error messages, and will catch if code uses operators
undefined in tECS VM, but it isn't thorough about checking for bad semantics or
things outside the very primitive grammar of tECS VM.
"""


def vmtoassembly(pathOrFile, outputFile='whatever.asm', customOutDir=None,
                 bootstrap=True):
    """
    Main function

    Accepts a path--either to a single VM file or to a directory--and converts
    file or files ending in .vm to a single assembly file.
    (*.vm=>whatever.asm)

    I kind of hate this code, but it's fundamentally some /really/ simple text
    processing, and it does what it should. Also, the documentation makes
    pretty clear what the translation's actually doing.

    """
    import os
    import processVmInstructions
    from processVmInstructions import processVmInstruction, writeBootstrap

    filelist = parseFileOrPath(pathOrFile)

    nToTranslate = len(filelist)
    asmOutPath, file_ = setupOutputFile(outputFile, customOutDir, filelist)
    processVmInstructions.initialize(file_)
    globallyUniqueN = 1

    if bootstrap:
        writeBootstrap()

    for f in filelist:
        read = setupInputFile(f)
        moduleprefix = os.path.basename(f)[:-3]

        lineNum = 1
        for line in read:
            line = tokenize(line)
            # `line' is now a list of operators and arguments.

            processVmInstruction(line, moduleprefix, lineNum, globallyUniqueN)
            # /\ Where the magic happens

            lineNum += 1
            globallyUniqueN += 1

        nToTranslate -= 1
        read.close()
        print('%s translated. %s file(s) to go.' % (f, nToTranslate))
    print('Output file: %s\n' % asmOutPath)
    file_.close()  # close output


def parseFileOrPath(path):
    """
    Returns a list containing either the single .vm file `path' points to OR
    the .vm files in the specified directory
    """
    import os
    import glob
    try:
        if path.endswith('.vm'):
            files = [path]
        else:
            files = []  # enter'd nonsense
            for inFile in glob.glob(os.path.join(path, '*.vm')):
                files.append(inFile)
            if files == []:
                raise
    except:
        raise RuntimeError('Badly formed file or path name, %s doesn\'t exist,'
                           ' or it doesn\'t  point to .vm files' % path)
    return files


def setupOutputFile(outputFile, customOutDir, filelist):
    import os
    import Output
    if customOutDir:
        directory = customOutDir
    else:
        directory = os.path.dirname(filelist[0])
    asmOutPath = os.path.join(directory, outputFile)

    try:
        file_ = Output.Output(asmOutPath)
    except:
        raise Exception('TRANSLATION FAILURE. You seem not to have write permission.')
    return asmOutPath, file_


def setupInputFile(file_):
    try:
        return open(file_)
    except:
        raise RuntimeError('Could not open file. Maybe check permissions.')


def tokenize(line):
    """
    Turns a line (string) into a nice li'l list of separate tECS-VM tokens
    (assuming the input is tECS-VM, to begin with).

    str->[]
    """
    line = line.split('//')[0]
    line = line.replace('\t', ' ')       # Normalize whitespace separators
    line = line.strip().split(' ')
    line = [x for x in line if x != '']  # pour on the list comprehension
    if line == []: line = ['']
    return line


if __name__ == '__main__':
    from interpreter import VMinterpreter
    VMinterpreter()
