###############################################################################
# Parser for the Jack compiler, tECS
#
# I've treated this file as largely self-documenting (since the functions are
# all named  according to function). Each parse function passes and accepts our
# token generator and/or specific tokens.
#
# On the first parse, our parse functions call the `backEnd' to construct our
# varTable and functionInfo table (including our listOfExtendedTypes -- i.e.
# the user-defined types we find while parsing).
#
# On the second parse, we call `backEnd', and use this information to check
# semantics and output code.
# -DR, August 2016

from CompilerError import CompilerError
from . import parserErrors as PErrorMsg
from . import uniqueIfAndWhileIds
import backEnd.processCode as backEnd
import backEnd.setGlobals as setGlobals
import backEnd.doesFunctionReturn as doesFunctionReturn
import backEnd.returnSemantics as returnSemantics


def initializeTagOutput(_output):
    """
    The main loop passes our output object to the parser, so that we can
    write out XML tags for parser/lexer tests (when applicable)
    """
    global tagOutput
    tagOutput = _output

# PARSER ####    #### PARSER ####    #### PARSER ####    #### PARSER ####
# Everything below is our parser.


def parseClass(generator):
    """
    Initial parse function. Each file holds a class, thus the `class` is the
    main unit of compilation
    """
    uniqueIfAndWhileIds.init()
    doesFunctionReturn.stackVarsInit()
    token = next(generator)
    if token.value == 'class':
        tagOutput.startt('class'); tagOutput.outt(token)
        token = next(generator)
        if parseClassName(token) is False:
            raise CompilerError(PErrorMsg.no_class_name(token))
        setGlobals(currentClass=token)
        parseLeftCurly(next(generator))
        token = next(generator)
        isCurly = parseRightCurly(token)
        if isCurly is False:

            # Here, we're parsing field & static vars + keeping a count
            backEnd.varTable.resetFieldStaticCount()
            backEnd.varTable.setInDeclaration(True)
            moreClassVarDecd = parseClassVarDec(token, generator)
            while moreClassVarDecd is True:
                moreClassVarDecd = parseClassVarDec(next(generator), generator)
            # Now we know the n fields that Class defines for its object type:
            backEnd.functionsInfo.setFieldN()

            # Time to parse subroutines:
            moreSubroutineDeclared = parseSubroutineDec(moreClassVarDecd, generator)
            while moreSubroutineDeclared is True:
                moreSubroutineDeclared = parseSubroutineDec(None, generator)
            rightcurly = parseRightCurly(moreSubroutineDeclared)
            if rightcurly is False:
                raise CompilerError(PErrorMsg.rightcurly(token))

            backEnd.varTable.addToAvailableTypes()

            tagOutput.endt('class')
            try:
                next(generator)
            except:
                pass
            else:
                ## CLEAN UP
                raise CompilerError("Expected end of file. Line %s" % token.line)
                ## CLEAN UP
    else:
        raise CompilerError(PErrorMsg.no_class_declr(token))


def parseClassVarDec(token, generator):
    '''Returns True if thing parsed is of the form classVarDec,
    Returns token if it plainly isn't,
    Raises CompilerError if things are badly formed.'''
    if token.value in ('static', 'field'):

        kind = token.value
        tagOutput.startt('classVarDec'); tagOutput.outt(token)

        token = next(generator)
        type_ = parseType(token)
        backEnd.varTable.checkTypeExistence(token)

        if not type_:
            raise CompilerError(PErrorMsg.no_type(token))

        token = next(generator)
        parseVarName(token)
        backEnd.varTable.addVariable(token, type_, kind, scope='class')
        
        token = next(generator)
        comma = parseComma(token)
        while comma is True:

            token = next(generator)
            parseVarName(token)
            backEnd.varTable.addVariable(token, type_, kind, scope='class')

            semi = parseSemicolon(token)
            if semi is False:
                token = next(generator)
                comma = parseComma(token)
            else:
                raise CompilerError(PErrorMsg.no_varname(token))

        if parseSemicolon(token) is True:
            tagOutput.endt('classVarDec'); return True
        else:
            raise CompilerError(PErrorMsg.no_semivar(token))
    else: return token


