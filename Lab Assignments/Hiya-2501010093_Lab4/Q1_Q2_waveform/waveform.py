# waveform.py: annotated waveform for Add.asm (6 cycles)
import matplotlib.pyplot as plt

instr = ["@2", "D=A", "@3", "D=D+A", "@0", "M=D"]
binary = ["0000000000000010", "1110110000010000", "0000000000000011",
          "1110000010010000", "0000000000000000", "1110001100001000"]

# Values at x = 0..6 (state at the start of each cycle; x=6 is after the last tock)
PC     = [0, 1, 2, 3, 4, 5, 6]
A      = [0, 2, 2, 3, 3, 0, 0]
D      = [0, 0, 2, 2, 5, 5, 5]
outM   = [0, 2, 0, 5, 0, 5, 5]   # ALU output (don't-care on @ instructions, shown as 0)
writeM = [0, 0, 0, 0, 0, 1, 0]
RAM0   = [0, 0, 0, 0, 0, 0, 5]

# Clock: high during tick (first half), low during tock (second half)
clk_x, clk_y = [], []
for c in range(6):
    clk_x += [c, c + 0.5]
    clk_y += [1, 0]
clk_x.append(6)
clk_y.append(0)

signals = [
    ("CLK", clk_x, clk_y),
    ("PC", list(range(7)), PC),
    ("A register", list(range(7)), A),
    ("D register", list(range(7)), D),
    ("ALU out / outM", list(range(7)), outM),
    ("writeM", list(range(7)), writeM),
    ("RAM[0]", list(range(7)), RAM0),
]

fig, axes = plt.subplots(len(signals), 1, figsize=(12, 10), sharex=True)
for ax, (name, x, y) in zip(axes, signals):
    ax.step(x, y, where="post", linewidth=2)
    ax.set_ylabel(name, rotation=0, ha="right", va="center")
    ax.set_ylim(min(y) - 1, max(y) + 1)
    ax.grid(True, axis="x", linestyle=":")
    for c in range(7):
        ax.axvline(c, color="gray", linewidth=0.5)

# Annotate each cycle with the instruction executed
for c in range(6):
    axes[0].text(c + 0.5, 1.6, f"C{c+1}: {instr[c]}", ha="center", fontsize=10,
                 bbox=dict(boxstyle="round", fc="lightyellow"))
axes[0].set_ylim(-0.5, 2.3)

axes[-1].set_xlabel("Clock cycle (each cycle = tick + tock)")
axes[-1].set_xticks(range(7))
fig.suptitle("Hack CPU waveform for Add.asm (RAM[0] = 2 + 3)", fontsize=14)
plt.tight_layout()
plt.savefig("waveform_add.png", dpi=150)
print("Saved waveform_add.png")