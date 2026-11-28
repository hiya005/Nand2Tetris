// Computer_Add.tst: traces Add.hack for 6 cycles
load Computer.hdl,
output-file Computer_Add.out,
output-list time%S1.4.1 pc[]%D1.3.1 instruction[]%B1.16.1 addressM[]%D1.3.1 outM[]%D1.6.1 writeM%B1.1.1;

ROM32K load Add.hack,
output;

repeat 6 {
  tick, output;
  tock, output;
}