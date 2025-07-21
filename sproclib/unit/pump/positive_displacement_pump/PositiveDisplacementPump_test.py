"""
Test module for PositiveDisplacementPump class in SPROCLIB

Tests positive displacement pump functionality including constant flow behavior,
pressure capability, and performance under high-pressure conditions.
"""

import pytest
import numpy as np
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.PositiveDisplacementPump import PositiveDisplacementPump


class TestPositiveDisplacementPump:
    """Test suite for PositiveDisplacementPump class."""
    
    @pytest.fixture
    def default_pd_pump(self):
        """Create a default positive displacement pump for testing."""
        return PositiveDisplacementPump(
            flow_rate=0.01,      # 36 m³/h constant flow
            eta=0.85,            # 85% efficiency
            rho=1000.0,          # Water density
            name="TestPDPump"
        )
    
    @pytest.fixture
    def high_pressure_pump(self):
        """Create a high-pressure PD pump for industrial applications."""
        return PositiveDisplacementPump(
            flow_rate=0.005,     # 18 m³/h metering flow
            eta=0.90,            # High efficiency
            rho=850.0,           # Light oil density
            name="HighPressurePump"
        )
    
    @pytest.fixture
    def metering_pump(self):
        """Create a precision metering pump."""
        return PositiveDisplacementPump(
            flow_rate=0.001,     # 3.6 m³/h precise flow
            eta=0.80,            # Lower efficiency for precision
            rho=1200.0,          # Dense chemical solution
            name="MeteringPump"
        )
    
    def test_initialization(self, default_pd_pump):
        """Test positive displacement pump initialization."""
        pump = default_pd_pump
        assert pump.flow_rate == 0.01
        assert pump.eta == 0.85
        assert pump.rho == 1000.0
        assert 'flow_rate' in pump.parameters
        assert pump.flow_nominal == pump.flow_rate  # Should inherit from base class
    
    def test_constant_flow_characteristic(self, default_pd_pump):
        """Test that PD pump delivers constant flow regardless of pressure."""
        # Test various inlet pressures
        inlet_pressures = [100000.0, 500000.0, 1000000.0]  # 1, 5, 10 bar
        
        # For PD pump, input is only inlet pressure
        for P_inlet in inlet_pressures:
            u = np.array([P_inlet])
            P_outlet, Power = default_pd_pump.steady_state(u)
            
            # Pressure rise should be constant (delta_P_nominal)
            delta_P = P_outlet - P_inlet
            expected_delta_P = default_pd_pump.delta_P_nominal
            
            assert abs(delta_P - expected_delta_P) < 1e-6, \
                f"Pressure rise should be constant, expected {expected_delta_P}, got {delta_P}"
            
            # Power should depend on total pressure rise
            expected_power = default_pd_pump.flow_rate * delta_P / default_pd_pump.eta
            assert abs(Power - expected_power) < 1e-6, \
                f"Power calculation error: expected {expected_power}, got {Power}"
    
    def test_power_scaling_with_pressure(self, default_pd_pump):
        """Test power scaling with discharge pressure."""
        base_inlet = 100000.0  # 1 bar
        inlet_pressures = np.array([base_inlet, 2*base_inlet, 5*base_inlet])
        
        powers = []
        for P_inlet in inlet_pressures:
            u = np.array([P_inlet])
            _, power = default_pd_pump.steady_state(u)
            powers.append(power)
        
        # Since delta_P is constant, power should be same for all inlet pressures
        power_variation = np.std(powers) / np.mean(powers)
        assert power_variation < 1e-10, \
            f"Power should be constant for PD pump, variation: {power_variation}"
    
    def test_high_pressure_capability(self, high_pressure_pump):
        """Test PD pump performance at high pressures."""
        # Simulate high-pressure injection application
        P_inlet = 1000000.0   # 10 bar inlet
        u = np.array([P_inlet])
        
        P_outlet, Power = high_pressure_pump.steady_state(u)
        
        # Check realistic high-pressure performance
        delta_P = P_outlet - P_inlet
        total_pressure = P_outlet / 1e5  # Convert to bar
        
        assert total_pressure > 20.0, f"High-pressure pump should reach >20 bar, got {total_pressure:.1f} bar"
        
        # Power should be substantial for high pressure
        Power_kW = Power / 1000.0
        assert 1.0 < Power_kW < 50.0, f"Power {Power_kW:.1f} kW outside expected range"
    
    def test_metering_precision(self, metering_pump):
        """Test precision characteristics of metering pump."""
        # Metering pumps should maintain flow regardless of pressure variations
        pressure_variations = [200000.0, 800000.0, 1500000.0]  # 2, 8, 15 bar
        
        outlet_pressures = []
        powers = []
        
        for P_inlet in pressure_variations:
            u = np.array([P_inlet])
            P_outlet, Power = metering_pump.steady_state(u)
            outlet_pressures.append(P_outlet)
            powers.append(Power)
        
        # All should have same pressure rise
        pressure_rises = np.array(outlet_pressures) - np.array(pressure_variations)
        pressure_rise_std = np.std(pressure_rises)
        
        assert pressure_rise_std < 1e-6, \
            f"Pressure rise should be constant for metering pump, std: {pressure_rise_std}"
        
        # Power should be constant (same delta_P, same flow)
        power_std = np.std(powers)
        assert power_std < 1e-6, \
            f"Power should be constant for metering pump, std: {power_std}"
    
    def test_dynamics_response_time(self, default_pd_pump):
        """Test dynamic response characteristics."""
        # Initial state: outlet pressure
        P_out_initial = 400000.0  # 4 bar initial
        x = np.array([P_out_initial])
        
        # Input: inlet pressure
        P_inlet = 100000.0  # 1 bar inlet
        u = np.array([P_inlet])
        
        # Calculate derivative
        dxdt = default_pd_pump.dynamics(0.0, x, u)
        
        # Expected steady-state outlet pressure
        P_out_ss = P_inlet + default_pd_pump.delta_P_nominal
        
        # PD pumps should have faster response (tau = 0.5s)
        tau = 0.5
        expected_derivative = (P_out_ss - P_out_initial) / tau
        
        assert abs(dxdt[0] - expected_derivative) < 1e-6, \
            f"Expected derivative {expected_derivative}, got {dxdt[0]}"
    
    def test_efficiency_impact_on_power(self, default_pd_pump):
        """Test impact of efficiency on power consumption."""
        P_inlet = 300000.0  # 3 bar inlet
        
        # Test different efficiencies
        efficiencies = [0.70, 0.85, 0.95]
        powers = []
        
        for eta in efficiencies:
            pump = PositiveDisplacementPump(flow_rate=0.01, eta=eta, rho=1000.0)
            u = np.array([P_inlet])
            _, power = pump.steady_state(u)
            powers.append(power)
        
        # Higher efficiency should reduce power consumption
        assert powers[0] > powers[1] > powers[2], \
            "Power should decrease with increasing efficiency"
        
        # Verify inverse relationship
        power_ratios = np.array(powers) / powers[-1]
        eta_ratios = efficiencies[-1] / np.array(efficiencies)
        
        np.testing.assert_allclose(power_ratios, eta_ratios, rtol=1e-10,
                                 err_msg="Power should be inversely proportional to efficiency")
    
    def test_viscous_fluid_handling(self, default_pd_pump):
        """Test PD pump behavior with different fluid densities."""
        P_inlet = 200000.0  # 2 bar inlet
        
        # Test different fluid densities (viscosity correlation)
        densities = [700.0, 1000.0, 1300.0]  # Light oil, water, heavy solution
        
        for rho in densities:
            pump = PositiveDisplacementPump(flow_rate=0.01, eta=0.85, rho=rho)
            u = np.array([P_inlet])
            P_outlet, Power = pump.steady_state(u)
            
            # Flow rate should be independent of density for PD pump
            # (This is modeled as constant flow_rate parameter)
            assert pump.flow_rate == 0.01, "Flow rate should be independent of density"
            
            # Pressure rise should be independent of density for this model
            delta_P = P_outlet - P_inlet
            assert abs(delta_P - pump.delta_P_nominal) < 1e-6, \
                f"Pressure rise should be independent of density, got {delta_P}"
    
    def test_describe_method(self, default_pd_pump):
        """Test the describe method returns proper metadata."""
        description = default_pd_pump.describe()
        
        # Check required keys
        required_keys = ['type', 'description', 'category', 'algorithms', 
                        'parameters', 'applications', 'limitations']
        
        for key in required_keys:
            assert key in description, f"Missing required key: {key}"
        
        # Check specific content
        assert description['type'] == 'PositiveDisplacementPump'
        assert 'flow_rate' in description['algorithms']
        assert 'flow_rate' in description['parameters']
        
        # Check applications are appropriate for PD pumps
        applications = description['applications']
        assert any('metering' in app.lower() or 'injection' in app.lower() 
                  for app in applications), "Should include metering/injection applications"
    
    def test_pressure_capability_limits(self, high_pressure_pump):
        """Test pump behavior at pressure limits."""
        # Test very high inlet pressure
        P_inlet = 5000000.0  # 50 bar inlet
        u = np.array([P_inlet])
        
        P_outlet, Power = high_pressure_pump.steady_state(u)
        
        # Should still maintain pressure rise
        delta_P = P_outlet - P_inlet
        assert abs(delta_P - high_pressure_pump.delta_P_nominal) < 1e-6
        
        # Total outlet pressure should be very high
        total_pressure_bar = P_outlet / 1e5
        assert total_pressure_bar > 70.0, f"Should achieve high pressure, got {total_pressure_bar:.1f} bar"
        
        # Power should be substantial
        Power_kW = Power / 1000.0
        assert Power_kW > 5.0, f"Power should be substantial at high pressure, got {Power_kW:.1f} kW"
    
    def test_zero_inlet_pressure_handling(self, default_pd_pump):
        """Test pump behavior with zero inlet pressure (self-priming)."""
        P_inlet = 0.0  # Atmospheric or vacuum condition
        u = np.array([P_inlet])
        
        P_outlet, Power = default_pd_pump.steady_state(u)
        
        # Should still provide full pressure rise
        delta_P = P_outlet - P_inlet
        assert abs(delta_P - default_pd_pump.delta_P_nominal) < 1e-6
        
        # Outlet pressure should equal nominal pressure rise
        assert abs(P_outlet - default_pd_pump.delta_P_nominal) < 1e-6
        
        # Power should be based on full pressure rise
        expected_power = default_pd_pump.flow_rate * default_pd_pump.delta_P_nominal / default_pd_pump.eta
        assert abs(Power - expected_power) < 1e-6
    
    def test_flow_rate_parameter_validation(self):
        """Test flow rate parameter validation."""
        # Test realistic flow rate ranges
        valid_flow_rates = [1e-6, 0.001, 0.01, 0.1]  # From μL/s to 360 m³/h
        
        for flow_rate in valid_flow_rates:
            pump = PositiveDisplacementPump(flow_rate=flow_rate)
            assert pump.flow_rate == flow_rate
            assert pump.flow_rate > 0, "Flow rate must be positive"
        
        # Test parameter consistency
        pump = PositiveDisplacementPump(flow_rate=0.05)
        assert pump.flow_nominal == pump.flow_rate, \
            "flow_nominal should equal flow_rate for PD pumps"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
