"""
Test file for Compressor class
Chemical engineering focused tests for gas compression calculations
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

import pytest
import numpy as np
from sproclib.unit.compressor.Compressor import Compressor


class TestCompressor:
    @pytest.fixture
    def default_compressor(self):
        """Default compressor instance for testing"""
        return Compressor()
    
    @pytest.fixture
    def natural_gas_compressor(self):
        """Natural gas pipeline compressor configuration"""
        return Compressor(
            eta_isentropic=0.82,
            P_suction=30e5,      # 30 bar
            P_discharge=80e5,    # 80 bar  
            T_suction=288.0,     # 15°C
            gamma=1.3,           # Natural gas
            M=0.016,             # kg/mol (CH4)
            flow_nominal=100.0   # mol/s
        )
    
    def test_initialization_default(self, default_compressor):
        """Test default parameter initialization"""
        comp = default_compressor
        assert comp.eta_isentropic == 0.75
        assert comp.P_suction == 1e5  # 1 bar
        assert comp.P_discharge == 3e5  # 3 bar
        assert comp.T_suction == 300.0  # K
        assert comp.gamma == 1.4  # Air
        assert comp.M == 0.028  # kg/mol (air)
        
    def test_initialization_custom(self, natural_gas_compressor):
        """Test custom parameter initialization"""
        comp = natural_gas_compressor
        assert comp.eta_isentropic == 0.82
        assert comp.P_suction == 30e5
        assert comp.P_discharge == 80e5
        assert comp.gamma == 1.3
        
    def test_steady_state_basic(self, default_compressor):
        """Test steady-state calculation with default conditions"""
        comp = default_compressor
        u = np.array([1e5, 300.0, 3e5, 1.0])  # [P_suc, T_suc, P_dis, flow]
        result = comp.steady_state(u)
        
        # Expected isentropic temperature rise
        T_isentropic = 300.0 * (3.0)**(0.4/1.4)  # ≈ 370.5 K
        T_expected = 300.0 + (T_isentropic - 300.0) / 0.75  # ≈ 394 K
        
        assert abs(result[0] - T_expected) < 1.0, f"Temperature {result[0]} != {T_expected}"
        assert result[1] > 0, "Power should be positive"
        
    def test_steady_state_natural_gas(self, natural_gas_compressor):
        """Test steady-state with natural gas parameters"""
        comp = natural_gas_compressor
        u = np.array([30e5, 288.0, 80e5, 50.0])  # [P_suc, T_suc, P_dis, flow]
        result = comp.steady_state(u)
        
        # Pressure ratio = 80/30 = 2.67
        # For natural gas (γ=1.3): (2.67)^(0.3/1.3) ≈ 1.245
        T_isentropic = 288.0 * (80.0/30.0)**(0.3/1.3)
        T_expected = 288.0 + (T_isentropic - 288.0) / 0.82
        
        assert abs(result[0] - T_expected) < 2.0, "Natural gas compression temperature"
        assert result[1] > 0, "Power consumption should be positive"
        
    def test_power_calculation(self, default_compressor):
        """Test power calculation consistency"""
        comp = default_compressor
        u = np.array([1e5, 300.0, 2e5, 2.0])  # Lower pressure ratio, higher flow
        result = comp.steady_state(u)
        
        # Manual power calculation
        T_out = result[0]
        expected_power = 2.0 * comp.R * (T_out - 300.0) / comp.M
        
        assert abs(result[1] - expected_power) < 1e-6, "Power calculation mismatch"
        
    def test_efficiency_effect(self, default_compressor):
        """Test effect of isentropic efficiency on outlet temperature"""
        comp_low_eff = Compressor(eta_isentropic=0.60)
        comp_high_eff = Compressor(eta_isentropic=0.90)
        
        u = np.array([1e5, 300.0, 4e5, 1.0])  # High pressure ratio
        
        result_low = comp_low_eff.steady_state(u)
        result_high = comp_high_eff.steady_state(u)
        
        # Lower efficiency should give higher outlet temperature
        assert result_low[0] > result_high[0], "Lower efficiency should increase outlet temperature"
        assert result_low[1] > result_high[1], "Lower efficiency should increase power consumption"
        
    def test_pressure_ratio_limits(self, default_compressor):
        """Test behavior at pressure ratio limits"""
        comp = default_compressor
        
        # Pressure ratio = 1 (no compression)
        u_no_compression = np.array([1e5, 300.0, 1e5, 1.0])
        result = comp.steady_state(u_no_compression)
        assert abs(result[0] - 300.0) < 0.1, "No temperature rise at PR=1"
        assert abs(result[1]) < 10.0, "Minimal power at PR=1"
        
        # High pressure ratio
        u_high_pr = np.array([1e5, 300.0, 10e5, 1.0])  # PR = 10
        result = comp.steady_state(u_high_pr)
        assert result[0] > 500.0, "Significant temperature rise at high PR"
        assert result[1] > 1000.0, "High power consumption at high PR"
        
    def test_dynamics_time_constant(self, default_compressor):
        """Test dynamic response characteristics"""
        comp = default_compressor
        
        # Initial state (outlet temperature)
        x = np.array([350.0])  # K
        u = np.array([1e5, 300.0, 3e5, 1.0])
        
        dxdt = comp.dynamics(0.0, x, u)
        
        # Should move toward steady-state value
        T_ss, _ = comp.steady_state(u)
        expected_rate = (T_ss - 350.0) / 2.0  # tau = 2.0 s
        
        assert abs(dxdt[0] - expected_rate) < 1e-6, "Dynamic response rate"
        
    def test_gas_property_variations(self):
        """Test with different gas properties"""
        # Hydrogen (γ=1.41, M=0.002)
        comp_h2 = Compressor(gamma=1.41, M=0.002)
        
        # CO2 (γ=1.30, M=0.044) 
        comp_co2 = Compressor(gamma=1.30, M=0.044)
        
        u = np.array([1e5, 300.0, 3e5, 1.0])
        
        result_h2 = comp_h2.steady_state(u)
        result_co2 = comp_co2.steady_state(u)
        
        # Hydrogen should have different compression characteristics
        assert result_h2[0] != result_co2[0], "Different gases should behave differently"
        # Hydrogen (lower molecular weight) should require less power per mole
        assert result_h2[1] < result_co2[1], "Hydrogen should require less power per mole"
        
    def test_describe_method(self, default_compressor):
        """Test describe method returns proper metadata"""
        comp = default_compressor
        metadata = comp.describe()
        
        assert metadata['type'] == 'Compressor'
        assert 'compression' in metadata['description'].lower()
        assert 'eta_isentropic' in metadata['parameters']
        assert metadata['parameters']['eta_isentropic']['units'] == 'dimensionless'
        assert 'T_out' in metadata['outputs']
        assert 'Power' in metadata['outputs']
        assert len(metadata['applications']) > 3
        assert len(metadata['limitations']) > 2
        
    def test_edge_cases(self, default_compressor):
        """Test edge cases and boundary conditions"""
        comp = default_compressor
        
        # Zero flow
        u_zero_flow = np.array([1e5, 300.0, 3e5, 0.0])
        result = comp.steady_state(u_zero_flow)
        assert result[1] == 0.0, "Zero power at zero flow"
        
        # Very small pressure difference
        u_small_dp = np.array([1e5, 300.0, 1.01e5, 1.0])
        result = comp.steady_state(u_small_dp)
        assert abs(result[0] - 300.0) < 5.0, "Small temperature rise for small ΔP"
        
    def test_parameter_validation_ranges(self, default_compressor):
        """Test parameter validation against typical ranges"""
        comp = default_compressor
        metadata = comp.describe()
        
        # Check efficiency is in valid range
        eta_range = metadata['valid_ranges']['eta_isentropic']
        assert eta_range['min'] <= comp.eta_isentropic <= eta_range['max']
        
        # Check temperature is in valid range  
        T_range = metadata['valid_ranges']['T_suction']
        assert T_range['min'] <= comp.T_suction <= T_range['max']
