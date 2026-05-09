# Prime Juggling Patterns

Companion computation code for the paper **"Enumerating Prime Patterns in Juggling Variations"** (Butler, Choi, Jeffries, McCambridge, Morgenstern, Orellana Mateo, 2026).

This package implements fast dynamic-programming algorithms to compute exact counts of prime juggling patterns for several juggling variations: normal, multiplex, colored, base-state, and passing.

## Mathematical Background

The core function is `c_t(n)`, which counts the number of prime-generating spacing sets for a partition of `n` into `t` distinct parts. The paper derives a closed-form generating function:

$$G_t(x) = \frac{1}{t(t+1)} \prod_{j=1}^t \frac{(j+1)x^j}{1 - (j+1)x^j}$$

and the linear recurrence:

$$h_t(n) = (t+1)[h_{t-1}(n-t) + h_t(n-t)]$$

with $h_0(0) = 1$, yielding $c_t(n) = h_t(n) / t(t+1)$. See `fast-ct/main.tex` for details.

## Pattern Variations

| Function | Description | Formula |
|----------|-------------|---------|
| `N'_2(n)` | Normal 2-ball prime patterns | $\sum_t c_t(n)$ |
| `M'_2(n)` | Multiplex 2-ball prime patterns | $\sum_t [c_t(n) + \sum_{m=1}^{n-1} t \cdot c_t(m)] + 1$ |
| `C'_2(n)` | Colored 2-ball prime patterns | Convolution formulas (odd/even cases) |
| `B'_2(n)` | Base-state (containing $\langle 1,1 \rangle$) | $\sum_t [t \cdot c_t(n-t) + t \cdot c_t(n-t-1)]$ |
| `P'_1(n,k)` | Passing 1-ball, $k$ hands | $\sum_{h=1}^k \binom{k}{h} \binom{n-1}{h-1} (h-1)!$ |

## Usage

### Quick Start

Run all computations up to a given period `n` (default: 10, hands `k` default: 3):

```bash
python -m main 50 3
```

### Individual Modules

Each variation can be run independently:

```bash
# Compute c_t(n) values (the core function)
python -m src.ct 50

# Compute normal 2-ball prime patterns
python -m src.normal 50

# Compute multiplex 2-ball prime patterns
python -m src.multiplex 50

# Compute colored 2-ball prime patterns
python -m src.colored 50

# Compute base-state patterns
python -m src.base 50

# Compute passing 1-ball patterns (n, k)
python -m src.passing 50 3
```

### Test Script

A simple test script computes asymptotic constants:

```bash
python -m test 20
```

Note: the test script is capped at `n <= 20`.

### Output

Data is cached incrementally to:

- `data/ct_data.json` — cached $c_t(n)$ values
- `data/patterns_data.json` — cached pattern counts

To recompute from scratch, delete these files and re-run.

## Project Structure

```
.
├── main.py              # Manager script (runs all variations)
├── test.py              # Test script (capped at n=20)
├── pyproject.toml       # Package configuration
├── README.md            # This file
├── src/
│   ├── __init__.py      # Package exports
│   ├── tools.py         # Caching and I/O utilities
│   ├── ct.py            # Core c_t(n) computation (DP recurrence)
│   ├── normal.py        # Normal pattern counts
│   ├── multiplex.py     # Multiplex pattern counts
│   ├── colored.py       # Colored pattern counts
│   ├── base.py          # Base-state pattern counts
│   └── passing.py       # Passing pattern counts
├── data/
│   ├── ct_data.json     # Cached c_t(n) values
│   └── patterns_data.json  # Cached pattern counts
├── fast-ct/
│   └── main.tex         # Paper: "A Faster Way to Compute c_t(n)"
└── context/
    └── paper.txt        # Main paper: "Enumerating Prime Patterns in Juggling Variations"
```

## References

- Banaian, E., Butler, S., Cox, C., Davis, J., Landgraf, J., & Ponce, S. (2016). *Counting Prime Juggling Patterns*. Graphs and Combinatorics, 32(5), 1675–1688.
- Butler, S., Choi, V., Jeffries, J., McCambridge, N., Morgenstern, A., & Orellana Mateo, S. (2026). *Enumerating Prime Patterns in Juggling Variations*. arXiv:2603.17284.
- Orellana Mateo, S. (2026). *A Faster Way to Compute c_t(n)*. (Companion note.)
