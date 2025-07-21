"""
Test file for ProcessOptimization class

This module contains test cases for the ProcessOptimization framework including
optimization algorithms, constraint handling, and engineering applications.
"""

import pytest
import numpy as np
from .process_optimization import ProcessOptimization


class TestProcessOptimization:
    """Test cases for ProcessOptimization class."""
    
    @pytest.fixture
    def default_instance(self):
        """Create a default ProcessOptimization instance for testing."""
        return ProcessOptimization("Test Optimization")
    
    def test_initialization(self, default_instance):
        """Test ProcessOptimization initialization."""
        assert default_instance.name == "Test Optimization"
        assert hasattr(default_instance, 'results')
        assert isinstance(default_instance.results, dict)
    
    def test_describe_method(self, default_instance):
        """Test the describe method returns proper metadata."""
        metadata = default_instance.describe()
        
        assert metadata['type'] == 'ProcessOptimization'
        assert 'description' in metadata
        assert 'algorithms' in metadata
        assert 'parameters' in metadata
        assert 'applications' in metadata
        assert 'limitations' in metadata
    
    def test_simple_optimization(self, default_instance):
        """Test basic optimization functionality."""
        # Minimize f(x) = (x-2)^2 + 1, minimum at x=2
        def objective(x):
            return (x[0] - 2.0)**2 + 1.0
        
        x0 = [0.0]  # Initial guess
        result = default_instance.optimize(objective, x0)
        
        assert result['success'] == True
        assert abs(result['x'][0] - 2.0) < 1e-3  # Should find minimum at x=2
        assert abs(result['fun'] - 1.0) < 1e-3   # Minimum value should be 1
    
    def test_constrained_optimization(self, default_instance):
        """Test optimization with constraints."""
        from scipy.optimize import LinearConstraint
        
        # Minimize f(x,y) = x^2 + y^2 subject to x + y >= 1
        def objective(x):
            return x[0]**2 + x[1]**2
        
        # Constraint: x + y >= 1 (or -x - y <= -1)
        constraint = LinearConstraint([[1, 1]], [-np.inf], [-1])
        
        x0 = [1.0, 1.0]  # Initial guess
        result = default_instance.optimize(objective, x0, constraints=constraint)
        
        assert result['success'] == True
        # Optimal solution should be approximately [0.5, 0.5]
        assert abs(result['x'][0] + result['x'][1] - 1.0) < 1e-3
    
    def test_bounded_optimization(self, default_instance):
        """Test optimization with bounds."""
        from scipy.optimize import Bounds
        
        # Minimize f(x) = (x-5)^2 with bounds 0 <= x <= 3
        def objective(x):
            return (x[0] - 5.0)**2
        
        bounds = Bounds([0], [3])  # x between 0 and 3
        
        x0 = [1.0]  # Initial guess
        result = default_instance.optimize(objective, x0, bounds=bounds)
        
        assert result['success'] == True
        # Should find boundary optimum at x=3 (closest to 5 within bounds)
        assert abs(result['x'][0] - 3.0) < 1e-3
    
    def test_chemical_engineering_example(self, default_instance):
        """Test optimization with chemical engineering parameters."""
        # Reactor optimization: minimize cost = capital + operating costs
        # Capital cost ∝ V^0.6, Operating cost ∝ 1/V (for given conversion)
        
        def reactor_cost(x):
            volume = x[0]  # m³
            if volume <= 0:
                return 1e6  # Penalty for invalid volume
            
            capital_cost = 10000 * (volume ** 0.6)  # $
            operating_cost = 50000 / volume  # $/year (normalized)
            return capital_cost + operating_cost
        
        # Bounds: 1 m³ <= V <= 100 m³
        from scipy.optimize import Bounds
        bounds = Bounds([1.0], [100.0])
        
        x0 = [10.0]  # Initial guess: 10 m³
        result = default_instance.optimize(reactor_cost, x0, bounds=bounds)
        
        assert result['success'] == True
        assert 1.0 <= result['x'][0] <= 100.0  # Within bounds
        assert result['x'][0] > 1.0  # Should not be at lower bound
    
    def test_heat_exchanger_optimization(self, default_instance):
        """Test heat exchanger area optimization."""
        # Minimize total cost = capital cost + pumping cost
        # For given heat duty Q and overall U
        
        def heat_exchanger_cost(x):
            area = x[0]  # m²
            if area <= 0:
                return 1e6
            
            # Heat transfer: Q = U * A * LMTD
            U = 500  # W/m²/K
            Q_required = 1e6  # W
            LMTD_required = Q_required / (U * area)
            
            if LMTD_required > 100:  # Practical limit
                return 1e6  # Penalty
            
            capital_cost = 1000 * area  # $
            # Pumping cost increases with pressure drop (∝ 1/area)
            pumping_cost = 5000 / area  # $/year (simplified)
            
            return capital_cost + pumping_cost
        
        from scipy.optimize import Bounds
        bounds = Bounds([1.0], [1000.0])  # 1 to 1000 m²
        
        x0 = [50.0]  # Initial guess
        result = default_instance.optimize(heat_exchanger_cost, x0, bounds=bounds)
        
        assert result['success'] == True
        assert 1.0 <= result['x'][0] <= 1000.0
    
    def test_edge_cases(self, default_instance):
        """Test edge cases and error handling."""
        # Test with invalid objective function
        def bad_objective(x):
            return float('inf')
        
        x0 = [1.0]
        result = default_instance.optimize(bad_objective, x0)
        
        # Should handle gracefully (may succeed or fail depending on scipy)
        assert 'success' in result
        
        # Test with empty initial guess
        with pytest.raises((ValueError, TypeError)):
            default_instance.optimize(lambda x: x[0]**2, [])
    
    def test_parameter_validation(self, default_instance):
        """Test parameter validation."""
        # Test name parameter
        opt = ProcessOptimization("")  # Empty name should work
        assert opt.name == ""
        
        # Test with None name
        with pytest.raises(TypeError):
            ProcessOptimization(None)
