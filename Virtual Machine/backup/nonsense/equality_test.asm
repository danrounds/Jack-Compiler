// eq        | true if x = y, else false | Equality
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		    //put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
D=M-D     //D=X-Y
@true
D;JEQ
@SP
A=M
M=0
@increment
A;JMP
(true)
@SP
A=M
M=-1
(increment)
@SP
M=M+1	    //final increment