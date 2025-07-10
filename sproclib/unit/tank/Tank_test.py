"""
Test suite for Tank model

This module contains tests for the Tank class including dynamics, steady-state,
and performance metrics calculations.
"""

import pytest
import numpy as np
from unit.tank.Tank import Tank


class TestTank:
    """Test class for Tank model."""
    
    @pytest.fixture
    def tank(self):
        """Create a standard tank for testing."""
        return Tank(A=1.0, C=0.5, name="TestTank")
    
    @pytest.fixture
    def custom_tank(self):
        """Create a custom tank with different parameters."""
        return Tank(A=2.0, C=0.3, name="CustomTank")
    
    def test_initialization(self, tank):
        """Test tank initialization."""
        assert tank.A == 1.0
        assert tank.C == 0.5
        assert tank.name == "TestTank"
        assert 'A' in tank.parameters
        assert 'C' in tank.parameters
        assert tank.parameters['A'] == 1.0
        assert tank.parameters['C'] == 0.5
    
    def test_describe_method(self, tank):
        """Test the describe method returns proper metadata."""
        desc = tank.describe()
        assert isinstance(desc, dict)
        assert desc['name'] == 'Tank'
        assert desc['class_name'] == 'Tank'
        assert 'algorithm' in desc
        assert 'equations' in desc
        assert 'parameters' in desc
        assert 'working_ranges' in desc
        assert len(desc['assumptions']) > 0
        assert len(desc['limitations']) > 0
    
    def test_dynamics_basic(self, tank):
        """Test basic dynamics calculation."""
        # Test with positive height and flow
        t = 0.0
        x = np.array([1.0])  # height = 1.0 m
        u = np.array([0.8])  # q_in = 0.8 m³/min
        
        dxdt = tank.dynamics(t, x, u)
        
        # Expected: dh/dt = (0.8 - 0.5*sqrt(1.0))/1.0 = 0.3
        expected = 0.8 - 0.5 * np.sqrt(1.0)
        assert abs(dxdt[0] - expected) < 1e-6
    
    def test_dynamics_zero_height(self, tank):
        """Test dynamics with zero height."""
        t = 0.0
        x = np.array([0.0])  # height = 0.0 m
        u = np.array([0.5])  # q_in = 0.5 m³/min
        
        dxdt = tank.dynamics(t, x, u)
        
        # Expected: dh/dt = (0.5 - 0.5*sqrt(0.0))/1.0 = 0.5
        expected = 0.5
        assert abs(dxdt[0] - expected) < 1e-6
    
    def test_dynamics_negative_height(self, tank):
        """Test that negative heights are handled properly."""
        t = 0.0
        x = np.array([-0.1])  # negative height
        u = np.array([0.5])
        
        dxdt = tank.dynamics(t, x, u)
        
        # Should treat negative height as zero
        expected = 0.5  # (0.5 - 0.5*sqrt(0))/1.0
        assert abs(dxdt[0] - expected) < 1e-6
    
    def test_steady_state(self, tank):
        """Test steady-state calculation."""
        u = np.array([0.6])  # q_in = 0.6 m³/min
        
        x_ss = tank.steady_state(u)
        
        # Expected: h_ss = (0.6/0.5)² = 1.44
        expected = (0.6 / 0.5) ** 2
        assert abs(x_ss[0] - expected) < 1e-6
    
    def test_steady_state_zero_flow(self, tank):
        """Test steady-state with zero inlet flow."""
        u = np.array([0.0])
        
        x_ss = tank.steady_state(u)
        
        # Expected: h_ss = 0
        assert abs(x_ss[0] - 0.0) < 1e-6
    
    def test_calculate_outlet_flow(self, tank):
        """Test outlet flow calculation."""
        # Test with positive height
        h = 4.0
        q_out = tank.calculate_outlet_flow(h)
        expected = 0.5 * np.sqrt(4.0)  # 0.5 * 2 = 1.0
        assert abs(q_out - expected) < 1e-6
        
        # Test with zero height
        q_out_zero = tank.calculate_outlet_flow(0.0)
        assert abs(q_out_zero - 0.0) < 1e-6
        
        # Test with negative height (should be treated as zero)
        q_out_neg = tank.calculate_outlet_flow(-1.0)
        assert abs(q_out_neg - 0.0) < 1e-6
    
    def test_calculate_volume(self, tank):
        """Test volume calculation."""
        # Test with positive height
        h = 3.0
        volume = tank.calculate_volume(h)
        expected = 1.0 * 3.0  # A * h = 3.0
        assert abs(volume - expected) < 1e-6
        
        # Test with zero height
        volume_zero = tank.calculate_volume(0.0)
        assert abs(volume_zero - 0.0) < 1e-6
        
        # Test with negative height (should be treated as zero)
        volume_neg = tank.calculate_volume(-1.0)
        assert abs(volume_neg - 0.0) < 1e-6
    
    def test_calculate_time_constant(self, tank):
        """Test time constant calculation."""
        # Test with positive height
        h_op = 1.0
        tau = tank.calculate_time_constant(h_op)
        expected = 2 * 1.0 * np.sqrt(1.0) / 0.5  # 2 * A * sqrt(h) / C = 4.0
        assert abs(tau - expected) < 1e-6
        
        # Test with zero height (should return infinity)
        tau_zero = tank.calculate_time_constant(0.0)
        assert tau_zero == float('inf')
    
    def test_get_performance_metrics(self, tank):
        """Test performance metrics calculation."""
        x = np.array([2.25])  # height = 2.25 m
        u = np.array([0.75])  # q_in = 0.75 m³/min
        
        metrics = tank.get_performance_metrics(x, u)
        
        # Check all expected keys are present
        expected_keys = ['height', 'outlet_flow', 'volume', 'time_constant', 
                        'mass_balance_error', 'residence_time']
        for key in expected_keys:
            assert key in metrics
        
        # Check specific values
        assert abs(metrics['height'] - 2.25) < 1e-6
        assert abs(metrics['outlet_flow'] - 0.5 * np.sqrt(2.25)) < 1e-6
        assert abs(metrics['volume'] - 1.0 * 2.25) < 1e-6
        
        # At steady state for q_in = 0.75: h_ss = (0.75/0.5)² = 2.25
        # So mass balance error should be very small
        q_out_expected = 0.5 * np.sqrt(2.25)
        mass_balance_error = 0.75 - q_out_expected
        assert abs(metrics['mass_balance_error'] - mass_balance_error) < 1e-6
    
    def test_custom_parameters(self, custom_tank):
        """Test tank with custom parameters."""
        assert custom_tank.A == 2.0
        assert custom_tank.C == 0.3
        
        # Test steady state with custom parameters
        u = np.array([0.6])
        x_ss = custom_tank.steady_state(u)
        expected = (0.6 / 0.3) ** 2  # (2.0)² = 4.0
        assert abs(x_ss[0] - expected) < 1e-6
    
    def test_edge_case_large_flow(self, tank):
        """Test with large inlet flow."""
        t = 0.0
        x = np.array([1.0])
        u = np.array([10.0])  # Large inlet flow
        
        dxdt = tank.dynamics(t, x, u)
        
        # Should handle large flows without numerical issues
        assert not np.isnan(dxdt[0])
        assert not np.isinf(dxdt[0])
        assert dxdt[0] > 0  # Tank should be filling
    
    def test_edge_case_large_height(self, tank):
        """Test with large tank height."""
        t = 0.0
        x = np.array([100.0])  # Very tall tank
        u = np.array([1.0])
        
        dxdt = tank.dynamics(t, x, u)
        
        # Should handle large heights without numerical issues
        assert not np.isnan(dxdt[0])
        assert not np.isinf(dxdt[0])
        # With large height, outlet flow dominates, so tank should be draining
        assert dxdt[0] < 0
    
    def test_consistency_dynamics_steady_state(self, tank):
        """Test that dynamics give zero derivative at steady state."""
        u = np.array([0.8])
        x_ss = tank.steady_state(u)
        
        # At steady state, dynamics should give zero derivative
        t = 0.0
        dxdt = tank.dynamics(t, x_ss, u)
        
        assert abs(dxdt[0]) < 1e-10
    
    def test_state_input_output_definitions(self, tank):
        """Test that state, input, and output definitions are correct."""
        assert 'h' in tank.state_variables
        assert tank.state_variables['h'] == 'Tank height [m]'
        
        assert 'q_in' in tank.inputs
        assert tank.inputs['q_in'] == 'Inlet flow rate [m³/min]'
        
        assert 'h' in tank.outputs
        assert 'q_out' in tank.outputs
        assert 'volume' in tank.outputs


if __name__ == "__main__":
    pytest.main([__file__])
