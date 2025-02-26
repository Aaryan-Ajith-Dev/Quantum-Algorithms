import qutip as qt
import numpy as np
from typing import Final


class QuantumCircuit:

    def __init__(self, n_qubits: int, n_bits: int) -> None:
        self.ket_0: Final[qt.Qobj] = qt.Qobj([1, 0])
        self.ket_1: Final[qt.Qobj] = qt.Qobj([0, 1])
        self.qubits = qt.tensor([self.ket_0] * n_qubits)
        self.n_qubits = n_qubits
        self.I: Final[qt.Qobj] = qt.qeye(2)
        self.bits = np.zeros(n_bits)
    
    def x(self, qubits) -> None:
        X = qt.Qobj([[0, 1], [1, 0]])
        if isinstance(qubits, int):  # Single qubit case
            operation = qt.tensor([self.I if i != qubits else X for i in range(self.n_qubits)])
        elif isinstance(qubits, list):  # Multiple qubits case
            operation = qt.tensor([X if i in qubits else self.I for i in range(self.n_qubits)])
        else:
            raise TypeError(f"Unsupported type for qubits: {type(qubits)}")
        self.qubits = operation * self.qubits

    def h(self, qubits):
        H = qt.Qobj([[1, 1], [1, -1]]) / np.sqrt(2)
        if isinstance(qubits, int):  # Single qubit case
            operation = qt.tensor([self.I if i != qubits else H for i in range(self.n_qubits)])
        elif isinstance(qubits, list):  # Multiple qubits case
            operation = qt.tensor([H if i in qubits else self.I for i in range(self.n_qubits)])
        else:
            raise TypeError(f"Unsupported type for qubits: {type(qubits)}")
        self.qubits = operation * self.qubits

    
    def cx(self, control: int, qubit: int):
        # control is the control qubit
        # qubit is the target qubit
        # angle is the phase angle
        operation = []
        control = self.n_qubits - control - 1
        qubit = self.n_qubits - qubit - 1
        for i in range(2**(self.n_qubits)):
            control_bit = (1 << control) & i
            row = []
            for j in range(self.n_qubits):
                if i & (1 << j):
                    if j == qubit and control_bit:
                        row.append(self.ket_0)
                    else:
                        row.append(self.ket_1)
                else:
                    if j == qubit and control_bit:
                        row.append(self.ket_1)
                    else:
                        row.append(self.ket_0)
            operation.append(qt.tensor(reversed(row)).data.to_array())
        operation = qt.Qobj(np.squeeze(np.array(operation)), dims = [[2]*self.n_qubits, [2]*self.n_qubits])
        self.qubits = operation * self.qubits


    def measure(self, qubit: int, bit: int) -> None:
        # measure qubit and store result in bit
        measure = self.qubits.ptrace(qubit)
        p = measure.diag()
        # randomly choose a result based on probabilities
        result = np.random.choice([0, 1], p = p)
        proj = None # projection operator
        if result:
            proj = self.ket_1 * self.ket_1.dag()
            self.bits[bit] = 1
        else:
            proj = self.ket_0 * self.ket_0.dag()
            self.bits[bit] = 0

        operation = qt.tensor([self.I if i != qubit else proj for i in range(self.n_qubits)])
        self.qubits = operation * self.qubits
        # normalize the state
        self.qubits = self.qubits.unit()

    def cp(self, control: int, qubit: int, angle: float):
        '''rotates qbit by a phase of angle if control is 1'''
        # control is the control qubit
        # qubit is the target qubit
        # angle is the phase angle
        operation = []
        control = self.n_qubits - control - 1
        qubit = self.n_qubits - qubit - 1
        for i in range(2**(self.n_qubits)):
            control_bit = (1 << control) & i
            row = []
            for j in range(self.n_qubits):
                if i & (1 << j):
                    if j == qubit and control_bit:
                        row.append(np.exp(1j * angle) * self.ket_1)
                    else:
                        row.append(self.ket_1)
                else:
                    if j == qubit and control_bit:
                        row.append(self.ket_0)
                    else:
                        row.append(self.ket_0)
            operation.append(qt.tensor(reversed(row)).data.to_array())
        operation = qt.Qobj(np.squeeze(np.array(operation)), dims = [[2]*self.n_qubits, [2]*self.n_qubits])
        self.qubits = operation * self.qubits

    def swap(self, qubit1: int, qubit2: int):
        self.cx(qubit1, qubit2)
        self.cx(qubit2, qubit1)
        self.cx(qubit1, qubit2)


if __name__ == '__main__':
    qc = QuantumCircuit(2, 2)
    qc.h([0])
    qc.cx(0, 1)
    print(qc.qubits)
    qc.measure(0, 0)
    qc.measure(1, 1)
    print(qc.bits)


