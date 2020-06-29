from numpy import log
from random import randint


'''
   Determines the most significant bit of an integer c
   @param c: Base
   @param n: Modulus
   @return: 1 or -1
'''
def n1(c, n):
    val = -1
    
    if c % n >= (n / 2):
        val = 1
        
    return val

'''
   Decides which 'guess' best fits with the output of the oracle using cross correlation.
   * Assumes that epsilon is already known (P. 106) *
   @param G: Base of a the logarithm.
   @param X: Power of the logarithm.
   @param n: Modulus.
   @param l: Lag of cross correlation - refers to how far the series are offset.
   @param d: The probability that the estimation will be incorrect.
'''
def EstimateCrossCorrelation(G, X, n, l, d):
    # Called 'sum' in algorithm
    total = 0
    
    # Compute the number of trials
    m = (2 / (np.sqrt(d) * e))

    # Compute estimate
    for trial in range(1, m + 1):
        t = randint(1, n)
        output = Oracle(G, X, n)  # Oracle(base, LHS, mod)

        if output == 0:
            output = -1
        
        total = total + (output(X + (period * G)) * n1(t + l, n))

    return round((total / m), 5)

'''
   Main algorithm for computing the logarithm.
   * Assumes that epsilon was calculated beforehand *
   @param G: Base of a the logarithm.
   @param X: Power of the logarithm.
   @param n: Modulus 
   @param e: Output from oracle function -> Maybe removed in the future.
'''
def Logarithm(G, X, n):
    step = (n * e)          # Compute step
    l = log(n)              # Number of iterations
    d = round((l / 4), 10)  # Limit on probability error

    # Declaring c outside of for loop so it's within scope for the last if statement
    c = 0 
    # Decrease # of calculations in for loop
    start = l - 1
    
    # Repeat until logarithm is found.
    while True:

        # Make initial guess. 
        for c in range(0, n, step):

            # Refine guess.
            for i in range(start, 0, -1):
                Xi = (2 ** i) * X

                if (EstimateCrossCorrelation(G, Xi, n, c/2, d)
                    > EstimateCrossCorrelation(G, Xi, n, c/2 + n/2, d)):
                    c = c/2
                else:
                    c = (c/2 + n/2)

        if (G ** c) == X:
            return c
