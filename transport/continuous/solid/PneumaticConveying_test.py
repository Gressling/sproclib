"""
Test module for PneumaticConveying class.

This module contains tests for the PneumaticConveying solid transport model,
covering particle-air flow interactions, pressure drop calculations, and edge cases.
"""

import pytest
import numpy as np
from PneumaticConveying import PneumaticConveying


class TestPneumaticConveying:
    """Test cases for PneumaticConveying class."""
    
    @pytest.fixture
    def pneumatic_conveying(self):
        """Create a standard PneumaticConveying instance for testing."""
        return PneumaticConveying(
            pipe_length=100.0,
            pipe_diameter=0.1,
            particle_density=1500.0,
            particle_diameter=500e-6,
            air_density=1.2,
            air_viscosity=18e-6,
            conveying_velocity=20.0,
            solid_loading_ratio=10.0
        )
    
    def test_initialization(self, pneumatic_conveying):
        """Test proper initialization of PneumaticConveying parameters."""
        assert pneumatic_conveying.pipe_length == 100.0
        assert pneumatic_conveying.pipe_diameter == 0.1
        assert pneumatic_conveying.particle_density == 1500.0
        assert pneumatic_conveying.particle_diameter == 500e-6
        assert pneumatic_conveying.air_density == 1.2
        assert pneumatic_conveying.air_viscosity == 18e-6
        assert pneumatic_conveying.conveying_velocity == 20.0
        assert pneumatic_conveying.solid_loading_ratio == 10.0
        assert pneumatic_conveying.name == "PneumaticConveying"
    
    def test_describe_method(self, pneumatic_conveying):
        """Test the describe method returns proper metadata."""
        description = pneumatic_conveying.describe()
        
        assert description['class_name'] == 'PneumaticConveying'
        assert 'algorithm' in description
        assert 'parameters' in description
        assert 'inputs' in description
        assert 'outputs' in description
        assert 'equations' in description
        assert 'working_ranges' in description
        
        # Check parameter structure
        assert 'pipe_diameter' in description['parameters']
        assert description['parameters']['pipe_diameter']['value'] == 0.1
        assert description['parameters']['pipe_diameter']['unit'] == 'm'
    
    def test_steady_state_normal_operation(self, pneumatic_conveying):
        """Test steady-state calculation under normal operating conditions."""
        # Input: [P_inlet, air_flow_rate, solid_mass_flow]
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2  # For 20 m/s air velocity
        u = np.array([150000.0, air_flow_rate, 0.1])  # 150 kPa, calculated flow, 0.1 kg/s solids
        
        result = pneumatic_conveying.steady_state(u)
        
        assert len(result) == 2
        P_out, particle_velocity = result
        
        # Outlet pressure should be lower than inlet
        assert P_out < u[0]
        assert P_out > 0
        
        # Particle velocity should be positive and less than air velocity
        assert particle_velocity > 0
        assert particle_velocity < 20.0  # Should be less than air velocity
    
    def test_steady_state_pressure_drop(self, pneumatic_conveying):
        """Test pressure drop calculation."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        
        # Low loading
        u_low = np.array([150000.0, air_flow_rate, 0.01])
        # High loading
        u_high = np.array([150000.0, air_flow_rate, 0.5])
        
        result_low = pneumatic_conveying.steady_state(u_low)
        result_high = pneumatic_conveying.steady_state(u_high)
        
        # High loading should result in greater pressure drop
        pressure_drop_low = u_low[0] - result_low[0]
        pressure_drop_high = u_high[0] - result_high[0]
        
        assert pressure_drop_high > pressure_drop_low
    
    def test_steady_state_particle_velocity(self, pneumatic_conveying):
        """Test particle velocity calculation."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        result = pneumatic_conveying.steady_state(u)
        P_out, particle_velocity = result
        
        # Particle velocity should be reasonable for pneumatic conveying
        assert 5.0 < particle_velocity < 25.0  # Typical range
    
    def test_steady_state_different_air_velocities(self, pneumatic_conveying):
        """Test effect of different air velocities."""
        pipe_area = np.pi * (0.1/2)**2
        
        # Low air velocity
        air_flow_low = pipe_area * 15.0 * 1.2
        u_low = np.array([150000.0, air_flow_low, 0.1])
        
        # High air velocity
        air_flow_high = pipe_area * 30.0 * 1.2
        u_high = np.array([150000.0, air_flow_high, 0.1])
        
        result_low = pneumatic_conveying.steady_state(u_low)
        result_high = pneumatic_conveying.steady_state(u_high)
        
        # Higher air velocity should result in higher particle velocity
        assert result_high[1] > result_low[1]
    
    def test_steady_state_zero_solids(self, pneumatic_conveying):
        """Test steady-state with zero solid flow (air only)."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.0])
        
        result = pneumatic_conveying.steady_state(u)
        P_out, particle_velocity = result
        
        # Should still have pressure drop due to air flow
        assert P_out < u[0]
        # Particle velocity calculation should handle zero solids
        assert particle_velocity >= 0
    
    def test_steady_state_high_pressure(self, pneumatic_conveying):
        """Test steady-state with high inlet pressure."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([500000.0, air_flow_rate, 0.1])  # 500 kPa
        
        result = pneumatic_conveying.steady_state(u)
        P_out, particle_velocity = result
        
        assert P_out > 0
        assert P_out < u[0]
        assert particle_velocity > 0
    
    def test_dynamics_response(self, pneumatic_conveying):
        """Test dynamic response calculation."""
        # Initial state: [P_out, particle_velocity]
        x = np.array([140000.0, 15.0])
        # Input: [P_inlet, air_flow_rate, solid_mass_flow]
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        dxdt = pneumatic_conveying.dynamics(0.0, x, u)
        
        assert len(dxdt) == 2
        dP_out_dt, dv_particle_dt = dxdt
        
        # Both derivatives should be finite
        assert np.isfinite(dP_out_dt)
        assert np.isfinite(dv_particle_dt)
        
        # Response should drive toward steady state
        steady_result = pneumatic_conveying.steady_state(u)
        if steady_result[0] > x[0]:
            assert dP_out_dt > 0
        if steady_result[1] > x[1]:
            assert dv_particle_dt > 0
    
    def test_dynamics_stability(self, pneumatic_conveying):
        """Test that dynamics are stable at steady state."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        steady_state = pneumatic_conveying.steady_state(u)
        
        # At steady state, derivatives should be close to zero
        dxdt = pneumatic_conveying.dynamics(0.0, steady_state, u)
        
        assert abs(dxdt[0]) < 1e-6  # Pressure derivative
        assert abs(dxdt[1]) < 1e-6  # Velocity derivative
    
    def test_reynolds_number_regimes(self, pneumatic_conveying):
        """Test behavior in different Reynolds number regimes."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        result = pneumatic_conveying.steady_state(u)
        
        # Should handle different Re regimes gracefully
        assert np.all(np.isfinite(result))
        assert result[0] > 0  # Positive pressure
        assert result[1] > 0  # Positive velocity
    
    def test_particle_size_effect(self):
        """Test effect of particle size on transport."""
        # Small particles
        small_conveyor = PneumaticConveying(particle_diameter=100e-6)
        # Large particles
        large_conveyor = PneumaticConveying(particle_diameter=2e-3)
        
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        small_result = small_conveyor.steady_state(u)
        large_result = large_conveyor.steady_state(u)
        
        # Different particle sizes should give different results
        assert not np.allclose(small_result, large_result, rtol=0.01)
    
    def test_particle_density_effect(self):
        """Test effect of particle density on transport."""
        # Light particles
        light_conveyor = PneumaticConveying(particle_density=500.0)
        # Heavy particles
        heavy_conveyor = PneumaticConveying(particle_density=3000.0)
        
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        light_result = light_conveyor.steady_state(u)
        heavy_result = heavy_conveyor.steady_state(u)
        
        # Different densities should affect terminal velocity
        assert not np.allclose(light_result, heavy_result, rtol=0.01)
    
    def test_pipe_geometry_effect(self):
        """Test effect of pipe geometry on performance."""
        # Small pipe
        small_pipe_conveyor = PneumaticConveying(pipe_diameter=0.05)
        # Large pipe
        large_pipe_conveyor = PneumaticConveying(pipe_diameter=0.2)
        
        # Adjust flow rates for same velocity
        small_area = np.pi * (0.05/2)**2
        large_area = np.pi * (0.2/2)**2
        
        air_flow_small = small_area * 20.0 * 1.2
        air_flow_large = large_area * 20.0 * 1.2
        
        u_small = np.array([150000.0, air_flow_small, 0.1])
        u_large = np.array([150000.0, air_flow_large, 0.1])
        
        small_result = small_pipe_conveyor.steady_state(u_small)
        large_result = large_pipe_conveyor.steady_state(u_large)
        
        # Different pipe sizes should affect pressure drop
        pressure_drop_small = u_small[0] - small_result[0]
        pressure_drop_large = u_large[0] - large_result[0]
        
        # Smaller pipe should have higher pressure drop per unit length
        length_ratio = small_pipe_conveyor.pipe_length / large_pipe_conveyor.pipe_length
        assert pressure_drop_small > pressure_drop_large * length_ratio
    
    def test_air_properties_effect(self):
        """Test effect of air properties on transport."""
        # Different air density (altitude effect)
        high_altitude_conveyor = PneumaticConveying(air_density=0.9)
        sea_level_conveyor = PneumaticConveying(air_density=1.2)
        
        pipe_area = np.pi * (0.1/2)**2
        # Same mass flow rate
        air_flow_rate = 0.1  # kg/s
        u = np.array([150000.0, air_flow_rate, 0.05])
        
        high_result = high_altitude_conveyor.steady_state(u)
        sea_result = sea_level_conveyor.steady_state(u)
        
        # Different air densities should affect results
        assert not np.allclose(high_result, sea_result, rtol=0.01)
    
    def test_input_validation_types(self, pneumatic_conveying):
        """Test that inputs are properly handled as arrays."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        
        u_list = [150000.0, air_flow_rate, 0.1]
        u_array = np.array([150000.0, air_flow_rate, 0.1])
        
        result_list = pneumatic_conveying.steady_state(u_list)
        result_array = pneumatic_conveying.steady_state(u_array)
        
        np.testing.assert_array_almost_equal(result_list, result_array)
    
    def test_edge_case_zero_air_flow(self, pneumatic_conveying):
        """Test behavior with zero air flow."""
        u = np.array([150000.0, 0.0, 0.1])
        
        result = pneumatic_conveying.steady_state(u)
        P_out, particle_velocity = result
        
        # Zero air flow should result in minimal pressure drop
        assert P_out <= u[0]
        # Particle velocity should be very low or zero
        assert particle_velocity >= 0
    
    def test_edge_case_very_low_pressure(self, pneumatic_conveying):
        """Test behavior with very low inlet pressure."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 5.0 * 1.2  # Low velocity
        u = np.array([10000.0, air_flow_rate, 0.01])  # 10 kPa
        
        result = pneumatic_conveying.steady_state(u)
        P_out, particle_velocity = result
        
        # Should handle low pressure gracefully
        assert P_out >= 0
        assert P_out <= u[0]
        assert particle_velocity >= 0
    
    def test_performance_consistency(self, pneumatic_conveying):
        """Test that model gives consistent results."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        # Run multiple times
        results = [pneumatic_conveying.steady_state(u) for _ in range(5)]
        
        # All results should be identical
        for i in range(1, len(results)):
            np.testing.assert_array_equal(results[0], results[i])
    
    def test_terminal_velocity_calculation(self, pneumatic_conveying):
        """Test terminal velocity calculation is reasonable."""
        pipe_area = np.pi * (0.1/2)**2
        air_flow_rate = pipe_area * 20.0 * 1.2
        u = np.array([150000.0, air_flow_rate, 0.1])
        
        result = pneumatic_conveying.steady_state(u)
        
        # Terminal velocity should be in reasonable range for given particle
        # For 500 micron particles at 1500 kg/m³, terminal velocity should be several m/s
        assert 1.0 < result[1] < 50.0
