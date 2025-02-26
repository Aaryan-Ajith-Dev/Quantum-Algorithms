from qiskit.circuit import QuantumCircuit
import math as mt

def QFT(qc: QuantumCircuit, qubits: list[int], inverse: bool = False) -> QuantumCircuit:
    sign = 1
    if inverse:
        sign = -1
    for i in range(len(qubits)):
        qc.h(qubits[i])
        for j in range(i+1, len(qubits)):
            qc.cp(sign * 2 * mt.pi / (2**(j - i + 1)), qubits[j], qubits[i])

    for i in range(len(qubits) // 2):
        qc.swap(qubits[i], qubits[-i-1])
    
    return qc
