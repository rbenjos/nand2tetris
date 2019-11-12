// we will implement a simple bubble sort, which will always
// run at O(n^2) since it wont stop if no bubbling was performed
// at a single run


// reset the outer loop counter
@i
M=0

(OUTER_LOOP)

    // we will use 2 variables for the addresses of 
	// the elements we want to swap. lets call them x and y
	// and reset them to the first addresses they can get -1
    @R14
    D = M - 1
    @x
    M = D
    @R14
    D = M
    @y
    M = D

	// reset the inner counter to 0
    @j
    M = 0

    // i++
    @R15
    D = M
    @i
    M = M + 1
    D = D - M

    // Go to inner loop
    @LOOP_INNER
    D; JGT

    // End of sorting
    @END
    D; JEQ


(INNER_LOOP)

    // if we are done, we can go back to the outer loop
    @j
    D = M
    @R15
    D = M - D
    D = D - 1
    @OUTER_LOOP
    D; JEQ

    // increment all of our addresses and counters
    @x
    M = M + 1
    @y
    M = M + 1
    @j
    M = M + 1

    // if the first element is bigger than the second
	// we will save their values and swap them
    @x
    A = M
    D = M
	@a
	M=D
	
    @y
    A = M
    D = M
	@b
	M=D
	
	@a
	D=M
	@b
	D=D-M
    @SWAP
    D; JLT

    // start the inner loop again
    @INNER_LOOP
    0; JMP

(SWAP)
	
	// array[x]=b
	// array[y]=a
	
    @b
	D=M
	@x
	A = M
	M=D
	
	@a
	D=M
	@y
	A = M
	M=D

    // back to the inner loop
    @INNER_LOOP
    0; JMP

(END)
    @END
    0; JMP