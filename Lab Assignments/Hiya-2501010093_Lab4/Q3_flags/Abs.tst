// Abs.tst: runs Abs.hack for x = -5 and then x = 7
load Abs.hack,
output-file Abs.out,
output-list time%S1.4.1 PC%D1.3.1 A%D1.6.1 D%D1.6.1 RAM[0]%D1.6.1 RAM[1]%D1.6.1;

// Case 1: negative input, JGE must NOT jump
set RAM[0] -5,
repeat 8 {
  ticktock;
  output;
}

// Case 2: positive input, JGE must jump
set PC 0,
set RAM[0] 7,
set RAM[1] 0,
repeat 8 {
  ticktock;
  output;
}