# ct.py
# Formula: c_t(n) = sum_{partitions p of n into t distinct parts} [ 1/(t(t+1)) * prod((i+1)/i)^pi ]
# Usage: python -m src.ct 50

import math
import sys
from fractions import Fraction
from .tools import get_c_function_value, save_c_function_value, force_save_caches


def get_max_t(n):
    """Calculates the exact maximum integer t such that t(t+1)/2 <= n."""
    return (math.isqrt(8 * n + 1) - 1) // 2


def compute_ct_up_to(max_n):
    """
    Compute all c_t(n) values up to max_n incrementally.
    For each t from 1 to max_t, compute the generating function once
    and save each value incrementally.
    """
    max_t = get_max_t(max_n)
    
    # dp[t][n] stores the coefficient h_t(n)
    dp = [[0] * (max_n + 1) for _ in range(max_t + 1)]
    dp[0][0] = 1
    
    for t in range(1, max_t + 1):
        min_n = (t * (t + 1)) // 2
        
        # Compute all values for this t at once
        for n in range(min_n, max_n + 1):
            dp[t][n] = (t + 1) * (dp[t-1][n-t] + dp[t][n-t])
        
        # Save each value incrementally
        for n in range(1, max_n + 1):
            
            existing = get_c_function_value(t, n)
            if existing is not None:
                continue
            
            if n < min_n:
                save_c_function_value(t, n, "0")
            else:
                final_val = Fraction(dp[t][n], t * (t + 1))
                save_c_function_value(t, n, str(final_val))
        
        print(f"  Computed c_{t}(n) for n=1..{max_n}")
    
    force_save_caches()


def c_t(t, n):
    """
    Retrieves c_t(n) from cache, returning 0 instantly if out of bounds.
    Does NOT compute - use compute_ct_up_to() for batch computation.
    """
    
    if n <= 0:
        return 0


    min_n = (t * (t + 1)) // 2
    if n < min_n:
        return 0
    
    value = get_c_function_value(t, n)
    if value is not None:
        return value
    
    return 0


def main():
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    print(f"Computing c_t(n) values up to n={n_val}...")
    print(f"Maximum t to compute: {get_max_t(n_val)}")
    
    compute_ct_up_to(n_val)
    
    print(f"Done! Data saved to data/ct_data.json")


if __name__ == "__main__":
    main()