def parseSubroutineDec(token, generator):
    if token is None: token = next(generator)
    setGlobals(currentFnType=token)
    if token.value in ('constructor', 'function', 'method'):

        doesFunctionReturn.stackInit()
        # \/ Sets an initial value for `k' parameters

        backEnd.functionsInfo.initKParams()
        tagOutput.startt('subroutineDec'); tagOutput.outt(token)

        token = next(generator)

        # if getattr(token, 'value') == 'void':
        #     tagOutput.outt(token); returnTyp = 'void'
        # elif parseType(token):
        #     returnTyp = getattr(token, 'value')
        # else:

        if parseType(token):
            backEnd.varTable.checkTypeExistence(token, subroutineDeclaration=True)
            returnTyp = token.value
        else:
            raise CompilerError(PErrorMsg.no_voidtype(token))

        subroutineToken = next(generator)
        parseSubroutineName(subroutineToken)
        setGlobals(currentFn=subroutineToken)

        backEnd.SubroutineDeclaration(token)

        parseLeftParen(next(generator))
        backEnd.varTable.resetVarCounter()  # Resets `localVarN' declared
        token = parseParameterList(generator)  # Figures out our `k' parameters
        parseRightParen(token)

        parseSubroutineBody(generator)

        doesFunctionReturn.codeCheck(subroutineToken)
        # Checks whether the code in the this subroutine will actually return

        backEnd.functionsInfo.addFunction(returnTyp, subroutineToken)
        # @ this point, variableTable.localVarN contains the total n of local
        # variables declared in the current function

        tagOutput.endt('subroutineDec'); return True
    else: return token


def parseParameterList(generator):
    '''
    Returns a token--either after evaluating `type varName` (',' `type varName`)
    or after finding nothing of that form. Returned token should be a '(', else
    calling function will grind to a halt
    '''

    tagOutput.startt('parameterList')

    token = next(generator)
    type_ = parseType(token)

    if type_:
        backEnd.varTable.checkTypeExistence(token)

        token = next(generator)
        parseVarName(token)
        backEnd.varTable.addVariable(token, type_, kind='argument', scope='function')

        token = next(generator)
        backEnd.functionsInfo.incrementKParams()
        comma = parseComma(token)

        # \/ Tallying the number of argument variables in our fn declarations:
        while comma is True:
            backEnd.functionsInfo.incrementKParams()

            token = next(generator)
            type_ = parseType(token)
            backEnd.varTable.checkTypeExistence(token)

            if type_:

                token = next(generator)
                parseVarName(token)
                backEnd.varTable.addVariable(token, type_, kind='argument', scope='function')

                token = next(generator)
                comma = parseComma(token)
            else:
                raise CompilerError(PErrorMsg.addlarguments(token))
    tagOutput.endt('parameterList')
    return token


def parseSubroutineBody(generator):
    tagOutput.startt('subroutineBody')
    parseLeftCurly(next(generator))
    token = next(generator)

    # a subroutine body is just variable declarations and statements
    while token.value == 'var':
        token = parseVarDec(token, generator)
    token = parseStatements(token, generator)

    end = parseRightCurly(token)
    if end is False:
        raise CompilerError(PErrorMsg.rightcurly(token))
    tagOutput.endt('subroutineBody')


def parseStatements(token, generator):
    tagOutput.startt('statements')

    doesFunctionReturn.warningTestInit()
    backEnd.varTable.setInDeclaration(False)

    while token.value != '}':
        doesFunctionReturn.IFissueWarning(token)  # Warns of unreachable code
        token = parseStatement(token, generator)
        if token is None:
            token = next(generator)
            doesFunctionReturn.warningReduc()

    backEnd.varTable.setInDeclaration(True)
    tagOutput.endt('statements'); return token


def parseStatement(token, generator):
    if parseLetStatement(token, generator) is False:
        boolORtoken = parseIfStatement(token, generator)
        #   == token, if it was an if statement.
        #   == False, if the parsed statement wasn't an if statement,
        if boolORtoken:
            return boolORtoken
        else:
            if parseWhileStatement(token, generator) is False:
                if parseDoStatement(token, generator) is False:
                    if parseReturnStatement(token, generator) is False:
                        raise CompilerError(PErrorMsg.badstatement(token))
    return None


def parseLetStatement(token, generator):
    if token.value == 'let':
        tagOutput.startt('letStatement'); tagOutput.outt(token)
        token = next(generator)
        parseVarName(token)
        variableToken = token

        token = next(generator)
        array = False
        if token.value == '[':
            array = True
            tagOutput.outt(token)
            token = parseExpression(next(generator), generator)
            if token.value != ']':
                raise CompilerError(PErrorMsg.badexpression(token))

            backEnd.LetStatement_ARRAY_BASE(variableToken)
            tagOutput.outt(token)
            token = next(generator)

        if token.value != '=':
            raise CompilerError(PErrorMsg.equals(token))
        else: tagOutput.outt(token)

        token = parseExpression(next(generator), generator)
        backEnd.LetStatement(array, variableToken)

        end = parseSemicolon(token)
        if end is False:
            raise CompilerError(PErrorMsg.semicolon(token))
        tagOutput.endt('letStatement')

        return True
    else:
        return False


