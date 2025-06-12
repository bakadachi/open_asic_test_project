#!/bin/bash

# Synthesize with yosys
yosys synth.ys > synth.log

# Check synth.log for warnings/errors
grep -i warning synth.log
grep -i error synth.log

# Optional: lint RTL
yosys -p "read_verilog rtl/*.v; hierarchy -top top_module; lint" > lint.log

# Review lint.log manually or parse for gated clock signals

echo "Synthesis and linting done. Check synth.log and lint.log for details."
