"""
Test module for ScrewFeeder class.

This module contains tests for the ScrewFeeder solid transport model,
covering volumetric feeding calculations, torque requirements, and edge cases.
"""

import pytest
import numpy as np
from .screw_feeder import ScrewFeeder


class TestScrewFeeder:
    """Test cases for ScrewFeeder class."""
    
    @pytest.fixture
    def screw_feeder(self):
        """Create a standard ScrewFeeder instance for testing."""
        return ScrewFeeder(
            screw_diameter=0.05,
            screw_length=0.5,
            screw_pitch=0.025,
            screw_speed=100.0,
            fill_factor=0.3,
            powder_density=800.0,
            powder_flowability=0.8,
            motor_torque_max=10.0
        )
    
    def test_initialization(self, screw_feeder):
        """Test proper initialization of ScrewFeeder parameters."""
        assert screw_feeder.screw_diameter == 0.05
        assert screw_feeder.screw_length == 0.5
        assert screw_feeder.screw_pitch == 0.025
        assert screw_feeder.screw_speed == 100.0
        assert screw_feeder.fill_factor == 0.3
        assert screw_feeder.powder_density == 800.0
        assert screw_feeder.powder_flowability == 0.8
        assert screw_feeder.motor_torque_max == 10.0
        assert screw_feeder.name == "ScrewFeeder"
    
    def test_describe_method(self, screw_feeder):
        """Test the describe method returns proper metadata."""
        description = screw_feeder.describe()
        
        assert description['class_name'] == 'ScrewFeeder'
        assert 'algorithm' in description
        assert 'parameters' in description
        assert 'inputs' in description
        assert 'outputs' in description
        assert 'equations' in description
        assert 'working_ranges' in description
        
        # Check parameter structure
        assert 'screw_diameter' in description['parameters']
        assert description['parameters']['screw_diameter']['value'] == 0.05
        assert description['parameters']['screw_diameter']['unit'] == 'm'
    
    def test_steady_state_normal_operation(self, screw_feeder):
        """Test steady-state calculation under normal operating conditions."""
        # Input: [screw_speed_setpoint, hopper_level, powder_moisture]
        u = np.array([100.0, 0.3, 0.02])  # 100 rpm, 30 cm level, 2% moisture
        
        result = screw_feeder.steady_state(u)
        
        assert len(result) == 2
        flow_rate, torque = result
        
        # Flow rate should be positive
        assert flow_rate > 0
        # Torque should be positive and within motor capacity
        assert torque > 0
        assert torque <= screw_feeder.motor_torque_max * 1.01  # Small tolerance
    
    def test_steady_state_zero_speed(self, screw_feeder):
        """Test steady-state with zero screw speed."""
        u = np.array([0.0, 0.3, 0.02])
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        # Zero speed should result in zero flow
        assert flow_rate == 0.0
        # Torque should still have base component
        assert torque >= 0
    
    def test_steady_state_high_speed(self, screw_feeder):
        """Test steady-state with high screw speed."""
        u = np.array([300.0, 0.3, 0.02])  # High speed
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        assert flow_rate > 0
        assert torque > 0
        
        # Compare with normal speed
        normal_result = screw_feeder.steady_state(np.array([100.0, 0.3, 0.02]))
        
        # Higher speed should generally give higher flow rate
        assert flow_rate >= normal_result[0]
    
    def test_steady_state_low_hopper_level(self, screw_feeder):
        """Test steady-state with low hopper level."""
        u = np.array([100.0, 0.1, 0.02])  # Low hopper level
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        assert flow_rate >= 0
        assert torque > 0
        
        # Compare with normal level
        normal_result = screw_feeder.steady_state(np.array([100.0, 0.3, 0.02]))
        
        # Low level should reduce flow rate
        assert flow_rate <= normal_result[0]
    
    def test_steady_state_high_moisture(self, screw_feeder):
        """Test steady-state with high moisture content."""
        u = np.array([100.0, 0.3, 0.15])  # 15% moisture
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        assert flow_rate >= 0
        assert torque > 0
        
        # Compare with dry powder
        dry_result = screw_feeder.steady_state(np.array([100.0, 0.3, 0.02]))
        
        # High moisture should reduce flow and increase torque
        assert flow_rate <= dry_result[0]
        assert torque >= dry_result[1]
    
    def test_steady_state_torque_limiting(self, screw_feeder):
        """Test torque limiting functionality."""
        # Conditions that should cause high torque
        u = np.array([400.0, 0.5, 0.2])  # High speed, high level, high moisture
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        # Torque should not exceed maximum
        assert torque <= screw_feeder.motor_torque_max * 1.01
        
        # Flow rate should be adjusted if torque limited
        assert flow_rate >= 0
    
    def test_dynamics_response(self, screw_feeder):
        """Test dynamic response calculation."""
        # Initial state: [flow_rate, torque]
        x = np.array([0.005, 3.0])
        # Input: [screw_speed_setpoint, hopper_level, powder_moisture]
        u = np.array([100.0, 0.3, 0.02])
        
        dxdt = screw_feeder.dynamics(0.0, x, u)
        
        assert len(dxdt) == 2
        dflow_dt, dtorque_dt = dxdt
        
        # Both derivatives should be finite
        assert np.isfinite(dflow_dt)
        assert np.isfinite(dtorque_dt)
        
        # Response should drive toward steady state
        steady_result = screw_feeder.steady_state(u)
        if steady_result[0] > x[0]:
            assert dflow_dt > 0
        if steady_result[1] > x[1]:
            assert dtorque_dt > 0
    
    def test_dynamics_stability(self, screw_feeder):
        """Test that dynamics are stable at steady state."""
        u = np.array([100.0, 0.3, 0.02])
        steady_state = screw_feeder.steady_state(u)
        
        # At steady state, derivatives should be close to zero
        dxdt = screw_feeder.dynamics(0.0, steady_state, u)
        
        assert abs(dxdt[0]) < 1e-10  # Flow rate derivative
        assert abs(dxdt[1]) < 1e-10  # Torque derivative
    
    def test_volumetric_flow_calculation(self, screw_feeder):
        """Test volumetric flow calculation."""
        u = np.array([100.0, 0.3, 0.02])
        
        # Calculate expected theoretical volume flow
        screw_area = np.pi * (screw_feeder.screw_diameter/2)**2
        volume_per_rev = screw_area * screw_feeder.screw_pitch
        theoretical_vol_flow = (100.0/60.0) * volume_per_rev
        
        result = screw_feeder.steady_state(u)
        flow_rate = result[0]
        
        # Actual mass flow should be related to theoretical volume flow
        expected_mass_flow = theoretical_vol_flow * screw_feeder.powder_density * screw_feeder.fill_factor
        
        # Should be in reasonable range considering corrections
        assert 0.1 * expected_mass_flow < flow_rate < 2.0 * expected_mass_flow
    
    def test_fill_factor_effect(self):
        """Test effect of different fill factors."""
        # Low fill factor
        low_fill_feeder = ScrewFeeder(fill_factor=0.1)
        # High fill factor
        high_fill_feeder = ScrewFeeder(fill_factor=0.6)
        
        u = np.array([100.0, 0.3, 0.02])
        
        low_result = low_fill_feeder.steady_state(u)
        high_result = high_fill_feeder.steady_state(u)
        
        # Higher fill factor should give higher flow rate
        assert high_result[0] > low_result[0]
    
    def test_powder_density_effect(self):
        """Test effect of powder density on flow rate."""
        # Light powder
        light_feeder = ScrewFeeder(powder_density=300.0)
        # Heavy powder
        heavy_feeder = ScrewFeeder(powder_density=1500.0)
        
        u = np.array([100.0, 0.3, 0.02])
        
        light_result = light_feeder.steady_state(u)
        heavy_result = heavy_feeder.steady_state(u)
        
        # Heavier powder should give higher mass flow rate
        assert heavy_result[0] > light_result[0]
    
    def test_powder_flowability_effect(self):
        """Test effect of powder flowability on performance."""
        # Poor flowability
        poor_flow_feeder = ScrewFeeder(powder_flowability=0.3)
        # Good flowability
        good_flow_feeder = ScrewFeeder(powder_flowability=0.9)
        
        u = np.array([100.0, 0.3, 0.02])
        
        poor_result = poor_flow_feeder.steady_state(u)
        good_result = good_flow_feeder.steady_state(u)
        
        # Better flowability should give higher flow rate
        assert good_result[0] > poor_result[0]
    
    def test_screw_geometry_effect(self):
        """Test effect of screw geometry on performance."""
        # Small diameter
        small_feeder = ScrewFeeder(screw_diameter=0.025)
        # Large diameter
        large_feeder = ScrewFeeder(screw_diameter=0.1)
        
        u = np.array([100.0, 0.3, 0.02])
        
        small_result = small_feeder.steady_state(u)
        large_result = large_feeder.steady_state(u)
        
        # Larger diameter should give higher capacity
        assert large_result[0] > small_result[0]
    
    def test_residence_time_calculation(self, screw_feeder):
        """Test residence time calculation in dynamics."""
        x = np.array([0.005, 3.0])
        u = np.array([100.0, 0.3, 0.02])
        
        # Expected residence time
        if u[0] > 0:
            expected_res_time = 60.0 * screw_feeder.screw_length / (screw_feeder.screw_pitch * u[0])
        else:
            expected_res_time = 10.0
        
        dxdt = screw_feeder.dynamics(0.0, x, u)
        
        # Should produce finite derivatives
        assert np.all(np.isfinite(dxdt))
        
        # Residence time should be reasonable
        assert expected_res_time > 0
        assert expected_res_time < 1000  # Reasonable upper bound
    
    def test_motor_torque_components(self, screw_feeder):
        """Test motor torque calculation components."""
        u = np.array([100.0, 0.3, 0.02])
        
        result = screw_feeder.steady_state(u)
        torque = result[1]
        
        # Torque should include base torque component
        expected_base_torque = 0.1 * screw_feeder.motor_torque_max
        assert torque >= expected_base_torque
        
        # Should be reasonable for given conditions
        assert torque <= screw_feeder.motor_torque_max
    
    def test_input_validation_types(self, screw_feeder):
        """Test that inputs are properly handled as arrays."""
        u_list = [100.0, 0.3, 0.02]
        u_array = np.array([100.0, 0.3, 0.02])
        
        result_list = screw_feeder.steady_state(u_list)
        result_array = screw_feeder.steady_state(u_array)
        
        np.testing.assert_array_almost_equal(result_list, result_array)
    
    def test_edge_case_zero_hopper_level(self, screw_feeder):
        """Test behavior with zero hopper level."""
        u = np.array([100.0, 0.0, 0.02])
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        # Zero hopper level should severely reduce flow
        assert flow_rate >= 0
        assert flow_rate < 1e-6  # Should be essentially zero
        # Torque should still be positive (base torque)
        assert torque > 0
    
    def test_edge_case_maximum_moisture(self, screw_feeder):
        """Test behavior with very high moisture content."""
        u = np.array([100.0, 0.3, 0.5])  # 50% moisture
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        # High moisture should significantly affect performance
        assert flow_rate >= 0
        assert torque > 0
        
        # Compare with dry conditions
        dry_result = screw_feeder.steady_state(np.array([100.0, 0.3, 0.0]))
        
        # Wet conditions should reduce flow and increase torque
        assert flow_rate <= dry_result[0]
        assert torque >= dry_result[1]
    
    def test_edge_case_very_low_speed(self, screw_feeder):
        """Test behavior with very low screw speed."""
        u = np.array([1.0, 0.3, 0.02])  # 1 rpm
        
        result = screw_feeder.steady_state(u)
        flow_rate, torque = result
        
        # Very low speed should give very low flow
        assert flow_rate >= 0
        assert flow_rate < 0.001  # Should be very small
        assert torque > 0
    
    def test_performance_consistency(self, screw_feeder):
        """Test that model gives consistent results."""
        u = np.array([100.0, 0.3, 0.02])
        
        # Run multiple times
        results = [screw_feeder.steady_state(u) for _ in range(5)]
        
        # All results should be identical
        for i in range(1, len(results)):
            np.testing.assert_array_equal(results[0], results[i])
    
    def test_flow_rate_linearity(self, screw_feeder):
        """Test approximate linearity of flow rate with speed."""
        base_speed = 100.0
        double_speed = 200.0
        
        u_base = np.array([base_speed, 0.3, 0.02])
        u_double = np.array([double_speed, 0.3, 0.02])
        
        result_base = screw_feeder.steady_state(u_base)
        result_double = screw_feeder.steady_state(u_double)
        
        # Flow rate should approximately double with speed
        # (allowing for torque limiting effects)
        ratio = result_double[0] / max(result_base[0], 1e-10)
        assert 1.5 < ratio < 2.5  # Approximately linear
