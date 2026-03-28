# colored.py
# Formula (Theorem 4.1 & Prop 4.2):
# If n is odd: C'(2,n) = sum_m=1^{(n-1)/2} sum_t [ t * c_t(m) * c_t(n-m) ]
# If n is even: C'(2,n) = sum_t sum_m=1^{n/2-1} [ t * c_t(m) * c_t(n-m) ] 
#                        + sum_t [ t * comb(c_t(n/2), 2) + ceil(t/2) * c_t(n/2) ]

import tools
from tools import c_t
from math import ceil
from fractions import Fraction

def C_prime_2(n):
    """Total colored 2-ball prime patterns."""
    tools.load_cache()
    tools.ensure_key("colored_2ball")
    n_str = str(n)
    
    if n_str in tools._cache["colored_2ball"]:
        return int(tools._cache["colored_2ball"][n_str])

    total = Fraction(0)
    if n % 2 != 0:
        # Odd case
        for m in range(1, (n // 2) + 1):
            for t in range(1, n + 1):
                total += Fraction(t) * c_t(t, m) * c_t(t, n - m)
    else:
        # Even case
        mid = n // 2
        for m in range(1, mid):
            for t in range(1, n + 1):
                total += Fraction(t) * c_t(t, m) * c_t(t, n - m)
        
        for t in range(1, n + 1):
            ct_mid = c_t(t, mid)
            comb_term = Fraction(t) * (ct_mid * (ct_mid - 1)) / 2
            ceil_term = Fraction(ceil(t / 2)) * ct_mid
            total += (comb_term + ceil_term)

    result = int(total)
    
    tools._cache["colored_2ball"][n_str] = result
    tools.save_cache()
    
    return result