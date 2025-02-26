from qiskit import Aer, transpile, assemble, execute
from qiskit.circuit import QuantumCircuit
from qiskit import QuantumRegister, ClassicalRegister
from math import ceil, log
from Test_Mult import cMULTmodN

def prepare_state(qc: QuantumCircuit, input, eigenvector, x: int, N: int, L: int, t: int) -> QuantumCircuit:
    '''Prepare quantum state for order finding (optimized)'''
    x_mod_N = x % N
    t1  = QuantumRegister(N+1, 't1')
    qc.add_register(t1)
    t2  = QuantumRegister(N+1, 't2')
    qc.add_register(t2)
    t3  = QuantumRegister(N+1, 't3')
    qc.add_register(t3)
    t4  = QuantumRegister(N+1, 't4')
    qc.add_register(t4)
    for i in range(L):
        if x_mod_N & (1 << i):
            qc.x(t1[-i-1])
            qc.x(t2[-i-1])
    
    for i in range(t):
        qc.cx(input[i], t3[0])
        qc.reset(t3)
        qc.reset(t4)
        cMULTmodN(qc, input[i], t1, t4, x**(2**i) % N, N, L)
        cMULTmodN(qc, input[i], t1, t3, x**(2**i) % N, N, L)
        qc.swap(t1, t3)
        qc.swap(t2, t4)
    
    return qc

def find_order(x: int, N: int, epsilon: int) -> int:
    '''Find r such that x^r = 1 mod N using AerSimulator'''
    L = 0
    while 2**L < N:
        L += 1
    
    t = 2 * L + 1 + ceil(log(2 + 1/(2 * epsilon), 2))
    print("t =", t)
    
    input = QuantumRegister(t, 'input')
    eigenvector = QuantumRegister(N, 'eigenvector')
    output = ClassicalRegister(t, 'output')
    
    qc = QuantumCircuit(input, eigenvector, output)
    qc.h(input[:])
    prepare_state(qc, input, eigenvector, x, N, L, t)
    qc.barrier()
    
    for i in range(t):
        qc.measure(input[i], output[i])
    
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_qc = transpile(qc, simulator)
    qobj = assemble(transpiled_qc, shots=1024)
    result = simulator.run(qobj).result()
    
    counts = result.get_counts()
    measured_string = max(counts, key=counts.get)
    bits = [int(bit) for bit in reversed(measured_string)]
    print("Measurement bits:", bits)
    
    frac = sum(bits[i] * 2**(-i - 1) for i in range(t))
    print("Fraction:", frac)
    
    _, r = continued_fractions(frac, 2)
    return r

def continued_fractions(q: float, n: int = 20) -> tuple[int, int]:
    '''Find s and r such that q = s/r using continued fractions'''
    if q != int(q) and n > 0:
        prev_p, prev_q = continued_fractions(1 / (q - int(q)), n - 1)
        return (int(q) * prev_p + prev_q, prev_p)
    else:
        return (int(q), 1)

if __name__ == "__main__":
    print("Order found:", find_order(2, 7, 0.01))
