# __init__.py
# src package initialization
from . import tools
from . import ct

from .tools import (
    get_prime_pattern_value,
    save_prime_pattern_value,
    get_c_function_value,
    save_c_function_value,
    get_max_computed_n,
    get_max_computed_t,
    force_save_caches
)

from .ct import c_t, compute_ct_up_to, get_max_t
from .normal import N_prime_2, compute_normal_up_to
from .multiplex import M_prime_2, compute_multiplex_up_to
from .colored import C_prime_2, compute_colored_up_to
from .base import B_prime_2, compute_base_up_to
from .passing import P_prime_1, compute_passing_up_to