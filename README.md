## Wu’s Method Example: 2008P1b

This repository contains a single Python script that solves the geometry problem 2008P1b using Wu’s algebraic method.

The script constructs the geometric configuration symbolically and translates geometric relations—including midpoints, orthocenter conditions, collinearity, circle constraints, and concyclicity—into multivariate polynomial equations.

Wu’s method is then applied through successive pseudo-division and variable elimination under a fixed elimination order. The final remainder is computed to verify the target concyclicity statement.

This file serves as a minimal working example demonstrating how classical Wu’s method can be implemented programmatically for an Olympiad-level geometry problem.

## Requirements

- Python >= 3.7
- QuantumIntelligence (PyPI)

QuantumIntelligence dependencies:
- torch
- numpy
- scipy
- matplotlib
- pynvml
- stim
- qiskit

