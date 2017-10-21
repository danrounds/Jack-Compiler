import globalVars

'''Parse error messages'''
def no_class_declr(self):
    return "Syntax Error: Jack language files begin with a `class` declaration. %s"\
        % globalVars.inputFileName
def no_class_name(self):
    return "Line %s: Expected class name, got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def no_type(self):
    return "Line %s: Expected type, got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def no_semivar(self):
    return "Line %s. Expected more variable names or a semicolon, got '%s'. %s"\
        % (self.line, self.value, globalVars.inputFileName)
def no_varname(self):
    return "Line %s. Expected varName, got semicolon. %s" % \
        (self.line, globalVars.inputFileName)
def no_voidtype(self):
    return "Syntax Error, line %s. Expected `void` or a type, got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def badstatement(self):
    return "Invalid statement type, Line %s. %s" % (self.line, globalVars.inputFileName)
def badexpression(self):
    return "Line %s: Expected expression, got '%s'. %s" % \
        (self.line, self.value, self.value)
def badidentifier(self):
    return "Line %s: Bad Identifier, '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def addlarguments(self):
    return "Line %s: Comma without add'l arguments. %s" % \
        (self.line, globalVars.inputFileName)
def endofstatement(self):
    return "Expected end of statement,`;`, Line %s. %s" % \
        (self.line, globalVars.inputFileName)
def leftparen(self):
    return "Line %s: Expected '(', got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def rightparen(self):
    return "Line %s: Expected ')', got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def leftcurly(self):
    return "Line %s: Expected '}', got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def rightcurly(self):
    return "Line %s: Expected '{', got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def semicolon(self):
    return "Line %s: Expected semicolon, got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def period(self):
    return "Line %s: Expected period, got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def equals(self):
    return "Line %s: Expected '=', got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
def closingsquare(self):
    return "Line %s: Expected closing ']', got '%s'. %s" % \
        (self.line, self.value, globalVars.inputFileName)
