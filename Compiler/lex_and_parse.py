###############################################################################
# Tokenizer and Parser for the Jack compiler, tECS
#
# I've treated this file as largely self-documenting (since the parse functions are all nameed
#  according to function). Each parse function passes and accepts our token generator and/or
#  specific tokens.
#
# On the first parse, our parse functions call the `back_end' to construct our varTable,
#  and functionInfo table (including our list_of_extended_types -- i.e. the user-defined types
#  we find while parsing).
#
# On the second parse, we call `back_end', and use this information to check semantics and output code.
# -DR, August 2016

import back_end
from back_end import CompilerError as CompilerError
# from . import back_end


class TErrorMsg():
    '''Error messages for our tokenizer'''
    def bad_token():
        return 'Unexpected character %r on line %d, %s'
    def bad_id():
        return "Poorly formed identifer, '%s'. Line %s, %s"
    def open_cmnt():
        return 'Non-terminating comment. Line %s, %s'
    def cmnt_end():
        return 'Comment end without a beginning. Line %s, %s'
    def int_overflow():
        return 'Line %s: Integer value is out of range (0 <= int <= 32767), %s'

class PErrorMsg():
    '''Parse error messages'''
    def __init__(self, token):
        self.value = getattr(token, 'value')
        self.line = getattr(token, 'line')
        self.file = back_end.global_infilename

    def no_class_declr(self):
        return "Syntax Error: Jack language files begin with a `class` declaration. %s"\
               % self.file
    def no_class_name(self):
        return "Line %s: Expected class name, got '%s'. %s" % \
               (self.line, self.value, self.file)
    def no_type(self):
        return "Line %s: Expected type, got '%s'. %s" % \
               (self.line, self.value, self.file)
    def no_semivar(self):
        return "Line %s. Expected more variable names or a semicolon, got '%s'. %s"\
               % (self.line, self.value, self.file)
    def no_varname(self):
        return "Line %s. Expected varName, got semicolon. %s" % \
               (self.line, self.file)
    def no_voidtype(self):
        return "Syntax Error, line %s. Expected `void` or a type, got '%s'. %s" % \
               (self.line, self.value, self.file)
    def badstatement(self):
        return "Invalid statement type, Line %s. %s" % (self.line, self.file)
    def badexpression(self):
        return "Line %s: Expected expression, got '%s'. %s" % \
               (self.line, self.value, self.value)
    def badidentifier(self):
        return "Line %s: Bad Identifier, '%s'. %s" % \
               (self.line, self.value, self.file)
    def addlarguments(self):
        return "Line %s: Comma without add'l arguments. %s" % \
               (self.line, self.file)
    def endofstatement(self):
        return "Expected end of statement,`;`, Line %s. %s" % \
               (self.line, self.file)
    def leftparen(self):
        return "Line %s: Expected '(', got '%s'. %s" % \
               (self.line, self.value, self.file)
    def rightparen(self):
        return "Line %s: Expected ')', got '%s'. %s" % \
               (self.line, self.value, self.file)
    def leftcurly(self):
        return "Line %s: Expected '}', got '%s'. %s" % \
               (self.line, self.value, self.file)
    def rightcurly(self):
        return "Line %s: Expected '{', got '%s'. %s" % \
               (self.line, self.value, self.file)
    def semicolon(self):
        return "Line %s: Expected semicolon, got '%s'. %s" % \
               (self.line, self.value, self.file)
    def period(self):
        return "Line %s: Expected period, got '%s'. %s" % \
               (self.line, self.value, self.file)
    def equals(self):
        return "Line %s: Expected '=', got '%s'. %s" % \
               (self.line, self.value, self.file)
    def closingsquare(self):
        return "Line %s: Expected closing ']', got '%s'. %s" % \
               (self.line, self.value, self.file)


##########################################################################################
## Lexing (tokenizing) stage
##########################################################################################
##########################################################################################

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





#### PARSER ####    #### PARSER ####    #### PARSER ####    #### PARSER ####
## Everything below is our parser.

