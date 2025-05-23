# iTensorPy


<p align="center">
  <img src="./logo.png" alt="iTensorPy Logo" width="300px">
</p>

[![Python Tests](https://github.com/Klaudiusz321/itensorpy/workflows/Python%20Tests/badge.svg)](https://github.com/Klaudiusz321/itensorpy/actions)
[![Codecov](https://codecov.io/gh/Klaudiusz321/itensorpy/branch/main/graph/badge.svg)](https://codecov.io/gh/Klaudiusz321/itensorpy)
[![PyPI version](https://badge.fury.io/py/itensorpy.svg)](https://badge.fury.io/py/itensorpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for tensor calculations in general relativity.

## Overview

iTensorPy is a symbolic tensor library for general relativity calculations. It provides tools for working with metrics, computing Christoffel symbols, Riemann and Ricci tensors, Einstein tensors, and other tensor operations relevant to general relativity and differential geometry.

## Features

- Symbolic manipulation of tensor expressions using SymPy
- Metric tensor support with easy definition and manipulation
- Automatic computation of:
  - Christoffel symbols with specialized handling for common metrics
  - Riemann curvature tensor
  - Ricci tensor and scalar
  - Einstein tensor
  - Curvature invariants (Kretschmann, Euler, and Chern-Pontryagin scalars)
- Common spacetime metrics included:
  - Minkowski (flat spacetime)
  - Schwarzschild (spherically symmetric black hole)
  - Kerr (rotating black hole)
  - Friedmann-Lemaître-Robertson-Walker (cosmological)
  - de Sitter and Anti-de Sitter
- Support for custom metrics via dictionary input or file loading
- Optimized calculations for known special cases
- New tensor operations systems with modular design (v0.3.0+)

## What's New in Version 0.3.0

- New modular architecture with specialized modules:
  - `tensor_ops`: Core tensor operations including arithmetic, contractions, and Einstein summation
  - `matrix_ops`: Matrix operations for determinants, eigenvalues, and linear solving
  - `differential_ops`: Differential operators like gradient, divergence, curl and Laplacian
- New `Field` class for handling tensor fields in different coordinate systems
- Enhanced tensor operations via the new `TensorND` class
- Improved performance for large tensor calculations
- Better simplification strategies for complex tensor expressions
- Enhanced documentation and examples
- Bug fixes and stability improvements

## What's New in Version 0.2.0

- Improved Christoffel symbols implementation with robust formula handling
- Specialized handling for common metrics including:
  - 2D sphere
  - Schwarzschild spacetime
  - Time-dependent metrics
- Fixed curvature scalar calculations:
  - Kretschmann scalar now correctly computes the contraction R_{abcd}R^{abcd}
  - Special case handling for Schwarzschild metrics gives exact analytical result
- Better mathematical equivalence testing using SymPy's simplify functions
- Enhanced performance and accuracy for tensor calculations

## Installation

```bash
pip install itensorpy
```

Or install from source:

```bash
git clone https://github.com/yourusername/itensorpy.git
cd itensorpy
pip install -e .
```

## Quick Examples

### Creating a Metric and Computing Tensors

```python
import sympy as sp
from sympy import symbols, sin
from itensorpy import Metric, ChristoffelSymbols, RiemannTensor, RicciTensor, RicciScalar, EinsteinTensor

# Define coordinates
t, r, theta, phi = symbols('t r theta phi')
coordinates = [t, r, theta, phi]

# Define a spherically symmetric metric
g_tt = -(1 - 2/r)  # Using units where M=1
g_rr = 1/(1 - 2/r)
g_theta_theta = r**2
g_phi_phi = r**2 * sin(theta)**2

# Create components dictionary
components = {
    (0, 0): g_tt,
    (1, 1): g_rr,
    (2, 2): g_theta_theta,
    (3, 3): g_phi_phi
}

# Create the metric
metric = Metric(components=components, coordinates=coordinates)

# Compute and display tensors
christoffel = ChristoffelSymbols.from_metric(metric)
riemann = RiemannTensor.from_metric(metric)
ricci = RicciTensor.from_metric(metric)
scalar = RicciScalar.from_ricci(ricci)
einstein = EinsteinTensor.from_metric(metric)

print(christoffel)
print(riemann)
print(ricci)
print(scalar)
print(einstein)
```

### Using Predefined Spacetimes

```python
from itensorpy.spacetimes import schwarzschild, minkowski
from itensorpy import ChristoffelSymbols, CurvatureInvariants

# Create a Schwarzschild metric
sch_metric = schwarzschild()
print(sch_metric)

# Compute Christoffel symbols
christoffel = ChristoffelSymbols.from_metric(sch_metric)
print(christoffel)

# Compute curvature invariants
curvature = CurvatureInvariants(sch_metric)
kretschmann = curvature.kretschmann_scalar()
print(f"Kretschmann scalar: {kretschmann}")  # Should be 48M²/r⁶

# Compute Einstein tensor (should be zero for vacuum solution)
sch_einstein = EinsteinTensor.from_metric(sch_metric)
print(sch_einstein)
```

### Using the New Field Class (v0.3.0+)

```python
import sympy as sp
from sympy import symbols, sin, cos
from itensorpy.differential_ops import Field

# Define coordinates
x, y, z = symbols('x y z')

# Define a vector field (e.g., electric field from a point charge)
Ex = x / (x**2 + y**2 + z**2)**(3/2)
Ey = y / (x**2 + y**2 + z**2)**(3/2)
Ez = z / (x**2 + y**2 + z**2)**(3/2)

# Create a field object
E_field = Field([Ex, Ey, Ez], coordinates=[x, y, z])

# Compute the divergence (should be zero except at origin)
div_E = E_field.divergence()
print(f"Divergence of E: {div_E}")

# Compute the curl (should be zero for conservative field)
curl_E = E_field.curl()
print(f"Curl of E: {curl_E}")
```

## Development and Testing

iTensorPy uses pytest for testing. To run the tests, clone the repository and run:

```bash
pip install -e ".[dev]"  # Install development dependencies
pytest                   # Run all tests
pytest -v                # Run with verbose output
pytest --cov=itensorpy   # Run with coverage report
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
