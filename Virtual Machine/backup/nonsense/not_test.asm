// not       | Not y                     | Bit-wise
@SP
AM=M-1		//decrement sp [stack pointer]
M=!M		//put mem.val. pointed to by sp into D (Y)
@SP
M=M+1		//final increment