"""
Tests for the Einstein tensor module.
"""

import pytest
import sympy as sp
from sympy import symbols, sin, cos, simplify

from itensorpy.metric import Metric
from itensorpy.ricci import RicciTensor, RicciScalar
from itensorpy.einstein import EinsteinTensor
from itensorpy.spacetimes import schwarzschild, minkowski, friedmann_lemaitre_robertson_walker


def test_flat_spacetime_einstein():
    """Test that the Einstein tensor vanishes in flat spacetime."""
    # Create a Minkowski metric
    metric = minkowski()
    
    # Compute Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # For flat spacetime, all components should be zero
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert einstein.get_component_lower(mu, nu) == 0
            assert einstein.get_component_upper(mu, nu) == 0


def test_sphere_einstein():
    """Test the Einstein tensor for a 2D sphere."""
    # Set up 2D sphere metric
    theta, phi = symbols('theta phi')
    coordinates = [theta, phi]  # Angular coordinates on the sphere
    
    # Metric for a sphere with radius a
    a = symbols('a', positive=True)  # Radius of the sphere
    g = sp.Matrix([[a**2, 0], [0, a**2 * sin(theta)**2]])
    metric = Metric(components=g, coordinates=coordinates)
    
    # Compute Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # For a 2D sphere, Einstein tensor is G_μν = 0 (in 2D, Einstein tensor vanishes)
    # This is because in 2D, the Ricci tensor is proportional to the metric:
    # R_μν = (R/2)g_μν, which makes G_μν = 0
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert simplify(einstein.get_component_lower(mu, nu)) == 0


def test_schwarzschild_einstein():
    """Test Einstein tensor components for Schwarzschild spacetime."""
    # Create Schwarzschild metric
    metric = schwarzschild()
    
    # Compute Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # Schwarzschild is a vacuum solution, so Einstein tensor should be zero
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert einstein.get_component_lower(mu, nu) == 0
            assert einstein.get_component_upper(mu, nu) == 0


def test_flrw_einstein():
    """Test Einstein tensor for FLRW metric."""
    # Create FLRW metric with zero curvature (k=0)
    metric = friedmann_lemaitre_robertson_walker(k=0)
    t, r, theta, phi = metric.coordinates
    a = metric.params[0]  # Scale factor
    
    # Get the time derivatives of a(t)
    adot = sp.diff(a, t)
    addot = sp.diff(adot, t)
    
    # Compute Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # For FLRW with k=0, we expect:
    # G_00 = 3(adot/a)^2
    # G_11 = -(2*addot/a + (adot/a)^2)
    # G_22 = -r^2(2*addot/a + (adot/a)^2)
    # G_33 = -r^2*sin^2(theta)(2*addot/a + (adot/a)^2)
    
    # Check G_00
    G_00 = einstein.get_component_lower(0, 0)
    expected00 = 3*(adot/a)**2
    assert simplify(G_00 - expected00) == 0
    
    # Check G_11
    G_11 = einstein.get_component_lower(1, 1)
    expected11 = -(2*addot/a + (adot/a)**2)
    assert simplify(G_11 - expected11) == 0
    
    # Check components with raised indices
    # G^0_0 should be -3(adot/a)^2
    G_00_up = einstein.get_component_upper(0, 0)
    expected00_up = -3*(adot/a)**2
    assert simplify(G_00_up - expected00_up) == 0


def test_einstein_creation_methods():
    """Test different ways to create Einstein tensor."""
    # Create a metric
    metric = schwarzschild()
    
    # Create Einstein tensor from metric
    einstein1 = EinsteinTensor.from_metric(metric)
    
    # Create Einstein tensor from Ricci tensor and scalar
    ricci = RicciTensor.from_metric(metric)
    ricci_scalar = RicciScalar.from_ricci(ricci)
    einstein2 = EinsteinTensor.from_ricci(ricci, ricci_scalar)
    
    # Both methods should give the same result
    n = metric.dimension
    for mu in range(n):
        for nu in range(n):
            assert simplify(einstein1.get_component_lower(mu, nu) - einstein2.get_component_lower(mu, nu)) == 0
            assert simplify(einstein1.get_component_upper(mu, nu) - einstein2.get_component_upper(mu, nu)) == 0


def test_einstein_field_equations():
    """Test Einstein's field equations for a simple case."""
    # Create FLRW metric with zero curvature (k=0)
    metric = friedmann_lemaitre_robertson_walker(k=0)
    t, r, theta, phi = metric.coordinates
    a = metric.params[0]  # Scale factor
    
    # Define energy-momentum tensor for perfect fluid
    rho = sp.Symbol('rho', real=True)  # Energy density
    p = sp.Symbol('p', real=True)      # Pressure
    
    # T_00 = rho, T_11 = p*g_11, T_22 = p*g_22, T_33 = p*g_33
    T = sp.zeros(4, 4)
    T[0, 0] = rho
    T[1, 1] = p * a**2
    T[2, 2] = p * a**2 * r**2
    T[3, 3] = p * a**2 * r**2 * sin(theta)**2
    
    # Compute Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # Get time derivatives of scale factor
    adot = sp.diff(a, t)
    addot = sp.diff(adot, t)
    
    # Einstein equations: G_μν = 8πGT_μν (we set 8πG = 1 for simplicity)
    # From G_00 = T_00, we get the Friedmann equation: 3(adot/a)^2 = rho
    G_00 = einstein.get_component_lower(0, 0)
    
    # Define Friedmann equation from Einstein tensor
    friedmann_eq = simplify(G_00 - rho)
    
    # Substituting rho = 3(adot/a)^2 should make the equation true
    rho_value = 3*(adot/a)**2
    assert simplify(friedmann_eq.subs(rho, rho_value)) == 0
    
    # From G_11 = T_11, we get: -(2*addot/a + (adot/a)^2) = p
    G_11 = einstein.get_component_lower(1, 1)
    
    # Define acceleration equation from Einstein tensor
    accel_eq = simplify(G_11 - p * a**2)
    
    # Substituting p = -(2*addot/a + (adot/a)^2)/a^2 should make the equation true
    p_value = -(2*addot/a + (adot/a)**2)/a**2
    assert simplify(accel_eq.subs(p, p_value)) == 0


def test_nonzero_components():
    """Test getting non-zero components of Einstein tensor."""
    # Create FLRW metric which has non-zero Einstein tensor
    metric = friedmann_lemaitre_robertson_walker(k=0)
    
    # Compute Einstein tensor
    einstein = EinsteinTensor.from_metric(metric)
    
    # Get non-zero components
    nonzero_lower = einstein.get_nonzero_components_lower()
    nonzero_upper = einstein.get_nonzero_components_upper()
    
    # FLRW should have G_00, G_11, G_22, G_33 non-zero
    assert len(nonzero_lower) >= 4  # May be more due to symmetry in indices
    assert (0, 0) in nonzero_lower
    assert (1, 1) in nonzero_lower
    assert (2, 2) in nonzero_lower
    assert (3, 3) in nonzero_lower
    
    # Similarly for upper components
    assert (0, 0) in nonzero_upper 