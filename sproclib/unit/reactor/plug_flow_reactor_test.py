"""
Test cases for PlugFlowReactor model

Tests cover initialization, dynamics, axial profiles,
conversion calculations, and discretization effects.

Author: SPROCLIB Development Team
"""

import pytest
import numpy as np
from unit.reactor.PlugFlowReactor import PlugFlowReactor


class TestPlugFlowReactor:
    """Test suite for PlugFlowReactor model."""
    
    @pytest.fixture
    def default_pfr(self):
        """Create a PlugFlowReactor instance with default parameters."""
        return PlugFlowReactor()
    
    @pytest.fixture
    def test_inputs(self):
        """Standard test inputs for PFR."""
        return np.array([10.0, 1.0, 350.0, 300.0])  # [q, CAi, Ti, Tw]
    
    @pytest.fixture
    def test_state(self):
        """Standard test state for PFR (all segments)."""
        pfr = PlugFlowReactor(n_segments=5)
        # Concentration decreasing along reactor, temperature varying
        CA = np.array([1.0, 0.8, 0.6, 0.4, 0.2])  # 5 segments
        T = np.array([350.0, 355.0, 360.0, 358.0, 355.0])  # 5 segments
        return np.concatenate([CA, T])
    
    def test_initialization_default(self):
        """Test PFR initialization with default parameters."""
        pfr = PlugFlowReactor()
        
        assert pfr.L == 10.0
        assert pfr.A_cross == 0.1
        assert pfr.n_segments == 20
        assert pfr.k0 == 7.2e10
        assert pfr.Ea == 72750.0
        assert pfr.delta_H == -52000.0
        assert pfr.name == "PlugFlowReactor"
        
        # Check derived properties
        assert pfr.dz == pfr.L / pfr.n_segments
        assert pfr.V_segment == pfr.A_cross * pfr.dz
    
    def test_initialization_custom(self):
        """Test PFR initialization with custom parameters."""
        pfr = PlugFlowReactor(
            L=20.0,
            A_cross=0.2,
            n_segments=10,
            name="CustomPFR"
        )
        
        assert pfr.L == 20.0
        assert pfr.A_cross == 0.2
        assert pfr.n_segments == 10
        assert pfr.name == "CustomPFR"
        assert pfr.dz == 2.0  # 20/10
    
    def test_reaction_rate(self, default_pfr):
        """Test reaction rate calculation."""
        CA = 1.0
        T = 350.0
        
        rate = default_pfr.reaction_rate(CA, T)
        
        assert rate > 0
        assert isinstance(rate, (int, float, np.number))
        
        # Test temperature dependence
        rate_higher_T = default_pfr.reaction_rate(CA, 400.0)
        assert rate_higher_T > rate
    
    def test_dynamics_calculation(self, default_pfr, test_inputs):
        """Test dynamics calculation with proper state size."""
        # Create state vector with correct size (2 * n_segments)
        n_seg = default_pfr.n_segments
        CA_segments = np.linspace(1.0, 0.5, n_seg)  # Decreasing concentration
        T_segments = np.full(n_seg, 350.0)  # Constant temperature
        x = np.concatenate([CA_segments, T_segments])
        
        dxdt = default_pfr.dynamics(0.0, x, test_inputs)
        
        assert len(dxdt) == 2 * n_seg
        assert len(dxdt) == len(x)
    
    def test_dynamics_mass_balance(self, default_pfr):
        """Test mass balance in dynamics."""
        n_seg = 5
        pfr_small = PlugFlowReactor(n_segments=n_seg)
        
        # Test with uniform concentration
        CA_segments = np.full(n_seg, 1.0)
        T_segments = np.full(n_seg, 350.0)
        x = np.concatenate([CA_segments, T_segments])
        u = np.array([10.0, 1.0, 350.0, 350.0])
        
        dxdt = pfr_small.dynamics(0.0, x, u)
        
        # Extract concentration derivatives
        dCAdt = dxdt[:n_seg]
        
        # First segment should have positive inlet effect
        # Later segments should show consumption
        assert len(dCAdt) == n_seg
    
    def test_steady_state_calculation(self, default_pfr, test_inputs):
        """Test steady-state calculation."""
        x_ss = default_pfr.steady_state(test_inputs)
        
        assert len(x_ss) == 2 * default_pfr.n_segments
        
        # Extract concentration and temperature profiles
        n_seg = default_pfr.n_segments
        CA_profile = x_ss[:n_seg]
        T_profile = x_ss[n_seg:]
        
        # Concentration should generally decrease along reactor
        assert CA_profile[0] >= CA_profile[-1]  # Inlet >= Outlet
        
        # All values should be reasonable
        assert all(ca >= 0 for ca in CA_profile)
        assert all(t > 0 for t in T_profile)
    
    def test_conversion_calculation(self, default_pfr):
        """Test conversion calculation."""
        n_seg = default_pfr.n_segments
        CA_inlet = 1.0
        CA_outlet = 0.3
        
        # Create state with inlet and outlet concentrations
        CA_profile = np.linspace(CA_inlet, CA_outlet, n_seg)
        T_profile = np.full(n_seg, 350.0)
        x = np.concatenate([CA_profile, T_profile])
        
        conversion = default_pfr.calculate_conversion(x)
        expected_conversion = (CA_inlet - CA_outlet) / CA_inlet
        
        assert abs(conversion - expected_conversion) < 1e-10
        assert 0 <= conversion <= 1
    
    def test_conversion_edge_cases(self, default_pfr):
        """Test conversion calculation edge cases."""
        n_seg = default_pfr.n_segments
        
        # Complete conversion
        CA_profile = np.linspace(1.0, 0.0, n_seg)
        T_profile = np.full(n_seg, 350.0)
        x = np.concatenate([CA_profile, T_profile])
        conversion = default_pfr.calculate_conversion(x)
        assert abs(conversion - 1.0) < 1e-10
        
        # No conversion
        CA_profile = np.full(n_seg, 1.0)
        T_profile = np.full(n_seg, 350.0)
        x = np.concatenate([CA_profile, T_profile])
        conversion = default_pfr.calculate_conversion(x)
        assert abs(conversion - 0.0) < 1e-10
    
    def test_describe_method(self, default_pfr):
        """Test describe method for metadata."""
        metadata = default_pfr.describe()
        
        required_keys = [
            'type', 'description', 'category', 'algorithms',
            'parameters', 'state_variables', 'inputs', 'outputs',
            'valid_ranges', 'applications', 'limitations'
        ]
        
        for key in required_keys:
            assert key in metadata
        
        assert metadata['type'] == 'PlugFlowReactor'
        assert metadata['category'] == 'reactor'
        assert 'L' in metadata['parameters']
        assert 'n_segments' in metadata['parameters']
    
    def test_axial_profile_consistency(self, default_pfr):
        """Test that axial profiles are physically reasonable."""
        u = np.array([50.0, 2.0, 400.0, 350.0])  # High flow, high concentration
        x_ss = default_pfr.steady_state(u)
        
        n_seg = default_pfr.n_segments
        CA_profile = x_ss[:n_seg]
        T_profile = x_ss[n_seg:]
        
        # Concentration should not increase along reactor (no reverse reaction)
        for i in range(1, n_seg):
            assert CA_profile[i] <= CA_profile[i-1] + 1e-6  # Allow small numerical errors
        
        # Temperature should be physically reasonable
        assert all(250.0 <= t <= 800.0 for t in T_profile)
    
    def test_different_discretizations(self):
        """Test that different discretizations give consistent results."""
        u = np.array([10.0, 1.0, 350.0, 300.0])
        
        # Test with different segment numbers
        pfr_coarse = PlugFlowReactor(n_segments=10)
        pfr_fine = PlugFlowReactor(n_segments=40)
        
        x_coarse = pfr_coarse.steady_state(u)
        x_fine = pfr_fine.steady_state(u)
        
        conv_coarse = pfr_coarse.calculate_conversion(x_coarse)
        conv_fine = pfr_fine.calculate_conversion(x_fine)
        
        # Conversions should be similar (within 5%)
        assert abs(conv_coarse - conv_fine) < 0.05
    
    def test_reactor_length_effect(self):
        """Test effect of reactor length on conversion."""
        u = np.array([10.0, 1.0, 350.0, 300.0])
        
        pfr_short = PlugFlowReactor(L=5.0)
        pfr_long = PlugFlowReactor(L=20.0)
        
        x_short = pfr_short.steady_state(u)
        x_long = pfr_long.steady_state(u)
        
        conv_short = pfr_short.calculate_conversion(x_short)
        conv_long = pfr_long.calculate_conversion(x_long)
        
        # Longer reactor should give higher conversion
        assert conv_long > conv_short
    
    def test_flow_rate_effect(self, default_pfr):
        """Test effect of flow rate on conversion."""
        CA0 = 1.0
        T0 = 350.0
        Tw = 300.0
        
        u_low = np.array([5.0, CA0, T0, Tw])   # Low flow rate
        u_high = np.array([50.0, CA0, T0, Tw]) # High flow rate
        
        x_low = default_pfr.steady_state(u_low)
        x_high = default_pfr.steady_state(u_high)
        
        conv_low = default_pfr.calculate_conversion(x_low)
        conv_high = default_pfr.calculate_conversion(x_high)
        
        # Lower flow rate should give higher conversion (longer residence time)
        assert conv_low > conv_high
    
    def test_temperature_effect(self, default_pfr):
        """Test effect of inlet temperature on conversion."""
        u_low_T = np.array([10.0, 1.0, 300.0, 300.0])  # Low temperature
        u_high_T = np.array([10.0, 1.0, 400.0, 400.0]) # High temperature
        
        x_low_T = default_pfr.steady_state(u_low_T)
        x_high_T = default_pfr.steady_state(u_high_T)
        
        conv_low_T = default_pfr.calculate_conversion(x_low_T)
        conv_high_T = default_pfr.calculate_conversion(x_high_T)
        
        # Higher temperature should give higher conversion (faster kinetics)
        assert conv_high_T > conv_low_T
    
    def test_parameter_consistency(self, default_pfr):
        """Test that parameters are stored consistently."""
        assert default_pfr.parameters['L'] == default_pfr.L
        assert default_pfr.parameters['A_cross'] == default_pfr.A_cross
        assert default_pfr.parameters['n_segments'] == default_pfr.n_segments
        assert default_pfr.parameters['dz'] == default_pfr.dz
    
    def test_heat_transfer_effect(self, default_pfr):
        """Test effect of wall temperature on reactor temperature profile."""
        u_cold_wall = np.array([10.0, 1.0, 400.0, 300.0])  # Cold wall
        u_hot_wall = np.array([10.0, 1.0, 400.0, 500.0])   # Hot wall
        
        x_cold = default_pfr.steady_state(u_cold_wall)
        x_hot = default_pfr.steady_state(u_hot_wall)
        
        n_seg = default_pfr.n_segments
        T_cold = x_cold[n_seg:]  # Temperature profile with cold wall
        T_hot = x_hot[n_seg:]    # Temperature profile with hot wall
        
        # Average temperature should be higher with hot wall
        assert np.mean(T_hot) > np.mean(T_cold)
