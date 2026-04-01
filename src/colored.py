# colored.py
# Formula (Theorem 4.1 & Prop 4.2):
# If n is odd: C'(2,n) = sum_m=1^{(n-1)/2} sum_t [ t * c_t(m) * c_t(n-m) ]
# If n is even: C'(2,n) = sum_t sum_m=1^{n/2-1} [ t * c_t(m) * c_t(n-m) ] 
#                        + sum_t [ t * comb(c_t(n/2), 2) + ceil(t/2) * c_t(n/2) ]
# Usage: python -m src.colored 50

import sys
import os

# Handle both direct execution and module execution
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from src.tools import get_prime_pattern_value, save_prime_pattern_value, get_max_computed_n, force_save_caches
    from src.ct import c_t, compute_ct_up_to, get_max_t
else:
    from .tools import get_prime_pattern_value, save_prime_pattern_value, get_max_computed_n, force_save_caches
    from .ct import c_t, compute_ct_up_to, get_max_t

from math import ceil


def compute_colored_up_to(max_n):
    """
    Compute C'_2(n) for all n from 1 to max_n incrementally.
    Saves each value as it's computed.
    """
    
    last_computed = get_max_computed_n("colored_2ball")
    start_n = last_computed + 1
    
    if start_n > max_n:
        print(f"  colored_2ball already computed up to n={max_n}")
        return
    
    for n in range(start_n, max_n + 1):
        
        existing = get_prime_pattern_value("colored_2ball", n)
        if existing is not None:
            continue

        total = 0
        if n % 2 != 0:
            # Odd case
            for m in range(1, (n // 2) + 1):
                for t in range(1, get_max_t(n) + 1):
                    total += t * int(c_t(t, m)) * int(c_t(t, n - m))
        else:
            # Even case
            mid = n // 2
            for m in range(1, mid):
                for t in range(1, get_max_t(n) + 1):
                    total += t * int(c_t(t, m)) * int(c_t(t, n - m))
            
            for t in range(1, get_max_t(n) + 1):
                ct_mid = int(c_t(t, mid))
                comb_term = t * (ct_mid * (ct_mid - 1)) // 2
                ceil_term = ceil(t / 2) * ct_mid
                total += (comb_term + ceil_term)

        result = total
        save_prime_pattern_value("colored_2ball", n, result)
    
    force_save_caches()
    print(f"  Computed colored_2ball for n={start_n}..{max_n}")


def C_prime_2(n):
    """
    Returns C'_2(n), computing and caching all values from 1 to n if needed.
    """

    existing = get_prime_pattern_value("colored_2ball", n)
    if existing is not None:
        return existing
    
    compute_colored_up_to(n)
    
    return get_prime_pattern_value("colored_2ball", n)


def main():
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    print(f"Computing c_t(n) values up to n={n_val}...")
    compute_ct_up_to(n_val)
    
    print(f"Computing colored_2ball values up to n={n_val}...")
    compute_colored_up_to(n_val)
    
    result = C_prime_2(n_val)
    print(f"C'_2({n_val}) = {result}")
    print(f"Data saved to data/")


if __name__ == "__main__":
    main()
