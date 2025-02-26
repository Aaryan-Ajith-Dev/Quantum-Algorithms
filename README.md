# Quantum Algorithms
## Overview
  This repository contains some quantum computing algorithms implemented in qiskit and a circuit simulator implemented in QuTip.
### List of Algorithms
- Deutsch's Algorithm
- CHSH game
- Shor
    - Factoring
    - QFT
    - Order Finding
- Circuit simulation (circuit.py)

## Shor's Algorithm
- Implemented QFT from standard qiskit gates.
- Implemented Order Finding which uses QFT and an external code for modular multiplication.
- Further used order finding to implement Shor’s algorithm.

### Notes
Since the simulated factoring code took long for the first non-trivial input (3 * 5 = 15), to ensure correctness, the order finding was tested separately
and the factoring code was tested with a classical order finder (commented in factoring.py).

## Circuit Simulation
-  Implemented basic single qubit operations (such as Pauli X, Hadamard) and multiqubit operations (such
as CNOT, Controlled Phase Gate, Swap Gate) from scratch (matrix multiplications).
-  Implemented measurement operations from scratch (implemented by taking a partial trace and randomly
choosing 0 or 1 based on the probabilities obtained after partial trace).

### Notes
The combined state of the system is stored directly as a tensor product without any additional optimizations.
The operations on the system are implemented from scratch via matrix multiplications and may take time for larger quantum systems.

## Reference for Modular Multiplication
Test_Mult.py from: 
https://github.com/tiagomsleao/ShorAlgQiskit/tree/master
