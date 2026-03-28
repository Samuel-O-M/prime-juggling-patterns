# base.py
# Formula (Corollary 7.2): B(n) = sum_t [ t * c_t(n-t) + t * c_t(n-t-1) ]

import tools
from tools import c_t
from fractions import Fraction

def B_prime_2(n):
    """Number of 2-ball prime cycles containing the base state <1,1>."""
    tools.load_cache()
    tools.ensure_key("base_state_2ball")
    n_str = str(n)
    
    if n_str in tools._cache["base_state_2ball"]:
        return int(tools._cache["base_state_2ball"][n_str])

    total = Fraction(0)
    for t in range(1, n + 1):
        term1 = Fraction(t) * c_t(t, n - t)
        term2 = Fraction(t) * c_t(t, n - t - 1)
        total += (term1 + term2)
        
    result = int(total)
    
    tools._cache["base_state_2ball"][n_str] = result
    tools.save_cache()
    
    return result