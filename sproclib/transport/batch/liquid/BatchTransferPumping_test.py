"""
Test suite for BatchTransferPumping class.
Tests cover steady-state calculations, dynamic behavior, and edge cases.
"""

import pytest
import numpy as np
import sys
import os

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from BatchTransferPumping import BatchTransferPumping


class TestBatchTransferPumping:
    """Test cases for BatchTransferPumping model."""

    @pytest.fixture
    def default_pump(self):
        """Create a default pump instance for testing."""
        return BatchTransferPumping(
            pump_capacity=0.01,      # 10 L/s
            pump_head_max=50.0,      # 50 m
            tank_volume=1.0,         # 1 m³
            pipe_length=20.0,        # 20 m
            pipe_diameter=0.05,      # 5 cm
            fluid_density=1000.0,    # Water
            fluid_viscosity=1e-3,    # Water viscosity
            transfer_efficiency=0.85
        )

    @pytest.fixture
    def high_viscosity_pump(self):
        """Create a pump instance for high viscosity fluid testing."""
        return BatchTransferPumping(
            pump_capacity=0.005,     # Lower capacity
            pump_head_max=30.0,      # Lower head
            tank_volume=0.5,         # Smaller tank
            pipe_length=10.0,        # Shorter pipe
            pipe_diameter=0.03,      # Smaller diameter
            fluid_density=1200.0,    # Heavy fluid
            fluid_viscosity=0.05,    # High viscosity (honey-like)
            transfer_efficiency=0.75
        )

    def test_initialization(self, default_pump):
        """Test proper initialization of pump parameters."""
        assert default_pump.pump_capacity == 0.01
        assert default_pump.pump_head_max == 50.0
        assert default_pump.tank_volume == 1.0
        assert default_pump.pipe_length == 20.0
        assert default_pump.pipe_diameter == 0.05
        assert default_pump.fluid_density == 1000.0
        assert default_pump.fluid_viscosity == 1e-3
        assert default_pump.transfer_efficiency == 0.85
        assert default_pump.name == "BatchTransferPumping"

    def test_describe_method(self, default_pump):
        """Test the describe method returns proper metadata."""
        description = default_pump.describe()
        
        assert isinstance(description, dict)
        assert description["name"] == "BatchTransferPumping"
        assert description["type"] == "Batch Transfer Process Model"
        assert description["category"] == "Transport/Batch/Liquid"
        assert "algorithms" in description
        assert "parameters" in description
        assert "equations" in description
        assert "working_ranges" in description
        
        # Check parameter structure
        assert "pump_capacity" in description["parameters"]
        assert description["parameters"]["pump_capacity"]["value"] == 0.01
        assert description["parameters"]["pump_capacity"]["unit"] == "m³/s"

    def test_steady_state_normal_operation(self, default_pump):
        """Test steady-state calculations under normal conditions."""
        # Normal transfer: source higher than destination
        u = np.array([0.8, 0.2, 1.0])  # 80% source, 20% dest, full pump speed
        result = default_pump.steady_state(u)
        
        assert len(result) == 2
        flow_rate, transfer_time = result
        
        # Flow rate should be positive and reasonable
        assert flow_rate > 0
        assert flow_rate <= default_pump.pump_capacity
        
        # Transfer time should be positive and finite
        assert transfer_time > 0
        assert np.isfinite(transfer_time)

    def test_steady_state_uphill_pumping(self, default_pump):
        """Test steady-state with significant uphill pumping."""
        # Large height difference
        u = np.array([0.2, 0.9, 1.0])  # Low source, high destination
        result = default_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        # Flow should still occur but be reduced due to head requirements
        assert flow_rate >= 0
        if flow_rate > 0:
            assert transfer_time > 0

    def test_steady_state_partial_pump_speed(self, default_pump):
        """Test steady-state with reduced pump speed."""
        # Half pump speed
        u = np.array([0.8, 0.2, 0.5])
        result = default_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        # Flow rate should be reduced proportionally
        u_full = np.array([0.8, 0.2, 1.0])
        result_full = default_pump.steady_state(u_full)
        flow_rate_full, _ = result_full
        
        assert flow_rate < flow_rate_full
        assert flow_rate > 0

    def test_steady_state_zero_pump_speed(self, default_pump):
        """Test steady-state with pump off."""
        u = np.array([0.8, 0.2, 0.0])  # Pump off
        result = default_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        assert flow_rate == 0.0
        assert transfer_time == 0.0

    def test_steady_state_empty_source(self, default_pump):
        """Test steady-state with empty source tank."""
        u = np.array([0.0, 0.2, 1.0])  # Empty source
        result = default_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        assert transfer_time == 0.0

    def test_dynamics_initialization(self, default_pump):
        """Test dynamic model initialization."""
        x = np.array([0.005, 0.8])  # Initial flow rate and source level
        u = np.array([0.8, 0.2, 1.0])  # Setpoint, dest level, pump speed
        
        dxdt = default_pump.dynamics(0.0, x, u)
        
        assert len(dxdt) == 2
        assert np.all(np.isfinite(dxdt))

    def test_dynamics_pump_startup(self, default_pump):
        """Test pump startup dynamics."""
        # Start with zero flow rate
        x = np.array([0.0, 0.8])
        u = np.array([0.8, 0.2, 1.0])
        
        dxdt = default_pump.dynamics(0.0, x, u)
        dflow_dt, dlevel_dt = dxdt
        
        # Flow rate should increase (positive derivative)
        assert dflow_dt > 0
        
        # Level should decrease (negative derivative) once flow starts
        assert dlevel_dt <= 0

    def test_dynamics_steady_state_approach(self, default_pump):
        """Test that dynamics approach steady-state values."""
        x = np.array([0.008, 0.8])  # Near steady-state flow
        u = np.array([0.8, 0.2, 1.0])
        
        # Get steady-state reference
        ss_result = default_pump.steady_state([0.8, 0.2, 1.0])
        ss_flow = ss_result[0]
        
        dxdt = default_pump.dynamics(0.0, x, u)
        dflow_dt, dlevel_dt = dxdt
        
        # If current flow is close to steady-state, derivative should be small
        if abs(x[0] - ss_flow) < 0.001:
            assert abs(dflow_dt) < 0.1

    def test_dynamics_empty_tank_constraint(self, default_pump):
        """Test that flow stops when tank is empty."""
        x = np.array([0.005, 0.0])  # Some flow, empty tank
        u = np.array([0.0, 0.2, 1.0])
        
        dxdt = default_pump.dynamics(0.0, x, u)
        dflow_dt, dlevel_dt = dxdt
        
        # Level derivative should be zero when empty
        assert dlevel_dt == 0.0

    def test_high_viscosity_flow(self, high_viscosity_pump):
        """Test behavior with high viscosity fluid."""
        u = np.array([0.8, 0.2, 1.0])
        result = high_viscosity_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        # Should still produce flow but with higher friction losses
        assert flow_rate >= 0
        if flow_rate > 0:
            assert transfer_time > 0

    def test_reynolds_number_regimes(self, default_pump):
        """Test that model handles different Reynolds number regimes."""
        # Test various pump speeds to get different flow rates
        pump_speeds = [0.1, 0.5, 1.0]
        u_base = [0.8, 0.2]
        
        results = []
        for speed in pump_speeds:
            u = np.array(u_base + [speed])
            result = default_pump.steady_state(u)
            results.append(result[0])  # Flow rate
        
        # Flow rates should increase with pump speed
        assert results[0] <= results[1] <= results[2]

    def test_parameter_sensitivity(self, default_pump):
        """Test model sensitivity to key parameters."""
        base_u = np.array([0.8, 0.2, 1.0])
        base_result = default_pump.steady_state(base_u)
        base_flow = base_result[0]
        
        # Test pipe diameter effect
        original_diameter = default_pump.pipe_diameter
        default_pump.pipe_diameter = original_diameter * 2  # Double diameter
        larger_pipe_result = default_pump.steady_state(base_u)
        larger_pipe_flow = larger_pipe_result[0]
        
        # Larger pipe should allow higher flow (less friction)
        assert larger_pipe_flow >= base_flow
        
        # Restore original value
        default_pump.pipe_diameter = original_diameter

    def test_edge_case_very_small_inputs(self, default_pump):
        """Test behavior with very small input values."""
        u = np.array([0.001, 0.0, 0.01])  # Very small values
        result = default_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        # Should handle small values without errors
        assert np.isfinite(flow_rate)
        assert np.isfinite(transfer_time)
        assert flow_rate >= 0

    def test_mass_conservation(self, default_pump):
        """Test that mass is conserved in dynamic simulation."""
        # Simple mass balance check
        x = np.array([0.005, 0.5])  # 5 L/s flow, 50% level
        u = np.array([0.5, 0.2, 1.0])
        
        dxdt = default_pump.dynamics(0.0, x, u)
        dflow_dt, dlevel_dt = dxdt
        
        # For a given flow rate, level change should match mass balance
        expected_dlevel_dt = -x[0] / default_pump.tank_volume
        
        # Allow small numerical differences
        assert abs(dlevel_dt - expected_dlevel_dt) < 1e-6

    def test_pump_head_limitation(self, default_pump):
        """Test that pump respects head limitations."""
        # Create scenario with very high head requirement
        u = np.array([0.1, 2.0, 1.0])  # Low source, very high destination
        result = default_pump.steady_state(u)
        
        flow_rate, transfer_time = result
        
        # Flow should be limited or zero due to insufficient head
        assert flow_rate <= default_pump.pump_capacity

    def test_numerical_stability(self, default_pump):
        """Test numerical stability with various input combinations."""
        test_cases = [
            [0.9, 0.1, 0.9],   # High source, low dest
            [0.1, 0.9, 0.1],   # Low source, high dest
            [0.5, 0.5, 0.5],   # Equal levels, medium speed
            [0.0, 1.0, 1.0],   # Empty source, full dest
            [1.0, 0.0, 1.0],   # Full source, empty dest
        ]
        
        for case in test_cases:
            u = np.array(case)
            result = default_pump.steady_state(u)
            
            # All results should be finite and non-negative
            assert np.all(np.isfinite(result))
            assert np.all(result >= 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
