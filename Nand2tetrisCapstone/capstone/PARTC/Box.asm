// Check keyboard input

(START)
    @KBD
    D=M

    @DRAW
    D;JGT

    @CLEAR
    0;JMP

(DRAW)
    @19360
    D=A
    @address
    M=D

    @20
    D=A
    @counter
    M=D

(DRAW_LOOP)
    // Draw first 16 pixels
    @address
    A=M
    M=-1

    // Move to second word
    @address
    M=M+1

    // Draw next 16 pixels
    @address
    A=M
    M=-1

    // Move to the next screen row
    @address
    D=M
    @31
    D=D+A
    @address
    M=D

    // Decrease row counter
    @counter
    M=M-1

    // Continue until all 20 rows are drawn
    D=M
    @DRAW_LOOP
    D;JGT

    // Return to keyboard check after drawing
    @START
    0;JMP


(CLEAR)
    // Starting screen address
    @19360
    D=A
    @address
    M=D

    // 20 rows to clear
    @20
    D=A
    @counter
    M=D


(CLEAR_LOOP)
    // Clear first 16 pixels
    @address
    A=M
    M=0

    // Move to second word
    @address
    M=M+1

    // Clear next 16 pixels
    @address
    A=M
    M=0

    // Move to next screen row
    @address
    D=M
    @31
    D=D+A
    @address
    M=D

    // Decrease counter
    @counter
    M=M-1
    D=M

    @CLEAR_LOOP
    D;JGT

    // Check keyboard again
    @START
    0;JMP