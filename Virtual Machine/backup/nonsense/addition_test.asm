// add       | x + y                     | Integer addition (2's complement)

@SP
AM=M-1		//decrement sp [stack pointer]
D=M		//put mem.val. pointed to by sp into D
@SP
AM=M-1
M=M+D