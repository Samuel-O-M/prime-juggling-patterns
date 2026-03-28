# main.py
# Manager script to run all variations and trigger auto-caching.

import tools
from normal import N_prime_2
from multiplex import M_prime_2
from colored import C_prime_2
from passing import P_prime_1
from base import B_prime_2

def generate_data(max_n, k_hands=3):
    print(f"Precomputing core engine values up to n={max_n}...")
    tools.prepare_c_cache(max_n)
    
    print(f"Executing variations up to n={max_n}...")
    for n in range(1, max_n + 1):
        print(f"Computing n={n}...")
        
        # Calling these will automatically read/compute/write sequentially
        N_prime_2(n)
        M_prime_2(n)
        C_prime_2(n)
        B_prime_2(n)
        
        # Passing computes dynamically without saving to the DB
        pass_val = P_prime_1(n, k_hands)

    print("Done! All persistent data has been strictly sorted and saved to data.json")

if __name__ == "__main__":
    import sys
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    generate_data(n_val)