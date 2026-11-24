
import sys
import os


# ------------------------------------------
# PASS 1: CLEAN ASSEMBLY AND IDENTIFY LABELS
# ------------------------------------------

def clean_assembly(filename):
    """Remove comments and blank lines from an assembly file."""
    instructions = []

    with open(filename, "r") as file:
        for line in file:
            line = line.split("//")[0].strip()

            if line:
                instructions.append(line)

    return instructions


def first_pass(instructions):
    """Identify labels and store their ROM addresses."""
    labels = {}
    rom_address = 0

    for instruction in instructions:
        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]
            labels[label] = rom_address
        else:
            rom_address += 1

    return labels


# ------------------------------------------
# HACK ASSEMBLY SYMBOL TABLES
# ------------------------------------------

PREDEFINED_SYMBOLS = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

for i in range(16):
    PREDEFINED_SYMBOLS[f"R{i}"] = i


DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "DM": "011",
    "A": "100",
    "AM": "101",
    "MA": "101",
    "AD": "110",
    "DA": "110",
    "AMD": "111",
    "ADM": "111",
    "MAD": "111",
    "MDA": "111",
    "DAM": "111",
    "DMA": "111"
}


COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}


JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


# ------------------------------------------
# PASS 2: TRANSLATE ASSEMBLY INTO MACHINE CODE
# ------------------------------------------

def second_pass(instructions, labels):
    """Translate A-instructions and C-instructions into binary."""

    symbols = PREDEFINED_SYMBOLS.copy()
    symbols.update(labels)

    machine_code = []
    next_variable_address = 16

    for instruction in instructions:

        # Skip label declarations
        if instruction.startswith("(") and instruction.endswith(")"):
            continue

        # A-instruction
        if instruction.startswith("@"):
            symbol = instruction[1:]

            if symbol.isdigit():
                address = int(symbol)

            else:
                if symbol not in symbols:
                    symbols[symbol] = next_variable_address
                    next_variable_address += 1

                address = symbols[symbol]

            if not 0 <= address <= 32767:
                raise ValueError(f"Invalid address: {address}")

            binary = format(address, "016b")
            machine_code.append(binary)

        # C-instruction
        else:
            dest = ""
            jump = ""

            if "=" in instruction:
                dest, instruction = instruction.split("=", 1)

            if ";" in instruction:
                comp, jump = instruction.split(";", 1)
            else:
                comp = instruction

            if comp not in COMP:
                raise ValueError(f"Invalid computation: {comp}")

            if dest not in DEST:
                raise ValueError(f"Invalid destination: {dest}")

            if jump not in JUMP:
                raise ValueError(f"Invalid jump: {jump}")

            binary = (
                "111"
                + COMP[comp]
                + DEST[dest]
                + JUMP[jump]
            )

            machine_code.append(binary)

    return machine_code, symbols


# ------------------------------------------
# SAVE OUTPUT FILES
# ------------------------------------------

def save_machine_code(machine_code, output_filename):
    """Save generated machine code to a .hack file."""

    with open(output_filename, "w") as file:
        for instruction in machine_code:
            file.write(instruction + "\n")


def save_symbols(labels, symbols, filename="symbols.txt"):
    """Save user-defined labels and variables with their addresses."""

    with open(filename, "w") as file:

        # Save labels
        for symbol, address in sorted(labels.items()):
            file.write(f"{symbol} = {address}\n")

        # Save variables
        for symbol, address in sorted(symbols.items()):
            if symbol not in PREDEFINED_SYMBOLS and symbol not in labels:
                file.write(f"{symbol} = {address}\n")


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python assembler.py <filename.asm>")
        sys.exit(1)

    input_filename = sys.argv[1]

    if not os.path.isfile(input_filename):
        print(f"Error: File '{input_filename}' not found.")
        sys.exit(1)

    if not input_filename.lower().endswith(".asm"):
        print("Error: Input file must have .asm extension.")
        sys.exit(1)

    output_filename = os.path.splitext(input_filename)[0] + ".hack"

    try:
        instructions = clean_assembly(input_filename)

        labels = first_pass(instructions)

        machine_code, symbols = second_pass(instructions, labels)

        save_machine_code(machine_code, output_filename)
        save_symbols(labels, symbols)

        print("Assembly successful!")
        print(f"Machine code saved to: {output_filename}")
        print("Symbols saved to: symbols.txt")

    except (ValueError, OSError) as error:
        print(f"Assembly Error: {error}")
        sys.exit(1)
