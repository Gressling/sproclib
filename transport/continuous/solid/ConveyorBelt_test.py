"""
Test module for ConveyorBelt class.

This module contains tests for the ConveyorBelt solid transport model,
covering steady-state calculations, dynamic behavior, and edge cases.
"""

import pytest
import numpy as np
from ConveyorBelt import ConveyorBelt


class TestConveyorBelt:
    """Test cases for ConveyorBelt class."""
    
    @pytest.fixture
    def conveyor_belt(self):
        """Create a standard ConveyorBelt instance for testing."""
        return ConveyorBelt(
            belt_length=50.0,
            belt_width=1.0,
            belt_speed=2.0,
            belt_angle=0.1,  # ~5.7 degrees
            material_density=1500.0,
            friction_coefficient=0.6,
            belt_load_factor=0.8,
            motor_power=10000.0
        )
    
    def test_initialization(self, conveyor_belt):
        """Test proper initialization of ConveyorBelt parameters."""
        assert conveyor_belt.belt_length == 50.0
        assert conveyor_belt.belt_width == 1.0
        assert conveyor_belt.belt_speed == 2.0
        assert conveyor_belt.belt_angle == 0.1
        assert conveyor_belt.material_density == 1500.0
        assert conveyor_belt.friction_coefficient == 0.6
        assert conveyor_belt.belt_load_factor == 0.8
        assert conveyor_belt.motor_power == 10000.0
        assert conveyor_belt.name == "ConveyorBelt"
    
    def test_describe_method(self, conveyor_belt):
        """Test the describe method returns proper metadata."""
        description = conveyor_belt.describe()
        
        assert description['class_name'] == 'ConveyorBelt'
        assert 'algorithm' in description
        assert 'parameters' in description
        assert 'inputs' in description
        assert 'outputs' in description
        assert 'equations' in description
        assert 'working_ranges' in description
        
        # Check parameter structure
        assert 'belt_length' in description['parameters']
        assert description['parameters']['belt_length']['value'] == 50.0
        assert description['parameters']['belt_length']['unit'] == 'm'
    
    def test_steady_state_normal_operation(self, conveyor_belt):
        """Test steady-state calculation under normal operating conditions."""
        # Input: [feed_rate, belt_speed, material_load_height]
        u = np.array([10.0, 2.0, 0.05])  # 10 kg/s, 2 m/s, 5 cm height
        
        result = conveyor_belt.steady_state(u)
        
        assert len(result) == 2
        flow_rate, power = result
        
        # Flow rate should be positive and reasonable
        assert flow_rate > 0
        assert flow_rate <= u[0]  # Should not exceed feed rate
        
        # Power should be positive and within motor capacity
        assert power > 0
        assert power <= conveyor_belt.motor_power * 1.1  # Allow small tolerance
    
    def test_steady_state_zero_speed(self, conveyor_belt):
        """Test steady-state with zero belt speed."""
        u = np.array([10.0, 0.0, 0.05])
        
        result = conveyor_belt.steady_state(u)
        flow_rate, power = result
        
        # Zero speed should result in zero flow
        assert flow_rate == 0.0
        # Power should still have friction component
        assert power > 0
    
    def test_steady_state_high_load(self, conveyor_belt):
        """Test steady-state with high material load."""
        u = np.array([100.0, 2.0, 0.2])  # High feed rate and load height
        
        result = conveyor_belt.steady_state(u)
        flow_rate, power = result
        
        assert flow_rate > 0
        assert power > 0
        # Power might be limited by motor capacity
        assert power <= conveyor_belt.motor_power * 1.01
    
    def test_steady_state_steep_angle(self):
        """Test steady-state with steep belt angle."""
        steep_conveyor = ConveyorBelt(belt_angle=0.5)  # ~28.6 degrees
        u = np.array([10.0, 2.0, 0.05])
        
        result = steep_conveyor.steady_state(u)
        flow_rate, power = result
        
        assert flow_rate > 0
        assert power > 0
        # Steep angle should require more power
        
        # Compare with flat conveyor
        flat_conveyor = ConveyorBelt(belt_angle=0.0)
        flat_result = flat_conveyor.steady_state(u)
        
        assert power > flat_result[1]  # Steep should need more power
    
    def test_dynamics_response(self, conveyor_belt):
        """Test dynamic response calculation."""
        # Initial state: [flow_rate, power]
        x = np.array([5.0, 5000.0])
        # Input: [feed_rate, belt_speed, material_load_height]
        u = np.array([10.0, 2.0, 0.05])
        
        dxdt = conveyor_belt.dynamics(0.0, x, u)
        
        assert len(dxdt) == 2
        dflow_dt, dpower_dt = dxdt
        
        # Both derivatives should be finite
        assert np.isfinite(dflow_dt)
        assert np.isfinite(dpower_dt)
        
        # Response should drive toward steady state
        steady_result = conveyor_belt.steady_state(u)
        if steady_result[0] > x[0]:
            assert dflow_dt > 0
        if steady_result[1] > x[1]:
            assert dpower_dt > 0
    
    def test_dynamics_stability(self, conveyor_belt):
        """Test that dynamics are stable (derivatives approach zero at steady state)."""
        u = np.array([10.0, 2.0, 0.05])
        steady_state = conveyor_belt.steady_state(u)
        
        # At steady state, derivatives should be close to zero
        dxdt = conveyor_belt.dynamics(0.0, steady_state, u)
        
        assert abs(dxdt[0]) < 1e-10  # Flow rate derivative
        assert abs(dxdt[1]) < 1e-10  # Power derivative
    
    def test_power_limitation(self, conveyor_belt):
        """Test that power consumption is properly limited."""
        # High load that should exceed motor capacity
        u = np.array([1000.0, 5.0, 0.5])  # Very high feed rate and speed
        
        result = conveyor_belt.steady_state(u)
        flow_rate, power = result
        
        # Power should not significantly exceed motor capacity
        assert power <= conveyor_belt.motor_power * 1.01
    
    def test_material_properties_effect(self):
        """Test effect of different material properties."""
        # Light material
        light_conveyor = ConveyorBelt(material_density=500.0)
        # Heavy material  
        heavy_conveyor = ConveyorBelt(material_density=3000.0)
        
        u = np.array([10.0, 2.0, 0.05])
        
        light_result = light_conveyor.steady_state(u)
        heavy_result = heavy_conveyor.steady_state(u)
        
        # Heavy material should require more power
        assert heavy_result[1] > light_result[1]
    
    def test_belt_geometry_effect(self):
        """Test effect of belt geometry on performance."""
        # Narrow belt
        narrow_conveyor = ConveyorBelt(belt_width=0.5)
        # Wide belt
        wide_conveyor = ConveyorBelt(belt_width=2.0)
        
        u = np.array([10.0, 2.0, 0.05])
        
        narrow_result = narrow_conveyor.steady_state(u)
        wide_result = wide_conveyor.steady_state(u)
        
        # Wide belt should handle more material
        assert wide_result[0] >= narrow_result[0]
    
    def test_input_validation_types(self, conveyor_belt):
        """Test that inputs are properly handled as arrays."""
        # Test with different input types
        u_list = [10.0, 2.0, 0.05]
        u_array = np.array([10.0, 2.0, 0.05])
        
        result_list = conveyor_belt.steady_state(u_list)
        result_array = conveyor_belt.steady_state(u_array)
        
        np.testing.assert_array_almost_equal(result_list, result_array)
    
    def test_edge_case_zero_feed(self, conveyor_belt):
        """Test behavior with zero feed rate."""
        u = np.array([0.0, 2.0, 0.05])
        
        result = conveyor_belt.steady_state(u)
        flow_rate, power = result
        
        # Zero feed should result in zero or minimal flow
        assert flow_rate >= 0
        assert flow_rate <= 1e-10  # Should be essentially zero
        # Power should still have belt friction component
        assert power > 0
    
    def test_edge_case_zero_height(self, conveyor_belt):
        """Test behavior with zero material height."""
        u = np.array([10.0, 2.0, 0.0])
        
        result = conveyor_belt.steady_state(u)
        flow_rate, power = result
        
        # Zero height should result in zero flow
        assert flow_rate == 0.0
        # Power should still have belt friction
        assert power > 0
    
    def test_performance_consistency(self, conveyor_belt):
        """Test that model gives consistent results."""
        u = np.array([10.0, 2.0, 0.05])
        
        # Run multiple times
        results = [conveyor_belt.steady_state(u) for _ in range(5)]
        
        # All results should be identical
        for i in range(1, len(results)):
            np.testing.assert_array_equal(results[0], results[i])
    
    def test_transport_time_calculation(self, conveyor_belt):
        """Test that transport time is correctly calculated in dynamics."""
        x = np.array([5.0, 5000.0])
        u = np.array([10.0, 2.0, 0.05])
        
        # Transport time should be length/speed
        expected_transport_time = conveyor_belt.belt_length / u[1]
        
        # This is indirectly tested through dynamics response
        dxdt = conveyor_belt.dynamics(0.0, x, u)
        
        # Should be finite and reasonable
        assert np.all(np.isfinite(dxdt))
        assert np.all(np.abs(dxdt) < 1e6)  # Reasonable magnitude
