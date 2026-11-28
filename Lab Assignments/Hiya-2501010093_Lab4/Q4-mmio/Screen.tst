// Screen.tst: keyboard read and screen write
load Screen.hack,
output-file Screen.out,
output-list time%S1.4.1 PC%D1.3.1 A%D1.6.1 D%D1.6.1 RAM[24576]%D1.6.1 RAM[16384]%D1.6.1;

// Case 1: no key pressed, the program just polls
set RAM[24576] 0,
repeat 6 {
  ticktock;
  output;
}

// Case 2: a key is pressed (75 = 'K'), the program draws
set RAM[24576] 75,
repeat 8 {
  ticktock;
  output;
}