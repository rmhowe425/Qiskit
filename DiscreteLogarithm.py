from numpy import log, sqrt, floor
from random import randint
from algorithm import oracle

e = 0.05   # Minimum epsilon from the Magic Box paper.

def calculate_order(a, n):
    power = 1
    curr = a
    while (curr != 1):
        curr *= a
        power += 1
    return power

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
   @param G: Base of the logarithm.
   @param X: Power of the logarithm.
   @param n: Modulus.
   @param l: Lag of cross correlation - refers to how far the series are offset.
   @param d: The probability that the estimation will be incorrect.

   * Assumes that epsilon is already known (P. 106) *
    
   Used while loops in place of for loops because Python's
   range function does not use floating point numbers and I
   didnt want to introduce logical errors by rounding off
   numbers using floor() or int(). 
'''
def EstimateCrossCorrelation(G, X, n, l, d, period):
    total = 0  # Called 'sum' in algorithm
    trial = 1  

    # Compute the number of trials
    m = (2 / (sqrt(d) * e))

    # Compute estimate
    while trial <= m:
        t = randint(1, n)
        output = oracle(G, X, n)  # Oracle(base, LHS, mod)

        if output == 0:
            output = -1
        
        total = total + (output(X + (period * G)) * n1(t + l, n))

    return (total / m)

'''
   Main algorithm for computing the logarithm.
   @param G: Base of a the logarithm.
   @param X: Power of the logarithm.
   @param n: Modulus

   * Assumes that epsilon was calculated beforehand *

   Used while loops in place of for loops because Python's
   range function does not use floating point numbers and I
   didnt want to introduce logical errors by rounding off
   numbers using floor() or int(). 
'''
def Logarithm(G, X, n):
    step = (n * e)         # Compute step
    l = log(n)             # Number of iterations
    d = round((l / 4), 10) # Limit on probability error

    period = calculate_order(G, n)

    # Repeat until logarithm is found.
    while True:
        c = 0
        i = l - 1

        # Make initial guess. 
        while c <= (n - 1):
            
            # Refine guess.
            while i >= 0:
                Xi = ((2 ** i) * X) % n

                if (EstimateCrossCorrelation(G, Xi, n, c/2, d, period)
                    > EstimateCrossCorrelation(G, Xi, n, c/2 + n/2, d, period)):
                    c = c/2
                else:
                    c = (c/2 + n/2)

                i -= 1
            c += step
            
        if ((G ** c) % n) == X:
            return c
