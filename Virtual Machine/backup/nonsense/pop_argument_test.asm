//@offset_n	//replace with string operation in python
//pop argument 3


//@257		//
//D=A		//test values
//@SP		//			//SP should be 256
//M=D		//
//@5000
//D=A
//@ARG					//ARG should point to 5000
//M=D	



//@offset_n	//replace with string operation in python
//D=A


//general pop, for `pop name_of_register n;   n != 0
@3		//replace with string operation in python
D=A	/// <<< /\ THESE FIRST TWO LINES ARE OPT. WHEN offset is 0
@THIS
D=M+D
@R13
M=D			//NAMEOFREGISTER =
@SP			//
AM=M-1			//
D=M			//
@R13			//
A=M			//temp := R5 - R12
M=D			//pointer (special cases, below)