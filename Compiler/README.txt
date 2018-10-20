This is the Jack to VM section of the compiler, complete with error-checks.


Files/MODULES in this folder:
--------------------------------------------------------------------------------
mainLoop.py       ::  Drives the whole compliation process. Can also output an
                      XML parse tree or XML tokens (for testing purposes)

lexer/            ::  Our tokenizer

parser/           ::  As the name suggests, it's our Jack-language parser

backEnd/          ::  Code output and semantic checks. Probably the most
                      complicated part of the compiler; also the part that makes
                      clear the correspondence between Jack statements and their
                      VM representation

tests.py          ::  Array of tests. Exectuable.
----


Lesser files in this folder:
--------------------------------------------------------------------------------
CompilerError.py  ::  Our defined exception type for the compiler

globalVars.py     ::  Place to hold variables for the entire compiler--really
                      only used to that the whole compiler has access to the
                      filename of the file we're parsing

cmp_test.bash     ::  Small series of diffs that gives us a little bit of
                      assurance everything is working
----


TEST material:
--------------------------------------------------------------------------------

/tests/           :: Folder full of Jack files for us to test

/tests/testcode0/Extras_(Non_Project) ::
                     Classroom projects -- the bulk of the files we test
                     Repo at: https://github.com/ybakos/n2t-games-2011

/tests/errors/    :: A bunch of Jack files designed to crash the compiler or
                     evoke warnings
----


For further documentation, check the respective files.

DJR,
23 August, 2017
