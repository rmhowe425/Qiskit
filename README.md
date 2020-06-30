# Implementation of "A Quantum 'Magic Box' for the Discrete Logarithm Problem"

*Qiskit Community Summer Jam: North Carolina*

### Project Description

Given a modulus *N*, let *a* be an element of multiplicative order *r* in the integers modulo *N*. Also let *b* be a power of *a*, such that *b* = *a<sup>m</sup>* (mod *N*). The *half bit* of *b*, *HB(b)*, is defined as follows:

*HB(b)* = 0 if 0 <= *m* <= *r*/2, and

*HB(b)* = 1 if *r*/2 < *m* <= *r*. 

In Kaliski's 2017 paper, he proposes a quantum implementation of a 'magic box' oracle that will predict the half-bit of *b* with greater than 50% accuracy. The oracle is based upon a 1999 paper by Mocsa and Ekert, which optimizes and generalizes Shor's algorithm to a variety of group-theoretic algorithms. In Kaliski's 1988 PhD thesis, he describes an algorithm that uses such an oracle to solve the discrete logarithm problem (that is, to find the value of *m*) in polynomial time. Such an algorithm has far-reaching importance, perhaps most notably for its potential to render discrete logarithm cryptosystems insecure. In fact, Kaliski phrases the problem more generally, so the same method could be applied to break elliptic curve cryptosystems as well.

Our first and foremost goal in this project is to implement Kaliski's quantum oracle. This is where the large-scale efficiency increase happens. If we have time, we'll also use this oracle within his algorithm to solve the discrete logarithm problem. IBM's quantum hardware does not yet seem to have the features needed to implement this algorithm efficiently. Most notably, we lack the ability to measure a subset of qubits partway through the circuit, do classical processing on the result of the measurement, and then build the rest of the circuit. Related control flow options are available, but for simulators only. These limitations mean that our implementation will be inefficient, but it's an important first step in realizing this algorithm in code.

There is much future work to be done. If IBM implements the control flow required by this algorithm, we can greatly improve its efficiency, and also run it on physical hardware. In addition, Kaliski lists a number of potential enhancements to the oracle in section 6 of his paper, many of which could be implemented in code.

### References

Kaliski Jr., B. (2017). A Quantum “Magic Box” for the Discrete Logarithm Problem. Cryptology EPrint Archive, Report 2017/745. https://eprint.iacr.org/2017/745

Kaliski Jr., B. (1988). Elliptic Curves and Cryptography: A Pseudorandom Bit Generator and Other Tools (Doctoral dissertation, MIT, Cambridge, USA). Retrieved from https://dspace.mit.edu/bitstream/handle/1721.1/14709/18494044-MIT.pdf

Mosca M., Ekert A. (1999) The Hidden Subgroup Problem and Eigenvalue Estimation on a Quantum Computer. In: Williams C.P. (eds) Quantum Computing and Quantum Communications. QCQC 1998. Lecture Notes in Computer Science, vol 1509. Springer, Berlin, Heidelberg