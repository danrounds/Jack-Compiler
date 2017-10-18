This is the "Virtual Machine" component of the Elements of Computing System-
defined compiler. It translates programs in tECS-VM language to Hack Assembly.
Both are defined in tECS.

Though in theory, someone could hand write programs in tECS-VM, the
possibility's remote. The translator assumes its input is machine-written, and
is thus lax about error-checking.

The VM language defines a stack-machine with simple stack-based/structured-
programming operations, i.e.,
      `call', `function', `pop', `push', `add', `sub', logical comparison, etc.

The language maps quite easily to a structured programming language, like Jack
(and v/v).

Here's an example subroutine in tECS:
      function Main.main 1         //function declaration
         call Game.new 0
         pop local 0
         push local 0
         call Game.run 1
         pop temp 0
         push local 0
         call Game.dispose 1       //function call
         pop temp 0
         push constant 0
         return

An abreviated sample of this module's output for the above is:
      (Main.main)
      @SP
      A=M
      M=0
      @SP
      M=M+1
      @RTN_ADR_Game.new7354
      D=A
      @SP
      A=M
...

That covers merely the first line of the above input, and a small portion of the
second.

Yes. Hack Assembly is verbose.

For more documentation, see VM.py

----
Daniel J Rounds,
27 August, 2016