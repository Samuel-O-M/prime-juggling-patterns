# passing.py
# Formula (Theorem 5.1): P'(1, n, k) = sum_{h=1}^k [ comb(k, h) * comb(n-1, h-1) * (h-1)! ]

from math import comb, factorial

def P_prime_1(n, k):
    """Total 1-ball passing prime patterns with k hands."""
    total = 0
    for h in range(1, min(k, n) + 1):
        term = comb(k, h) * comb(n - 1, h - 1) * factorial(h - 1)
        total += term
    return total