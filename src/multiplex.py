# multiplex.py
# Formula (Corollary 3.1):
# M'(2, n) = sum_t [ c_t(n) + sum_{m=1}^{n-1} t * c_t(m) ] + 1
# Usage: python -m src.multiplex 50

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


def compute_multiplex_up_to(max_n):
    """
    Compute M'_2(n) for all n from 1 to max_n incrementally.
    Saves each value as it's computed.
    """
    
    last_computed = get_max_computed_n("multiplex_2ball")
    start_n = last_computed + 1
    
    if start_n > max_n:
        print(f"  multiplex_2ball already computed up to n={max_n}")
        return
    
    for n in range(start_n, max_n + 1):
        
        existing = get_prime_pattern_value("multiplex_2ball", n)
        if existing is not None:
            continue

        total_ct_sum = 0
        for t in range(1, get_max_t(n) + 1):
            term_n = int(c_t(t, n))
            sum_m = sum(t * int(c_t(t, m)) for m in range(1, n))
            total_ct_sum += (term_n + sum_m)

        result = int(total_ct_sum + 1)
        save_prime_pattern_value("multiplex_2ball", n, result)
    
    force_save_caches()
    print(f"  Computed multiplex_2ball for n={start_n}..{max_n}")


def M_prime_2(n):
    """
    Returns M'_2(n), computing and caching all values from 1 to n if needed.
    """
    
    existing = get_prime_pattern_value("multiplex_2ball", n)
    if existing is not None:
        return existing
    
    compute_multiplex_up_to(n)
    
    return get_prime_pattern_value("multiplex_2ball", n)


def main():
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    
    print(f"Computing c_t(n) values up to n={n_val}...")
    compute_ct_up_to(n_val)
    
    print(f"Computing multiplex_2ball values up to n={n_val}...")
    compute_multiplex_up_to(n_val)
    
    result = M_prime_2(n_val)
    print(f"M'_2({n_val}) = {result}")
    print(f"Data saved to data/")


if __name__ == "__main__":
    main()