def parseClass(generator):
    '''Initial parse function. Each file holds a class, thus the `class` is the main unit of compilation'''
    back_end.DoesFunctionReturnStack.stackvars_init()
    token = next(generator)
    if token.value == 'class':
        back_end.output.startt('class'); back_end.output.outt(token)
        token = next(generator)
        if parseClassName(token) == False:
            raise CompilerError(PErrorMsg(token).no_class_name())
        back_end.setCurrentClass(token)
        parseLeftCurly(next(generator))
        token = next(generator)
        isCurly = parseRightCurly(token)
        if isCurly == False:

            # Here, we're parsing field & static vars + keeping a count
            back_end.varTable.resetFieldStaticCount()
            back_end.varTable.Declaration(True)
            moreClassVarDecd = parseClassVarDec(token, generator)
            while moreClassVarDecd == True:
                moreClassVarDecd = parseClassVarDec(next(generator), generator)
            # Now we know the n fields that Class defines for its object type:
            back_end.functionsInfo.codifyField_N()

            # Time to parse subroutines:
            moreSubroutineDeclared = parseSubroutineDec(moreClassVarDecd, generator)
            while moreSubroutineDeclared == True:
                moreSubroutineDeclared = parseSubroutineDec(None, generator)
            rightcurly = parseRightCurly(moreSubroutineDeclared)
            if rightcurly == False:
                raise CompilerError(PErrorMsg(token).rightcurly())

            back_end.varTable.addToAvailableTypes()

            back_end.output.endt('class')
            try:
                next(generator)
            except:
                pass
            else:
                ## CLEAN UP
                raise CompilerError("Expected end of file. Line %s" % token.line)
                ## CLEAN UP
    else:
        raise CompilerError(PErrorMsg(token).no_class_declr())

def parseClassVarDec(token, generator):
    '''Returns True if thing parsed is of the form classVarDec,
    Returns token if it plainly isn't,
    Raises CompilerError if things are badly formed.'''
    if token.value in ('static', 'field'):

        kind = token.value
        back_end.output.startt('classVarDec'); back_end.output.outt(token)

        token = next(generator)
        type_ = parseType(token)
        back_end.varTable.checkTypeExistence(token)

        if not type_:
            raise CompilerError(PErrorMsg(token).no_type())

        token = next(generator)
        parseVarName(token)
        back_end.varTable.addVariable(token, type_, kind, scope='class')
        
        token = next(generator)
        comma = parseComma(token)
        while comma == True:

            token = next(generator)
            parseVarName(token)
            back_end.varTable.addVariable(token, type_, kind, scope='class')

            semi = parseSemicolon(token)
            if semi == False:
                token = next(generator)
                comma = parseComma(token)
            else:
                raise CompilerError(PErrorMsg(token).no_varname())

        if parseSemicolon(token) == True:
            back_end.output.endt('classVarDec'); return True
        else:
            raise CompilerError(PErrorMsg(token).no_semivar())
    else: return token

def parseSubroutineDec(token, generator):
    if token == None: token = next(generator)
    functTyp = back_end.functionsInfo.defFunctTyp(token)
    if functTyp in ('constructor', 'function', 'method'):
        
        back_end.DoesFunctionReturnStack.stack_init()
        
        back_end.functionsInfo.init_k_params()  # Sets an initial value for `k' parameters
        back_end.output.startt('subroutineDec'); back_end.output.outt(token)

        token = next(generator)

        # if getattr(token, 'value') == 'void':
        #     back_end.output.outt(token); returnTyp = 'void'
        # elif parseType(token):
        #     returnTyp = getattr(token, 'value')
        # else:

        if parseType(token):
            back_end.varTable.checkTypeExistence(token, subroutineDeclaration=True)
            returnTyp = token.value
        else:
            raise CompilerError(PErrorMsg(token).no_voidtype())

        subroutinetoken = next(generator)
        parseSubroutineName(subroutinetoken)
        back_end.setCurrentFunction(subroutinetoken)

        back_end.CodeProcess.SubroutineDeclaration(token)

        parseLeftParen(next(generator))
        back_end.varTable.resetVarCounter()    # Resets `localVarN' declared
        token = parseParameterList(generator)  # Will figure out our `k' parameters
        parseRightParen(token)

        parseSubroutineBody(generator)

        back_end.DoesFunctionReturnStack.codecheck(subroutinetoken)
        # checks whether the code in the this subroutine (i.e. function) will actually return
        
        back_end.functionsInfo.addFunction(returnTyp, subroutinetoken)
        # @ this point,variableTable.localVarN contains the total n of local vars decl'd in the current function

        back_end.output.endt('subroutineDec'); return True
    else: return token

