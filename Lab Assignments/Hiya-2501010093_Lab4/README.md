# Lab 4 – Hack Computer Architecture, Status Flags, Memory-Mapped I/O and Toolchain

**Name:** Hiya Adlakha  
**Roll Number:** 2501010093  
**Project Folder:** `Hiya-2501010093_lab4`

---

## Project Structure

```text
Hiya-2501010093_lab4/
│
├── Q1_Q2_waveform/
│   ├── Add.asm
│   ├── Add.hack
│   ├── CPU.hdl
│   ├── Memory.hdl
│   ├── Computer.hdl
│   ├── Computer_Add.tst
│   ├── Computer_Add.out
│   ├── waveform.py
│   └── waveform_add.png
│
├── Q3_flags/
│   ├── Abs.asm
│   ├── Abs.hack
│   ├── Abs.tst
│   ├── Abs.out
│   └── faulty_flag_demo.py
│
├── Q4-mmio/
│   ├── Screen.asm
│   ├── Screen.hack
│   ├── Screen.tst
│   └── Screen.out
│
├── Q5_toolchain/
│   ├── toolchain_diagram.py
│   └── toolchain_diagram.png
│
└── README.md
```

---

# Q1 & Q2 – Computer Architecture, Add Program and Waveform

## 1. Computer Architecture

The Hack Computer consists of three major components connected through `Computer.hdl`.

| Component | Function |
|---|---|
| ROM32K | Stores program instructions and is addressed using the Program Counter (PC). |
| CPU | Fetches, decodes and executes instructions. |
| Memory | Handles data storage and access through the CPU's address output (`addressM`). |

## 2. Hack Instruction Format

The Hack C-instruction follows this 16-bit format:

`111 a cccccc ddd jjj`

- **Bit 15:** Instruction type (0 = A-instruction, 1 = C-instruction).
- **Bit 12 (a):** Selects A or M as the ALU's y-input.
- **Bits 11–6:** ALU control bits (zx, nx, zy, ny, f, no).
- **Bits 5–3:** Destination bits (A, D, M).
- **Bits 2–0:** Jump condition bits (negative, zero, positive).

## 3. Memory Map

| Address Range | Memory Component |
|---|---|
| 0 – 16383 | RAM16K |
| 16384 – 24575 | Screen |
| 24576 | Keyboard |

## 4. Add.asm Program

The program performs addition of two numbers and stores the result in RAM[0].

```asm
@2
D=A
@3
D=D+A
@0
M=D
```

**Expected Result:**

`RAM[0] = 2 + 3 = 5`

## 5. Execution Trace

The `Computer_Add.tst` script executes the program in six cycles.

| Cycle | Instruction | A Register | D Register | RAM[0] |
|---|---|---:|---:|---:|
| 1 | @2 | 2 | 0 | 0 |
| 2 | D=A | 2 | 2 | 0 |
| 3 | @3 | 3 | 2 | 0 |
| 4 | D=D+A | 3 | 5 | 0 |
| 5 | @0 | 0 | 5 | 0 |
| 6 | M=D | 0 | 5 | 5 |

The final value stored in RAM[0] is **5**.

## 6. Fetch–Decode–Execute Timing

### Hack Timing Model

The Hack computer executes one instruction per clock cycle, consisting of a Tick followed by a Tock.

The instruction execution process has three phases:

**1. Fetch**

- ROM32K is combinational.
- As soon as the PC settles at the start of a cycle, the corresponding instruction appears on the instruction bus.
- The instruction is fetched from `ROM[PC]`.

**2. Decode**

- The CPU control logic is combinational.
- Signals `i`, `a`, `c1..c6`, `d1..d3` and `j1..j3` are decoded from the instruction bits.
- Control signals settle after fetching and before the clock edge.

**3. Execute**

- The ALU performs its computation combinationally.
- Results are latched into A, D or RAM at the clock edge.
- A, D, RAM and PC show their updated values after the Tock.
- Execution therefore completes at the end of the cycle.

### Instruction 1: @2

**Cycle:** 1  
**PC:** 0  
**Binary Instruction:** `0000000000000010`

| Phase | Completion Time | What Happens |
|---|---|---|
| Fetch | Start of cycle 1 (t = 0) | `ROM[0]` appears on the instruction bus. |
| Decode | Before the Tick | Bit 15 = 0, so it is an A-instruction. `loadA = 1` and `aIn = instruction`. |
| Execute | End of cycle 1 (t = 1) | `A ← 2` and `PC ← 1`. The trace shows A = 2 at time 1. |

**Explanation:** The instruction loads the constant value 2 into the A register.

### Instruction 2: D=D+A

**Cycle:** 4  
**PC:** 3  
**Binary Instruction:** `1110000010010000`

