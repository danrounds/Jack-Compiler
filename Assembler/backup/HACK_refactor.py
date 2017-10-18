#!/usr/bin/env python3

import sys

class hacklanguage():
    # fullOPs = ["0","1","-1","D","M","A","!D","!M","!A","-D","-M","-A","D+1","M+1","A+1",
    #    "D-1","M-1","A-1","D+M","D+A","D-M","D-A","M-D","A-D","D&M","D&A","D|M","D|A"]

    C_instructions_to_binary = {
        '0':  '0101010',
        '1':  '0111111',
        '-1': '0111010',

        'D':  '0001100',    '!D': '0001101',    '-D': '0001111',
        'A':  '0110000',    '!A': '0110001',    '-A': '0110011',
        'M':  '1110000',    '!M': '1110001',    '-M': '1110011',

        'D+1':'0011111',    'D-1':'0001110',
        'A+1':'0110111',    'A-1':'0110010',
        'M+1':'1110111',    'M-1':'1110010',

        'D+A':'0000010',    'D-A':'0010011',    'A-D':'0000111',
        'A+D':'0000010',

        'D+M':'1000010',    'D-M':'1010011',    'M-D':'1000111',
        'M+D':'1000010',

        'D&A':'0000000',    'D|A':'0010101',
        'A&D':'0000000',    'A|D':'0010101',
        'D&M':'1000000',    'D|M':'1010101',
        'M&D':'1000000',    'M|D':'1010101',
    }

    inst_destinations = {
        'null':'000',
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'A':   '100',
        'AM':  '101',
        'AD':  '110',
        'AMD': '111',
    }

    jump_table = {
        'null':'000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }

    built_in_references = {"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"R0":0,"R1":1,"R2":2,
   "R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10, "R11":11,"R12":12,"R13":13,
   "R14":14,"R15":15,"SCREEN":16384,"KB":24576}

    # operands = ["=","+","-",";","!","|"]
    validstringsymbols = "_.$:"


class system():
    '''This defines the basic parameters of the HACK architecture/computer/memory model'''
    start_statics_mem = 16
    max_literal = 32767


class SymbolTable():
    def __init__(self):
        import re
        self.variableRAM = system.start_statics_mem
        self.table = hacklanguage.built_in_references
        self.RAMlocationswithjumps = set()
        self.exceededStatics = False
        self.label_match = re.compile(r'[A-Za-z_\.\$:][\dA-Za-z_\.\$:]*').match

    def addLabel(self, label, number, line):
        if not self.table.__contains__(label):
            self.isWellDefinedLabel(label, line)
            self.table[label] = number
            self.RAMlocationswithjumps.add(number)
        else:
            raise Exception('Label {} already defined. Line {}'.format(label, line))

    def checkValue(self, label, line):
        self.isWellDefinedLabel(label, line)
        try:
            return self.table[label]
        except:
            RAM = self.variableRAM
            if not self.exceededStatics and RAM > 255:
                import sys
                print("ASSEMBLER WARNING: You've exceeded the 240 static variables allowed in the Jack+Hack ", file=sys.stderr, end='')
                print("specs. If you're not compiling from Jack or aren't using RAM[256] as the base of your ", file=sys.stderr, end='')
                print("stack, you can probably ignore this warning. Otherwise, expect lot of undefined behavior.\n", file=sys.stderr)
                self.exceededStatics = True
            self.table[label] = RAM
            self.variableRAM += 1
            return RAM

    def isWellDefinedLabel(self, label, line):
        try:
            match_length = self.label_match(label).span()[1]
            if match_length < len(label):
                raise
        except:
            raise Exception('Malformed label: {}. Line {}'.format(label, line))

global max_literal_reached
def parseAInstruction(line, in_line_no, symbolTable):
    global max_literal_reached
    value = line[1:]
    try:
        value = int(value)
        if value < 0:
            raise SyntaxError('Literals cannot be negative.')
    except SyntaxError:
        raise
    except:
        value = symbolTable.checkValue(value, in_line_no)

    if not max_literal_reached and value > system.max_literal:
        print('ASSEMBLER ERROR: Line {} (assembly input), `{}\' exceeds the size for constants. '.format(in_line_no, value), file=sys.stderr, end='')
        print('You\'ve either used too large a literal or are referencing one that is. ',  file=sys.stderr, end='')
        print('Hack\'s memory/constant limit is {}'.format(system.max_literal), file=sys.stderr)
        print('Subsequent constant/size warnings will be suppressed.\n', file=sys.stderr)
        max_literal_reached = True

    return "{:b}".format(value).zfill(16) # Converts to binary, and pads zeros,
                                                    #  so we have all 16 bits

def parseCInstruction(line, in_line_no):
    if line.__contains__(';'):
        # JUMPs
        components = line.split(';')
        try:
            if len(components) == 2:
                destination = '000'
                op = hacklanguage.C_instructions_to_binary[components[0]]
                jmp = hacklanguage.jump_table[components[1]]
            else:
                raise
        except:
            raise SyntaxError('Malformed jump instruction: `{}\' Line {}'.format(line, in_line_no))

    elif line.__contains__('='):
        # OPs with destination
        components = line.split('=')
        try:
            if len(components) == 2:
                destination = hacklanguage.inst_destinations[components[0]]
                op = hacklanguage.C_instructions_to_binary[components[1]]
                jmp = '000'

            elif len(line) == 1:
                # OPs without destination (i.e. NO-OPs)
                destination = '000'
                op = hacklanguage.C_instructions_to_binary[components[0]]
                jmp = '000'

            else:
                raise
        except:
            raise SyntaxError('Malformed C-instruction: `{}\', line {}'.format(line, in_line_no))

    else:
        raise SyntaxError('Malformed command: `{}\' line {}'.format(line, in_line_no))

    return '111' + op + destination + jmp

global max_literal_reached
max_literal_reached = False

def assembler(asmfilename, outputname='a.hack', custom_out_dir=None,):
    '''Turns Hack Assembly into Hack Machine code'''

    symbolTable = SymbolTable()
    outputname, output = openOutputFile(asmfilename, outputname, custom_out_dir)

    with open(asmfilename, 'r') as read:
        parseLabels(read, symbolTable)

        in_line_no = 1

        read.seek(0)
        for line in read:
            line = removeWhiteSpace(line)

            if not (line == '' or line.startswith('//') or line.startswith('(') and line.endswith(')')):
                # Here \/, we've ruled out comments and labels

                # A-instructions
                if line.startswith('@'):
                    opcode = parseAInstruction(line, in_line_no, symbolTable)

                # C-instructions & misc. lines of garbage 
                else:
                    opcode = parseCInstruction(line, in_line_no)

                output.write('{}\n'.format(opcode))
            in_line_no += 1

        print("Assembly successful. Output file:", outputname)
        output.close()


def openOutputFile(asmfilename, outputname, custom_out_dir):
    import os

    if custom_out_dir:
        directory = custom_out_dir
    else:
        directory = os.path.dirname(asmfilename)
    outputname =  os.path.join(directory, outputname)

    try: # Setup output
        output = open(outputname, 'w')
    except:
        raise Exception('Can\'t seem to open the output file, {}. Check permissions and try again.'.format(outputname))

    return outputname, output


def removeWhiteSpace(line):
    line = line.replace(' ', '')
    line = line.replace('\t', '')
    line = line.replace('\n', '')
    return line


def parseLabels(file_, symbolTable):
    '''Initial parse. Populates our symbol table with values for `(labels)\''''
    import sys

    in_line_no = 1; out_line_no = 0
    size_limit_reached = False

    for line in file_:
        line = line.strip()

        if line.startswith('//'):  # comments
            pass

        if line.startswith('(')  and line.endswith(')'):  # labels
            label = line[1:-1]
            symbolTable.addLabel(label, out_line_no, in_line_no)

        else:                   # commands (or garbage. We'll find out later)
            out_line_no += 1
            if not size_limit_reached and out_line_no > system.max_literal:
                print('ASSEMBLER ERROR. Output exceeds Hack\'s memory size. ', file=sys.stderr, end='')
                print('Output will continue, but cannot be relied upon.\n' ,file=sys.stderr)
                size_limit_reached = True

        in_line_no +=1

if __name__ == '__main__':
    assembler('Example.asm', 'Example.hack')
