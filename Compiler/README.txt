This is the Jack to VM section of the compiler, complete with error-checks.


Files/MODULES in this folder:
--------------------------------------------------------------------------------
main_loop.py      ::  Drives the whole compliation process. Can also output an
                      XML parse tree or XML tokens (for testing purposes)

lexer/            ::  Our tokenizer

parser/           ::  As the name suggests, it's our Jack-language parser

backEnd/          ::  Code output and semantic checks. Probably the most
                      complicated part of the compiler; also the part that makes
                      clear the correspondence between Jack statements and their
                      VM representation

tests.py          ::  Array of tests. Exectuable.
----



TEST material:
--------------------------------------------------------------------------------

/tests/           :: Folder full of Jack files for us to test

/tests/testcode0/Extras_(Non_Project) ::
                     Classroom projects -- the bulk of the files we test

/tests/errors/    :: A bunch of Jack files designed to crash the compiler or
                     evoke warnings
----


For further documentation, check the respective files.

DJR,
23 August, 2017
