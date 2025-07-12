"""
Test cases for CSTR (Continuous Stirred Tank Reactor) model

Tests cover initialization, dynamics, steady-state calculations,
performance metrics, and edge cases.

Author: SPROCLIB Development Team
"""

import pytest
import numpy as np
from unit.reactor.cstr import CSTR


class TestCSTR:
    """Test suite for CSTR model."""
    
    @pytest.fixture
    def default_cstr(self):
        """Create a CSTR instance with default parameters."""
        return CSTR()
    
    @pytest.fixture
    def test_inputs(self):
        """Standard test inputs for CSTR."""
        return np.array([10.0, 1.0, 350.0, 300.0])  # [q, CAi, Ti, Tc]
    
    @pytest.fixture
    def test_state(self):
        """Standard test state for CSTR."""
        return np.array([0.5, 360.0])  # [CA, T]
    
    def test_initialization_default(self):
        """Test CSTR initialization with default parameters."""
        cstr = CSTR()
        
        assert cstr.V == 100.0
        assert cstr.k0 == 7.2e10
        assert cstr.Ea == 72750.0
        assert cstr.R == 8.314
        assert cstr.rho == 1000.0
        assert cstr.Cp == 0.239
        assert cstr.dHr == -50000.0
        assert cstr.UA == 50000.0
        assert cstr.name == "CSTR"
    
    def test_initialization_custom(self):
        """Test CSTR initialization with custom parameters."""
        cstr = CSTR(
            V=200.0,
            k0=1e11,
            Ea=80000.0,
            name="CustomCSTR"
        )
        
        assert cstr.V == 200.0
        assert cstr.k0 == 1e11
        assert cstr.Ea == 80000.0
        assert cstr.name == "CustomCSTR"
    
    def test_reaction_rate(self, default_cstr):
        """Test reaction rate calculation."""
        T = 350.0
        k = default_cstr.reaction_rate(T)
        
        # Expected value based on Arrhenius equation
        expected_k = 7.2e10 * np.exp(-72750.0 / (8.314 * 350.0))
        
        assert abs(k - expected_k) < 1e-10
        assert k > 0
    
    def test_reaction_rate_temperature_dependence(self, default_cstr):
        """Test that reaction rate increases with temperature."""
        k1 = default_cstr.reaction_rate(300.0)
        k2 = default_cstr.reaction_rate(350.0)
        k3 = default_cstr.reaction_rate(400.0)
        
        assert k1 < k2 < k3
    
    def test_dynamics_calculation(self, default_cstr, test_state, test_inputs):
        """Test dynamics calculation."""
        t = 0.0
        dxdt = default_cstr.dynamics(t, test_state, test_inputs)
        
        assert len(dxdt) == 2
        assert isinstance(dxdt[0], (int, float, np.number))  # dCA/dt
        assert isinstance(dxdt[1], (int, float, np.number))  # dT/dt
    
    def test_dynamics_mass_balance(self, default_cstr):
        """Test mass balance in dynamics."""
        # Test case with no reaction (very low temperature)
        x = np.array([1.0, 250.0])  # Low temperature for minimal reaction
        u = np.array([10.0, 2.0, 250.0, 250.0])  # Higher inlet concentration
        
        dxdt = default_cstr.dynamics(0.0, x, u)
        
        # At low temperature, dCA/dt should be dominated by flow term
        # dCA/dt ≈ q/V*(CAi - CA) = 10/100*(2-1) = 0.1
        expected_flow_term = u[0]/default_cstr.V * (u[1] - x[0])
        
        assert abs(dxdt[0] - expected_flow_term) < 0.5  # Allow for small reaction term
    
    def test_dynamics_energy_balance(self, default_cstr):
        """Test energy balance in dynamics."""
        # Test case with no reaction and heat transfer
        x = np.array([0.0, 350.0])  # No concentration, so no reaction heat
        u = np.array([10.0, 0.0, 300.0, 320.0])  # Cooler inlet, warmer coolant
        
        dxdt = default_cstr.dynamics(0.0, x, u)
        
        # dT/dt should include flow term and heat transfer term
        flow_term = u[0]/default_cstr.V * (u[2] - x[1])
        heat_transfer_term = default_cstr.UA * (u[3] - x[1]) / (default_cstr.V * default_cstr.rho * default_cstr.Cp)
        expected_dTdt = flow_term + heat_transfer_term
        
        assert abs(dxdt[1] - expected_dTdt) < 1.0
    
    def test_steady_state_calculation(self, default_cstr, test_inputs):
        """Test steady-state calculation."""
        x_ss = default_cstr.steady_state(test_inputs)
        
        assert len(x_ss) == 2
        assert x_ss[0] >= 0  # Concentration should be non-negative
        assert x_ss[1] > 0   # Temperature should be positive
        
        # Check that steady-state satisfies dynamics = 0
        dxdt = default_cstr.dynamics(0.0, x_ss, test_inputs)
        assert abs(dxdt[0]) < 1e-6
        assert abs(dxdt[1]) < 1e-6
    
    def test_conversion_calculation(self, default_cstr):
        """Test conversion calculation."""
        CA = 0.5
        CAi = 1.0
        
        conversion = default_cstr.calculate_conversion(CA, CAi)
        expected_conversion = (CAi - CA) / CAi
        
        assert abs(conversion - expected_conversion) < 1e-10
        assert 0 <= conversion <= 1
    
    def test_conversion_edge_cases(self, default_cstr):
        """Test conversion calculation edge cases."""
        # Zero inlet concentration
        assert default_cstr.calculate_conversion(0.5, 0.0) == 0.0
        
        # Complete conversion
        assert default_cstr.calculate_conversion(0.0, 1.0) == 1.0
        
        # No conversion
        assert default_cstr.calculate_conversion(1.0, 1.0) == 0.0
    
    def test_residence_time_calculation(self, default_cstr):
        """Test residence time calculation."""
        q = 10.0
        tau = default_cstr.calculate_residence_time(q)
        expected_tau = default_cstr.V / q
        
        assert abs(tau - expected_tau) < 1e-10
    
    def test_residence_time_zero_flow(self, default_cstr):
        """Test residence time with zero flow rate."""
        tau = default_cstr.calculate_residence_time(0.0)
        assert tau == float('inf')
    
    def test_heat_generation_calculation(self, default_cstr):
        """Test heat generation calculation."""
        CA = 1.0
        T = 350.0
        
        Q_gen = default_cstr.calculate_heat_generation(CA, T)
        
        # Should be positive for exothermic reaction (heat generated)
        # Q_gen = (-dHr) * r * V, where dHr = -50000 (exothermic)
        assert Q_gen > 0
        assert isinstance(Q_gen, (int, float, np.number))
    
    def test_performance_metrics(self, default_cstr, test_state, test_inputs):
        """Test performance metrics calculation."""
        metrics = default_cstr.get_performance_metrics(test_state, test_inputs)
        
        expected_keys = [
            'conversion', 'residence_time', 'reaction_rate_constant',
            'heat_generation', 'productivity', 'selectivity', 'space_time_yield'
        ]
        
        for key in expected_keys:
            assert key in metrics
            assert isinstance(metrics[key], (int, float, np.number))
        
        # Check reasonable values
        assert 0 <= metrics['conversion'] <= 1
        assert metrics['residence_time'] > 0
        assert metrics['reaction_rate_constant'] > 0
        assert metrics['selectivity'] == 1.0  # Single reaction
    
    def test_describe_method(self, default_cstr):
        """Test describe method for metadata."""
        metadata = default_cstr.describe()
        
        # Check required keys exist
        required_keys = [
            'type', 'description', 'category', 'algorithms',
            'parameters', 'state_variables', 'inputs', 'outputs',
            'valid_ranges', 'applications', 'limitations'
        ]
        
        for key in required_keys:
            assert key in metadata
        
        assert metadata['type'] == 'CSTR'
        assert metadata['category'] == 'reactor'
        assert 'parameters' in metadata
        assert 'V' in metadata['parameters']
    
    def test_negative_concentration_handling(self, default_cstr):
        """Test handling of negative concentrations."""
        x = np.array([-0.1, 350.0])  # Negative concentration
        u = np.array([10.0, 1.0, 350.0, 300.0])
        
        dxdt = default_cstr.dynamics(0.0, x, u)
        
        # Should not crash and should handle gracefully
        assert len(dxdt) == 2
    
    def test_low_temperature_handling(self, default_cstr):
        """Test handling of very low temperatures."""
        x = np.array([1.0, 200.0])  # Very low temperature
        u = np.array([10.0, 1.0, 350.0, 300.0])
        
        dxdt = default_cstr.dynamics(0.0, x, u)
        
        # Should not crash and should handle gracefully
        assert len(dxdt) == 2
    
    def test_high_flow_rate(self, default_cstr):
        """Test with very high flow rate."""
        x = np.array([0.1, 350.0])
        u = np.array([1000.0, 1.0, 350.0, 300.0])  # Very high flow rate
        
        dxdt = default_cstr.dynamics(0.0, x, u)
        
        # Should approach plug flow behavior (high flow rate)
        assert len(dxdt) == 2
        assert not np.isnan(dxdt).any()
        assert not np.isinf(dxdt).any()
    
    def test_parameter_consistency(self, default_cstr):
        """Test that parameters are stored consistently."""
        assert default_cstr.parameters['V'] == default_cstr.V
        assert default_cstr.parameters['k0'] == default_cstr.k0
        assert default_cstr.parameters['Ea'] == default_cstr.Ea
    
    def test_state_variable_definitions(self, default_cstr):
        """Test state variable definitions."""
        assert 'CA' in default_cstr.state_variables
        assert 'T' in default_cstr.state_variables
        assert len(default_cstr.state_variables) == 2
    
    def test_input_variable_definitions(self, default_cstr):
        """Test input variable definitions."""
        expected_inputs = ['q', 'CAi', 'Ti', 'Tc']
        for inp in expected_inputs:
            assert inp in default_cstr.inputs
    
    def test_output_variable_definitions(self, default_cstr):
        """Test output variable definitions."""
        expected_outputs = ['CA', 'T', 'reaction_rate', 'heat_generation']
        for out in expected_outputs:
            assert out in default_cstr.outputs
