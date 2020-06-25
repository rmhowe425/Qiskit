from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
import math

# In our final Jupyter notebook we won't have to
# break things up functionally like this, but it
# should help for now.

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
    
    if r[-2] != 1:
        raise Exception
    
    return t[-2] % N

# b is some power of a, and the oracle outputs m,
# where b = a^m (mod N) with >50% probability.
# (this is where our main algorithm goes)
def oracle(a, b, N):
    # Find number of bits(n) needed to store a value from 0 to N-1
    # and initialize 2 quantum registers of size n
    n = math.ceil(math.log(N)/math.log(2))
    qc = QuantumCircuit(2*n, 2*n)
    
    #Change second register to state |1>
    qc.x(2*n-1)
    
    #Add H gate to first register
    for i in range(n):
        qc.h(i)
    
    # Apply U_(a^x) here

    qc.append(QFT(n), [i for i in range(n)])

    for i in range(n):
        qc.measure(i, i)
    
    print(qc.draw(output="text"))
    
    return 0

oracle(2, 2, 8)

# Solves the discrete logarithm problem for 
# b = a^m (mod N) using repeated calls to the
# oracle defined above.
def logarithm(a, b, N):
    return 0