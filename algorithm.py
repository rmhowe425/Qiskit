from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.circuit.library import QFT
from qiskit.extensions import UnitaryGate
import numpy as np


# In our final Jupyter notebook we won't have to
# break things up functionally like this, but it
# should help for now.

# Verification user input to construct problem to be solved
# When  𝑎  and  𝑁  are positive Z,  𝑎  is less than  𝑁 , ? and they have no common factors? 
def verify(a,b,N):
    if a<0 or b<0 or N<0 or a>N:
        print("Invalid input")
        return 0
    else:
        print("Valid input")


# Calculates the multiplicative inverse of x mod N
# (the number y such that xy = 1 (mod N)) using
# the extended Euclidean algorithm.
def invert(x, N):
    q = [0, 0]
    r = [N, x]
    t = [0, 1]

    while r[-1] != 0:
        q.append(r[-2]//r[-1])
        r.append(r[-2] - (q[-1]*r[-1]))
        t.append(t[-2] - (q[-1]*t[-1]))
    
    # if r[-2] != 1:
    #     raise Exception
    
    return int(t[-2] % N)

# Returns a unitary matrix which has the effect of multiplying each
# input |x> by a in mod N, resulting in the state |ax>.
def create_controlled_unitary(a, N):
    dim = 2**int(np.ceil(np.log(N)/np.log(2)) + 1)
    U = np.zeros((dim, dim))
    # Generate a permutation of the multiplicative group of Z_N.
    for i in range(int(dim/2)):
        U[i,i] = 1
    for i in range(N):
        U[int(dim/2) + i, ((a*i) % N)+int(dim/2)] = 1
    # The remaining states are irrelevant.
    for i in range(N, int(dim/2)):
        U[int(dim/2) + i, int(dim/2) + i] = 1
    return U

def create_unitary(a, N):
    a = int(np.round(a) % N)
    dim = 2**int(np.ceil(np.log(N)/np.log(2)))
    U = np.zeros((dim, dim))
    # Generate a permutation of the multiplicative group of Z_N.
    for i in range(N):
        U[i, ((a*i) % N)] = 1
    # The remaining states are irrelevant.
    for i in range(N, dim):
        U[i, i] = 1
    return U

# b is some power of a, and the oracle outputs m,
# where b = a^m (mod N) with >50% probability.
# (this is where our main algorithm goes)
def oracle(a, b, N, verbose=False):

    # Calculate the order of a
    r = 1
    product = a
    while product != 1:
        product = (product * a) % N
        r += 1

    # Find number of bits(n) needed to store a value from 0 to N-1
    # and initialize 2 quantum registers of size n
    n = int(np.ceil(np.log(N)/np.log(2)))
    qr1, qr2 = QuantumRegister(n), QuantumRegister(n)
    cr1, cr2 = ClassicalRegister(n), ClassicalRegister(1)
    qc = QuantumCircuit(qr1, qr2, cr1, cr2)
    
    #Change second register to state |00...01>
    qc.x(qr2[n-1])
    
    #Add H gate to first register
    for i in range(n):
        qc.h(qr1[i])
    
    # We need log_2(n) different matrices U_(a^(2^x))
    for i in range(n):
        U = create_controlled_unitary(a**(2**(n-i)) % N, N)
        qubits = [qr1[i]] + [qr2[j] for j in range(n)]
        qc.iso(U, qubits, [])


    qc.append(QFT(n), [qr1[i] for i in range(n)])

    for i in range(n):
        qc.measure(qr1[i], cr1[i])
    
    # Now cr1 is in state y. We define k to be the closest integer to y*r / 2**n.
    # Reuse the first quantum register, because we don't need it anymore.
    for i in range(2**(n-1), 2**n):
        qc.x(qr1[0]).c_if(cr1, i)

    qc.h(qr1[0])

    qc.barrier()

    # I don't think there's any way to get the result of the measurement mid-circuit
    # in qiskit. So this is a stop-gap method for now.

    for y in range(2**n):
        k = int(np.round(y*r/(2**n))) % r
        kInv = bin(invert(k, r))[2:]

        # Pad kInv with initial zeros
        while len(kInv) < n:
            kInv = '0' + kInv

        if '1' in kInv:
            for i in range(len(kInv)):
                bit = int(kInv[i])
                if bit == 1:
                    # Apply U operation only if the value of cr1 is y.
                    U = create_unitary(b**(2**i), N)
                    qc.iso(U, [qr2[i] for i in range(n)], []).c_if(cr1, y)
    
    qc.barrier()
    qc.rz(-np.pi/2 , qr1[0])
    qc.h(qr1[0])
    qc.measure(qr1[0], cr2[0])
    
    if verbose:
        print(qc.draw(output="text"))

    backend_name = 'qasm_simulator'
    shots = int(np.ceil(8*np.pi))
    backend = Aer.get_backend(backend_name)
    if verbose:
        print("Running circuit on", backend_name, "...")
    result = execute(qc, backend, shots=shots).result().get_counts(qc)

    if verbose:
        print(result)
    
    zeros_count = 0
    ones_count = 0

    for k in result.keys():
        half_bit = k[0]
        if half_bit == '0':
            zeros_count += result[k]
        else:
            ones_count += result[k]

    if verbose:
        print('Zeros:', zeros_count, '\tOnes:', ones_count)
    
    if zeros_count > ones_count:
        return 0
    else:
        return 1

# print(oracle(3, 1, 13, True))

# Solves the discrete logarithm problem for 
# b = a^m (mod N) using repeated calls to the
# oracle defined above.
def logarithm(a, b, N):
    return 0
