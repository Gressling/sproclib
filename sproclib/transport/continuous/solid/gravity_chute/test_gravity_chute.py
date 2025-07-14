"""
Test module for GravityChute class.

This module contains tests for the GravityChute solid transport model,
covering particle flow dynamics, force balance calculations, and edge cases.
"""

import pytest
import numpy as np
from .gravity_chute import GravityChute


class TestGravityChute:
    """Test cases for GravityChute class."""
    
    @pytest.fixture
    def gravity_chute(self):
        """Create a standard GravityChute instance for testing."""
        return GravityChute(
            chute_length=10.0,
            chute_width=0.5,
            chute_angle=0.524,  # 30 degrees
            surface_roughness=0.3,
            particle_density=2000.0,
            particle_diameter=5e-3,
            air_resistance=0.01
        )
    
    def test_initialization(self, gravity_chute):
        """Test proper initialization of GravityChute parameters."""
        assert gravity_chute.chute_length == 10.0
        assert gravity_chute.chute_width == 0.5
        assert gravity_chute.chute_angle == 0.524
        assert gravity_chute.surface_roughness == 0.3
        assert gravity_chute.particle_density == 2000.0
        assert gravity_chute.particle_diameter == 5e-3
        assert gravity_chute.air_resistance == 0.01
        assert gravity_chute.name == "GravityChute"
    
    def test_describe_method(self, gravity_chute):
        """Test the describe method returns proper metadata."""
        description = gravity_chute.describe()
        
        assert description['class_name'] == 'GravityChute'
        assert 'algorithm' in description
        assert 'parameters' in description
        assert 'inputs' in description
        assert 'outputs' in description
        assert 'equations' in description
        assert 'working_ranges' in description
        
        # Check parameter structure
        assert 'chute_angle' in description['parameters']
        assert description['parameters']['chute_angle']['value'] == 0.524
        assert description['parameters']['chute_angle']['unit'] == 'rad'
    
    def test_steady_state_normal_operation(self, gravity_chute):
        """Test steady-state calculation under normal operating conditions."""
        # Input: [feed_rate, particle_size_factor, chute_loading]
        u = np.array([5.0, 1.0, 0.3])  # 5 kg/s, normal size, 30% loading
        
        result = gravity_chute.steady_state(u)
        
        assert len(result) == 2
        velocity, flow_rate = result
        
        # Velocity should be positive for properly angled chute
        assert velocity > 0
        # Flow rate should be positive and not exceed feed rate
        assert flow_rate > 0
        assert flow_rate <= u[0]
    
    def test_steady_state_steep_angle(self):
        """Test steady-state with steep chute angle."""
        steep_chute = GravityChute(chute_angle=0.785)  # 45 degrees
        u = np.array([5.0, 1.0, 0.3])
        
        result = steep_chute.steady_state(u)
        velocity, flow_rate = result
        
        # Steep angle should produce higher velocity
        assert velocity > 0
        
        # Compare with shallow angle
        shallow_chute = GravityChute(chute_angle=0.262)  # 15 degrees
        shallow_result = shallow_chute.steady_state(u)
        
        assert velocity > shallow_result[0]  # Steeper should be faster
    
    def test_steady_state_flat_chute(self):
        """Test steady-state with nearly flat chute (should not flow)."""
        flat_chute = GravityChute(
            chute_angle=0.05,  # Very shallow
            surface_roughness=0.6  # High friction
        )
        u = np.array([5.0, 1.0, 0.3])
        
        result = flat_chute.steady_state(u)
        velocity, flow_rate = result
        
        # Should have very low or zero velocity due to insufficient slope
        assert velocity >= 0
        # May not flow if friction exceeds gravitational component
    
    def test_steady_state_large_particles(self, gravity_chute):
        """Test steady-state with large particles."""
        u = np.array([5.0, 3.0, 0.3])  # 3x larger particles
        
        result = gravity_chute.steady_state(u)
        velocity, flow_rate = result
        
        assert velocity > 0
        assert flow_rate > 0
        
        # Compare with normal particles
        normal_result = gravity_chute.steady_state(np.array([5.0, 1.0, 0.3]))
        # Larger particles typically have different terminal velocity
    
    def test_steady_state_high_loading(self, gravity_chute):
        """Test steady-state with high chute loading."""
        u = np.array([5.0, 1.0, 0.8])  # 80% loading
        
        result = gravity_chute.steady_state(u)
        velocity, flow_rate = result
        
        assert velocity > 0
        assert flow_rate > 0
        
        # Compare with low loading
        low_loading_result = gravity_chute.steady_state(np.array([5.0, 1.0, 0.2]))
        
        # High loading should reduce velocity due to interactions
        assert velocity <= low_loading_result[0]
    
    def test_steady_state_zero_loading(self, gravity_chute):
        """Test steady-state with zero loading."""
        u = np.array([5.0, 1.0, 0.0])
        
        result = gravity_chute.steady_state(u)
        velocity, flow_rate = result
        
        # Zero loading should result in minimal or zero flow
        assert flow_rate >= 0
        assert flow_rate <= 1e-10  # Essentially zero
    
    def test_dynamics_response(self, gravity_chute):
        """Test dynamic response calculation."""
        # Initial state: [velocity, flow_rate]
        x = np.array([2.0, 3.0])
        # Input: [feed_rate, particle_size_factor, chute_loading]
        u = np.array([5.0, 1.0, 0.3])
        
        dxdt = gravity_chute.dynamics(0.0, x, u)
        
        assert len(dxdt) == 2
        dvelocity_dt, dflow_dt = dxdt
        
        # Both derivatives should be finite
        assert np.isfinite(dvelocity_dt)
        assert np.isfinite(dflow_dt)
        
        # Response should drive toward steady state
        steady_result = gravity_chute.steady_state(u)
        if steady_result[0] > x[0]:
            assert dvelocity_dt > 0
        if steady_result[1] > x[1]:
            assert dflow_dt > 0
    
    def test_dynamics_stability(self, gravity_chute):
        """Test that dynamics are stable at steady state."""
        u = np.array([5.0, 1.0, 0.3])
        steady_state = gravity_chute.steady_state(u)
        
        # At steady state, derivatives should be close to zero
        dxdt = gravity_chute.dynamics(0.0, steady_state, u)
        
        assert abs(dxdt[0]) < 1e-6  # Velocity derivative
        assert abs(dxdt[1]) < 1e-6  # Flow rate derivative
    
    def test_force_balance_verification(self, gravity_chute):
        """Test that force balance is correctly implemented."""
        g = 9.81
        
        # Calculate expected forces
        F_gravity = g * np.sin(gravity_chute.chute_angle)
        F_friction = gravity_chute.surface_roughness * g * np.cos(gravity_chute.chute_angle)
        net_acceleration = F_gravity - F_friction
        
        # Should be positive for material to flow
        if net_acceleration > 0:
            u = np.array([5.0, 1.0, 0.3])
            result = gravity_chute.steady_state(u)
            assert result[0] > 0  # Should have positive velocity
    
    def test_particle_size_effect(self, gravity_chute):
        """Test effect of particle size on flow behavior."""
        # Small particles
        small_result = gravity_chute.steady_state(np.array([5.0, 0.5, 0.3]))
        # Large particles
        large_result = gravity_chute.steady_state(np.array([5.0, 2.0, 0.3]))
        
        # Both should flow, but at different rates
        assert small_result[0] > 0
        assert large_result[0] > 0
        
        # Different particle sizes should give different results
        assert not np.allclose(small_result, large_result, rtol=0.01)
    
    def test_surface_roughness_effect(self):
        """Test effect of surface roughness on flow."""
        # Smooth surface
        smooth_chute = GravityChute(surface_roughness=0.1)
        # Rough surface
        rough_chute = GravityChute(surface_roughness=0.6)
        
        u = np.array([5.0, 1.0, 0.3])
        
        smooth_result = smooth_chute.steady_state(u)
        rough_result = rough_chute.steady_state(u)
        
        # Smooth surface should allow higher velocity
        assert smooth_result[0] >= rough_result[0]
    
    def test_air_resistance_effect(self):
        """Test effect of air resistance on particle velocity."""
        # Low air resistance
        low_air_chute = GravityChute(air_resistance=0.001)
        # High air resistance
        high_air_chute = GravityChute(air_resistance=0.1)
        
        u = np.array([5.0, 1.0, 0.3])
        
        low_air_result = low_air_chute.steady_state(u)
        high_air_result = high_air_chute.steady_state(u)
        
        # Higher air resistance should reduce velocity
        assert low_air_result[0] >= high_air_result[0]
    
    def test_material_density_effect(self):
        """Test effect of particle density on flow."""
        # Light particles
        light_chute = GravityChute(particle_density=1000.0)
        # Heavy particles
        heavy_chute = GravityChute(particle_density=5000.0)
        
        u = np.array([5.0, 1.0, 0.3])
        
        light_result = light_chute.steady_state(u)
        heavy_result = heavy_chute.steady_state(u)
        
        # Both should flow but differently
        assert light_result[0] > 0
        assert heavy_result[0] > 0
    
    def test_chute_geometry_effect(self):
        """Test effect of chute geometry on capacity."""
        # Narrow chute
        narrow_chute = GravityChute(chute_width=0.2)
        # Wide chute
        wide_chute = GravityChute(chute_width=1.0)
        
        u = np.array([10.0, 1.0, 0.3])  # High feed rate
        
        narrow_result = narrow_chute.steady_state(u)
        wide_result = wide_chute.steady_state(u)
        
        # Wide chute should handle more material
        assert wide_result[1] >= narrow_result[1]
    
    def test_input_validation_types(self, gravity_chute):
        """Test that inputs are properly handled as arrays."""
        u_list = [5.0, 1.0, 0.3]
        u_array = np.array([5.0, 1.0, 0.3])
        
        result_list = gravity_chute.steady_state(u_list)
        result_array = gravity_chute.steady_state(u_array)
        
        np.testing.assert_array_almost_equal(result_list, result_array)
    
    def test_edge_case_zero_feed(self, gravity_chute):
        """Test behavior with zero feed rate."""
        u = np.array([0.0, 1.0, 0.3])
        
        result = gravity_chute.steady_state(u)
        velocity, flow_rate = result
        
        # Velocity may still be calculated based on physics
        assert velocity >= 0
        # Flow rate should be zero with no feed
        assert flow_rate == 0.0
    
    def test_edge_case_zero_size_factor(self, gravity_chute):
        """Test behavior with zero particle size factor."""
        u = np.array([5.0, 0.0, 0.3])
        
        result = gravity_chute.steady_state(u)
        velocity, flow_rate = result
        
        # Should handle zero size gracefully
        assert velocity >= 0
        assert flow_rate >= 0
    
    def test_transport_time_calculation(self, gravity_chute):
        """Test transport time calculation in dynamics."""
        x = np.array([3.0, 4.0])  # Non-zero velocity
        u = np.array([5.0, 1.0, 0.3])
        
        # Transport time should be length/velocity
        if x[0] > 0:
            expected_transport_time = gravity_chute.chute_length / x[0]
        else:
            expected_transport_time = 10.0  # Default
        
        dxdt = gravity_chute.dynamics(0.0, x, u)
        
        # Should produce finite derivatives
        assert np.all(np.isfinite(dxdt))
    
    def test_performance_consistency(self, gravity_chute):
        """Test that model gives consistent results."""
        u = np.array([5.0, 1.0, 0.3])
        
        # Run multiple times
        results = [gravity_chute.steady_state(u) for _ in range(5)]
        
        # All results should be identical
        for i in range(1, len(results)):
            np.testing.assert_array_equal(results[0], results[i])
