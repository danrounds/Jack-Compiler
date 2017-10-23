import sys

class Output(object):
    """
    Wrapper for a file object. We do all our output through an instance of this
    class. If we instantialize our object with the path to a file
     [i.e., instance = Output('this/is/a/file')], output goes to that file.

    If we don't (i.e. we pass it no value--instance = Output(None), output
    defaults to STDOUT, AND keeps a tally of the number of operations we
    output. This is purely for purposes of the interpreter.

    Dynamically-defined method:
       out(string)
         This is raison d'être of the entire class. We use it for all of our
         ...output.
    """

    def __init__(self, filename=None):
        """Defines instance.out(string) -- the output method"""
        if filename is not None:
            # file
            self.fileobject = open(filename, 'w')
            self.out = self.fileobject.write
        else:
            # STDOUT + bookkeeping
            self.out = self.interpreterOutput
            self.N_INSTRUCTIONS = 0

    def close(self):
        """
        Closes our file object. This is unnecessary, if you're simply using
        STDOUT (i.e. if you're using our interpreter).
        """
        self.fileobject.close()

    def interpreterOutput(self, line):
        """
        Output function for the interpreter. Tracks the number of instructions
        we output
        """
        instructions = line.split()   # Just counting any line that
        n = len(instructions)         # isn't a (goto_label) --
        for i in instructions:        # remember that labels are
            if i[0] == '(':           # pseudo instructions
                n -= 1                # ..
        self.N_INSTRUCTIONS += n      # .
        sys.stdout.write(line)
######
