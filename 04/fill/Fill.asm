// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//pseudo code:

// if the value at memory cell keyboard is 0, whiten the whole screen
// if not, blacken the whole screen
// coloring the entire screen is looping over all of the registers and changing them to -1 or 0





(LISTEN)

@KBD
D=M

@WHITEN
D;JEQ

@BLACKEN
0;JMP

(WHITEN)
@SCREEN
D=A
@pointer
M=D

(LOOP_WHITE)

@pointer
A=M
M=0

@pointer
M=M+1
@24576
D=A
@pointer
D=M-D

@LISTEN
D;JEQ

@LOOP_WHITE
0;JMP

(BLACKEN)
@SCREEN
D=A
@pointer
M=D

(LOOP_BLACK)

@pointer
A=M
M=-1

@pointer
M=M+1
@24576
D=A
@pointer
D=M-D

@LISTEN
D;JEQ

@LOOP_BLACK
0;JMP