def parseParameterList(generator):
    '''Returns a token--either after evaluating `type varName` (',' `type varName`) or after finding
    nothing of that form. Returned token should be a '(', else calling function will grind to a halt'''

    back_end.output.startt('parameterList')

    token = next(generator)
    type_= parseType(token)

    if type_:
        back_end.varTable.checkTypeExistence(token)

        token = next(generator)
        parseVarName(token)
        back_end.varTable.addVariable(token, type_, _kind='argument', scope='function')

        token = next(generator)
        back_end.functionsInfo.increment_k_params()
        comma = parseComma(token)

        # we're tallying the number of argument variables in our function declarations:
        while comma == True:
            back_end.functionsInfo.increment_k_params()

            token = next(generator)
            type_ = parseType(token)
            back_end.varTable.checkTypeExistence(token)

            if type_:

                token = next(generator)
                parseVarName(token)
                back_end.varTable.addVariable(token, type_, _kind='argument', scope='function')

                token = next(generator)
                comma = parseComma(token)
            else:
                raise CompilerError(PErrorMsg(token).addlarguments())
    back_end.output.endt('parameterList')
    return token

def parseSubroutineBody(generator):
    back_end.output.startt('subroutineBody')
    parseLeftCurly(next(generator))
    token = next(generator)

    # a subroutine body is just variable declarations and statements
    while token.value == 'var':
        token = parseVarDec(token, generator)
    token = parseStatements(token, generator)

    end = parseRightCurly(token)
    if end == False:
        raise CompilerError(PErrorMsg(token).rightcurly())
    back_end.output.endt('subroutineBody')

def parseStatements(token, generator):
    back_end.output.startt('statements')
    
    back_end.DoesFunctionReturnStack.warning_test_init()
    back_end.varTable.Declaration(False)
    
    while token.value != '}':
        back_end.DoesFunctionReturnStack.IFissue_warning(token) # warns if there's unreachable code
        token = parseStatement(token, generator)
        if token == None:
            token = next(generator)
            back_end.DoesFunctionReturnStack.warning_reduc()

    back_end.varTable.Declaration(True)
    back_end.output.endt('statements'); return token

def parseStatement(token, generator):
    if parseLetStatement(token, generator) == False:
        boolORtoken = parseIfStatement(token, generator)
        #   == token, if it was an if statement.
        #   == False, if the parsed statement wasn't an if statement,
        if boolORtoken: 
            return boolORtoken
        else:
            if parseWhileStatement(token, generator) == False:
                if parseDoStatement(token, generator) == False:
                    if parseReturnStatement(token, generator) == False:
                        raise CompilerError(PErrorMsg(token).badstatement())
    return None
        
def parseLetStatement(token, generator):
    if token.value == 'let':
        back_end.output.startt('letStatement'); back_end.output.outt(token)
        token = next(generator)
        parseVarName(token)
        variableToken = token

        token = next(generator)
        array = False
        if token.value == '[':
            array = True
            back_end.output.outt(token)
            token = parseExpression(next(generator), generator)
            if token.value != ']':
                raise CompilerError(PErrorMsg(token).badexpression())

            back_end.CodeProcess.LetStatement_ARRAY_BASE(variableToken)
            back_end.output.outt(token)
            token = next(generator)

        if token.value != '=':
            raise CompilerError(PErrorMsg(token).equals())
        else: back_end.output.outt(token)

        token = parseExpression(next(generator), generator)
        back_end.CodeProcess.LetStatement(array, variableToken)

        end = parseSemicolon(token)
        if end == False:
            raise CompilerError(PErrorMsg(token).semicolon())
        back_end.output.endt('letStatement')

        return True
    else:
        return False

def parseIfStatement(token, generator):
    if token.value == 'if':
        n = back_end.IfWhileIdentifiers.updateIfID()

        back_end.DoesFunctionReturnStack.stack_addIfStmnt()

        back_end.output.startt('ifStatement'); back_end.output.outt(token)
        parseLeftParen(next(generator))
        token = parseExpression(next(generator), generator)
        parseRightParen(token)
        parseLeftCurly(next(generator))

        back_end.CodeProcess.IfStatement_IF(n)

        token = parseStatements(next(generator), generator)
        endbracket = parseRightCurly(token)
        if endbracket == False:
            raise CompilerError(PErrorMsg(token).rightcurly())
        token = next(generator)
        if token.value == 'else':
            back_end.output.outt(token)

            back_end.DoesFunctionReturnStack.stack_addElseStmnt()

            parseLeftCurly(next(generator))
            back_end.CodeProcess.IfStatement_ELSE_A(n)
            token = parseStatements(next(generator), generator)
            back_end.CodeProcess.IfStatement_ELSE_B(n)
            endbracket = parseRightCurly(token)
            if endbracket == False:
                raise CompilerError(PErrorMsg(token).rightcurly())
            token = next(generator)
        else:
            back_end.CodeProcess.IfStatement_NOELSE(n)
        back_end.output.endt('ifStatement'); return token
    return False
    
