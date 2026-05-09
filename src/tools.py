# tools.py

import json
import os
import time

_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(_parent_dir, "data")
PATTERNS_DATA_FILE = os.path.join(DATA_DIR, "patterns_data.json")
CT_DATA_FILE = os.path.join(DATA_DIR, "ct_data.json")

os.makedirs(DATA_DIR, exist_ok=True)

SAVE_INTERVAL_SECONDS = 60
_last_pattern_save_time = time.time()
_last_ct_save_time = time.time()

_prime_patterns_cache = None
_c_function_cache = None


def _load_json_file(filepath):
    """Load a JSON file, returning empty dict if it doesn't exist or is invalid."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def _save_json_file(filepath, data):
    """Save data to a JSON file with sorted keys."""
    temp_filepath = filepath + ".tmp"
    try:
        with open(temp_filepath, "w") as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_filepath, filepath)
    except:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        raise


def _get_prime_patterns_cache():
    """Get the prime patterns cache, loading if necessary."""
    global _prime_patterns_cache
    if _prime_patterns_cache is None:
        _prime_patterns_cache = _load_json_file(PATTERNS_DATA_FILE)
    return _prime_patterns_cache


def _get_c_function_cache():
    """Get the c function cache, loading if necessary."""
    global _c_function_cache
    if _c_function_cache is None:
        _c_function_cache = _load_json_file(CT_DATA_FILE)
    return _c_function_cache


def load_cache():
    """Loads both caches into memory."""
    _get_prime_patterns_cache()
    _get_c_function_cache()


def save_prime_pattern_value(pattern_type, n, value):
    """
    Save a single prime pattern value to the data file.
    Writes immediately to disk for incremental saving.
    """
    global _last_pattern_save_time
    cache = _get_prime_patterns_cache()
    if pattern_type not in cache:
        cache[pattern_type] = {}
    cache[pattern_type][str(n)] = value
    if time.time() - _last_pattern_save_time >= SAVE_INTERVAL_SECONDS:
        _save_json_file(PATTERNS_DATA_FILE, cache)
        _last_pattern_save_time = time.time()
        print("[Checkpoint] Saved prime patterns to disk")


def save_c_function_value(t, n, value):
    """
    Save a single c_t(n) value to the data file.
    Writes immediately to disk for incremental saving.
    """
    global _last_ct_save_time
    cache = _get_c_function_cache()
    t_key = f"c_{t}"
    if t_key not in cache:
        cache[t_key] = {}
    cache[t_key][str(n)] = str(value)
    if time.time() - _last_ct_save_time >= SAVE_INTERVAL_SECONDS:
        _save_json_file(CT_DATA_FILE, cache)
        _last_ct_save_time = time.time()
        print("[Checkpoint] Saved c_t values to disk")


def force_save_caches():
    """Force save both caches to disk if they exist."""
    global _prime_patterns_cache, _c_function_cache
    if _prime_patterns_cache is not None:
        _save_json_file(PATTERNS_DATA_FILE, _prime_patterns_cache)
    if _c_function_cache is not None:
        _save_json_file(CT_DATA_FILE, _c_function_cache)


def get_prime_pattern_value(pattern_type, n):
    """Get a prime pattern value from cache, or None if not found."""
    cache = _get_prime_patterns_cache()
    if pattern_type in cache and str(n) in cache[pattern_type]:
        return cache[pattern_type][str(n)]
    return None


def get_c_function_value(t, n):
    """Get a c_t(n) value from cache, or None if not found."""
    cache = _get_c_function_cache()
    t_key = f"c_{t}"
    if t_key in cache and str(n) in cache[t_key]:
        return cache[t_key][str(n)]
    return None


def get_max_computed_n(pattern_type):
    """Get the maximum n computed for a given pattern type."""
    cache = _get_prime_patterns_cache()
    if pattern_type not in cache or not cache[pattern_type]:
        return 0
    return max(int(k) for k in cache[pattern_type].keys())


def get_max_computed_t():
    """Get the maximum t computed in the c function cache."""
    cache = _get_c_function_cache()
    if not cache:
        return 0
    t_keys = [k for k in cache.keys() if k.startswith("c_")]
    if not t_keys:
        return 0
    return max(int(k.split("_")[1]) for k in t_keys)
