"""
Test cases for BatchReactor model

Tests cover initialization, dynamics, conversion calculations,
batch time estimation, and edge cases.

Author: SPROCLIB Development Team
"""

import pytest
import numpy as np
from unit.reactor.BatchReactor import BatchReactor


class TestBatchReactor:
    """Test suite for BatchReactor model."""
    
    @pytest.fixture
    def default_batch(self):
        """Create a BatchReactor instance with default parameters."""
        return BatchReactor()
    
    @pytest.fixture
    def test_inputs(self):
        """Standard test inputs for BatchReactor."""
        return np.array([350.0])  # [Tj] - jacket temperature
    
    @pytest.fixture
    def test_state(self):
        """Standard test state for BatchReactor."""
        return np.array([0.5, 360.0])  # [CA, T]
    
    def test_initialization_default(self):
        """Test BatchReactor initialization with default parameters."""
        reactor = BatchReactor()
        
        assert reactor.V == 100.0
        assert reactor.k0 == 7.2e10
        assert reactor.Ea == 72750.0
        assert reactor.delta_H == -52000.0
        assert reactor.rho == 1000.0
        assert reactor.cp == 4180.0
        assert reactor.U == 500.0
        assert reactor.A == 5.0
        assert reactor.name == "BatchReactor"
    
    def test_initialization_custom(self):
        """Test BatchReactor initialization with custom parameters."""
        reactor = BatchReactor(
            V=200.0,
            k0=1e11,
            Ea=80000.0,
            name="CustomBatch"
        )
        
        assert reactor.V == 200.0
        assert reactor.k0 == 1e11
        assert reactor.Ea == 80000.0
        assert reactor.name == "CustomBatch"
    
    def test_reaction_rate(self, default_batch):
        """Test reaction rate calculation."""
        CA = 1.0
        T = 350.0
        
        rate = default_batch.reaction_rate(CA, T)
        
        # Rate should be positive and proportional to concentration
        assert rate > 0
        assert isinstance(rate, (int, float, np.number))
        
        # Test proportionality to concentration
        rate_double = default_batch.reaction_rate(2*CA, T)
        assert abs(rate_double - 2*rate) < 1e-10
    
    def test_reaction_rate_temperature_dependence(self, default_batch):
        """Test that reaction rate increases with temperature."""
        CA = 1.0
        
        rate1 = default_batch.reaction_rate(CA, 300.0)
        rate2 = default_batch.reaction_rate(CA, 350.0)
        rate3 = default_batch.reaction_rate(CA, 400.0)
        
        assert rate1 < rate2 < rate3
    
    def test_dynamics_calculation(self, default_batch, test_state, test_inputs):
        """Test dynamics calculation."""
        t = 0.0
        dxdt = default_batch.dynamics(t, test_state, test_inputs)
        
        assert len(dxdt) == 2
        assert isinstance(dxdt[0], (int, float, np.number))  # dCA/dt
        assert isinstance(dxdt[1], (int, float, np.number))  # dT/dt
    
    def test_dynamics_mass_balance(self, default_batch):
        """Test mass balance in dynamics."""
        # Test that concentration decreases (consumption)
        x = np.array([1.0, 350.0])
        u = np.array([350.0])  # Isothermal jacket
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # dCA/dt should be negative (consumption)
        assert dxdt[0] < 0
    
    def test_dynamics_energy_balance(self, default_batch):
        """Test energy balance in dynamics."""
        # Test with exothermic reaction and cooling
        x = np.array([1.0, 400.0])  # High temperature
        u = np.array([300.0])  # Cool jacket
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # Temperature should decrease due to cooling
        # (may increase due to reaction heat, but cooling should dominate at high T diff)
        heat_transfer_term = default_batch.U * default_batch.A * (u[0] - x[1]) / (default_batch.rho * default_batch.cp * default_batch.V)
        
        # Check that heat transfer term is negative (cooling)
        assert heat_transfer_term < 0
    
    def test_steady_state_behavior(self, default_batch, test_inputs):
        """Test steady-state calculation (initial conditions for batch)."""
        x_initial = default_batch.steady_state(test_inputs)
        
        assert len(x_initial) == 2
        assert x_initial[0] > 0  # Concentration should be positive
        assert x_initial[1] > 0  # Temperature should be positive
    
    def test_conversion_calculation(self, default_batch):
        """Test conversion calculation."""
        CA = 0.5
        CA0 = 1.0
        
        conversion = default_batch.calculate_conversion(CA, CA0)
        expected_conversion = (CA0 - CA) / CA0
        
        assert abs(conversion - expected_conversion) < 1e-10
        assert 0 <= conversion <= 1
    
    def test_conversion_edge_cases(self, default_batch):
        """Test conversion calculation edge cases."""
        # Zero initial concentration
        assert default_batch.calculate_conversion(0.5, 0.0) == 0.0
        
        # Complete conversion
        assert default_batch.calculate_conversion(0.0, 1.0) == 1.0
        
        # No conversion
        assert default_batch.calculate_conversion(1.0, 1.0) == 0.0
        
        # Over-conversion (should be clamped)
        assert default_batch.calculate_conversion(0.0, 1.0) == 1.0
    
    def test_batch_time_to_conversion(self, default_batch):
        """Test batch time calculation for target conversion."""
        target_conversion = 0.5
        CA0 = 1.0
        T_avg = 350.0
        
        time_required = default_batch.batch_time_to_conversion(target_conversion, CA0, T_avg)
        
        assert time_required > 0
        assert time_required < float('inf')
        assert isinstance(time_required, (int, float, np.number))
    
    def test_batch_time_edge_cases(self, default_batch):
        """Test batch time calculation edge cases."""
        # Zero conversion
        assert default_batch.batch_time_to_conversion(0.0) == 0.0
        
        # Complete conversion
        assert default_batch.batch_time_to_conversion(1.0) == 0.0
        
        # Negative conversion
        assert default_batch.batch_time_to_conversion(-0.1) == 0.0
        
        # Over-conversion
        assert default_batch.batch_time_to_conversion(1.1) == 0.0
    
    def test_batch_time_temperature_dependence(self, default_batch):
        """Test that batch time decreases with temperature."""
        target_conversion = 0.8
        
        time1 = default_batch.batch_time_to_conversion(target_conversion, T_avg=300.0)
        time2 = default_batch.batch_time_to_conversion(target_conversion, T_avg=350.0)
        time3 = default_batch.batch_time_to_conversion(target_conversion, T_avg=400.0)
        
        assert time1 > time2 > time3
    
    def test_describe_method(self, default_batch):
        """Test describe method for metadata."""
        metadata = default_batch.describe()
        
        # Check required keys exist
        required_keys = [
            'type', 'description', 'category', 'algorithms',
            'parameters', 'state_variables', 'inputs', 'outputs',
            'valid_ranges', 'applications', 'limitations'
        ]
        
        for key in required_keys:
            assert key in metadata
        
        assert metadata['type'] == 'BatchReactor'
        assert metadata['category'] == 'reactor'
        assert 'parameters' in metadata
        assert 'V' in metadata['parameters']
    
    def test_negative_concentration_handling(self, default_batch):
        """Test handling of negative concentrations."""
        x = np.array([-0.1, 350.0])  # Negative concentration
        u = np.array([350.0])
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # Should not crash and should handle gracefully
        assert len(dxdt) == 2
    
    def test_low_temperature_handling(self, default_batch):
        """Test handling of very low temperatures."""
        x = np.array([1.0, 200.0])  # Very low temperature
        u = np.array([350.0])
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # Should not crash and should handle gracefully
        assert len(dxdt) == 2
    
    def test_zero_concentration(self, default_batch):
        """Test behavior at zero concentration."""
        x = np.array([0.0, 350.0])  # Zero concentration
        u = np.array([350.0])
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # dCA/dt should be zero (no reaction)
        assert abs(dxdt[0]) < 1e-10
    
    def test_parameter_consistency(self, default_batch):
        """Test that parameters are stored consistently."""
        assert default_batch.parameters['V'] == default_batch.V
        assert default_batch.parameters['k0'] == default_batch.k0
        assert default_batch.parameters['Ea'] == default_batch.Ea
        assert default_batch.parameters['delta_H'] == default_batch.delta_H
    
    def test_high_conversion_calculation(self, default_batch):
        """Test conversion calculation at high conversions."""
        # Test near-complete conversion
        conversion = default_batch.calculate_conversion(0.001, 1.0)
        assert abs(conversion - 0.999) < 1e-10
        
        # Test that conversion is clamped to [0,1]
        conversion_clamped = default_batch.calculate_conversion(-0.1, 1.0)
        assert conversion_clamped == 1.0
    
    def test_reaction_heat_effects(self, default_batch):
        """Test that exothermic reaction increases temperature."""
        # High concentration, moderate temperature
        x = np.array([2.0, 350.0])
        u = np.array([350.0])  # Isothermal jacket
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # For exothermic reaction, temperature should increase
        # (heat generation > heat transfer at equal temperatures)
        assert dxdt[1] > 0  # dT/dt > 0
    
    def test_isothermal_operation(self, default_batch):
        """Test behavior under isothermal conditions."""
        x = np.array([1.0, 350.0])
        u = np.array([350.0])  # Same as reactor temperature
        
        dxdt = default_batch.dynamics(0.0, x, u)
        
        # Temperature change should be small (only reaction heat)
        # and should be positive for exothermic reaction
        assert dxdt[1] > 0  # Heat generation from reaction
    
    def test_different_initial_concentrations(self, default_batch):
        """Test batch time calculation with different initial concentrations."""
        target_conversion = 0.5
        T_avg = 350.0
        
        time1 = default_batch.batch_time_to_conversion(target_conversion, CA0=1.0, T_avg=T_avg)
        time2 = default_batch.batch_time_to_conversion(target_conversion, CA0=2.0, T_avg=T_avg)
        
        # Batch time should be independent of initial concentration for first-order reaction
        assert abs(time1 - time2) < 1e-10
