# Q5 – Fetch-Decode-Execute Trace
**Program:** `Add.asm`

## 1. Objective
To understand how the Hack CPU fetches, decodes, and executes instructions, and how the A register, D register, RAM, and Program Counter (PC) change during execution.

## 2. Program Instructions

| ROM Address | Assembly Instruction | 16-bit Binary Code |
|---|---|---|
| 0 | `@2` | `0000000000000010` |
| 1 | `D=A` | `1110110000010000` |
| 2 | `@3` | `0000000000000011` |
| 3 | `D=D+A` | `1110000010010000` |
| 4 | `@0` | `0000000000000000` |
| 5 | `M=D` | `1110001100001000` |

## 3. Initial CPU State

Before execution, the CPU registers and memory contain:

- A = 0
- D = 0
- PC = 0
- RAM[0] = 0

**Note:** M represents the value stored at the memory address currently held in the A register (M = RAM[A]).

## 4. Fetch-Decode-Execute Process

The CPU executes the first three instructions as follows:

| Step | Fetch (ROM[PC]) | Decode | Execute | A | D | M | PC After |
|---|---|---|---|---:|---:|---:|---:|
| 1 | `0000000000000010` | A-instruction, value = 2 | A ← 2 | 2 | 0 | 0 | 1 |
| 2 | `1110110000010000` | C-instruction; comp = A, dest = D | D ← A = 2 | 2 | 2 | 0 | 2 |
| 3 | `0000000000000011` | A-instruction, value = 3 | A ← 3 | 3 | 2 | 0 | 3 |

### Remaining Instructions

| Step | Instruction | Execution | A | D | M | PC After |
|---|---|---|---:|---:|---:|---:|
| 4 | `D=D+A` | D ← 2 + 3 = 5 | 3 | 5 | 0 | 4 |
| 5 | `@0` | A ← 0 | 0 | 5 | 0 | 5 |
| 6 | `M=D` | RAM[0] ← 5 | 0 | 5 | 5 | 6 |

## 5. Register Trace

The following table shows the CPU state after each instruction:

```text
Step | Instruction      | A | D | M | PC
------------------------------------------------
  1  | 0000000000000010 | 2 | 0 | 0 | 1
  2  | 1110110000010000 | 2 | 2 | 0 | 2
  3  | 0000000000000011 | 3 | 2 | 0 | 3
  4  | 1110000010010000 | 3 | 5 | 0 | 4
  5  | 0000000000000000 | 0 | 5 | 0 | 5
  6  | 1110001100001000 | 0 | 5 | 5 | 6
```

## 6. Final RAM State

After all six instructions are executed:

```text
RAM[0..5] = [5, 0, 0, 0, 0, 0]
```

The final result is stored in RAM[0].

## 7. Conclusion

The Fetch-Decode-Execute cycle was successfully traced for the `Add.asm` program. The CPU loaded 2 into the A register, copied it into the D register, added 3 to obtain 5, and finally stored the result in RAM[0].

**Final Output: RAM[0] = 5**