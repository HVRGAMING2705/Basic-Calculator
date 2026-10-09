# NumPy Scientific Computing Lab

The original notebook did scalar arithmetic with NumPy. This lab shows
what NumPy is actually for: vectorized computation, broadcasting, and
linear algebra — plus hard numbers on why it matters.

## Features (`scientific.py`)

- **Vectorized arithmetic**: `add`, `multiply`, `power`,
  `safe_divide` (no ZeroDivisionError — returns inf/nan), `stats`
- **Broadcasting demos**: `rowwise_normalize`, `pairwise_distances`
  (distance matrix with zero Python loops), `outer_product_table`
- **Matrix operations**: `matmul`, `inverse`, `determinant`, `eigen`
  (eigenvalues/vectors), `solve_linear` (Ax = b),
  `least_squares_fit` (polynomial fit)

## Demos

- `benchmark.py` — Python loops vs NumPy for sum-of-squares and matrix
  multiplication, with `timeit` and a bar chart (`benchmark.png`).
- `least_squares.py` — fits a quadratic to noisy data and plots data,
  true curve, and fit (`least_squares.png`)

## How to run

```bash
pip install -r requirements.txt   # numpy, matplotlib
python benchmark.py
python least_squares.py
```

```python
from scientific import solve_linear, eigen
solve_linear([[3, 1], [1, 2]], [9, 8])   # array([2., 3.])
eigen([[2, 0], [0, 3]])                  # eigenvalues 2 and 3
```

## Sample output

```
n=1,000,000: python loop     98.15 ms | numpy    5.6 ms | speedup       18x
matmul 120x120: python loop   0.102 s | numpy    1.1 ms | speedup        90x
true coeffs:      [0.5, -3, 2]
fitted coeffs:    [0.475, -2.706, 1.511]
```
