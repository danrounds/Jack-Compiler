// neg       |-y                         | Arithmetic negation (2's complement)
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
M=!M
M=M+1
@SP
M=M+1