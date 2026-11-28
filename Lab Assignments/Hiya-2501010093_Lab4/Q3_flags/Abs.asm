// Abs.asm: RAM[1] = |RAM[0]|
@R0
D=M          // D = x
@POSITIVE
D;JGE        // if x >= 0, skip negation (uses ng flag)
D=-D         // x < 0, so negate
(POSITIVE)
@R1
M=D          // RAM[1] = |x|
(END)
@END
0;JMP