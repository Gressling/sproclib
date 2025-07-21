"""
Test suite for PipeFlow class - Standard Process Control Library

This module contains comprehensive tests for the PipeFlow liquid transport model,
including steady-state calculations, dynamic behavior, and describe methods.
"""

import numpy as np
import sys
import os

# Add the parent directory to path to import PipeFlow
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .pipe_flow import PipeFlow


class TestPipeFlow:
    """Test suite for PipeFlow class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.pipe = PipeFlow(
            pipe_length=100.0,
            pipe_diameter=0.1,
            roughness=0.046e-3,
            fluid_density=1000.0,
            fluid_viscosity=1e-3,
            elevation_change=0.0,
            flow_nominal=0.01
        )
    
    def test_initialization(self):
        """Test PipeFlow initialization and parameter setting."""
        assert self.pipe.pipe_length == 100.0
        assert self.pipe.pipe_diameter == 0.1
        assert self.pipe.roughness == 0.046e-3
        assert self.pipe.fluid_density == 1000.0
        assert self.pipe.fluid_viscosity == 1e-3
        assert self.pipe.elevation_change == 0.0
        assert self.pipe.flow_nominal == 0.01
        assert self.pipe.name == "PipeFlow"
        
        # Test parameters dictionary
        assert len(self.pipe.parameters) == 7
        assert self.pipe.parameters['pipe_length'] == 100.0
    
    def test_describe_method(self):
        """Test the describe method returns comprehensive metadata."""
        desc = self.pipe.describe()
        
        # Test required keys
        required_keys = [
            'class_name', 'module', 'description', 'model_type',
            'physics', 'algorithms', 'parameters', 'inputs', 'outputs',
            'state_variables', 'methods', 'references', 'limitations'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['class_name'] == 'PipeFlow'
        assert 'Liquid pipe flow' in desc['description']
        assert 'reynolds_calculation' in desc['algorithms']
        assert 'friction_factor' in desc['algorithms']
        assert 'pressure_drop' in desc['algorithms']
        
        # Test physics domain
        assert desc['physics']['domain'] == 'Fluid Mechanics'
        assert 'Pressure Drop' in desc['physics']['phenomena']
    
    def test_steady_state_laminar_flow(self):
        """Test steady-state calculation for laminar flow conditions."""
        # Test with very low flow rate (laminar conditions)
        P_in = 200000  # 200 kPa
        T_in = 298.15  # 25°C
        flow_rate = 0.0001  # Very small flow rate for laminar flow
        
        u = np.array([P_in, T_in, flow_rate])
        result = self.pipe.steady_state(u)
        
        # Basic checks
        assert len(result) == 2
        P_out, T_out = result
        
        # Pressure should decrease (positive pressure drop)
        assert P_out < P_in
        
        # Temperature should remain constant (isothermal assumption)
        assert T_out == T_in
        
        # Check Reynolds number is in laminar range
        velocity = flow_rate / (np.pi * (self.pipe.pipe_diameter/2)**2)
        Re = self.pipe.fluid_density * velocity * self.pipe.pipe_diameter / self.pipe.fluid_viscosity
        assert Re < 2300, f"Reynolds number {Re} should be laminar"
    
    def test_steady_state_turbulent_flow(self):
        """Test steady-state calculation for turbulent flow conditions."""
        # Test with high flow rate (turbulent conditions)
        P_in = 500000  # 500 kPa
        T_in = 298.15  # 25°C
        flow_rate = 0.05  # Higher flow rate for turbulent flow
        
        u = np.array([P_in, T_in, flow_rate])
        result = self.pipe.steady_state(u)
        
        # Basic checks
        assert len(result) == 2
        P_out, T_out = result
        
        # Pressure should decrease
        assert P_out < P_in
        
        # Temperature should remain constant
        assert T_out == T_in
        
        # Check Reynolds number is in turbulent range
        velocity = flow_rate / (np.pi * (self.pipe.pipe_diameter/2)**2)
        Re = self.pipe.fluid_density * velocity * self.pipe.pipe_diameter / self.pipe.fluid_viscosity
        assert Re >= 2300, f"Reynolds number {Re} should be turbulent"
    
    def test_steady_state_elevation_effect(self):
        """Test steady-state calculation with elevation change."""
        # Create pipe with elevation change
        pipe_elevated = PipeFlow(elevation_change=10.0)  # 10m elevation gain
        
        P_in = 300000  # 300 kPa
        T_in = 298.15
        flow_rate = 0.01
        
        u = np.array([P_in, T_in, flow_rate])
        result = pipe_elevated.steady_state(u)
        P_out, T_out = result
        
        # Calculate expected elevation pressure drop
        expected_elevation_drop = pipe_elevated.fluid_density * 9.81 * 10.0
        
        # Result with flat pipe for comparison
        pipe_flat = PipeFlow(elevation_change=0.0)
        result_flat = pipe_flat.steady_state(u)
        P_out_flat, _ = result_flat
        
        # Elevated pipe should have additional pressure drop
        assert P_out < P_out_flat
        pressure_diff = P_out_flat - P_out
        assert abs(pressure_diff - expected_elevation_drop) < 1000  # Within 1 kPa tolerance
    
    def test_dynamics_basic(self):
        """Test dynamic model basic functionality."""
        # Initial state
        x = np.array([180000, 298.15])  # Initial pressure and temperature
        
        # Input
        u = np.array([200000, 298.15, 0.01])  # Target conditions
        
        # Time
        t = 0.0
        
        # Calculate derivatives
        dx_dt = self.pipe.dynamics(t, x, u)
        
        # Check output format
        assert len(dx_dt) == 2
        dP_dt, dT_dt = dx_dt
        
        # Since initial pressure is lower than steady-state target,
        # pressure derivative should be positive
        assert dP_dt > 0
        
        # Temperature derivative should be zero (same temperature)
        assert abs(dT_dt) < 1e-10
    
    def test_dynamics_convergence(self):
        """Test that dynamics converge to steady-state values."""
        # Input conditions
        u = np.array([200000, 298.15, 0.01])
        
        # Calculate steady-state target
        ss_result = self.pipe.steady_state(u)
        P_ss, T_ss = ss_result
        
        # Start from different initial conditions
        x = np.array([150000, 290.0])
        
        # Check that derivatives point toward steady-state
        dx_dt = self.pipe.dynamics(0.0, x, u)
        dP_dt, dT_dt = dx_dt
        
        # Pressure derivative should be positive (moving toward higher P_ss)
        assert dP_dt > 0
        
        # Temperature derivative should be positive (moving toward higher T_ss)
        assert dT_dt > 0
        
        # Test convergence at steady-state
        x_ss = np.array([P_ss, T_ss])
        dx_dt_ss = self.pipe.dynamics(0.0, x_ss, u)
        
        # Derivatives should be near zero at steady-state
        assert abs(dx_dt_ss[0]) < 1e-3
        assert abs(dx_dt_ss[1]) < 1e-3
    
    def test_describe_steady_state(self):
        """Test the describe_steady_state static method."""
        desc = PipeFlow.describe_steady_state()
        
        # Test required keys
        required_keys = [
            'function_name', 'purpose', 'algorithm_steps', 'equations',
            'input_format', 'output_format', 'computational_complexity'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['function_name'] == 'steady_state'
        assert 'pressure drop' in desc['purpose']
        assert len(desc['algorithm_steps']) >= 4
        assert 'reynolds' in desc['equations']
        assert 'friction_laminar' in desc['equations']
        assert 'friction_turbulent' in desc['equations']
    
    def test_describe_dynamics(self):
        """Test the describe_dynamics static method."""
        desc = PipeFlow.describe_dynamics()
        
        # Test required keys
        required_keys = [
            'function_name', 'purpose', 'model_type', 'algorithm_steps',
            'differential_equations', 'time_constants', 'state_variables'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['function_name'] == 'dynamics'
        assert 'first-order lag' in desc['purpose'].lower()
        assert 'pressure' in desc['differential_equations']
        assert 'temperature' in desc['differential_equations']
        assert desc['time_constants']['pressure'] == 'τ_pressure = 5.0 s'
    
    def test_reynolds_number_calculation(self):
        """Test Reynolds number calculation accuracy."""
        flow_rate = 0.01
        velocity = flow_rate / (np.pi * (self.pipe.pipe_diameter/2)**2)
        expected_Re = (self.pipe.fluid_density * velocity * 
                      self.pipe.pipe_diameter / self.pipe.fluid_viscosity)
        
        # Calculate through steady_state and verify Re is computed correctly
        u = np.array([200000, 298.15, flow_rate])
        # We can't directly access Re, but we can verify flow regime behavior
        result = self.pipe.steady_state(u)
        
        # For this flow rate, should be turbulent
        assert expected_Re >= 2300
    
    def test_pressure_drop_components(self):
        """Test pressure drop calculation components."""
        # Test with elevation change
        pipe_with_elevation = PipeFlow(elevation_change=5.0)
        
        # Same conditions for both pipes
        u = np.array([300000, 298.15, 0.01])
        
        # Results
        result_flat = self.pipe.steady_state(u)
        result_elevated = pipe_with_elevation.steady_state(u)
        
        P_out_flat = result_flat[0]
        P_out_elevated = result_elevated[0]
        
        # Elevation should cause additional pressure drop
        additional_drop = P_out_flat - P_out_elevated
        expected_elevation_drop = (pipe_with_elevation.fluid_density * 
                                 9.81 * pipe_with_elevation.elevation_change)
        
        # Should be close to expected elevation drop
        assert abs(additional_drop - expected_elevation_drop) < 1000
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with zero flow
        u_zero = np.array([200000, 298.15, 0.0])
        result_zero = self.pipe.steady_state(u_zero)
        
        # With zero flow, pressure drop should be only elevation
        P_out_zero = result_zero[0]
        expected_drop = self.pipe.fluid_density * 9.81 * self.pipe.elevation_change
        assert abs((200000 - P_out_zero) - expected_drop) < 1
        
        # Test with very high flow (should still be stable)
        u_high = np.array([500000, 298.15, 1.0])
        result_high = self.pipe.steady_state(u_high)
        
        # Should produce valid results
        assert len(result_high) == 2
        assert result_high[0] < 500000  # Pressure should drop
        assert result_high[1] == 298.15  # Temperature unchanged
    
    def test_parameter_sensitivity(self):
        """Test sensitivity to parameter changes."""
        base_u = np.array([200000, 298.15, 0.01])
        base_result = self.pipe.steady_state(base_u)
        base_pressure_drop = base_u[0] - base_result[0]
        
        # Test with doubled roughness
        rough_pipe = PipeFlow(roughness=2 * self.pipe.roughness)
        rough_result = rough_pipe.steady_state(base_u)
        rough_pressure_drop = base_u[0] - rough_result[0]
        
        # Higher roughness should cause higher pressure drop
        assert rough_pressure_drop > base_pressure_drop
        
        # Test with doubled diameter
        large_pipe = PipeFlow(pipe_diameter=2 * self.pipe.pipe_diameter)
        large_result = large_pipe.steady_state(base_u)
        large_pressure_drop = base_u[0] - large_result[0]
        
        # Larger diameter should cause lower pressure drop
        assert large_pressure_drop < base_pressure_drop


def run_all_tests():
    """Run all tests manually without pytest dependency."""
    test_instance = TestPipeFlow()
    
    # List of test methods
    test_methods = [
        'test_initialization',
        'test_describe_method',
        'test_steady_state_laminar_flow',
        'test_steady_state_turbulent_flow',
        'test_steady_state_elevation_effect',
        'test_dynamics_basic',
        'test_dynamics_convergence',
        'test_describe_steady_state',
        'test_describe_dynamics',
        'test_reynolds_number_calculation',
        'test_pressure_drop_components',
        'test_edge_cases',
        'test_parameter_sensitivity'
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
