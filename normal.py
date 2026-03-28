# normal.py
# Formula: N'(2, n) = sum_{t=1}^n c_t(n)

import tools
from tools import c_t

def N_prime_2(n):
    """Total normal 2-ball prime patterns."""
    tools.load_cache()
    tools.ensure_key("normal_2ball")
    n_str = str(n)
    
    if n_str in tools._cache["normal_2ball"]:
        return int(tools._cache["normal_2ball"][n_str])

    total = sum(c_t(t, n) for t in range(1, n + 1))
    result = int(total)
    
    tools._cache["normal_2ball"][n_str] = result
    tools.save_cache()
    
    return result