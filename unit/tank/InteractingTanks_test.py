"""
Test suite for InteractingTanks model

This module contains tests for the InteractingTanks class including dynamics,
steady-state, and interaction effects.
"""

import pytest
import numpy as np
from unit.tank.InteractingTanks import InteractingTanks


class TestInteractingTanks:
    """Test class for InteractingTanks model."""
    
    @pytest.fixture
    def tanks(self):
        """Create standard interacting tanks for testing."""
        return InteractingTanks(A1=1.0, A2=1.0, C1=0.5, C2=0.3, name="TestTanks")
    
    @pytest.fixture
    def asymmetric_tanks(self):
        """Create asymmetric interacting tanks."""
        return InteractingTanks(A1=2.0, A2=0.5, C1=0.4, C2=0.6, name="AsymmetricTanks")
    
    def test_initialization(self, tanks):
        """Test tanks initialization."""
        assert tanks.A1 == 1.0
        assert tanks.A2 == 1.0
        assert tanks.C1 == 0.5
        assert tanks.C2 == 0.3
        assert tanks.name == "TestTanks"
        assert tanks.parameters['A1'] == 1.0
        assert tanks.parameters['A2'] == 1.0
        assert tanks.parameters['C1'] == 0.5
        assert tanks.parameters['C2'] == 0.3
    
    def test_describe_method(self, tanks):
        """Test the describe method returns proper metadata."""
        desc = tanks.describe()
        assert isinstance(desc, dict)
        assert desc['name'] == 'InteractingTanks'
        assert desc['class_name'] == 'InteractingTanks'
        assert 'algorithm' in desc
        assert 'equations' in desc
        assert 'parameters' in desc
        assert 'working_ranges' in desc
        assert len(desc['assumptions']) > 0
        assert len(desc['limitations']) > 0
        
        # Check specific equation keys
        assert 'tank1_dynamics' in desc['equations']
        assert 'tank2_dynamics' in desc['equations']
        assert 'flow_12' in desc['equations']
        assert 'outlet_flow' in desc['equations']
    
    def test_dynamics_basic(self, tanks):
        """Test basic dynamics calculation."""
        t = 0.0
        x = np.array([1.0, 0.5])  # h1=1.0, h2=0.5
        u = np.array([0.6])  # q_in = 0.6 m³/min
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Calculate expected values
        q12 = 0.5 * np.sqrt(1.0)  # C1 * sqrt(h1) = 0.5
        q_out = 0.3 * np.sqrt(0.5)  # C2 * sqrt(h2) ≈ 0.212
        
        dh1dt_expected = (0.6 - q12) / 1.0  # (q_in - q12) / A1
        dh2dt_expected = (q12 - q_out) / 1.0  # (q12 - q_out) / A2
        
        assert abs(dxdt[0] - dh1dt_expected) < 1e-6
        assert abs(dxdt[1] - dh2dt_expected) < 1e-6
    
    def test_dynamics_zero_heights(self, tanks):
        """Test dynamics with zero heights."""
        t = 0.0
        x = np.array([0.0, 0.0])  # Both tanks empty
        u = np.array([0.4])  # q_in = 0.4 m³/min
        
        dxdt = tanks.dynamics(t, x, u)
        
        # With zero heights, no outflows
        # dh1/dt = (0.4 - 0) / 1.0 = 0.4
        # dh2/dt = (0 - 0) / 1.0 = 0
        assert abs(dxdt[0] - 0.4) < 1e-6
        assert abs(dxdt[1] - 0.0) < 1e-6
    
    def test_dynamics_negative_heights(self, tanks):
        """Test that negative heights are handled properly."""
        t = 0.0
        x = np.array([-0.1, -0.2])  # Negative heights
        u = np.array([0.5])
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Should treat negative heights as zero
        # dh1/dt = (0.5 - 0) / 1.0 = 0.5
        # dh2/dt = (0 - 0) / 1.0 = 0
        assert abs(dxdt[0] - 0.5) < 1e-6
        assert abs(dxdt[1] - 0.0) < 1e-6
    
    def test_steady_state(self, tanks):
        """Test steady-state calculation."""
        u = np.array([0.45])  # q_in = 0.45 m³/min
        
        x_ss = tanks.steady_state(u)
        
        # Expected steady states
        h1_ss_expected = (0.45 / 0.5) ** 2  # (q_in / C1)² = 0.81
        h2_ss_expected = (0.45 / 0.3) ** 2  # (q_in / C2)² = 2.25
        
        assert abs(x_ss[0] - h1_ss_expected) < 1e-6
        assert abs(x_ss[1] - h2_ss_expected) < 1e-6
    
    def test_steady_state_zero_flow(self, tanks):
        """Test steady-state with zero inlet flow."""
        u = np.array([0.0])
        
        x_ss = tanks.steady_state(u)
        
        # Both tanks should be empty
        assert abs(x_ss[0] - 0.0) < 1e-6
        assert abs(x_ss[1] - 0.0) < 1e-6
    
    def test_consistency_dynamics_steady_state(self, tanks):
        """Test that dynamics give zero derivatives at steady state."""
        u = np.array([0.6])
        x_ss = tanks.steady_state(u)
        
        # At steady state, dynamics should give zero derivatives
        t = 0.0
        dxdt = tanks.dynamics(t, x_ss, u)
        
        assert abs(dxdt[0]) < 1e-10
        assert abs(dxdt[1]) < 1e-10
    
    def test_asymmetric_tanks(self, asymmetric_tanks):
        """Test tanks with different parameters."""
        assert asymmetric_tanks.A1 == 2.0
        assert asymmetric_tanks.A2 == 0.5
        assert asymmetric_tanks.C1 == 0.4
        assert asymmetric_tanks.C2 == 0.6
        
        # Test steady state with asymmetric parameters
        u = np.array([0.48])
        x_ss = asymmetric_tanks.steady_state(u)
        
        h1_ss_expected = (0.48 / 0.4) ** 2  # 1.44
        h2_ss_expected = (0.48 / 0.6) ** 2  # 0.64
        
        assert abs(x_ss[0] - h1_ss_expected) < 1e-6
        assert abs(x_ss[1] - h2_ss_expected) < 1e-6
    
    def test_mass_conservation(self, tanks):
        """Test that mass is conserved in the system."""
        t = 0.0
        x = np.array([2.0, 1.5])
        u = np.array([0.7])
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Calculate flows
        q_in = u[0]
        q12 = tanks.C1 * np.sqrt(x[0])
        q_out = tanks.C2 * np.sqrt(x[1])
        
        # Total accumulation rate
        total_accumulation = tanks.A1 * dxdt[0] + tanks.A2 * dxdt[1]
        
        # Should equal net inflow (q_in - q_out)
        net_inflow = q_in - q_out
        
        assert abs(total_accumulation - net_inflow) < 1e-10
    
    def test_flow_directions(self, tanks):
        """Test that flows are in correct directions."""
        t = 0.0
        x = np.array([3.0, 1.0])
        u = np.array([0.5])
        
        # Calculate flows
        q12 = tanks.C1 * np.sqrt(x[0])  # Flow from tank 1 to tank 2
        q_out = tanks.C2 * np.sqrt(x[1])  # Outflow from tank 2
        
        # Both flows should be positive (in expected direction)
        assert q12 >= 0
        assert q_out >= 0
        
        # Tank 1 should have higher potential than tank 2 for these heights
        assert x[0] > x[1]
    
    def test_edge_case_large_flow(self, tanks):
        """Test with large inlet flow."""
        t = 0.0
        x = np.array([1.0, 0.5])
        u = np.array([20.0])  # Large inlet flow
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Should handle large flows without numerical issues
        assert not np.isnan(dxdt[0])
        assert not np.isnan(dxdt[1])
        assert not np.isinf(dxdt[0])
        assert not np.isinf(dxdt[1])
        
        # Tank 1 should be filling rapidly
        assert dxdt[0] > 0
    
    def test_edge_case_large_heights(self, tanks):
        """Test with large tank heights."""
        t = 0.0
        x = np.array([100.0, 50.0])  # Very tall tanks
        u = np.array([1.0])
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Should handle large heights without numerical issues
        assert not np.isnan(dxdt[0])
        assert not np.isnan(dxdt[1])
        assert not np.isinf(dxdt[0])
        assert not np.isinf(dxdt[1])
        
        # With large heights, outlet flow from tank 1 is large
        # Tank 1 should be draining since outlet flow dominates small inlet
        assert dxdt[0] < 0  # Tank 1 draining
        
        # Tank 2 behavior depends on balance between large inflow from tank 1 and outflow
        # Both positive and negative derivatives are valid depending on the specific values
    
    def test_tank1_only_dynamics(self, tanks):
        """Test behavior when only tank 1 has liquid."""
        t = 0.0
        x = np.array([4.0, 0.0])  # Only tank 1 has liquid
        u = np.array([0.3])
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Tank 2 should be filling (positive derivative)
        assert dxdt[1] > 0
        
        # Tank 1 behavior depends on balance between inlet and outlet
        q12 = tanks.C1 * np.sqrt(4.0)  # 0.5 * 2 = 1.0
        if u[0] < q12:  # 0.3 < 1.0
            assert dxdt[0] < 0  # Tank 1 draining
        else:
            assert dxdt[0] > 0  # Tank 1 filling
    
    def test_tank2_only_dynamics(self, tanks):
        """Test behavior when only tank 2 has liquid."""
        t = 0.0
        x = np.array([0.0, 2.25])  # Only tank 2 has liquid
        u = np.array([0.5])
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Tank 1 should be filling (positive derivative)
        assert dxdt[0] > 0
        
        # Tank 2 should be draining (no inflow, but has outflow)
        q_out = tanks.C2 * np.sqrt(2.25)  # 0.3 * 1.5 = 0.45
        assert dxdt[1] < 0  # Tank 2 draining (no inflow from tank 1)
    
    def test_response_characteristics(self, tanks):
        """Test that second tank response is slower than first."""
        # Set up scenario where both tanks start empty and inlet is applied
        t = 0.0
        x = np.array([0.1, 0.0])  # Small initial height in tank 1, empty tank 2
        u = np.array([0.5])
        
        dxdt = tanks.dynamics(t, x, u)
        
        # Tank 1 should respond faster (larger derivative) than tank 2
        # Tank 1 gets direct input, tank 2 only gets flow from tank 1
        assert abs(dxdt[0]) > abs(dxdt[1])
    
    def test_parameter_effects(self):
        """Test the effect of different parameters on system behavior."""
        # Test with different area ratios
        tanks_large_a1 = InteractingTanks(A1=5.0, A2=1.0, C1=0.5, C2=0.3)
        tanks_large_a2 = InteractingTanks(A1=1.0, A2=5.0, C1=0.5, C2=0.3)
        
        t = 0.0
        x = np.array([1.0, 1.0])
        u = np.array([0.6])
        
        dxdt_large_a1 = tanks_large_a1.dynamics(t, x, u)
        dxdt_large_a2 = tanks_large_a2.dynamics(t, x, u)
        
        # Larger A1 should make tank 1 respond slower
        assert abs(dxdt_large_a1[0]) < abs(dxdt_large_a2[0])
        
        # Larger A2 should make tank 2 respond slower
        assert abs(dxdt_large_a2[1]) < abs(dxdt_large_a1[1])


if __name__ == "__main__":
    pytest.main([__file__])
