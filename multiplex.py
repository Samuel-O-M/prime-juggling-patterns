# multiplex.py
# Formula (Corollary 3.1):
# M'(2, n) = sum_t [ c_t(n) + sum_{m=1}^{n-1} t * c_t(m) ] + 1

import tools
from tools import c_t
from fractions import Fraction

def M_prime_2(n):
    """Total multiplex 2-ball prime patterns."""
    tools.load_cache()
    tools.ensure_key("multiplex_2ball")
    n_str = str(n)
    
    if n_str in tools._cache["multiplex_2ball"]:
        return int(tools._cache["multiplex_2ball"][n_str])

    total_ct_sum = Fraction(0)
    for t in range(1, n + 1):
        term_n = c_t(t, n)
        sum_m = sum(Fraction(t) * c_t(t, m) for m in range(1, n))
        total_ct_sum += (term_n + sum_m)

    result = int(total_ct_sum + 1)
    
    tools._cache["multiplex_2ball"][n_str] = result
    tools.save_cache()
    
    return result