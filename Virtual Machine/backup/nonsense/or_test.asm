// or        | x Or y                    | Bit-wise
//leaves value in area formerly pointed to by sp
@SP
AM=M-1		//decrement sp [stack pointer]
D=M		//put mem.val. pointed to by sp into D (Y)
@SP
AM=M-1
M=M|D		//M=X-Y
@SP
M=M+1		//final increment