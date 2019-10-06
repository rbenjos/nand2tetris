// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// pseudo code:


// we can repeatadly add one of the numbers to itself and decrement from the other until it reaches 1


 
//while(RAM[1]!=1)
//{
//RAM[0] += RAM[0];
//RAM[1] -= 1;
//} 
//

// code:

@R2
M=0

(LOOP)
@R0
D=M

@R2
M=M+D

@R1
M=M-1
D=M
@END
D;JEQ
@LOOP
0;JMP

(END)
@END
0;JMP
