"""
Test module for Pump class in SPROCLIB

Tests the base pump model functionality including steady-state calculations,
dynamic response, and parameter validation for chemical engineering applications.
"""

import pytest
import numpy as np
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.Pump import Pump


class TestPump:
    """Test suite for base Pump class."""
    
    @pytest.fixture
    def default_pump(self):
        """Create a default pump instance for testing."""
        return Pump(
            eta=0.75,
            rho=1000.0,
            flow_nominal=0.1,
            delta_P_nominal=200000.0,
            name="TestPump"
        )
    
    @pytest.fixture
    def industrial_pump(self):
        """Create a pump with realistic industrial parameters."""
        return Pump(
            eta=0.82,                    # High efficiency pump
            rho=950.0,                   # Light hydrocarbon density
            flow_nominal=0.05,           # 180 m³/h
            delta_P_nominal=500000.0,    # 5 bar pressure rise
            name="IndustrialPump"
        )
    
    def test_initialization(self, default_pump):
        """Test pump initialization with default parameters."""
        assert default_pump.eta == 0.75
        assert default_pump.rho == 1000.0
        assert default_pump.flow_nominal == 0.1
        assert default_pump.delta_P_nominal == 200000.0
        assert default_pump.name == "TestPump"
        assert 'eta' in default_pump.parameters
        assert 'rho' in default_pump.parameters
    
    def test_parameter_validation(self):
        """Test parameter validation for physical limits."""
        # Test efficiency limits
        with pytest.raises(AssertionError):
            pump = Pump(eta=1.2)  # Efficiency > 1.0
            assert pump.eta <= 1.0, "Efficiency must be ≤ 1.0"
            
        with pytest.raises(AssertionError):
            pump = Pump(eta=-0.1)  # Negative efficiency
            assert pump.eta >= 0.0, "Efficiency must be ≥ 0.0"
        
        # Test density limits
        with pytest.raises(AssertionError):
            pump = Pump(rho=-100.0)  # Negative density
            assert pump.rho > 0.0, "Density must be positive"
    
    def test_steady_state_calculation(self, default_pump):
        """Test steady-state pressure and power calculations."""
        # Test conditions: 1 bar inlet, 0.1 m³/s flow
        P_inlet = 100000.0  # Pa
        flow = 0.1          # m³/s
        u = np.array([P_inlet, flow])
        
        result = default_pump.steady_state(u)
        P_outlet, Power = result
        
        # Verify pressure rise
        expected_P_outlet = P_inlet + default_pump.delta_P_nominal
        assert abs(P_outlet - expected_P_outlet) < 1e-6, f"Expected {expected_P_outlet}, got {P_outlet}"
        
        # Verify power calculation: P = Q * ΔP / η
        expected_Power = flow * default_pump.delta_P_nominal / default_pump.eta
        assert abs(Power - expected_Power) < 1e-6, f"Expected {expected_Power} W, got {Power} W"
    
    def test_power_scaling(self, default_pump):
        """Test power scaling with flow rate."""
        P_inlet = 150000.0  # Pa
        flows = np.array([0.05, 0.1, 0.2])  # m³/s
        
        powers = []
        for flow in flows:
            u = np.array([P_inlet, flow])
            _, power = default_pump.steady_state(u)
            powers.append(power)
        
        # Power should scale linearly with flow rate
        power_ratios = np.array(powers) / powers[0]
        flow_ratios = flows / flows[0]
        
        np.testing.assert_allclose(power_ratios, flow_ratios, rtol=1e-10,
                                 err_msg="Power should scale linearly with flow rate")
    
    def test_dynamics_time_constant(self, default_pump):
        """Test dynamic response characteristics."""
        # Initial state: outlet pressure
        P_out_initial = 250000.0  # Pa
        x = np.array([P_out_initial])
        
        # Input: inlet pressure and flow
        P_inlet = 100000.0  # Pa
        flow = 0.1          # m³/s
        u = np.array([P_inlet, flow])
        
        # Calculate derivative
        dxdt = default_pump.dynamics(0.0, x, u)
        
        # Expected steady-state outlet pressure
        P_out_ss = P_inlet + default_pump.delta_P_nominal
        
        # Expected derivative: (P_ss - P_out) / tau
        tau = 1.0  # Default time constant
        expected_derivative = (P_out_ss - P_out_initial) / tau
        
        assert abs(dxdt[0] - expected_derivative) < 1e-6, \
            f"Expected derivative {expected_derivative}, got {dxdt[0]}"
    
    def test_industrial_conditions(self, industrial_pump):
        """Test pump under realistic industrial conditions."""
        # Typical process conditions
        P_inlet = 300000.0   # 3 bar absolute
        flow = 0.05          # 180 m³/h
        u = np.array([P_inlet, flow])
        
        P_outlet, Power = industrial_pump.steady_state(u)
        
        # Check pressure rise
        delta_P = P_outlet - P_inlet
        assert abs(delta_P - industrial_pump.delta_P_nominal) < 1e-6
        
        # Check power in reasonable range (kW)
        Power_kW = Power / 1000.0
        assert 10.0 < Power_kW < 50.0, f"Power {Power_kW:.1f} kW outside expected range"
    
    def test_efficiency_impact(self, default_pump):
        """Test impact of efficiency on power consumption."""
        P_inlet = 100000.0  # Pa
        flow = 0.1          # m³/s
        u = np.array([P_inlet, flow])
        
        # Test different efficiencies
        efficiencies = [0.6, 0.75, 0.9]
        powers = []
        
        for eta in efficiencies:
            pump = Pump(eta=eta, rho=1000.0, flow_nominal=0.1, delta_P_nominal=200000.0)
            _, power = pump.steady_state(u)
            powers.append(power)
        
        # Higher efficiency should result in lower power consumption
        assert powers[0] > powers[1] > powers[2], \
            "Power should decrease with increasing efficiency"
        
        # Verify inverse relationship: P ∝ 1/η
        power_ratios = np.array(powers) / powers[-1]  # Normalize by highest efficiency
        eta_ratios = efficiencies[-1] / np.array(efficiencies)
        
        np.testing.assert_allclose(power_ratios, eta_ratios, rtol=1e-10,
                                 err_msg="Power should be inversely proportional to efficiency")
    
    def test_density_effect(self, default_pump):
        """Test effect of fluid density on pump operation."""
        P_inlet = 100000.0  # Pa
        flow = 0.1          # m³/s
        
        # Test different fluid densities
        densities = [800.0, 1000.0, 1200.0]  # kg/m³ (light oil, water, brine)
        
        for rho in densities:
            pump = Pump(eta=0.75, rho=rho, flow_nominal=0.1, delta_P_nominal=200000.0)
            u = np.array([P_inlet, flow])
            P_outlet, Power = pump.steady_state(u)
            
            # Pressure rise should be independent of density for this model
            delta_P = P_outlet - P_inlet
            assert abs(delta_P - pump.delta_P_nominal) < 1e-6, \
                f"Pressure rise should be independent of density, got {delta_P}"
    
    def test_describe_method(self, default_pump):
        """Test the describe method returns proper metadata."""
        description = default_pump.describe()
        
        # Check required keys
        required_keys = ['type', 'description', 'category', 'algorithms', 
                        'parameters', 'state_variables', 'inputs', 'outputs',
                        'valid_ranges', 'applications', 'limitations']
        
        for key in required_keys:
            assert key in description, f"Missing required key: {key}"
        
        # Check specific content
        assert description['type'] == 'Pump'
        assert description['category'] == 'unit/pump'
        assert 'eta' in description['parameters']
        assert 'power_calculation' in description['algorithms']
        
        # Check parameter units
        assert description['parameters']['eta']['units'] == 'dimensionless'
        assert description['parameters']['rho']['units'] == 'kg/m³'
        assert description['parameters']['delta_P_nominal']['units'] == 'Pa'
    
    def test_zero_flow_condition(self, default_pump):
        """Test pump behavior at zero flow (shutoff condition)."""
        P_inlet = 100000.0  # Pa
        flow = 0.0          # m³/s (shutoff)
        u = np.array([P_inlet, flow])
        
        P_outlet, Power = default_pump.steady_state(u)
        
        # Should still provide full pressure rise
        delta_P = P_outlet - P_inlet
        assert abs(delta_P - default_pump.delta_P_nominal) < 1e-6
        
        # Power should be zero at zero flow
        assert abs(Power) < 1e-10, f"Power should be zero at zero flow, got {Power}"
    
    def test_negative_flow_handling(self, default_pump):
        """Test pump behavior with negative flow (reverse flow)."""
        P_inlet = 100000.0  # Pa
        flow = -0.05        # m³/s (reverse flow)
        u = np.array([P_inlet, flow])
        
        P_outlet, Power = default_pump.steady_state(u)
        
        # Should handle negative flow (reverse operation)
        expected_power = flow * default_pump.delta_P_nominal / default_pump.eta
        assert abs(Power - expected_power) < 1e-6, \
            "Power calculation should handle negative flow correctly"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
