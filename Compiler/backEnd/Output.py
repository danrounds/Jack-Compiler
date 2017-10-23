class OutputSetup():
    '''Outputs XML or code, depending on the `stage` variable'''
    def __init__(self, stage):
        self.stage = stage
        if stage == 'test':
            self.code = OutputSetup.null
        elif stage == 'initial':
            self.outt = self.startt = self.endt = self.code = OutputSetup.null

    def defineOutputValues(self, stage, output_file_name):
        self.stage = stage
        if stage == 'initial':
            return
        else:
            self.global_file_out = open(output_file_name, 'w')

        if self.stage == 'codeOutput':
            self.code = self.codeoutput

    def closeFile(self):
        if self.stage == 'initial':
            pass
        else:
            self.global_file_out.close()

    # XML output
    def outt(self, token):
        if self.stage == 'test':
            val, tag = token.value, token.typ
            if   val == '<': val = '&lt;'
            elif val == '>': val = '&gt;'
            elif val == '&': val = '&amp;'
            self.global_file_out.write("<%s> %s </%s>\n" % (tag, val, tag))

    def startt(self, tag):
        if self.stage == 'test':
            self.global_file_out.write("<%s>\n" % tag)

    def endt(self, tag):
        if self.stage == 'test':
            self.global_file_out.write("</%s>\n" % tag)

    # Code output
    def codeoutput(self, line_of_code):
        self.global_file_out.write(line_of_code + '\n')

    ###
    def null(*args, **kwargs):
        pass
