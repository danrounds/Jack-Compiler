import globalVars


"""Parse error messages"""
def noClassName(token):
    return 'Line %s: Expected class name, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def noClassDeclr(token):
    return 'Syntax Error: Jack language files begin with a `class` declaration. %s'\
        % globalVars.inputFileName


def expectedType(token):
    return 'Line %s: Expected type, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedSemiOrVariable(token):
    return 'Line %s. Expected more variable names or a semicolon, got `%s`. %s'\
        % (token.line, token.value, globalVars.inputFileName)


def expectedVarName(token):
    return 'Line %s. Expected varName, got semicolon. %s' % \
        (token.line, globalVars.inputFileName)


def expectedVoidOrType(token):
    return 'Syntax Error, line %s. Expected `void` or a type, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def badStatement(token):
    return 'Invalid statement type, Line %s. %s' % \
        (token.line, globalVars.inputFileName)


def badExpression(token):
    return 'Line %s: Expected expression, got `%s`. %s' % \
        (token.line, token.value, token.value)


def badIdentifier(token):
    return 'Line %s: Bad Identifier, `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedAddlArguments(token):
    return 'Line %s: Comma without add\'l arguments. %s' % \
        (token.line, globalVars.inputFileName)


def expectedEndOfStatement(token):
    return 'Expected end of statement,`;`, Line %s. %s' % \
        (token.line, globalVars.inputFileName)


def expectedLeftParen(token):
    return 'Line %s: Expected `(`, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedRightParen(token):
    return 'Line %s: Expected `)`, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedLeftCurly(token):
    return 'Line %s: Expected `}`, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedRightCurly(token):
    return 'Line %s: Expected `{`, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedSemicolon(token):
    return 'Line %s: Expected semicolon, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedPeriod(token):
    return 'Line %s: Expected period, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedEquals(token):
    return 'Line %s: Expected `=`, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedClosingSquare(token):
    return 'Line %s: Expected closing `]`, got `%s`. %s' % \
        (token.line, token.value, globalVars.inputFileName)


def expectedEndOfFile(token):
    return 'Expected end of file. Line %s, %s' % \
        (token.line, globalVars.inputFileName)
