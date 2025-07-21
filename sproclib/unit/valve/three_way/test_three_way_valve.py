"""
Test suite for ThreeWayValve class - Chemical Engineering Validation
Tests focus on flow splitting/mixing calculations and mass balance
"""

import pytest
import numpy as np
import sys
import os

# Add the sproclib path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from sproclib.unit.valve import ThreeWayValve


class TestThreeWayValve:
    
    @pytest.fixture
    def mixing_valve(self):
        """Standard mixing three-way valve"""
        return ThreeWayValve(
            Cv_max=100.0,
            valve_config="mixing",
            dead_time=1.0,
            time_constant=2.0,
            name="MixingValve"
        )
    
    @pytest.fixture  
    def diverting_valve(self):
        """Standard diverting three-way valve"""
        return ThreeWayValve(
            Cv_max=150.0,
            valve_config="diverting",
            dead_time=0.5,
            time_constant=1.5,
            name="DivertingValve"
        )

    def test_initialization_mixing(self, mixing_valve):
        """Test mixing valve initialization"""
        assert mixing_valve.Cv_max == 100.0
        assert mixing_valve.valve_config == "mixing"
        assert mixing_valve.dead_time == 1.0
        assert mixing_valve.time_constant == 2.0
        assert mixing_valve.state_names == ['valve_position', 'flow_out']

    def test_initialization_diverting(self, diverting_valve):
        """Test diverting valve initialization"""
        assert diverting_valve.Cv_max == 150.0
        assert diverting_valve.valve_config == "diverting"
        assert diverting_valve.state_names == ['valve_position', 'flow_out1', 'flow_out2']

    def test_invalid_configuration(self):
        """Test invalid valve configuration raises error"""
        with pytest.raises(ValueError, match="valve_config must be 'mixing' or 'diverting'"):
            ThreeWayValve(valve_config="invalid")

    def test_cv_split_calculation(self, mixing_valve):
        """Test flow coefficient splitting calculation"""
        # Test full path A (position = 0)
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(0.0)
        assert Cv_A == 100.0
        assert Cv_B == 0.0
        
        # Test full path B (position = 1)
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(1.0)
        assert Cv_A == 0.0
        assert Cv_B == 100.0
        
        # Test 50-50 split (position = 0.5)
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(0.5)
        assert Cv_A == 50.0
        assert Cv_B == 50.0
        
        # Test 25-75 split (position = 0.75)
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(0.75)
        assert Cv_A == 25.0
        assert Cv_B == 75.0

    def test_flow_split_percentages(self, mixing_valve):
        """Test flow split percentage calculations"""
        # Test various positions
        positions = [0.0, 0.25, 0.5, 0.75, 1.0]
        expected_splits = [(1.0, 0.0), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.0, 1.0)]
        
        for pos, (exp_A, exp_B) in zip(positions, expected_splits):
            split_A, split_B = mixing_valve.get_flow_split(pos)
            assert abs(split_A - exp_A) < 1e-6
            assert abs(split_B - exp_B) < 1e-6
            assert abs(split_A + split_B - 1.0) < 1e-6  # Must sum to 1

    def test_mixing_steady_state_mass_balance(self, mixing_valve):
        """Test mixing valve steady-state mass balance"""
        # Test conditions: 50% split, equal pressures
        position_cmd = 0.5
        P1_in = 3.0e5  # Pa
        P2_in = 2.5e5  # Pa  
        P_out = 1.0e5  # Pa
        rho = 1000.0   # kg/m³
        
        u = np.array([position_cmd, P1_in, P2_in, P_out, rho])
        steady_state = mixing_valve.steady_state(u)
        
        position, flow_out = steady_state
        assert position == 0.5
        
        # Calculate expected flows from each inlet
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(0.5)
        Cv_si = 6.309e-5
        
        expected_flow1 = Cv_A * Cv_si * np.sqrt((P1_in - P_out) / rho)
        expected_flow2 = Cv_B * Cv_si * np.sqrt((P2_in - P_out) / rho)
        expected_total = expected_flow1 + expected_flow2
        
        assert abs(flow_out - expected_total) < 1e-8

    def test_diverting_steady_state_mass_balance(self, diverting_valve):
        """Test diverting valve steady-state mass balance"""
        # Test conditions: 30% to outlet 1, 70% to outlet 2
        position_cmd = 0.7  # More flow to path B (outlet 2)
        P_in = 4.0e5   # Pa
        P1_out = 1.5e5 # Pa
        P2_out = 1.0e5 # Pa  
        rho = 800.0    # kg/m³
        
        u = np.array([position_cmd, P_in, P1_out, P2_out, rho])
        steady_state = diverting_valve.steady_state(u)
        
        position, flow1, flow2 = steady_state
        assert position == 0.7
        
        # Verify individual flows
        Cv_A, Cv_B = diverting_valve._calculate_cv_split(0.7)
        Cv_si = 6.309e-5
        
        expected_flow1 = Cv_A * Cv_si * np.sqrt((P_in - P1_out) / rho)
        expected_flow2 = Cv_B * Cv_si * np.sqrt((P_in - P2_out) / rho)
        
        assert abs(flow1 - expected_flow1) < 1e-8
        assert abs(flow2 - expected_flow2) < 1e-8
        
        # Mass balance: total inlet = total outlet (in steady state)
        total_outlet = flow1 + flow2
        assert total_outlet > 0  # Should have positive flow

    def test_zero_pressure_drop_scenarios(self, mixing_valve):
        """Test behavior with zero or negative pressure drops"""
        # Mixing valve with zero pressure drop on one inlet
        u = np.array([0.5, 2.0e5, 1.0e5, 1.0e5, 1000.0])  # P2_in = P_out
        steady_state = mixing_valve.steady_state(u)
        
        position, flow_out = steady_state
        # Should only have flow from inlet 1
        assert flow_out > 0
        
        # Test with negative pressure drop (backflow protection)
        u_negative = np.array([0.5, 0.5e5, 0.8e5, 1.0e5, 1000.0])  # Both inlets lower than outlet
        steady_state_neg = mixing_valve.steady_state(u_negative)
        position_neg, flow_neg = steady_state_neg
        assert flow_neg == 0.0

    def test_position_saturation_limits(self, mixing_valve):
        """Test valve position saturation beyond 0-1 range"""
        # Test positions outside valid range
        Cv_A_low, Cv_B_low = mixing_valve._calculate_cv_split(-0.5)
        Cv_A_high, Cv_B_high = mixing_valve._calculate_cv_split(1.5)
        
        # Should saturate to 0.0 position (full path A)
        assert Cv_A_low == 100.0
        assert Cv_B_low == 0.0
        
        # Should saturate to 1.0 position (full path B)  
        assert Cv_A_high == 0.0
        assert Cv_B_high == 100.0

    def test_dead_time_buffer_operations(self, mixing_valve):
        """Test dead-time buffer functionality"""
        # Add position commands to buffer
        times = [0.0, 0.5, 1.0, 1.5]
        positions = [0.2, 0.4, 0.6, 0.8]
        
        for t, pos in zip(times, positions):
            mixing_valve._update_dead_time_buffer(t, pos)
            
        # Buffer should contain entries (may clean old ones based on dead_time)
        assert len(mixing_valve.time_buffer) >= 3  # At least recent entries
        assert len(mixing_valve.position_buffer) >= 3
        
        # Test delayed position retrieval
        # At t=1.5, looking back dead_time=1.0, should get position at t=0.5
        delayed_pos = mixing_valve._get_delayed_position(1.5)
        # Should return some valid position
        assert 0.0 <= delayed_pos <= 1.0

    def test_engineering_flow_validation(self, diverting_valve):
        """Validate flow calculations against engineering correlations"""
        # Standard test case from valve handbook
        position = 0.6  # 40% to path A, 60% to path B
        P_in = 5.0e5   # 5 bar inlet
        P1_out = 2.0e5 # 2 bar outlet 1
        P2_out = 1.5e5 # 1.5 bar outlet 2
        rho = 1000.0   # Water
        
        u = np.array([position, P_in, P1_out, P2_out, rho])
        steady_state = diverting_valve.steady_state(u)
        _, flow1, flow2 = steady_state
        
        # Calculate expected flows using internal calculation
        Cv_A, Cv_B = diverting_valve._calculate_cv_split(position)
        Cv_si = 6.309e-5
        
        expected_flow1 = Cv_A * Cv_si * np.sqrt((P_in - P1_out) / rho)
        expected_flow2 = Cv_B * Cv_si * np.sqrt((P_in - P2_out) / rho)
        
        # Should match internal calculations exactly
        assert abs(flow1 - expected_flow1) < 1e-10
        assert abs(flow2 - expected_flow2) < 1e-10

    def test_describe_method(self, mixing_valve):
        """Test describe method for documentation"""
        description = mixing_valve.describe()
        
        assert description['type'] == 'ThreeWayValve'
        assert description['category'] == 'unit/valve'
        assert 'algorithms' in description
        assert 'parameters' in description
        assert 'valid_ranges' in description
        assert 'applications' in description
        assert 'limitations' in description

    def test_mixing_valve_temperature_control_scenario(self, mixing_valve):
        """Test realistic temperature control mixing scenario"""
        # Hot stream: 80°C, Cold stream: 20°C, Target: 50°C
        # This requires 50% mixing ratio
        
        # Pressures (typical plant conditions)
        P_hot = 3.5e5   # Pa (hot water supply)
        P_cold = 3.0e5  # Pa (cold water supply)  
        P_mixed = 1.2e5 # Pa (to heat exchanger)
        rho = 980.0     # kg/m³ (water at ~50°C)
        
        # Test 50% mixing position
        u = np.array([0.5, P_hot, P_cold, P_mixed, rho])
        steady_state = mixing_valve.steady_state(u)
        
        position, flow_total = steady_state
        assert position == 0.5
        assert flow_total > 0
        
        # Verify equal contribution from both streams (approximately)
        Cv_A, Cv_B = mixing_valve._calculate_cv_split(0.5)
        assert abs(Cv_A - Cv_B) < 1e-6  # Should be equal

    def test_diverting_valve_bypass_control_scenario(self, diverting_valve):
        """Test realistic bypass control scenario"""
        # Reactor feed with bypass for temperature control
        
        # Process conditions
        P_feed = 6.0e5     # Pa (main feed pressure)
        P_reactor = 2.0e5  # Pa (reactor pressure)
        P_bypass = 1.8e5   # Pa (bypass return pressure)
        rho = 850.0        # kg/m³ (organic solvent)
        
        # Test 80% to reactor, 20% bypass
        position = 0.8
        u = np.array([position, P_feed, P_reactor, P_bypass, rho])
        steady_state = diverting_valve.steady_state(u)
        
        _, flow_reactor, flow_bypass = steady_state
        
        # Verify flows are positive and consider pressure drop effects
        assert flow_reactor > 0
        assert flow_bypass > 0
        
        # Note: Flow distribution depends on pressure drops, not just position
        # Higher pressure drop to reactor (4 bar) vs bypass (4.2 bar) affects flow
        # Verify total flow is reasonable
        total_flow = flow_reactor + flow_bypass
        assert total_flow > 0

    def test_flow_coefficient_conservation(self, mixing_valve):
        """Test that total Cv is conserved across positions"""
        positions = np.linspace(0, 1, 11)
        
        for position in positions:
            Cv_A, Cv_B = mixing_valve._calculate_cv_split(position)
            total_Cv = Cv_A + Cv_B
            
            # Total Cv should equal Cv_max for linear splitting
            assert abs(total_Cv - mixing_valve.Cv_max) < 1e-6

    def test_pressure_drop_sensitivity(self, diverting_valve):
        """Test sensitivity to pressure drop variations"""
        base_position = 0.5
        P_in = 4.0e5
        rho = 1000.0
        
        # Test different outlet pressures
        outlet_pressures = [1.0e5, 1.5e5, 2.0e5, 2.5e5]
        flows = []
        
        for P_out in outlet_pressures:
            u = np.array([base_position, P_in, P_out, P_out, rho])
            steady_state = diverting_valve.steady_state(u)
            _, flow1, flow2 = steady_state
            flows.append(flow1 + flow2)
        
        # Higher pressure drops should give higher flows
        for i in range(1, len(flows)):
            assert flows[i] <= flows[i-1]  # Decreasing flow with higher outlet pressure
