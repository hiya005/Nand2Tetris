// Draws a rectangle at the top-left corner of the screen.
// R0 contains the rectangle height.
// Each screen word represents 16 horizontal pixels.

    @R0
    D=M
    @counter
    M=D

    @SCREEN
    D=A
    @address
    M=D

(LOOP)
    @counter
    D=M
    @END
    D;JEQ

    @address
    A=M
    M=-1

    @address
    M=M+1

    @counter
    M=M-1

    @LOOP
    0;JMP

(END)
    @END
    0;JMP