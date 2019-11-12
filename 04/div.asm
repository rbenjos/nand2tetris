// algorithm:

// R13/R14
// R13
// R14
// R15 = 0
// counter = 0

// while R14<R13 : 
// R14<<;
// counter ++

// R14>>;
// counter

//	while counter > -1
// {
//		R14<<2;
//		R15 >> 2
//		counter --;
//		while(R14<R13)
// 		{
//  		R13 -= R14;
//  		R15 ++;}
// 		}
// }
// return R15

@R15
M=0
@counter
M=0

//initializing loop

(INIT_LOOP)
// the if at the begining of the while
@R14
D=M
@R13
D=D-M
@OUTER_LOOP
D;JGT

@R14
M=M<<
@counter
M=M+1
@INIT_LOOP
0;JEQ

(OUTER_LOOP)
// while counter > -1
@counter
D=M
@END
D;JLE

@R14
M=M>>
@R15
M=M<<
@counter
M=M-1

(INNER_LOOP)
// while R14<R13
@R14
D=M
@R13
D=D-M
@OUTER_LOOP
D;JGT
@R14
D=M
@R13
M=M-D
@R15
M=M+1
@INNER_LOOP
0;JEQ

(END)
@END
0;JMP


