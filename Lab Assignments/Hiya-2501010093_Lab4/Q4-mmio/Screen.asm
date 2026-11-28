// Screen.asm: if any key is pressed, blacken the first 16 pixels of the screen
(LOOP)
@KBD
D=M          // D = keyboard register (RAM[24576])
@DRAW
D;JNE        // key pressed (D != 0): go to DRAW
@LOOP
0;JMP        // no key: keep polling
(DRAW)
@SCREEN
M=-1         // RAM[16384] = 1111111111111111 (16 black pixels)
@LOOP
0;JMP