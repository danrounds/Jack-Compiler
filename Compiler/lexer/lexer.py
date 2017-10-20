##########################################################################################
## Lexing (tokenizing) stage
##########################################################################################
##########################################################################################

from back_end import CompilerError as CompilerError
from . import lexer_errors as TErrorMsg

import collections
# \/ data type yielded by the tokenizer (called `generator`, throughout the code)
Token = collections.namedtuple('Token', ['typ', 'value', 'line'])
# - typ   : The type of syntactic unit we're dealing with
# - value : The actual token, as it appeared in the file we're parsing
# - line  : The line number we found the token on. We use this for error-checks
def lexer(filename):  
    '''Modified version of the tokenizer in Python documentation

You can think of this as a data structure that yields tagged Jack tokens.'''
    import re
    keywords = {'class', 'constructor', 'function', 'method', 'field',
                'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
                'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while',
                'return'}
    
    token_specification = [
        ('NEWLINE',         r'\n'),                     # Line endings
        ('SKIP',            r'[ \t]'),                  # Spaces and tabs(skip)
        ('COMMENT',         r'//.*\n'),                 # Single-line comment
        ('WHOLECMNT',       r'/\*.*\*/'),               # SINGLELINESTARCOMMENT
        ('STRTCMNT',        r'/\*'),                    # MULTILINECOMMENTstart
        ('ENDCMNT',         r'.*\*/'),                  # MULTILINECOMMENTend
        ('BAD_ID',          r'\d+[A-Za-z]+'),           # 1dentifier
        ('integerConstant', r'\d+'),                    # Integer
        ('identifier',      r'[A-Za-z_][\dA-Za-z_]*'),  # Identifiers
        ('symbol',  r'[{}\()\[\]\.,;\+\-\*/&\|<>=~]'),  # Symbols
        ('stringConstant',  r'"[^\n]*?"'),              # String
        ('GARBAGE',         r'.+?')                     # Everything else
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    ln = 1
    opencomment = False

    with open(filename) as inputvariable:
    # `with` method assures file closes, even if exception is raised
        for s in inputvariable:
            pos = line_start = 0
            mo = get_token(s)
            while mo is not None:
            # the loop continues until it's reg-exed the entire line
                typ = mo.lastgroup
                
                if typ == 'NEWLINE' or typ == 'COMMENT':
                # increment line counter whether or not it falls in a comment
                    ln += 1

                elif typ == 'ENDCMNT':
                    if opencomment == False:
                    # ENDCMNT tokens shouldn't happen unless 'opencomment' is True
                        raise CompilerError(TErrorMsg.cmnt_end() % (ln, filename))
                    opencomment = False

                elif opencomment == False:
                # tokenizing when we're not 'in' a comment:
                    if typ == 'STRTCMNT':
                        opencomment = True
                        startcommentline = ln
                    elif typ == 'GARBAGE':
                        #                    (s[pos], ln, filename))
                        raise CompilerError(TErrorMsg.bad_token() % \
                                           (s[pos], ln, filename))
                    elif typ == 'BAD_ID':
                        err = mo.group(typ) 
                        raise CompilerError(TErrorMsg.bad_id() % (err,ln,filename))

                    elif typ != 'SKIP' and typ not in ('ENDCMNT', 'WHOLECMNT'):
                        val = mo.group(typ)
                        if typ == 'identifier' and val in keywords:
                            typ = 'keyword'
                        elif typ == 'INTEGER':
                            if 0 > int(val) or 32767 < int(val):
                                raise CompilerError(TErrorMsg.int_overflow() % \
                                                   ln, filename)
                        elif typ == 'stringConstant':
                            val = val[1:-1]
                        yield Token(typ, val, ln)

                pos = mo.end()              # end() returns end char of current str
                mo = get_token(s, pos) 
        inputvariable.close()
        if opencomment == True:
        # triggered if EOF is reached but a comment is still open
            raise CompilerError(TErrorMsg.open_cmnt() % (startcommentline, filename))





