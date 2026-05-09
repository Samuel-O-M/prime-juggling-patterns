# passing.py
# Formula (Theorem 5.1): P'(1, n, k) = sum_{h=1}^k [ comb(k, h) * comb(n-1, h-1) * (h-1)! ]
# Usage: python -m src.passing 50 3

import sys
from .tools import get_prime_pattern_value, save_prime_pattern_value, get_max_computed_n, force_save_caches

from math import comb, factorial


def compute_passing_up_to(max_n, k=3):
    """
    Compute P'_1(n, k) for all n from 1 to max_n incrementally.
    Saves each value as it's computed.
    """
    # Find where we left off
    pattern_type = f"passing_1ball_k{k}"
    last_computed = get_max_computed_n(pattern_type)
    start_n = last_computed + 1
    
    if start_n > max_n:
        print(f"  {pattern_type} already computed up to n={max_n}")
        return
    
    for n in range(start_n, max_n + 1):
        
        existing = get_prime_pattern_value(pattern_type, n)
        if existing is not None:
            continue

        total = 0
        for h in range(1, min(k, n) + 1):
            term = comb(k, h) * comb(n - 1, h - 1) * factorial(h - 1)
            total += term
        
        save_prime_pattern_value(pattern_type, n, total)
    
    force_save_caches()
    print(f"  Computed {pattern_type} for n={start_n}..{max_n}")


def P_prime_1(n, k=3):
    """
    Returns P'_1(n, k), computing and caching all values from 1 to n if needed.
    """
    pattern_type = f"passing_1ball_k{k}"
    
    existing = get_prime_pattern_value(pattern_type, n)
    if existing is not None:
        return existing
    
    compute_passing_up_to(n, k)
    
    return get_prime_pattern_value(pattern_type, n)


def main():
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    k_val = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    print(f"Computing passing_1ball_k{k_val} values up to n={n_val}...")
    compute_passing_up_to(n_val, k_val)
    
    result = P_prime_1(n_val, k_val)
    print(f"P'_1({n_val}, k={k_val}) = {result}")
    print(f"Data saved to data/")


if __name__ == "__main__":
    main()