def parseWhileStatement(token, generator):
    if token.value == 'while':

        n = back_end.IfWhileIdentifiers.updateWhileID()

        back_end.CodeProcess.WhileStatement_1(n)

        back_end.output.startt('whileStatement')
        back_end.output.outt(token)
        parseLeftParen(next(generator))
        token = parseExpression(next(generator), generator)
        parseRightParen(token)

        back_end.CodeProcess.WhileStatement_2(n)

        parseLeftCurly(next(generator))
        token = parseStatements(next(generator), generator)
        endcurly = parseRightCurly(token)
        back_end.CodeProcess.WhileStatement_3(n)

        if endcurly == False:
            raise CompilerError(PErrorMsg(token).endofstatement())
        back_end.output.endt('whileStatement'); return True
    else: return False
    
def parseDoStatement(token, generator):
    if token.value == 'do':
        back_end.output.startt('doStatement'); back_end.output.outt(token)
        token = next(generator)
        token = parseSubroutineCall(token, next(generator), generator, callerexpectsreturnval=False)
        parseSemicolon(token)
        back_end.CodeProcess.DoStatementNULLPOP()
        back_end.output.endt('doStatement')
        return True
    else:
        return False
    
def parseReturnStatement(token, generator):
    if token.value == 'return':        

        back_end.DoesFunctionReturnStack.stack_addReturnStmnt()

        back_end.output.startt('returnStatement'); back_end.output.outt(token)
        token = next(generator)

        back_end.Semantics.checkReturn(token)

        if token.value != ';':
            token = parseExpression(token, generator)
        else:
            back_end.CodeProcess.ReturnStatementVoidPrep(token)
        parseSemicolon(token)

        back_end.CodeProcess.ReturnStatementOutput()
        back_end.output.endt('returnStatement'); return True
    else: return False

def parseExpression(token, generator):
    back_end.output.startt('expression')
    token = parseTerm(token, generator)
    moreterms = parseOp(token)
    while moreterms == True:
        op = token.value
        token = parseTerm(next(generator), generator)
        back_end.CodeProcess.ExpressionOP(op)
        moreterms = parseOp(token)
    back_end.output.endt('expression'); return token


def parseTerm(token, generator):
    back_end.output.startt('term')
    typ = token.typ

    if typ in ['integerConstant', 'stringConstant'] or parseKeywordConstant(token) == True:
    # integerConstant | stringConstant | keywordConstant
        if typ == 'integerConstant':
            back_end.CodeProcess.TermINTEGER(token)
        elif typ == 'stringConstant':
            back_end.CodeProcess.TermSTRING(token)
        else: #== KeywordConstant
            back_end.CodeProcess.TermKEYWORD(token)
        back_end.output.outt(token)
        token = next(generator)
    else:
        lookahead = next(generator)
        if lookahead.value  == ('['):
        # varName `[` expression `]`
            parseVarName(token)
            variableToken = token

            back_end.output.outt(lookahead)
            token = parseExpression(next(generator), generator)
            back_end.CodeProcess.TermARRAY(variableToken)
            if token.value != ']':
                raise CompilerError(PErrorMsg(token).closingsquare())
            else:
                back_end.output.outt(token)
            token = next(generator)
        elif token.typ == 'identifier' and lookahead.value in ('(', '.'):
            # subroutineCall
            token = parseSubroutineCall(token, lookahead, generator, callerexpectsreturnval=True)
        else:
            if token.value in ('~', '-'):
            # unaryOp term
                op = token
                back_end.output.outt(token)
                token = parseTerm(lookahead, generator)
                back_end.CodeProcess.TermUNARYOP(op)
            else:
                try:
                # varName
                    parseVarName(token)
                    variableToken = token
                    back_end.CodeProcess.TermVARNAME(variableToken)
                    token = lookahead
                except CompilerError:
                # `(` expression `)`
                    parseLeftParen(token)
                    token = parseExpression(lookahead, generator)
                    parseRightParen(token)
                    token = next(generator)
    back_end.output.endt('term'); return token


