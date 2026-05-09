# main.py
# Manager script to run all variations and trigger auto-caching.
# Usage: python -m main [n] [k]
# Example: python -m main 50 3

import sys

from src.ct import compute_ct_up_to, get_max_t
from src.normal import N_prime_2, compute_normal_up_to
from src.multiplex import M_prime_2, compute_multiplex_up_to
from src.colored import C_prime_2, compute_colored_up_to
from src.passing import P_prime_1, compute_passing_up_to
from src.base import B_prime_2, compute_base_up_to


def generate_data(max_n, k_hands=3):
    print(f"Computing all values up to n={max_n}...")
    print(f"Maximum t: {get_max_t(max_n)}")
    print()
    
    # Step 1: Compute c_t(n) values
    print("Step 1: Computing c_t(n) values...")
    compute_ct_up_to(max_n)
    print()
    
    # Step 2: Compute normal patterns
    print("Step 2: Computing normal_2ball...")
    compute_normal_up_to(max_n)
    print()
    
    # Step 3: Compute multiplex patterns
    print("Step 3: Computing multiplex_2ball...")
    compute_multiplex_up_to(max_n)
    print()
    
    # Step 4: Compute colored patterns
    print("Step 4: Computing colored_2ball...")
    compute_colored_up_to(max_n)
    print()
    
    # Step 5: Compute base state patterns
    print("Step 5: Computing base_state_2ball...")
    compute_base_up_to(max_n)
    print()

    # Step 6: Compute passing patterns
    print("Step 6: Computing passing_1ball...")
    compute_passing_up_to(max_n, k_hands)
    print()

    print("Done! All data has been computed and saved incrementally.")
    print(f"  - C function data: data/ct_data.json")
    print(f"  - Prime patterns data: data/patterns_data.json")


if __name__ == "__main__":
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    k_val = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    generate_data(n_val, k_val)
