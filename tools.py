# tools.py
# Formula: c_t(n) = sum_{partitions p of n into t distinct parts} [ 1/(t(t+1)) * prod((i+1)/i)^pi ]

import json
import os
import math
from fractions import Fraction

DATA_FILE = "data.json"
_cache = None

def load_cache():
    """Loads the precomputed database into memory."""
    global _cache
    if _cache is not None:
        return
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                _cache = json.load(f)
        except (json.JSONDecodeError, ValueError):
            _cache = {}
    else:
        _cache = {}

def save_cache():
    """Sorts the cache numerically and writes it to the JSON file."""
    global _cache
    sorted_cache = {}
    
    # Sort top-level keys: variations first (alphabetical), then c_1, c_2...
    def sort_key(k):
        if k.startswith("c_"):
            return (1, int(k.split("_")[1]))
        return (0, k)
        
    for key in sorted(_cache.keys(), key=sort_key):
        # Sort inner dictionary keys as integers so "10" comes after "9", not "1"
        inner_dict = _cache[key]
        sorted_cache[key] = {str(k): inner_dict[str(k)] for k in sorted(int(x) for x in inner_dict.keys())}
        
    with open(DATA_FILE, "w") as f:
        json.dump(sorted_cache, f, indent=4)

def ensure_key(key):
    """Ensures a top-level key exists in the cache."""
    global _cache
    if key not in _cache:
        _cache[key] = {}

def get_max_t(n):
    """Calculates the exact maximum integer t such that t(t+1)/2 <= n."""
    return (math.isqrt(8 * n + 1) - 1) // 2

def get_partitions_distinct(n, t, max_val=None):
    """Fast recursive generator for partitions of n into t distinct parts."""
    if t == 0:
        if n == 0:
            yield []
        return
    if max_val is None:
        max_val = n
    
    min_possible = t * (t + 1) // 2
    if n < min_possible:
        return
        
    for i in range(min(n, max_val), t - 1, -1):
        for p in get_partitions_distinct(n - i, t - 1, i - 1):
            yield [i] + p

def _compute_c_t_exact(t, n):
    """Pure mathematical computation of c_t(n) without cache overhead."""
    total_sum = Fraction(0)
    denom_outer = t * (t + 1)
    
    for p in get_partitions_distinct(n, t):
        prod_term = Fraction(1)
        for i, p_i in enumerate(p, 1):
            prod_term *= Fraction(i + 1, i) ** p_i
        total_sum += prod_term
    
    return total_sum / denom_outer

def prepare_c_cache(max_n):
    """Precomputes all valid c_t(n) sequentially and saves them."""
    load_cache()
    max_t = get_max_t(max_n)
    dirty = False
    
    for t in range(1, max_t + 1):
        t_key = f"c_{t}"
        ensure_key(t_key)
        
        min_n = (t * (t + 1)) // 2
        for n in range(min_n, max_n + 1):
            n_str = str(n)
            if n_str not in _cache[t_key]:
                val = _compute_c_t_exact(t, n)
                _cache[t_key][n_str] = str(val)
                dirty = True
                
    if dirty:
        save_cache()

def c_t(t, n):
    """Retrieves c_t(n) from cache, returning 0 instantly if out of bounds."""
    # Strict boundary check prevents -1, 0, or useless t's from being cached.
    if n < (t * (t + 1)) // 2:
        return Fraction(0)
        
    global _cache
    load_cache()
    
    t_key = f"c_{t}"
    n_str = str(n)
    
    if t_key in _cache and n_str in _cache[t_key]:
        return Fraction(_cache[t_key][n_str])
        
    # Fallback if a valid computation was somehow missed
    val = _compute_c_t_exact(t, n)
    ensure_key(t_key)
    _cache[t_key][n_str] = str(val)
    save_cache()
    
    return val