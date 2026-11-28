# faulty_flag_demo.py: run Abs.hack with correct and faulty ng flag
rom = [l.strip() for l in open("Abs.hack") if l.strip()]

def run(x, ng_stuck_zero=False):
    ram = {0: x, 1: 0}
    A = D = pc = 0
    for _ in range(20):
        if pc >= len(rom):
            break
        ins = rom[pc]
        if ins[0] == "0":                      # A-instruction
            A = int(ins, 2)
            pc += 1
            continue
        y = ram.get(A, 0) if ins[3] == "1" else A
        comp = {"110000": y, "001100": D, "001111": -D, "101010": 0}[ins[4:10]]
        zr = (comp == 0)
        ng = (comp < 0) and not ng_stuck_zero  # fault injected here
        j1, j2, j3 = ins[13] == "1", ins[14] == "1", ins[15] == "1"
        jump = (j1 and ng) or (j2 and zr) or (j3 and not ng and not zr)
        target = A                             # jump goes to the old A
        if ins[12] == "1":
            ram[A] = comp
        if ins[11] == "1":
            D = comp
        if ins[10] == "1":
            A = comp
        pc = target if jump else pc + 1
    return ram[1]

for x in (-5, 7):
    print(f"x={x:3d}  correct -> {run(x)}   ng stuck at 0 -> {run(x, True)}")