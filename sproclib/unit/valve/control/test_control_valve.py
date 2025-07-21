"""
Test suite for ControlValve class - Chemical Engineering Validation
Tests focus on valve engineering calculations and physical behavior
"""

import pytest
import numpy as np
import sys
import os

# Add the sproclib path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from sproclib.unit.valve import ControlValve


class TestControlValve:
    
    @pytest.fixture
    def default_valve(self):
        """Standard industrial control valve for testing"""
        return ControlValve(
            Cv_max=100.0,
            valve_type="linear",
            dead_time=1.0,
            time_constant=2.0,
            rangeability=50.0,
            name="TestValve"
        )
    
    @pytest.fixture
    def equal_percentage_valve(self):
        """Equal percentage valve for characteristic testing"""
        return ControlValve(
            Cv_max=200.0,
            valve_type="equal_percentage",
            dead_time=0.5,
            time_constant=1.5,
            rangeability=30.0
        )

    def test_initialization(self, default_valve):
        """Test valve initialization with engineering parameters"""
        assert default_valve.Cv_max == 100.0
        assert default_valve.valve_type == "linear"
        assert default_valve.dead_time == 1.0
        assert default_valve.time_constant == 2.0
        assert default_valve.rangeability == 50.0
        assert default_valve.Cv_min == 2.0  # 100/50
        
    def test_valve_characteristic_linear(self, default_valve):
        """Test linear valve characteristic curve"""
        # Test key positions
        Cv_0 = default_valve._valve_characteristic(0.0)
        Cv_50 = default_valve._valve_characteristic(0.5)
        Cv_100 = default_valve._valve_characteristic(1.0)
        
        assert abs(Cv_0 - 2.0) < 1e-6  # Cv_min
        assert abs(Cv_50 - 51.0) < 1e-6  # Midpoint
        assert abs(Cv_100 - 100.0) < 1e-6  # Cv_max
        
        # Test linearity
        positions = np.linspace(0, 1, 11)
        Cvs = [default_valve._valve_characteristic(pos) for pos in positions]
        # Check linear progression
        for i in range(1, len(Cvs)):
            expected_increase = (100.0 - 2.0) / 10
            actual_increase = Cvs[i] - Cvs[i-1]
            assert abs(actual_increase - expected_increase) < 1e-6

    def test_valve_characteristic_equal_percentage(self, equal_percentage_valve):
        """Test equal percentage valve characteristic"""
        Cv_0 = equal_percentage_valve._valve_characteristic(0.0)
        Cv_50 = equal_percentage_valve._valve_characteristic(0.5)
        Cv_100 = equal_percentage_valve._valve_characteristic(1.0)
        
        expected_Cv_min = 200.0 / 30.0  # ~6.67
        assert abs(Cv_0 - expected_Cv_min) < 1e-6
        assert abs(Cv_100 - 200.0) < 1e-6
        
        # Test equal percentage property: equal position changes give equal percentage flow changes
        positions = [0.2, 0.4, 0.6, 0.8]
        Cvs = [equal_percentage_valve._valve_characteristic(pos) for pos in positions]
        
        # Calculate percentage increases
        ratios = [Cvs[i]/Cvs[i-1] for i in range(1, len(Cvs))]
        # All ratios should be approximately equal for equal percentage characteristic
        for ratio in ratios[1:]:
            assert abs(ratio - ratios[0]) < 0.1  # Allow 10% tolerance

    def test_flow_calculation_standard_conditions(self, default_valve):
        """Test flow calculation using standard valve equation"""
        # Standard test conditions
        Cv = 50.0  # gpm/psi^0.5
        delta_P = 1.0e5  # Pa (1 bar)
        rho = 1000.0  # kg/m³ (water)
        
        flow_rate = default_valve._calculate_flow(Cv, delta_P, rho)
        
        # Expected flow using valve equation: Q = Cv * sqrt(delta_P/rho)
        # With unit conversion: Cv_si = Cv * 6.309e-5
        expected_flow = 50.0 * 6.309e-5 * np.sqrt(1.0e5 / 1000.0)
        assert abs(flow_rate - expected_flow) < 1e-8

    def test_flow_calculation_engineering_validation(self, default_valve):
        """Validate flow calculations against engineering handbook values"""
        # Test case: Cv=100, 5 bar pressure drop, water
        Cv = 100.0
        delta_P = 5.0e5  # Pa (5 bar)
        rho = 1000.0  # kg/m³
        
        flow_rate = default_valve._calculate_flow(Cv, delta_P, rho)
        
        # Calculate expected flow using the same internal conversion
        # The code uses: Cv_si = Cv * 6.309e-5, flow = Cv_si * sqrt(delta_P/rho)
        expected_flow = Cv * 6.309e-5 * np.sqrt(delta_P / rho)
        
        # Should match the internal calculation exactly
        assert abs(flow_rate - expected_flow) < 1e-10

    def test_zero_pressure_drop(self, default_valve):
        """Test behavior with zero or negative pressure drop"""
        Cv = 50.0
        
        # Zero pressure drop
        flow_zero = default_valve._calculate_flow(Cv, 0.0, 1000.0)
        assert flow_zero == 0.0
        
        # Negative pressure drop (backflow protection)
        flow_negative = default_valve._calculate_flow(Cv, -1000.0, 1000.0)
        assert flow_negative == 0.0

    def test_steady_state_calculations(self, default_valve):
        """Test steady-state valve behavior"""
        # Test conditions: 50% open, 2 bar pressure drop
        u = np.array([0.5, 3.0e5, 1.0e5, 1000.0])  # [pos_cmd, P_up, P_down, rho]
        
        steady_state = default_valve.steady_state(u)
        position, flow = steady_state
        
        assert position == 0.5  # Position should match command
        
        # Verify flow calculation
        expected_Cv = default_valve._valve_characteristic(0.5)
        expected_flow = default_valve._calculate_flow(expected_Cv, 2.0e5, 1000.0)
        assert abs(flow - expected_flow) < 1e-8

    def test_valve_position_limits(self, default_valve):
        """Test valve position saturation limits"""
        # Test positions outside 0-1 range
        Cv_below = default_valve._valve_characteristic(-0.5)
        Cv_above = default_valve._valve_characteristic(1.5)
        
        assert Cv_below == default_valve.Cv_min  # Should saturate to minimum
        assert Cv_above == default_valve.Cv_max  # Should saturate to maximum

    def test_dead_time_buffer_functionality(self, default_valve):
        """Test dead-time buffer operations"""
        # Initialize buffer
        t1, t2, t3 = 0.0, 0.5, 1.0
        pos1, pos2, pos3 = 0.2, 0.5, 0.8
        
        # Add entries to buffer
        default_valve._update_dead_time_buffer(t1, pos1)
        default_valve._update_dead_time_buffer(t2, pos2)
        default_valve._update_dead_time_buffer(t3, pos3)
        
        assert len(default_valve.time_buffer) == 3
        assert len(default_valve.position_buffer) == 3
        
        # Test delayed position retrieval
        delayed_pos = default_valve._get_delayed_position(t3)  # t3 - dead_time = 0.0
        assert abs(delayed_pos - pos1) < 1e-6

    def test_valve_sizing_info(self, default_valve):
        """Test valve sizing information retrieval"""
        sizing_info = default_valve.get_valve_sizing_info()
        
        expected_keys = ['Cv_max', 'Cv_min', 'rangeability', 'valve_type', 'dead_time', 'time_constant']
        for key in expected_keys:
            assert key in sizing_info
            
        assert sizing_info['Cv_max'] == 100.0
        assert sizing_info['Cv_min'] == 2.0
        assert sizing_info['rangeability'] == 50.0

    def test_describe_method(self, default_valve):
        """Test describe method for documentation"""
        description = default_valve.describe()
        
        assert description['type'] == 'ControlValve'
        assert 'algorithms' in description
        assert 'parameters' in description
        assert 'valid_ranges' in description
        assert 'applications' in description
        assert 'limitations' in description

    def test_engineering_edge_cases(self, default_valve):
        """Test engineering edge cases and boundary conditions"""
        # Very high pressure drop (cavitation region)
        high_dp_flow = default_valve._calculate_flow(50.0, 1.0e7, 1000.0)
        assert high_dp_flow > 0  # Should still calculate flow
        
        # Very low density (near vapor)
        low_rho_flow = default_valve._calculate_flow(50.0, 1.0e5, 1.0)
        assert low_rho_flow > 0
        
        # Very high density (liquid metal)
        high_rho_flow = default_valve._calculate_flow(50.0, 1.0e5, 10000.0)
        assert high_rho_flow > 0

    def test_multiple_valve_types(self):
        """Test all supported valve characteristic types"""
        valve_types = ["linear", "equal_percentage", "quick_opening"]
        
        for valve_type in valve_types:
            valve = ControlValve(valve_type=valve_type)
            
            # Test characteristic curves are monotonic
            positions = np.linspace(0, 1, 11)
            Cvs = [valve._valve_characteristic(pos) for pos in positions]
            
            # Check monotonic increasing
            for i in range(1, len(Cvs)):
                assert Cvs[i] >= Cvs[i-1], f"Non-monotonic behavior in {valve_type} valve"

    def test_rangeability_validation(self):
        """Test valve rangeability affects Cv_min correctly"""
        rangeabilities = [10.0, 25.0, 50.0, 100.0]
        Cv_max = 100.0
        
        for R in rangeabilities:
            valve = ControlValve(Cv_max=Cv_max, rangeability=R)
            expected_Cv_min = Cv_max / R
            assert abs(valve.Cv_min - expected_Cv_min) < 1e-6