def parseIfStatement(token, generator):
    if token.value == 'if':
        n = uniqueIfAndWhileIds.getIfID()

        doesFunctionReturn.stackAddIfStmnt()

        tagOutput.startt('ifStatement'); tagOutput.outt(token)
        parseLeftParen(next(generator))
        token = parseExpression(next(generator), generator)
        parseRightParen(token)
        parseLeftCurly(next(generator))

        backEnd.IfStatement_IF(n)

        token = parseStatements(next(generator), generator)
        endbracket = parseRightCurly(token)
        if endbracket is False:
            raise CompilerError(PErrorMsg.rightcurly(token))
        token = next(generator)
        if token.value == 'else':
            tagOutput.outt(token)

            doesFunctionReturn.stackAddElseStmnt()

            parseLeftCurly(next(generator))
            backEnd.IfStatement_ELSE_A(n)
            token = parseStatements(next(generator), generator)
            backEnd.IfStatement_ELSE_B(n)
            endbracket = parseRightCurly(token)
            if endbracket is False:
                raise CompilerError(PErrorMsg.rightcurly(token))
            token = next(generator)
        else:
            backEnd.IfStatement_NOELSE(n)
        tagOutput.endt('ifStatement'); return token
    return False


def parseWhileStatement(token, generator):
    if token.value == 'while':

        n = uniqueIfAndWhileIds.getWhileID()

        backEnd.WhileStatement_1(n)

        tagOutput.startt('whileStatement')
        tagOutput.outt(token)
        parseLeftParen(next(generator))
        token = parseExpression(next(generator), generator)
        parseRightParen(token)

        backEnd.WhileStatement_2(n)

        parseLeftCurly(next(generator))
        token = parseStatements(next(generator), generator)
        endcurly = parseRightCurly(token)
        backEnd.WhileStatement_3(n)

        if endcurly is False:
            raise CompilerError(PErrorMsg.endofstatement(token))
        tagOutput.endt('whileStatement'); return True
    else: return False


def parseDoStatement(token, generator):
    if token.value == 'do':
        tagOutput.startt('doStatement'); tagOutput.outt(token)
        token = next(generator)
        token = parseSubroutineCall(token, next(generator), generator, callerExpectsReturnVal=False)
        parseSemicolon(token)
        backEnd.DoStatementNULLPOP()
        tagOutput.endt('doStatement')
        return True
    else:
        return False
    
def parseReturnStatement(token, generator):
    if token.value == 'return':        

        doesFunctionReturn.stackAddReturnStmnt()

        tagOutput.startt('returnStatement'); tagOutput.outt(token)
        token = next(generator)

        returnSemantics.checkReturn(token)

        if token.value != ';':
            token = parseExpression(token, generator)
        else:
            backEnd.ReturnStatementVoidPrep(token)
        parseSemicolon(token)

        backEnd.ReturnStatementOutput()
        tagOutput.endt('returnStatement'); return True
    else: return False


def parseExpression(token, generator):
    tagOutput.startt('expression')
    token = parseTerm(token, generator)
    moreterms = parseOp(token)
    while moreterms is True:
        op = token.value
        token = parseTerm(next(generator), generator)
        backEnd.ExpressionOP(op)
        moreterms = parseOp(token)
    tagOutput.endt('expression'); return token


def parseTerm(token, generator):
    tagOutput.startt('term')
    typ = token.typ

    if typ in ['integerConstant', 'stringConstant'] or parseKeywordConstant(token) is True:
        # integerConstant | stringConstant | keywordConstant
        if typ == 'integerConstant':
            backEnd.TermINTEGER(token)
        elif typ == 'stringConstant':
            backEnd.TermSTRING(token)
        else:  #== KeywordConstant
            backEnd.TermKEYWORD(token)
        tagOutput.outt(token)
        token = next(generator)
    else:
        lookahead = next(generator)
        if lookahead.value == ('['):
            # varName `[` expression `]`
            parseVarName(token)
            variableToken = token

            tagOutput.outt(lookahead)
            token = parseExpression(next(generator), generator)
            backEnd.TermARRAY(variableToken)
            if token.value != ']':
                raise CompilerError(PErrorMsg.closingsquare(token))
            else:
                tagOutput.outt(token)
            token = next(generator)
        elif token.typ == 'identifier' and lookahead.value in ('(', '.'):
            # subroutineCall
            token = parseSubroutineCall(token, lookahead, generator, callerExpectsReturnVal=True)
        else:
            if token.value in ('~', '-'):
                # unaryOp term
                op = token
                tagOutput.outt(token)
                token = parseTerm(lookahead, generator)
                backEnd.TermUNARYOP(op)
            else:
                try:
                    # varName
                    parseVarName(token)
                    variableToken = token
                    backEnd.TermVARNAME(variableToken)
                    token = lookahead
                except CompilerError:
                    # `(` expression `)`
                    parseLeftParen(token)
                    token = parseExpression(lookahead, generator)
                    parseRightParen(token)
                    token = next(generator)
    tagOutput.endt('term'); return token