| Phase | Completion Time | What Happens |
|---|---|---|
| Fetch | Start of cycle 4 (t = 3) | `ROM[3]` appears on the instruction bus. |
| Decode | Before the Tick | `i = 1`, `a = 0` (y = A), `c = 000010` (D + A), `d = 010` (destination D), `j = 000` (no jump). `loadD = 1`. |
| Execute | End of cycle 4 (t = 4) | ALU computes 2 + 3 = 5. `D ← 5` and `PC ← 4`. The trace shows D = 5 at time 4. |

**Explanation:** The ALU adds the values stored in D and A registers and stores the result in D.

### Instruction 3: M=D

**Cycle:** 6  
**PC:** 5  
**Binary Instruction:** `1110001100001000`

| Phase | Completion Time | What Happens |
|---|---|---|
| Fetch | Start of cycle 6 (t = 5) | `ROM[5]` appears on the instruction bus. |
| Decode | Before the Tick | `i = 1`, `a = 0`, `c = 001100` (ALU outputs D), `d = 001` (destination M), `j = 000`. `writeM = 1` and `addressM = 0`. |
| Execute | End of cycle 6 (t = 6) | `outM = 5` is written to RAM[0] at the clock edge. The trace shows `writeM = 1` during the cycle and RAM[0] = 5 at time 6. |

**Explanation:** The value stored in D is written into the memory location selected by the A register, which is address 0.

### Timing Summary

| Instruction | Cycle | Fetch Time | Execute Completion | Final Result |
|---|---:|---:|---:|---|
| @2 | 1 | t = 0 | t = 1 | A = 2 |
| D=D+A | 4 | t = 3 | t = 4 | D = 5 |
| M=D | 6 | t = 5 | t = 6 | RAM[0] = 5 |

**Key Observation:** Fetch and Decode are combinational operations, whereas register and memory updates occur at the clock edge. The updated values become visible after the Tock.

## 7. Waveform Analysis

The Python script `waveform.py` generates an annotated waveform representing the execution of the Add.asm program.

The waveform displays the following signals:

- CLK – Clock signal
- PC – Program Counter
- A – A register
- D – D register
- ALU out – ALU output
- writeM – Memory write signal
- RAM[0] – Stored result

The clock operates through two phases: Tick (high) and Tock (low).

**Output:** `waveform_add.png`

---

# Q3 – Status Flags and Fault Injection

## 1. Absolute Value Program

The `Abs.asm` program calculates the absolute value of the number stored in RAM[0] and saves the result in RAM[1].

```asm
@R0
D=M
@POSITIVE
D;JGE
D=-D
(POSITIVE)
@R1
M=D
(END)
@END
0;JMP
```

**Objective:**

`RAM[1] = |RAM[0]|`

The program uses the ALU's status flags to determine whether the input is negative or non-negative.

## 2. Status Flags

| Flag | Meaning |
|---|---|
| ng | Set to 1 when the ALU output is negative. |
| zr | Set to 1 when the ALU output is zero. |

The `D;JGE` instruction checks whether the value in D is greater than or equal to zero.

- If the value is non-negative, execution jumps to `POSITIVE`.
- If the value is negative, the instruction `D=-D` executes to calculate its positive equivalent.

## 3. Fault Injection

The Python script `faulty_flag_demo.py` simulates a faulty Hack CPU in which the `ng` flag is forced to remain 0 (stuck-at-0 fault).

The jump condition is calculated as:

```python
jump = (j1 AND ng) OR (j2 AND zr) OR (j3 AND NOT ng AND NOT zr)
```

## 4. Test Results

| Input (RAM[0]) | Correct Output | Faulty Output |
|---:|---:|---:|
| -5 | 5 | -5 |
| 7 | 7 | 7 |

**Observation:**

When the `ng` flag is stuck at 0, a negative number is incorrectly treated as non-negative. Consequently, the `JGE` instruction jumps to the `POSITIVE` label, skipping the negation operation.

Positive inputs continue to work correctly because the fault does not affect their execution.

**Conclusion:** The experiment demonstrates how a stuck-at-0 fault in the ALU's negative flag can cause incorrect program execution.

---

# Q4 – Memory-Mapped I/O

## 1. Introduction

Memory-Mapped I/O allows the CPU to interact with hardware devices through specific memory addresses.

In the Hack Computer:

- Keyboard address (`KBD`) = 24576
- Screen address (`SCREEN`) = 16384

## 2. Screen.asm Program

The program continuously checks the keyboard register. When a key is pressed, it writes `-1` to the first screen memory location.

```asm
(LOOP)
@KBD
D=M
@DRAW
D;JNE
@LOOP
0;JMP

(DRAW)
@SCREEN
M=-1
@LOOP
0;JMP
```

## 3. Program Execution

