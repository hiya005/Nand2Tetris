@0
M=0

@1
M=1

(LOOP)
@1
D=M

@6
D=D-A

@END
D;JGE

@1
D=M

@0
M=D+M

@1
M=M+1

@LOOP
0;JMP

(END)
@END
0;JMP
