class CompilerError(Exception):
    '''Our Exception type for all our compiler's errors.'''
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

