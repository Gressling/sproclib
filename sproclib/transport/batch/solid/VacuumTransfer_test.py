"""
Test file for VacuumTransfer class

This module contains test cases for the VacuumTransfer model including
steady-state calculations, dynamic behavior, and edge cases.
"""

import pytest
import numpy as np
import sys
import os

# Add the project root to the path for testing
project_root = os.path.join(os.path.dirname(__file__), '../../..')
sys.path.insert(0, project_root)

from transport.batch.solid.VacuumTransfer import VacuumTransfer


class TestVacuumTransfer:
    """Test class for VacuumTransfer model."""
    
    @pytest.fixture
    def default_vacuum_transfer(self):
        """Create a default VacuumTransfer instance for testing."""
        return VacuumTransfer(
            vacuum_pump_capacity=100.0,
            transfer_line_diameter=0.05,
            transfer_line_length=5.0,
            powder_density=600.0,
            particle_size=100e-6,
            cyclone_efficiency=0.95,
            vacuum_level_max=-80000.0,
            filter_resistance=1000.0
        )
    
    @pytest.fixture
    def high_capacity_vacuum(self):
        """Create a high-capacity VacuumTransfer instance for testing."""
        return VacuumTransfer(
            vacuum_pump_capacity=500.0,
            transfer_line_diameter=0.1,
            transfer_line_length=20.0,
            powder_density=800.0,
            particle_size=50e-6,
            cyclone_efficiency=0.98,
            vacuum_level_max=-100000.0,
            filter_resistance=500.0
        )
    
    @pytest.fixture
    def fine_powder_vacuum(self):
        """Create a VacuumTransfer instance for fine powder handling."""
        return VacuumTransfer(
            vacuum_pump_capacity=50.0,
            transfer_line_diameter=0.03,
            transfer_line_length=10.0,
            powder_density=400.0,
            particle_size=20e-6,
            cyclone_efficiency=0.92,
            vacuum_level_max=-60000.0,
            filter_resistance=2000.0
        )
    
    def test_initialization(self, default_vacuum_transfer):
        """Test proper initialization of VacuumTransfer."""
        assert default_vacuum_transfer.vacuum_pump_capacity == 100.0
        assert default_vacuum_transfer.transfer_line_diameter == 0.05
        assert default_vacuum_transfer.transfer_line_length == 5.0
        assert default_vacuum_transfer.powder_density == 600.0
        assert default_vacuum_transfer.particle_size == 100e-6
        assert default_vacuum_transfer.cyclone_efficiency == 0.95
        assert default_vacuum_transfer.vacuum_level_max == -80000.0
        assert default_vacuum_transfer.filter_resistance == 1000.0
        assert default_vacuum_transfer.name == "VacuumTransfer"
    
    def test_steady_state_normal_operation(self, default_vacuum_transfer):
        """Test steady-state calculation under normal operating conditions."""
        # Half-full source, moderate vacuum, clean filter
        u = np.array([0.5, -50000.0, 0.1])  # [powder_level, vacuum_setpoint, filter_loading]
        result = default_vacuum_transfer.steady_state(u)
        
        assert len(result) == 2
        powder_rate, vacuum_level = result
        
        # Should have positive transfer rate and negative vacuum
        assert powder_rate >= 0
        assert vacuum_level <= 0
        
        # Vacuum level should be reasonable
        assert vacuum_level >= -100000.0
    
    def test_steady_state_no_powder(self, default_vacuum_transfer):
        """Test steady-state with no powder available."""
        u = np.array([0.0, -50000.0, 0.0])  # [powder_level=0, vacuum_setpoint, filter_loading]
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        assert powder_rate == 0.0
        assert vacuum_level == 0.0
    
    def test_steady_state_high_filter_loading(self, default_vacuum_transfer):
        """Test steady-state with highly loaded filter."""
        u = np.array([0.8, -60000.0, 0.9])  # High filter loading
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # High filter loading should reduce vacuum performance
        # Compare with clean filter case
        u_clean = np.array([0.8, -60000.0, 0.0])
        result_clean = default_vacuum_transfer.steady_state(u_clean)
        
        # Loaded filter should have lower vacuum magnitude
        assert abs(vacuum_level) <= abs(result_clean[1])
    
    def test_steady_state_fine_particles(self, fine_powder_vacuum):
        """Test steady-state with fine particles (harder to pick up)."""
        u = np.array([0.7, -50000.0, 0.2])
        result = fine_powder_vacuum.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # Fine particles require higher air velocity for pickup
        # Should still transfer but possibly at lower rate
        assert powder_rate >= 0
        assert vacuum_level <= 0
    
    def test_steady_state_large_particles(self, default_vacuum_transfer):
        """Test steady-state with larger particles."""
        # Temporarily modify particle size
        original_size = default_vacuum_transfer.particle_size
        default_vacuum_transfer.particle_size = 300e-6  # Larger particles
        
        u = np.array([0.6, -40000.0, 0.1])
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # Larger particles are easier to pick up
        assert powder_rate >= 0
        assert vacuum_level <= 0
        
        # Restore original value
        default_vacuum_transfer.particle_size = original_size
    
    def test_air_velocity_calculation(self, default_vacuum_transfer):
        """Test air velocity calculation logic."""
        u = np.array([0.5, -50000.0, 0.0])
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # If transfer occurs, air velocity must be sufficient
        if powder_rate > 0:
            # Calculate pickup velocity
            g = 9.81
            air_density = 1.2
            particle_size = default_vacuum_transfer.particle_size
            powder_density = default_vacuum_transfer.powder_density
            
            terminal_velocity = np.sqrt(4 * g * particle_size * powder_density / (3 * 0.44 * air_density))
            pickup_velocity = 2 * terminal_velocity
            
            # Air velocity should exceed pickup velocity
            air_velocity = np.sqrt(2 * abs(vacuum_level) / air_density)
            assert air_velocity >= pickup_velocity
    
    def test_pump_capacity_limits(self, default_vacuum_transfer):
        """Test that transfer is limited by pump capacity."""
        # Very high vacuum setpoint
        u = np.array([1.0, -150000.0, 0.0])
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # Vacuum should be limited by pump capacity and system resistance
        assert abs(vacuum_level) <= abs(default_vacuum_transfer.vacuum_level_max)
    
    def test_cyclone_efficiency_effect(self, default_vacuum_transfer):
        """Test effect of cyclone efficiency on transfer rate."""
        # Test with different cyclone efficiencies
        original_efficiency = default_vacuum_transfer.cyclone_efficiency
        
        # High efficiency
        default_vacuum_transfer.cyclone_efficiency = 0.99
        u = np.array([0.8, -60000.0, 0.1])
        result_high = default_vacuum_transfer.steady_state(u)
        
        # Low efficiency
        default_vacuum_transfer.cyclone_efficiency = 0.80
        result_low = default_vacuum_transfer.steady_state(u)
        
        # Higher efficiency should give higher transfer rate
        if result_high[0] > 0 and result_low[0] > 0:
            assert result_high[0] >= result_low[0]
        
        # Restore original value
        default_vacuum_transfer.cyclone_efficiency = original_efficiency
    
    def test_dynamics_initialization(self, default_vacuum_transfer):
        """Test dynamic model initialization and basic response."""
        x = np.array([0.0, 0.0])  # [transfer_rate, vacuum_level]
        u = np.array([0.7, -50000.0, 0.2])
        
        result = default_vacuum_transfer.dynamics(0.0, x, u)
        
        assert len(result) == 2
        dtransfer_rate_dt, dvacuum_dt = result
        
        # Both should respond toward steady-state values
        assert isinstance(dtransfer_rate_dt, (int, float))
        assert isinstance(dvacuum_dt, (int, float))
    
    def test_dynamics_steady_state_convergence(self, default_vacuum_transfer):
        """Test that dynamics converge to steady-state values."""
        u = np.array([0.6, -40000.0, 0.1])
        ss_result = default_vacuum_transfer.steady_state(u)
        
        # Start near steady-state
        x = np.array([ss_result[0], ss_result[1]])
        result = default_vacuum_transfer.dynamics(0.0, x, u)
        
        dtransfer_rate_dt, dvacuum_dt = result
        
        # Derivatives should be small when at steady-state
        assert abs(dtransfer_rate_dt) < 1.0  # Small compared to typical rates
        assert abs(dvacuum_dt) < 1000.0      # Small compared to typical pressures
    
    def test_dynamics_response_times(self, default_vacuum_transfer):
        """Test that dynamic response times are reasonable."""
        # Step change in inputs
        x = np.array([0.0, 0.0])
        u = np.array([0.8, -60000.0, 0.0])
        
        result = default_vacuum_transfer.dynamics(0.0, x, u)
        dtransfer_rate_dt, dvacuum_dt = result
        
        # Response rates should be reasonable (not too fast or slow)
        if abs(dtransfer_rate_dt) > 0:
            tau_transfer = abs(result[0] / dtransfer_rate_dt)
            assert 1.0 <= tau_transfer <= 10.0  # Reasonable time constant
        
        if abs(dvacuum_dt) > 0:
            tau_vacuum = abs(result[1] / dvacuum_dt)
            assert 2.0 <= tau_vacuum <= 20.0    # Reasonable time constant
    
    def test_describe_method(self, default_vacuum_transfer):
        """Test the describe method returns proper metadata."""
        metadata = default_vacuum_transfer.describe()
        
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
        assert params['vacuum_pump_capacity']['value'] == 100.0
        assert params['transfer_line_diameter']['value'] == 0.05
        assert params['powder_density']['value'] == 600.0
    
    def test_parameter_validation_ranges(self):
        """Test operation within specified parameter ranges."""
        # Test with parameters at range boundaries
        vacuum_min = VacuumTransfer(
            vacuum_pump_capacity=10.0,
            transfer_line_diameter=0.02,
            powder_density=200.0,
            particle_size=10e-6,
            cyclone_efficiency=0.8,
            vacuum_level_max=-100000.0
        )
        
        vacuum_max = VacuumTransfer(
            vacuum_pump_capacity=500.0,
            transfer_line_diameter=0.15,
            powder_density=1500.0,
            particle_size=500e-6,
            cyclone_efficiency=0.99,
            vacuum_level_max=-10000.0
        )
        
        # Both should operate without errors
        u = np.array([0.5, -30000.0, 0.3])
        
        result_min = vacuum_min.steady_state(u)
        result_max = vacuum_max.steady_state(u)
        
        assert len(result_min) == 2
        assert len(result_max) == 2
        assert all(np.isfinite(result_min))
        assert all(np.isfinite(result_max))
    
    def test_edge_case_zero_vacuum(self, default_vacuum_transfer):
        """Test behavior with zero vacuum setpoint."""
        u = np.array([0.5, 0.0, 0.1])
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # No vacuum should result in no transfer
        assert powder_rate == 0.0
    
    def test_edge_case_very_high_vacuum(self, default_vacuum_transfer):
        """Test behavior with very high vacuum setpoint."""
        u = np.array([0.8, -200000.0, 0.1])  # Higher than max capacity
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        # Should be limited by maximum vacuum capacity
        assert abs(vacuum_level) <= abs(default_vacuum_transfer.vacuum_level_max)
    
    def test_mass_balance_consistency(self, default_vacuum_transfer):
        """Test that powder transfer rates are physically reasonable."""
        u = np.array([0.6, -50000.0, 0.2])
        result = default_vacuum_transfer.steady_state(u)
        
        powder_rate, vacuum_level = result
        
        if powder_rate > 0:
            # Transfer rate should not exceed available material
            available_volume = 0.6 * default_vacuum_transfer.powder_density
            max_available_rate = available_volume * 0.1  # 10% per minute
            assert powder_rate <= max_available_rate


if __name__ == "__main__":
    pytest.main([__file__])