def parseSubroutineCall(token, lookahead, generator, callerExpectsReturnVal):
    if lookahead.value == '(':
        subroutineToken = token
        parseSubroutineName(token)

        calledFunctRole = returnSemantics.checkDotlessFunctionCall(subroutineToken, callerExpectsReturnVal)
        backEnd.SubroutineCall_NoDot_A(calledFunctRole)

        parseLeftParen(lookahead)
        token, numberOfParams = parseExpressionList(generator, methodCall=False)

        backEnd.SubroutineCall_NoDot_B(subroutineToken, numberOfParams)

        parseRightParen(token)
        token = next(generator)
    else:
        worked = parseClassName(token)  # parseVarName(token)
        classOrObject = token

        if worked is False:
            return token
        else:
            token = lookahead
            if token.value == '.':
                tagOutput.outt(token)
                subroutineToken = next(generator)
                parseSubroutineName(subroutineToken)

                methodCall, fn = backEnd.SubroutineCall_WithDot_A(subroutineToken, classOrObject)

                parseLeftParen(next(generator))
                token, numberOfExprs = parseExpressionList(generator, methodCall)

                backEnd.SubroutineCall_WithDot_B(subroutineToken, fn, numberOfExprs)

                parseRightParen(token)
                token = next(generator)
            else:
                raise CompilerError(PErrorMsg.period(token))
    return token


def parseExpressionList(generator, methodCall):
    tagOutput.startt('expressionList')
    token = next(generator)
    numofexpressions = 0
    if token.value != ')':
        token = parseExpression(token, generator)
        comma = parseComma(token)
        numofexpressions += 1
        while comma is True:
            numofexpressions += 1
            token = parseExpression(next(generator), generator)
            comma = parseComma(token)
    if methodCall: numofexpressions += 1
    tagOutput.endt('expressionList'); return token, numofexpressions


def parseOp(token):
    value = token.value
    if value in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
        tagOutput.outt(token); return True
    else: return False


def parseKeywordConstant(token):
    if token.value in ['true', 'false', 'null', 'this']:
        return True
    else: return False


def parseVarDec(token, generator):
    # Parses varDec, returns next token, and adds variables to variable table
    tagOutput.startt('varDec'); tagOutput.outt(token)

    token = next(generator)
    type_ = parseType(token)
    backEnd.varTable.checkTypeExistence(token)

    token = next(generator)
    parseVarName(token)
    backEnd.varTable.addVariable(token, type_, kind='var', scope='function')

    token = next(generator)
    comma = parseComma(token)

    # kind=`var' means local variable. We're tallying the number of locals
    while comma is True:
        token = next(generator)
        parseVarName(token)
        backEnd.varTable.addVariable(token, type_, kind='var', scope='function')

        token = next(generator)
        comma = parseComma(token)

    end = parseSemicolon(token)
    if end is False:
        raise CompilerError(PErrorMsg.semicolon(token))
    else: token = next(generator)
    tagOutput.endt('varDec')
    return token


def parseClassName(token):
    if token.typ == 'identifier':
        tagOutput.outt(token)
        return token.value
    else: return False


def parseType(token):
    type_ = token.value
    if type_ in ('int', 'char', 'boolean', 'void'):
        tagOutput.outt(token)
        return type_
    else:
        return parseClassName(token)

def parseSubroutineName(token):
    if token.typ == 'identifier':
        tagOutput.outt(token)
    else: raise CompilerError(PErrorMsg.badidentifier(token))


def parseVarName(token):
    if 'identifier' == token.typ:
        tagOutput.outt(token)
    else: raise CompilerError(PErrorMsg.badidentifier(token))


def parseLeftCurly(token):
    if token.value == '{':
        # \/ Updates how far embedded in curly braces we are, for purposes of
        # FunctionReturnStack,which determines whether fns are likely to return
        doesFunctionReturn.stackVarsIncr()

        tagOutput.outt(token)
    else: raise CompilerError(PErrorMsg.leftcurly(token))


def parseRightCurly(token):
    if token.value == '}':
        # \/ Updates how deeply embedded in curly braces we are
        doesFunctionReturn.stackVarsDecr()
        # /\
        tagOutput.outt(token); return True
    else: return False


def parseLeftParen(token):
    if token.value == '(':
        tagOutput.outt(token)
    else: raise CompilerError(PErrorMsg.leftparen(token))


def parseRightParen(token):
    if token.value == ')':
        tagOutput.outt(token)
    else: raise CompilerError(PErrorMsg.rightparen(token))


def parseComma(token):
    if token.value == ',':
        tagOutput.outt(token); return True
    else: return False


def parseSemicolon(token):
    if token.value == ';':
        tagOutput.outt(token); return True
    else: return False