def parseSubroutineCall(token, lookahead, generator, callerexpectsreturnval):
    if lookahead.value == '(':
        subroutinetoken = token
        parseSubroutineName(token)

        back_end.CodeProcess.SubroutineCall_NoDot_A(subroutinetoken, callerexpectsreturnval)

        parseLeftParen(lookahead)
        token, numberofparams = parseExpressionList(generator, methodcall=False)

        back_end.CodeProcess.SubroutineCall_NoDot_B(subroutinetoken, numberofparams)

        parseRightParen(token)
        token = next(generator)
    else:
        worked = parseClassName(token) #parseVarName(token)
        classORvariable = token

        if worked == False:
            return token
        else:
            token = lookahead
            if token.value == '.':
                back_end.output.outt(token)
                subroutinetoken = next(generator)
                parseSubroutineName(subroutinetoken)

                methodcall, function = back_end.CodeProcess.SubroutineCall_WithDot_A(subroutinetoken, classORvariable)

                parseLeftParen(next(generator))
                token, numberofexpressions = parseExpressionList(generator, methodcall)

                back_end.CodeProcess.SubroutineCall_WithDot_B(subroutinetoken, function, numberofexpressions)

                parseRightParen(token)
                token = next(generator)
            else:
                raise CompilerError(PErrorMsg(token).period())
    return token


def parseExpressionList(generator, methodcall):
    back_end.output.startt('expressionList')
    token = next(generator)
    numofexpressions = 0
    if token.value != ')':
        token = parseExpression(token, generator)
        comma = parseComma(token)
        numofexpressions += 1
        while comma == True:
            numofexpressions += 1
            token = parseExpression(next(generator), generator)
            comma = parseComma(token)
    if methodcall: numofexpressions += 1
    back_end.output.endt('expressionList'); return token, numofexpressions

def parseOp(token):
    value = token.value
    if value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
        back_end.output.outt(token); return True
    else: return False

def parseKeywordConstant(token):
    if token.value in ['true', 'false', 'null', 'this']:
        return True
    else: return False

def parseVarDec(token, generator):
# parses varDec, returns the next token, and adds variables to variable table
    back_end.output.startt('varDec'); back_end.output.outt(token)

    token = next(generator)
    type_ = parseType(token)
    back_end.varTable.checkTypeExistence(token)

    token = next(generator)
    parseVarName(token)
    back_end.varTable.addVariable(token, type_, _kind='var', scope='function')

    token = next(generator)
    comma = parseComma(token)

    # _kind=`var' means local variable. We're tallying the number of locals
    while comma == True:
        token = next(generator)
        parseVarName(token)
        back_end.varTable.addVariable(token, type_, _kind='var', scope='function')

        token = next(generator)
        comma = parseComma(token)

    end = parseSemicolon(token)
    if end == False:
        raise CompilerError(PErrorMsg(token).semicolon())
    else: token = next(generator)
    back_end.output.endt('varDec')
    return token

def parseClassName(token):
    if token.typ == 'identifier':
        back_end.output.outt(token)
        return token.value
    else: return False

def parseType(token):
    type_ = token.value
    if type_ in ('int', 'char', 'boolean', 'void'):
    # if type_ in ('int', 'char', 'boolean'):
        back_end.output.outt(token)
        return type_
    else:
        return parseClassName(token)
  
def parseSubroutineName(token):
    if token.typ == 'identifier':
        back_end.output.outt(token)
    else: raise CompilerError(PErrorMsg(token).badidentifier())

def parseVarName(token):
    if 'identifier' == token.typ:
        back_end.output.outt(token)
    else: raise CompilerError(PErrorMsg(token).badidentifier())

def parseLeftCurly(token):
    if token.value == '{':
        ### \/ Updates how far embedded in curly braces we are, for purposes of the FunctionReturnStack
        ###    (which determines whether functions are likely to return
        back_end.DoesFunctionReturnStack.stackvars_incr()

        back_end.output.outt(token)
    else: raise CompilerError(PErrorMsg(token).leftcurly())

def parseRightCurly(token):
    if token.value == '}':
        ### Updates how deeply embedded in curly braces we are
        back_end.DoesFunctionReturnStack.stackvars_decr()
        ### /\
        back_end.output.outt(token); return True
    else: return False

def parseLeftParen(token):
    if token.value == '(':
        back_end.output.outt(token)
    else: raise CompilerError(PErrorMsg(token).leftparen())

def parseRightParen(token):
    if token.value == ')':
        back_end.output.outt(token)
    else: raise CompilerError(PErrorMsg(token).rightparen())

def parseComma(token):
    if token.value == ',':
        back_end.output.outt(token); return True
    else: return False

def parseSemicolon(token):
    if token.value == ';':
        back_end.output.outt(token); return True
    else: return False
