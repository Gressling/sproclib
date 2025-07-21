"""
Test file for DrumBinTransfer class

This module contains test cases for the DrumBinTransfer model including
steady-state calculations, dynamic behavior, and edge cases.
"""

import pytest
import numpy as np
import sys
import os

# Add the project root to the path for testing
project_root = os.path.join(os.path.dirname(__file__), '../../..')
sys.path.insert(0, project_root)

from .drum_bin_transfer import DrumBinTransfer


class TestDrumBinTransfer:
    """Test class for DrumBinTransfer model."""
    
    @pytest.fixture
    def default_transfer(self):
        """Create a default DrumBinTransfer instance for testing."""
        return DrumBinTransfer(
            container_capacity=0.5,
            transfer_rate_max=100.0,
            material_density=800.0,
            discharge_efficiency=0.9,
            handling_time=120.0,
            conveyor_speed=0.5,
            transfer_distance=10.0
        )
    
    @pytest.fixture
    def high_capacity_transfer(self):
        """Create a high-capacity DrumBinTransfer instance for testing."""
        return DrumBinTransfer(
            container_capacity=2.0,
            transfer_rate_max=500.0,
            material_density=1200.0,
            discharge_efficiency=0.95,
            handling_time=180.0,
            conveyor_speed=1.0,
            transfer_distance=25.0
        )
    
    def test_initialization(self, default_transfer):
        """Test proper initialization of DrumBinTransfer."""
        assert default_transfer.container_capacity == 0.5
        assert default_transfer.transfer_rate_max == 100.0
        assert default_transfer.material_density == 800.0
        assert default_transfer.discharge_efficiency == 0.9
        assert default_transfer.handling_time == 120.0
        assert default_transfer.conveyor_speed == 0.5
        assert default_transfer.transfer_distance == 10.0
        assert default_transfer.name == "DrumBinTransfer"
    
    def test_steady_state_normal_operation(self, default_transfer):
        """Test steady-state calculation under normal operating conditions."""
        # Full container, moderate setpoint, good flowability
        u = np.array([1.0, 80.0, 0.8])  # [fill_level, rate_setpoint, flowability]
        result = default_transfer.steady_state(u)
        
        assert len(result) == 2
        transfer_rate, batch_time = result
        
        # Transfer rate should be limited by setpoint
        assert 0 < transfer_rate <= 80.0
        assert batch_time > 0
        
        # Check that transfer rate considers flowability
        flowability_factor = 0.5 + 0.5 * 0.8
        max_effective_rate = 100.0 * flowability_factor * 0.9
        assert transfer_rate <= max_effective_rate
    
    def test_steady_state_empty_container(self, default_transfer):
        """Test steady-state with empty container."""
        u = np.array([0.0, 50.0, 0.5])  # [fill_level, rate_setpoint, flowability]
        result = default_transfer.steady_state(u)
        
        transfer_rate, batch_time = result
        assert transfer_rate == 0.0
        assert batch_time == 0.0
    
    def test_steady_state_low_fill_level(self, default_transfer):
        """Test steady-state with low fill level (incomplete discharge)."""
        u = np.array([0.05, 50.0, 0.8])  # 5% fill level
        result = default_transfer.steady_state(u)
        
        transfer_rate, batch_time = result
        
        # Rate should be reduced due to low level factor
        level_factor = 0.05 / 0.1  # 0.5
        assert transfer_rate > 0
        assert batch_time > 0
    
    def test_steady_state_poor_flowability(self, default_transfer):
        """Test steady-state with poor flowability material."""
        u = np.array([0.8, 80.0, 0.1])  # Poor flowability
        result = default_transfer.steady_state(u)
        
        transfer_rate, batch_time = result
        
        # Rate should be significantly reduced
        flowability_factor = 0.5 + 0.5 * 0.1  # 0.55
        expected_max_rate = 100.0 * flowability_factor * 0.9
        assert transfer_rate <= expected_max_rate
        assert transfer_rate < 80.0  # Less than setpoint due to poor flowability
    
    def test_steady_state_high_setpoint(self, default_transfer):
        """Test steady-state with setpoint higher than maximum capacity."""
        u = np.array([1.0, 200.0, 1.0])  # High setpoint, excellent flowability
        result = default_transfer.steady_state(u)
        
        transfer_rate, batch_time = result
        
        # Rate should be limited by maximum effective rate
        max_effective_rate = 100.0 * 1.0 * 0.9  # 90 kg/min
        assert transfer_rate <= max_effective_rate
    
    def test_dynamics_initialization(self, default_transfer):
        """Test dynamic model initialization and basic response."""
        x = np.array([0.0, 1.0])  # [transfer_rate, fill_level]
        u = np.array([1.0, 50.0, 0.8])  # [target_fill_level, rate_setpoint, flowability]
        
        result = default_transfer.dynamics(0.0, x, u)
        
        assert len(result) == 2
        dtransfer_rate_dt, dfill_level_dt = result
        
        # Transfer rate should increase toward steady-state
        assert dtransfer_rate_dt > 0
        
        # Fill level should decrease due to discharge
        assert dfill_level_dt < 0
    
    def test_dynamics_steady_state_convergence(self, default_transfer):
        """Test that dynamics converge to steady-state values."""
        # Start at steady-state conditions
        u = np.array([1.0, 50.0, 0.8])
        ss_result = default_transfer.steady_state([1.0, 50.0, 0.8])
        transfer_rate_ss = ss_result[0]
        
        x = np.array([transfer_rate_ss, 1.0])  # At steady-state transfer rate
        result = default_transfer.dynamics(0.0, x, u)
        
        dtransfer_rate_dt, dfill_level_dt = result
        
        # Transfer rate derivative should be near zero
        assert abs(dtransfer_rate_dt) < 1e-6
        
        # Fill level should still decrease
        assert dfill_level_dt < 0
    
    def test_dynamics_empty_container(self, default_transfer):
        """Test dynamics when container becomes empty."""
        x = np.array([50.0, 0.0])  # [transfer_rate, fill_level=0]
        u = np.array([0.0, 50.0, 0.8])
        
        result = default_transfer.dynamics(0.0, x, u)
        
        dtransfer_rate_dt, dfill_level_dt = result
        
        # Fill level derivative should be zero when empty
        assert dfill_level_dt == 0.0
    
    def test_mass_balance(self, default_transfer):
        """Test mass balance consistency in dynamics."""
        x = np.array([60.0, 0.5])  # [transfer_rate, fill_level]
        u = np.array([0.5, 80.0, 0.8])
        
        result = default_transfer.dynamics(0.0, x, u)
        dtransfer_rate_dt, dfill_level_dt = result
        
        # Calculate expected volume flow rate
        mass_flow_rate = 60.0 / 60.0  # kg/s
        volume_flow_rate = mass_flow_rate / 800.0  # m³/s
        expected_dfill_dt = -volume_flow_rate / 0.5  # 1/s
        
        assert abs(dfill_level_dt - expected_dfill_dt) < 1e-6
    
    def test_describe_method(self, default_transfer):
        """Test the describe method returns proper metadata."""
        metadata = default_transfer.describe()
        
        assert isinstance(metadata, dict)
        assert 'model_type' in metadata
        assert 'description' in metadata
        assert 'algorithms' in metadata
        assert 'parameters' in metadata
        assert 'inputs' in metadata
        assert 'outputs' in metadata
        assert 'states' in metadata
        assert 'equations' in metadata
        assert 'operating_ranges' in metadata
        assert 'applications' in metadata
        assert 'assumptions' in metadata
        
        # Check parameter values match initialization
        params = metadata['parameters']
        assert params['container_capacity']['value'] == 0.5
        assert params['transfer_rate_max']['value'] == 100.0
        assert params['material_density']['value'] == 800.0
    
    def test_parameter_validation_ranges(self, default_transfer):
        """Test operation within specified parameter ranges."""
        # Test with parameters at range boundaries
        transfer_min = DrumBinTransfer(
            container_capacity=0.1,
            transfer_rate_max=10.0,
            material_density=200.0,
            discharge_efficiency=0.5
        )
        
        transfer_max = DrumBinTransfer(
            container_capacity=2.0,
            transfer_rate_max=500.0,
            material_density=2000.0,
            discharge_efficiency=1.0
        )
        
        # Both should operate without errors
        u = np.array([0.5, 50.0, 0.7])
        
        result_min = transfer_min.steady_state(u)
        result_max = transfer_max.steady_state(u)
        
        assert len(result_min) == 2
        assert len(result_max) == 2
        assert all(np.isfinite(result_min))
        assert all(np.isfinite(result_max))
    
    def test_edge_case_zero_inputs(self, default_transfer):
        """Test behavior with zero inputs."""
        u = np.array([0.0, 0.0, 0.0])
        result = default_transfer.steady_state(u)
        
        transfer_rate, batch_time = result
        assert transfer_rate == 0.0
        assert batch_time == 0.0
    
    def test_edge_case_maximum_inputs(self, default_transfer):
        """Test behavior with maximum inputs."""
        u = np.array([1.0, 1000.0, 1.0])  # Very high setpoint
        result = default_transfer.steady_state(u)
        
        transfer_rate, batch_time = result
        
        # Should be limited by maximum effective rate
        max_effective = 100.0 * 1.0 * 0.9
        assert transfer_rate <= max_effective
        assert batch_time > 0


if __name__ == "__main__":
    pytest.main([__file__])
