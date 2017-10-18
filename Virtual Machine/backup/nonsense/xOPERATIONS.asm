// add       | x + y                     | Integer addition (2's complement)
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		//put mem.val. pointed to by sp into D
@SP
AM=M-1
M=M+D



// sub       | x - y                     | Integer subtraction (2's complement)
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		//put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
M=M-D		//M=X-Y
@SP
M=M+1		//final increment



// neg       |-y                         | Arithmetic negation (2's complement)
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
M=!M
M=M+1
@SP
M=M+1



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



// gt        | true if x > y, else false | Greater than
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		    //put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
D=M-D     //D=X-Y
@true
D;JGT
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



// lt        | true if x < y, else false | Less than
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		    //put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
D=M-D     //D=X-Y
@true
D;JLT
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



// and       | x And y                   | Bit-wise
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		//put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
M=M&D		//M=X&Y
@SP
M=M+1		//final increment



// or        | x Or y                    | Bit-wise
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		//put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
M=M|D		//M=X|Y
@SP
M=M+1		//final increment



// not       | Not y                     | Bit-wise
@SP
AM=M-1		//decrement sp [stack pointer]
M=!M		//put mem.val. pointed to by sp into D (Y)
@SP
M=M+1		//final increment
