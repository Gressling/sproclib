"""
Test suite for PeristalticFlow class - Standard Process Control Library

This module contains comprehensive tests for the PeristalticFlow pump model,
including steady-state calculations, dynamic behavior, and describe methods.
"""

import numpy as np
import sys
import os

# Add the parent directory to path to import PeristalticFlow
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PeristalticFlow import PeristalticFlow


class TestPeristalticFlow:
    """Test suite for PeristalticFlow class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.pump = PeristalticFlow(
            tube_diameter=0.01,
            tube_length=1.0,
            pump_speed=100.0,
            occlusion_factor=0.9,
            fluid_density=1000.0,
            fluid_viscosity=1e-3,
            pulsation_damping=0.8
        )
    
    def test_initialization(self):
        """Test PeristalticFlow initialization and parameter setting."""
        assert self.pump.tube_diameter == 0.01
        assert self.pump.tube_length == 1.0
        assert self.pump.pump_speed == 100.0
        assert self.pump.occlusion_factor == 0.9
        assert self.pump.fluid_density == 1000.0
        assert self.pump.fluid_viscosity == 1e-3
        assert self.pump.pulsation_damping == 0.8
        assert self.pump.name == "PeristalticFlow"
        
        # Test parameters dictionary
        assert len(self.pump.parameters) == 7
        assert self.pump.parameters['tube_diameter'] == 0.01
    
    def test_describe_method(self):
        """Test the describe method returns comprehensive metadata."""
        desc = self.pump.describe()
        
        # Test required keys
        required_keys = [
            'class_name', 'module', 'description', 'model_type',
            'physics', 'algorithms', 'parameters', 'inputs', 'outputs',
            'state_variables', 'methods', 'performance_characteristics'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['class_name'] == 'PeristalticFlow'
        assert 'Peristaltic pump' in desc['description']
        assert 'theoretical_flow' in desc['algorithms']
        assert 'backpressure_correction' in desc['algorithms']
        
        # Test physics domain
        assert 'Fluid Mechanics' in desc['physics']['domain']
        assert 'Positive displacement' in desc['physics']['phenomena']
        
        # Test performance characteristics
        assert 'flow_accuracy' in desc['performance_characteristics']
        assert 'pressure_capability' in desc['performance_characteristics']
    
    def test_steady_state_basic(self):
        """Test basic steady-state calculation."""
        P_in = 100000  # 100 kPa
        pump_speed = 120.0  # rpm
        occlusion = 1.0  # Full occlusion
        
        u = np.array([P_in, pump_speed, occlusion])
        result = self.pump.steady_state(u)
        
        # Basic checks
        assert len(result) == 2
        flow_rate, P_out = result
        
        # Flow rate should be positive
        assert flow_rate > 0
        
        # Outlet pressure should be slightly higher (pump effect)
        assert P_out > P_in
    
    def test_steady_state_speed_relationship(self):
        """Test relationship between pump speed and flow rate."""
        P_in = 100000
        occlusion = 1.0
        
        # Test different speeds
        speeds = [60.0, 120.0, 180.0]
        flow_rates = []
        
        for speed in speeds:
            u = np.array([P_in, speed, occlusion])
            result = self.pump.steady_state(u)
            flow_rates.append(result[0])
        
        # Flow rate should increase with pump speed
        assert flow_rates[1] > flow_rates[0]
        assert flow_rates[2] > flow_rates[1]
        
        # Should be approximately linear relationship
        ratio1 = flow_rates[1] / flow_rates[0]
        ratio2 = flow_rates[2] / flow_rates[1]
        expected_ratio = 2.0  # Double speed = double flow
        
        # Allow some tolerance for backpressure effects
        assert abs(ratio1 - expected_ratio) < 0.5
        assert abs(ratio2 - 1.5) < 0.5  # 180/120 = 1.5
    
    def test_steady_state_occlusion_effect(self):
        """Test effect of tube occlusion on flow rate."""
        P_in = 100000
        pump_speed = 100.0
        
        # Test different occlusion levels
        occlusions = [0.5, 0.8, 1.0]
        flow_rates = []
        
        for occlusion in occlusions:
            u = np.array([P_in, pump_speed, occlusion])
            result = self.pump.steady_state(u)
            flow_rates.append(result[0])
        
        # Flow rate should increase with occlusion
        assert flow_rates[1] > flow_rates[0]
        assert flow_rates[2] > flow_rates[1]
        
        # Should be proportional to occlusion
        ratio = flow_rates[1] / flow_rates[0]  # 0.8 / 0.5 = 1.6
        assert abs(ratio - 1.6) < 0.3
    
    def test_steady_state_backpressure_effect(self):
        """Test backpressure effect on flow rate."""
        pump_speed = 100.0
        occlusion = 1.0
        
        # Test different inlet pressures
        pressures = [50000, 200000, 500000, 800000]
        flow_rates = []
        
        for P_in in pressures:
            u = np.array([P_in, pump_speed, occlusion])
            result = self.pump.steady_state(u)
            flow_rates.append(result[0])
        
        # Flow rate should decrease with increasing backpressure
        assert flow_rates[1] < flow_rates[0]
        assert flow_rates[2] < flow_rates[1]
        assert flow_rates[3] < flow_rates[2]
        
        # At very high pressure, flow should be significantly reduced
        assert flow_rates[3] < 0.5 * flow_rates[0]
    
    def test_theoretical_flow_calculation(self):
        """Test theoretical flow rate calculation."""
        pump_speed = 60.0  # rpm
        occlusion = 1.0
        
        # Calculate expected theoretical flow
        tube_area = np.pi * (self.pump.tube_diameter/2)**2
        expected_flow = (pump_speed / 60.0) * tube_area * self.pump.occlusion_factor
        
        # Test with zero backpressure (should get close to theoretical)
        u = np.array([0, pump_speed, occlusion])
        result = self.pump.steady_state(u)
        actual_flow = result[0]
        
        # Should be close to theoretical (allowing for pressure factor)
        assert abs(actual_flow - expected_flow) < 0.2 * expected_flow
    
    def test_dynamics_basic(self):
        """Test dynamic model basic functionality."""
        # Initial state [flow_rate, pulsation]
        x = np.array([0.001, 0.0])
        
        # Input [P_inlet, pump_speed, occlusion]
        u = np.array([100000, 120.0, 1.0])
        
        # Time
        t = 0.0
        
        # Calculate derivatives
        dx_dt = self.pump.dynamics(t, x, u)
        
        # Check output format
        assert len(dx_dt) == 2
        dflow_dt, dpulsation_dt = dx_dt
        
        # Flow rate should increase (positive derivative)
        assert dflow_dt > 0
        
        # Pulsation derivative depends on current state
        assert isinstance(dpulsation_dt, (int, float, np.number))
    
    def test_dynamics_convergence(self):
        """Test that dynamics converge to steady-state values."""
        # Input conditions
        u = np.array([100000, 100.0, 1.0])
        
        # Calculate steady-state target
        ss_result = self.pump.steady_state(u)
        flow_ss = ss_result[0]
        
        # Start from different initial conditions
        x = np.array([0.0, 0.0])
        
        # Check that derivatives point toward steady-state
        dx_dt = self.pump.dynamics(0.0, x, u)
        dflow_dt, dpulsation_dt = dx_dt
        
        # Flow derivative should be positive (moving toward higher flow_ss)
        assert dflow_dt > 0
        
        # Test convergence behavior
        # After some time, flow should approach steady-state
        x_intermediate = np.array([0.8 * flow_ss, 0.001])
        dx_dt_intermediate = self.pump.dynamics(0.0, x_intermediate, u)
        
        # Should still be positive but smaller
        assert dx_dt_intermediate[0] > 0
        assert dx_dt_intermediate[0] < dflow_dt
    
    def test_pulsation_modeling(self):
        """Test pulsation amplitude modeling."""
        # High speed should create more pulsation
        u_high_speed = np.array([100000, 200.0, 1.0])
        u_low_speed = np.array([100000, 50.0, 1.0])
        
        # Initial state with some pulsation
        x = np.array([0.001, 0.0])
        
        # Calculate pulsation dynamics
        dx_high = self.pump.dynamics(0.0, x, u_high_speed)
        dx_low = self.pump.dynamics(0.0, x, u_low_speed)
        
        # Both should have pulsation dynamics
        assert isinstance(dx_high[1], (int, float, np.number))
        assert isinstance(dx_low[1], (int, float, np.number))
    
    def test_describe_steady_state(self):
        """Test the describe_steady_state static method."""
        desc = PeristalticFlow.describe_steady_state()
        
        # Test required keys
        required_keys = [
            'function_name', 'purpose', 'algorithm_steps', 'equations',
            'input_format', 'output_format', 'performance_factors'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['function_name'] == 'steady_state'
        assert 'peristaltic pump' in desc['purpose']
        assert len(desc['algorithm_steps']) >= 4
        assert 'tube_area' in desc['equations']
        assert 'theoretical_flow' in desc['equations']
        assert 'pressure_factor' in desc['equations']
    
    def test_describe_dynamics(self):
        """Test the describe_dynamics static method."""
        desc = PeristalticFlow.describe_dynamics()
        
        # Test required keys
        required_keys = [
            'function_name', 'purpose', 'model_type', 'algorithm_steps',
            'differential_equations', 'time_constants', 'pulsation_model'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['function_name'] == 'dynamics'
        assert 'pulsation' in desc['purpose'].lower()
        assert 'flow_rate' in desc['differential_equations']
        assert 'pulsation' in desc['differential_equations']
        assert 'τ_flow = 2.0 s' in desc['time_constants']['flow_response']
    
    def test_tube_area_calculation(self):
        """Test tube cross-sectional area calculation."""
        expected_area = np.pi * (self.pump.tube_diameter/2)**2
        
        # Test with known conditions
        u = np.array([100000, 60.0, 1.0])  # 1 rev/s
        result = self.pump.steady_state(u)
        flow_rate = result[0]
        
        # Calculate implied area from flow rate
        # theoretical_flow = (pump_speed / 60.0) * area * occlusion_factor
        pump_speed_hz = 60.0 / 60.0  # 1 Hz
        
        # Account for pressure factor (approximately 1 at low pressure)
        pressure_factor = max(0.1, 1.0 - 100000 / 1e6)
        
        implied_theoretical = flow_rate / pressure_factor
        implied_area = implied_theoretical / (pump_speed_hz * self.pump.occlusion_factor)
        
        # Should be close to expected area
        assert abs(implied_area - expected_area) < 0.5 * expected_area
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with zero speed
        u_zero_speed = np.array([100000, 0.0, 1.0])
        result_zero = self.pump.steady_state(u_zero_speed)
        
        # Should produce zero flow
        assert abs(result_zero[0]) < 1e-10
        
        # Test with zero occlusion
        u_zero_occlusion = np.array([100000, 100.0, 0.0])
        result_zero_occ = self.pump.steady_state(u_zero_occlusion)
        
        # Should produce zero flow
        assert abs(result_zero_occ[0]) < 1e-10
        
        # Test with very high pressure
        u_high_pressure = np.array([2e6, 100.0, 1.0])  # 2 MPa
        result_high_p = self.pump.steady_state(u_high_pressure)
        
        # Should still produce some flow (minimum 10% of theoretical)
        assert result_high_p[0] > 0
    
    def test_parameter_sensitivity(self):
        """Test sensitivity to parameter changes."""
        base_u = np.array([100000, 100.0, 1.0])
        base_result = self.pump.steady_state(base_u)
        base_flow = base_result[0]
        
        # Test with doubled tube diameter
        large_tube_pump = PeristalticFlow(tube_diameter=2 * self.pump.tube_diameter)
        large_result = large_tube_pump.steady_state(base_u)
        large_flow = large_result[0]
        
        # Larger tube should give higher flow (area scales as D²)
        assert large_flow > base_flow
        flow_ratio = large_flow / base_flow
        assert flow_ratio > 3.0  # Should be about 4x for 2x diameter
        
        # Test with different occlusion factor
        tight_pump = PeristalticFlow(occlusion_factor=0.5)
        tight_result = tight_pump.steady_state(base_u)
        tight_flow = tight_result[0]
        
        # Lower occlusion factor should give lower flow
        assert tight_flow < base_flow
    
    def test_time_constants(self):
        """Test dynamic time constants are reasonable."""
        # Test flow response time constant
        x1 = np.array([0.0, 0.0])
        x2 = np.array([0.001, 0.0])
        u = np.array([100000, 100.0, 1.0])
        
        dx1 = self.pump.dynamics(0.0, x1, u)
        dx2 = self.pump.dynamics(0.0, x2, u)
        
        # Higher flow should have smaller derivative (approaching steady-state)
        assert dx1[0] > dx2[0]
        
        # Time constant should be evident in dynamics
        # τ = 2.0 s means 63% response in 2 seconds
        # dflow/dt = (flow_ss - flow) / τ
        # For large error, should have fast response
        assert dx1[0] > 0.001  # Reasonable response rate


def run_all_tests():
    """Run all tests manually without pytest dependency."""
    test_instance = TestPeristalticFlow()
    
    # List of test methods
    test_methods = [
        'test_initialization',
        'test_describe_method', 
        'test_steady_state_basic',
        'test_steady_state_speed_relationship',
        'test_steady_state_occlusion_effect',
        'test_steady_state_backpressure_effect',
        'test_theoretical_flow_calculation',
        'test_dynamics_basic',
        'test_dynamics_convergence',
        'test_pulsation_modeling',
        'test_describe_steady_state',
        'test_describe_dynamics',
        'test_tube_area_calculation',
        'test_edge_cases',
        'test_parameter_sensitivity',
        'test_time_constants'
    ]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            test_instance.setup_method()  # Reset for each test
            method = getattr(test_instance, method_name)
            method()
            print(f"✓ {method_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {method_name}: {str(e)}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Run the tests
    success = run_all_tests()
    if not success:
        exit(1)
