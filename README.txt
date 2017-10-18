JackCC -- Jack Complete Compiler 
---------------------

Jack is a C-esque, weakly-typed structured programming language. This is a spec-
compliant compiler.

Jack, along with the tECS VM intermediary language, Hack Architecture, and
corresponding Hack Assembly language are defined in the book The Elements of
Computing Systems, by Nisan and Schoken (2005).

This project is the synthesis of the three major projects defined in tECS --
assembler, VM platform, and compiler. They are modular, both because of the
soundness of separation of concerns and encapsulation of function, but also
because each project has an interface (in the sense of input=>output) defined in
tECS (as well as corresponding tests).


                                  Package Contents:
-------------------------------------------------------------------------------
Compiler/                       Jack to VM compiler
    A non-optimizing compiler which turns Jack Language code into our VM
    intermediary representation. It offers fairly robust error checking.

Virtual Machine/            A VM to assembly translator
    Turns VM file(s) into HACK Assembly language.
    The VM language defines a stack machine with structured programming
    constructs and arithmetic/logical operations. The VM language serves mainly
    as an intermediary language from Jack to the barebones Hack architecture.

    This module also inclues an "interpreter," which shows us the Hack Assembly
    output for given VM commands. This is useful for gaining an intuition to
    what the VM is actually doing.

    The VM's documentation, moreso than the other projects, probably best
    explains how the Jack/Hack system actually works, from a low-level
    perspective.

Assembler/                       Hack Assembler
    Turns HACK Assembly into a list of 16-bit opcodes for the Hack Architecture.
    The Hack machine is a two-register machine with a Harvard architecture
    (split RAM and program memories). All instructions are 16-bits in length and
    take 1-cycle to complete, (i.e. no microcode -- i.e. no hardware
    multiplication or divide), so programs are /quite/ verbose.

    The assembler offers reasonably robust error checking, as it is quite possible
    someone would want to use it as a standalone. It doesn't have a CLI
    frontend, and so can currently only be used as such inside an interactive
    Python session.
             

./jackcc.py                      CLI frontend
    The front-end, tying together the three modular components above and
    providing a CLI.

    Example usage:
               $ ./jackcc.py ~/input_directory_of_dot_jack_files/

    This will run the compiler and translate our Jack project into machine code.
    Flags enable us to choose output type (VM, Hack, or asm), choose a file-
    name, etc.
    E.g.,

               $ ./jackcc.py -Ho output.asm ~/input_directory_of_dot_jack_files/

    This compiles Jack to an assembly file: output.asm


                                Project info:
--------------------------------------------------------------------------------
All projects are coded in Python 3. Individual projects have their own README
files; individual modules have their own docstrings, explaining their
perculiarities. Dependencies (beyond the obvious Python 3) are limited to `diff'
and a little bit of Bash (for tests). The compiler was originally written in
Windows, but I no longer have a Windows system with which to try out the old,
Windows-based tests. I guess you could say MinGW would cover Windows
dependencies.

/Virtual Machine/, /Compiler/, and the base directory all contain project-
specific tests. /Assembler/ and /Compiler/ include some example input files that
test error-detection. The projects have been extensively tested using tools
included with tECS, but they're not included, here (they're not easily
automated).

A NOTE ABOUT TESTS: My tests relied on publicly-hosted but non-open-source code.
The relevant code has been omitted from this repo. As a result, some tests might
fail (I've not run the tests without the relevant code). The code was a
collection of ambitious student games, written in Jack. Without them,  I was
writing a compiler for an abstractly-defined language with very little
accompanying practice. When and if I find a substitute, I'll throw it into this
repo.

A NOTE ON STYLE: My code lines are almost invariably longer than 80 characters,
because my variable/function/method/&c names are verbose. This is a conscious
stylistic choice, but perhaps I'm underestimating the number of people stuck
reading code on hardline terminals. Apologies to you, if you're one.


                               Project History:
--------------------------------------------------------------------------------
This is a project I completed in 2012--basically the first substantial
programming project I ever worked on. In making this worth hosting on GitHub, I
did a bit of refactoring, clean-up, and re-writing. It needs work, in terms of
code style (consistency, etc), and it really should be modularized, a bit more
(as in: discrete components belong in their own modules).

Other than that, it's done--insofar as something I could extend for the rest
of my life can be considered "done".

---
Daniel J Rounds,
2017