1. The program reads the keyboard register using `@KBD` and `D=M`.
2. It checks whether the keyboard value is non-zero.
3. If no key is pressed, execution returns to `LOOP`.
4. If a key is pressed, execution jumps to `DRAW`.
5. The instruction `M=-1` writes sixteen 1-bits to the first screen memory word.
6. Execution returns to the keyboard-checking loop.

Since `-1` in 16-bit two's complement representation is `1111111111111111`, writing this value blackens the first 16 pixels.

## 4. Test Cases

| Test Case | Keyboard Value (RAM[24576]) | Expected Result |
|---|---:|---|
| No key pressed | 0 | Program continues polling; RAM[16384] remains 0. |
| Key pressed (K) | 75 | Program jumps to DRAW; RAM[16384] becomes -1. |

**Conclusion:** This experiment demonstrates how the Hack Computer interacts with external devices using memory-mapped I/O.

---

# Q5 – Hack Toolchain vs Real Toolchain

## 1. Hack Toolchain

The Hack toolchain converts assembly instructions into machine-readable binary code.

**Execution Flow:**

```text
Prog.asm
   ↓
Assembler
   ↓
Prog.hack (16-bit Binary)
   ↓
Loaded into ROM32K
   ↓
Hack CPU Executes Instructions
```

The assembler performs two major operations:

- Converts symbols into addresses.
- Converts assembly mnemonics into binary instructions.

The resulting `.hack` file contains 16-bit binary instructions that are loaded into ROM32K.

## 2. Real Toolchain (C/Linux)

A real-world C program passes through multiple stages before execution.

**Execution Flow:**

```text
main.c
   ↓
Preprocessor + Compiler
   ↓
main.s (Assembly Code)
   ↓
Assembler
   ↓
main.o (Object File)
   ↓
Linker + Libraries
   ↓
a.out / ELF (Executable)
   ↓
OS Loader
   ↓
Running Process
```

| Component | Function |
|---|---|
| Preprocessor | Processes header files, macros and conditional compilation. |
| Compiler | Converts C source code into assembly language. |
| Assembler | Converts assembly instructions into machine code. |
| Linker | Resolves symbols, handles relocation and combines object files and libraries. |
| OS Loader | Maps the executable into memory, handles dynamic linking and sets up the stack. |
| Running Process | Represents the program during execution. |

The object file (`main.o`) may contain unresolved symbols that are resolved by the linker using other object files and libraries such as `libc.a`.

## 3. Key Differences

| Hack Toolchain | Real Toolchain |
|---|---|
| Starts with assembly code. | Starts with high-level C source code. |
| Uses an assembler directly. | Uses a preprocessor, compiler and assembler. |
| Produces a `.hack` binary file. | Produces object files and an executable. |
| Loads instructions into ROM32K. | Uses an OS loader to map the executable into memory. |
| Uses fixed Hack memory addresses. | Supports relocation, virtual memory and memory protection. |

**Conclusion:** The Hack toolchain is simpler and directly converts assembly code into binary instructions. Real-world toolchains require additional stages such as compilation, linking and loading to support libraries, relocation and operating-system memory management.

---

# How to Run the Project

## 1. Hardware Simulator

Use the Nand2Tetris Hardware Simulator to test the computer architecture and Add program.

1. Open the Hardware Simulator.
2. Load `Q1_Q2_waveform/Computer_Add.tst`.
3. Run the test script.
4. Verify the execution trace and RAM[0] result.

## 2. CPU Emulator

Use the CPU Emulator to execute the assembly programs.

- Q3: `Q3_flags/Abs.tst`
- Q4: `Q4-mmio/Screen.tst`

The test scripts load the corresponding `.hack` files and generate execution traces in `.out` files.

## 3. Reassembling Programs

To regenerate the machine code:

1. Open the Nand2Tetris Assembler.
2. Load the required `.asm` file.
3. Assemble the program.
4. Save the generated `.hack` file in the corresponding folder.

## 4. Running Python Scripts

Python 3 and Matplotlib are required for generating the waveform and toolchain diagram.

Install Matplotlib:

```bash
pip install matplotlib
```

Run the waveform generator:

```bash
cd Q1_Q2_waveform
python waveform.py
```

Run the fault injection demonstration:

```bash
cd Q3_flags
python faulty_flag_demo.py
```

Run the toolchain diagram generator:

```bash
cd Q5_toolchain
python toolchain_diagram.py
```

**Note:** Run `faulty_flag_demo.py` from inside the `Q3_flags` directory because the script reads `Abs.hack` from its current directory.

---

# Overall Conclusion

This lab explores the internal working of the Hack Computer and the process of executing machine instructions. It covers computer architecture, assembly programming, Fetch–Decode–Execute timing, ALU status flags, fault injection, memory-mapped I/O and the comparison between Hack and real-world software toolchains.

Through these experiments, the relationship between assembly instructions, hardware components, clock cycles, memory operations and program execution becomes clearer.