import sys

from src.normal import N_prime_2
from src.multiplex import M_prime_2
from src.colored import C_prime_2


def main(max_n):
    if max_n > 20:
        print("Error: maximum n is 20 for this test script.")
        return

    for i in range(1, max_n + 1):
         
        print("This is n=" + str(i))

        n_val = N_prime_2(i)
        n_const = n_val / 2**i

        print("this is normal juggling")
        print("const value is gamma =" + str(n_const))

        m_val = M_prime_2(i)
        m_const = m_val / 2**i

        print("this is multiplex juggling")
        print("const value is gamma =" + str(m_const))
        
        c_val = C_prime_2(i)
        c_const = c_val / (i * 2**i)

        print("this is colored juggling")
        print("const value is gamma =" + str(c_const))


if __name__ == "__main__":
    n_val = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    main(n_val)
