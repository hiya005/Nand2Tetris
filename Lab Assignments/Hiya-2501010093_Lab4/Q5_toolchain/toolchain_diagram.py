# toolchain_diagram.py: Hack toolchain vs real toolchain
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 8)
ax.axis("off")

def box(x, y, text, color, w=2.2, h=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                fc=color, ec="black"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.5))

FILE, TOOL, HW = "#fff2cc", "#cfe2f3", "#d9ead3"

# ---- Hack toolchain ----
ax.text(0.3, 7.7, "HACK TOOLCHAIN", fontsize=12, fontweight="bold")
xs = [0.3, 3.1, 5.9, 8.7, 11.5]
y = 6.4
box(xs[0], y, "Prog.asm\n(symbols, mnemonics)", FILE)
box(xs[1], y, "ASSEMBLER\nsymbols -> addresses\nmnemonics -> bits", TOOL)
box(xs[2], y, "Prog.hack\n(16-bit binary)", FILE)
box(xs[3], y, "Loaded into\nROM32K", HW)
box(xs[4], y, "Hack CPU runs\n(absolute addresses)", HW)
for i in range(4):
    arrow(xs[i] + 2.2, y + 0.5, xs[i + 1], y + 0.5)

# ---- Real toolchain, row 1 ----
ax.text(0.3, 5.2, "REAL TOOLCHAIN (C / Linux)", fontsize=12, fontweight="bold")
y1 = 3.8
box(xs[0], y1, "main.c\n(source)", FILE)
box(xs[1], y1, "PREPROCESSOR\n+ COMPILER", TOOL)
box(xs[2], y1, "main.s\n(assembly)", FILE)
box(xs[3], y1, "ASSEMBLER\nasm -> machine code", TOOL)
box(xs[4], y1, "main.o\n(object, has\nunresolved symbols)", FILE)
for i in range(4):
    arrow(xs[i] + 2.2, y1 + 0.5, xs[i + 1], y1 + 0.5)

# ---- Real toolchain, row 2 (right to left) ----
y2 = 2.0
box(xs[4], y2, "LINKER\nresolve symbols,\nrelocate", TOOL)
box(xs[3], y2, "a.out / ELF\n(executable)", FILE)
box(xs[2], y2, "LOADER (OS)\nmap to memory,\ndynamic linking, stack", TOOL)
box(xs[1], y2, "Running process\n(virtual memory,\nNX / ASLR)", HW)
arrow(xs[4] + 1.1, y1, xs[4] + 1.1, y2 + 1.0)          # main.o -> linker
box(xs[4], 0.3, "libc.a / other .o\n(libraries)", FILE)
arrow(xs[4] + 1.1, 1.3, xs[4] + 1.1, y2)                # libs -> linker
for i in (4, 3, 2):
    arrow(xs[i], y2 + 0.5, xs[i - 1] + 2.2, y2 + 0.5)

plt.savefig("toolchain_diagram.png", dpi=150, bbox_inches="tight")
print("Saved toolchain_diagram.png")