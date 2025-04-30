"""
Tests for the Ricci tensor and scalar curvature module.
"""

import pytest
import sympy as sp
from sympy import symbols, sin, cos, simplify

from itensorpy.metric import Metric
from itensorpy.riemann import RiemannTensor
from itensorpy.ricci import RicciTensor, RicciScalar
from itensorpy.spacetimes import schwarzschild, minkowski, friedmann_lemaitre_robertson_walker


def test_flat_spacetime_ricci():
    """Test that the Ricci tensor vanishes in flat spacetime."""
    # Create a Minkowski metric
    metric = minkowski()
    
    # Compute Ricci tensor
    ricci = RicciTensor.from_metric(metric)
    
    # For flat spacetime, all components should be zero
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert ricci.get_component(mu, nu) == 0
    
    # The Ricci scalar should also be zero
    ricci_scalar = RicciScalar.from_ricci(ricci)
    assert ricci_scalar.get_value() == 0


def test_sphere_ricci():
    """Test the Ricci tensor for a 2D sphere."""
    # Set up 2D sphere metric
    theta, phi = symbols('theta phi')
    coordinates = [theta, phi]  # Angular coordinates on the sphere
    
    # Metric for a sphere with radius a
    a = symbols('a', positive=True)  # Radius of the sphere
    g = sp.Matrix([[a**2, 0], [0, a**2 * sin(theta)**2]])
    metric = Metric(components=g, coordinates=coordinates)
    
    # Compute Riemann tensor
    riemann = RiemannTensor.from_metric(metric)
    
    # Compute Ricci tensor
    ricci = RicciTensor.from_riemann(riemann)
    
    # For a sphere of radius a, Ricci tensor components are:
    # R_00 = 1/a^2
    # R_11 = sin^2(theta)/a^2
    
    # Check R_00
    R_00 = ricci.get_component(0, 0)
    assert simplify(R_00 - 1/a**2) == 0
    
    # Check R_11
    R_11 = ricci.get_component(1, 1)
    assert simplify(R_11 - sin(theta)**2/a**2) == 0
    
    # Ricci scalar for a sphere is 2/a^2
    ricci_scalar = RicciScalar.from_ricci(ricci)
    R = ricci_scalar.get_value()
    assert simplify(R - 2/a**2) == 0


def test_schwarzschild_ricci():
    """Test Ricci tensor components for Schwarzschild spacetime."""
    # Create Schwarzschild metric
    metric = schwarzschild()
    
    # Compute Ricci tensor
    ricci = RicciTensor.from_metric(metric)
    
    # Schwarzschild is a vacuum solution, so Ricci tensor should be zero
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert ricci.get_component(mu, nu) == 0
    
    # The Ricci scalar should also be zero
    ricci_scalar = RicciScalar.from_ricci(ricci)
    assert ricci_scalar.get_value() == 0


def test_flrw_ricci():
    """Test Ricci tensor for FLRW metric."""
    # Create FLRW metric with zero curvature (k=0)
    metric = friedmann_lemaitre_robertson_walker(k=0)
    t, r, theta, phi = metric.coordinates
    a = metric.params[0]  # Scale factor
    
    # Get the time derivatives of a(t)
    adot = sp.diff(a, t)
    addot = sp.diff(adot, t)
    
    # Compute Ricci tensor
    ricci = RicciTensor.from_metric(metric)
    
    # For FLRW with k=0, we expect:
    # R_00 = -3*addot/a
    # R_11 = a*addot + 2*adot**2
    # R_22 = r**2 * (a*addot + 2*adot**2)
    # R_33 = r**2*sin(theta)**2 * (a*addot + 2*adot**2)
    
    # Check R_00
    R_00 = ricci.get_component(0, 0)
    assert simplify(R_00 + 3*addot/a) == 0
    
    # Check R_11
    R_11 = ricci.get_component(1, 1)
    expected = a*addot + 2*adot**2
    assert simplify(R_11 - expected) == 0
    
    # Compute Ricci scalar
    ricci_scalar = RicciScalar.from_ricci(ricci)
    R = ricci_scalar.get_value()
    
    # For FLRW with k=0, Ricci scalar is 6*(addot/a + (adot/a)**2)
    expected_R = 6*(addot/a + (adot/a)**2)
    assert simplify(R - expected_R) == 0


def test_ricci_creation_methods():
    """Test different ways to create Ricci tensor and scalar."""
    # Create a metric
    metric = schwarzschild()
    
    # Create Ricci tensor from metric
    ricci1 = RicciTensor.from_metric(metric)
    
    # Create Riemann tensor first
    riemann = RiemannTensor.from_metric(metric)
    ricci2 = RicciTensor.from_riemann(riemann)
    
    # Both methods should give the same result
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert simplify(ricci1.get_component(mu, nu) - ricci2.get_component(mu, nu)) == 0
    
    # Test creating Ricci scalar
    scalar1 = RicciScalar.from_metric(metric)
    scalar2 = RicciScalar.from_ricci(ricci1)
    
    assert simplify(scalar1.get_value() - scalar2.get_value()) == 0


def test_nonzero_components():
    """Test getting non-zero components of Ricci tensor."""
    # Create a simple metric with known non-zero Ricci components
    theta, phi = symbols('theta phi')
    a = symbols('a', positive=True)
    
    # 2D sphere metric
    g = sp.Matrix([[a**2, 0], [0, a**2 * sin(theta)**2]])
    metric = Metric(components=g, coordinates=[theta, phi])
    
    # Compute Ricci tensor
    ricci = RicciTensor.from_metric(metric)
    
    # Get non-zero components
    nonzero = ricci.get_nonzero_components()
    
    # For sphere, only R_00 and R_11 are non-zero
    assert len(nonzero) == 2
    assert (0, 0) in nonzero
    assert (1, 1) in nonzero
    
    # Check the values
    assert simplify(nonzero[(0, 0)] - 1/a**2) == 0
    assert simplify(nonzero[(1, 1)] - sin(theta)**2/a**2) == 0 