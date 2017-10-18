This is the assembler portion of the Jack-to-Hack-Machine compiler.

The Hack Machine is a two-register, flat-memory machine, with 32K of program
memory and even less RAM.

Hack Assembly offers a tiny bit of synatitic sugar, so that we can treat certain
RAM[n] as virtual registers, and portions of our address space as keyboard input
and screen output. None of the machine's instructions are specific to I/O or to
providing the stack model that the virtual register names imply.

The Hack CPU provides nothing but 2s-complement addition, in-/direct addressing,
and conditional jumps. I.e., the very basics of what we need to define a
digital computer.

This, combined with the fact that we only have two registers to work with (and
the fact that all instructions are one-cycle long) means that Hack programs are
extremely verbose.


          SAMPLE INPUT                    SAMPLE OUTPUT
===========================================================================
          (Square.new)                      
          @SP                             0000000000000000
          A=M                             1111110000100000
          M=0                             1110101010001000
          @SP                             0000000000000000
          M=M+1                           1111110111001000
          @SP                             0000000000000000
          A=M                             1111110000100000
          M=0                             1110101010001000
          @SP                             0000000000000000
          M=M+1                           1111110111001000
          @SP                             0000000000000000
          A=M                             1111110000100000
          M=0                             1110101010001000


The assembler provides some error-checking, as it's conceivable someone would
want to use it as a standalone. It doesn't yet have a CLI, though. Check the
source for details as to how it works. In the backup folder, HACK_refactor.py
is a perhaps more easily readable version of the assembler (for reference).

Daniel J Rounds,
27 August, 2016
