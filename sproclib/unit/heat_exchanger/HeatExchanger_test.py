"""
Test file for HeatExchanger class
Chemical engineering validation tests using real heat transfer calculations
"""

import pytest
import numpy as np
import sys
import os

# Add the parent directory to the Python path to import HeatExchanger
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from sproclib.unit.heat_exchanger.HeatExchanger import HeatExchanger


class TestHeatExchanger:
    """Test suite for HeatExchanger class focusing on chemical engineering principles"""
    
    @pytest.fixture
    def default_heat_exchanger(self):
        """Create a default heat exchanger for testing (typical water-water system)"""
        return HeatExchanger(
            U=500.0,           # W/m²·K - typical for water-water
            A=10.0,            # m² - small industrial size
            m_hot=2.0,         # kg/s - hot water flow
            m_cold=2.5,        # kg/s - cold water flow
            cp_hot=4180.0,     # J/kg·K - water specific heat
            cp_cold=4180.0,    # J/kg·K - water specific heat
            V_hot=0.2,         # m³ - hot side volume
            V_cold=0.2,        # m³ - cold side volume
            rho_hot=1000.0,    # kg/m³ - water density
            rho_cold=1000.0    # kg/m³ - water density
        )
    
    @pytest.fixture
    def oil_water_heat_exchanger(self):
        """Create oil-water heat exchanger for process industry testing"""
        return HeatExchanger(
            U=250.0,           # W/m²·K - lower U for oil-water system
            A=25.0,            # m² - larger industrial size
            m_hot=3.0,         # kg/s - hot oil flow
            m_cold=5.0,        # kg/s - cold water flow
            cp_hot=2100.0,     # J/kg·K - oil specific heat
            cp_cold=4180.0,    # J/kg·K - water specific heat
            V_hot=0.5,         # m³ - oil side volume
            V_cold=0.3,        # m³ - water side volume
            rho_hot=850.0,     # kg/m³ - oil density
            rho_cold=1000.0    # kg/m³ - water density
        )
    
    def test_initialization_default(self, default_heat_exchanger):
        """Test initialization with default water-water parameters"""
        hx = default_heat_exchanger
        
        # Verify basic parameters
        assert hx.U == 500.0, "Overall heat transfer coefficient should be 500 W/m²·K"
        assert hx.A == 10.0, "Heat transfer area should be 10 m²"
        assert hx.m_hot == 2.0, "Hot fluid mass flow rate should be 2 kg/s"
        assert hx.m_cold == 2.5, "Cold fluid mass flow rate should be 2.5 kg/s"
        
        # Verify calculated heat capacity rates
        expected_C_hot = 2.0 * 4180.0  # 8360 W/K
        expected_C_cold = 2.5 * 4180.0  # 10450 W/K
        assert abs(hx.C_hot - expected_C_hot) < 1e-6, f"Hot side heat capacity rate should be {expected_C_hot} W/K"
        assert abs(hx.C_cold - expected_C_cold) < 1e-6, f"Cold side heat capacity rate should be {expected_C_cold} W/K"
        
        # Verify Cmin and Cmax
        assert hx.C_min == expected_C_hot, "Cmin should be the hot side capacity rate"
        assert hx.C_max == expected_C_cold, "Cmax should be the cold side capacity rate"
        
        # Verify NTU calculation
        expected_NTU = (500.0 * 10.0) / expected_C_hot  # UA/Cmin
        assert abs(hx.NTU - expected_NTU) < 1e-6, f"NTU should be {expected_NTU}"
        
        # Verify effectiveness is within reasonable range
        assert 0 < hx.effectiveness < 1, "Effectiveness should be between 0 and 1"
    
    def test_effectiveness_ntu_calculation(self, default_heat_exchanger):
        """Test effectiveness-NTU method calculation for counter-current flow"""
        hx = default_heat_exchanger
        
        # For counter-current heat exchanger with Cr ≠ 1:
        # ε = (1 - exp(-NTU(1-Cr))) / (1 - Cr*exp(-NTU(1-Cr)))
        Cr = hx.C_min / hx.C_max
        NTU = hx.NTU
        
        # Manual calculation
        exp_term = np.exp(-NTU * (1 - Cr))
        expected_effectiveness = (1 - exp_term) / (1 - Cr * exp_term)
        
        assert abs(hx.effectiveness - expected_effectiveness) < 1e-6, \
            f"Effectiveness calculation error: expected {expected_effectiveness}, got {hx.effectiveness}"
    
    def test_steady_state_heat_balance(self, default_heat_exchanger):
        """Test steady-state heat balance using realistic temperatures"""
        hx = default_heat_exchanger
        
        # Typical process conditions (K)
        T_hot_in = 363.15   # 90°C hot water inlet
        T_cold_in = 293.15  # 20°C cold water inlet
        
        # Calculate steady-state outlet temperatures
        u = np.array([T_hot_in, T_cold_in])
        T_outlets = hx.steady_state(u)
        T_hot_out, T_cold_out = T_outlets
        
        # Verify energy balance: Q_hot = Q_cold
        Q_hot = hx.C_hot * (T_hot_in - T_hot_out)
        Q_cold = hx.C_cold * (T_cold_out - T_cold_in)
        
        assert abs(Q_hot - Q_cold) < 1e-3, \
            f"Heat balance error: Q_hot = {Q_hot:.3f} W, Q_cold = {Q_cold:.3f} W"
        
        # Verify temperature constraints
        assert T_hot_out > T_cold_out, "Hot outlet must be warmer than cold outlet"
        assert T_hot_out < T_hot_in, "Hot fluid must cool down"
        assert T_cold_out > T_cold_in, "Cold fluid must heat up"
        
        # Verify maximum possible heat transfer is not exceeded
        Q_max = hx.C_min * (T_hot_in - T_cold_in)
        assert Q_hot <= Q_max + 1e-6, "Heat transfer cannot exceed theoretical maximum"
    
    def test_lmtd_calculation(self, default_heat_exchanger):
        """Test Log Mean Temperature Difference calculation"""
        hx = default_heat_exchanger
        
        # Test case with known values
        T_hot_in = 373.15   # 100°C
        T_cold_in = 293.15  # 20°C
        T_hot_out = 323.15  # 50°C
        T_cold_out = 313.15 # 40°C
        
        lmtd = hx.calculate_lmtd(T_hot_in, T_cold_in, T_hot_out, T_cold_out)
        
        # Manual LMTD calculation
        delta_T1 = T_hot_in - T_cold_out  # 373.15 - 313.15 = 60 K
        delta_T2 = T_hot_out - T_cold_in  # 323.15 - 293.15 = 30 K
        expected_lmtd = (delta_T1 - delta_T2) / np.log(delta_T1 / delta_T2)
        expected_lmtd = (60 - 30) / np.log(60 / 30)  # 30 / ln(2) ≈ 43.3 K
        
        assert abs(lmtd - expected_lmtd) < 1e-6, \
            f"LMTD calculation error: expected {expected_lmtd:.3f} K, got {lmtd:.3f} K"
    
    def test_heat_transfer_rate_calculation(self, default_heat_exchanger):
        """Test heat transfer rate calculation"""
        hx = default_heat_exchanger
        
        # Realistic operating conditions
        T_hot_in = 358.15   # 85°C
        T_cold_in = 288.15  # 15°C
        
        # Get steady-state outlet temperatures
        u = np.array([T_hot_in, T_cold_in])
        T_hot_out, T_cold_out = hx.steady_state(u)
        
        # Calculate heat transfer rate
        Q = hx.calculate_heat_transfer_rate(T_hot_in, T_cold_in, T_hot_out, T_cold_out)
        
        # Verify heat transfer rate is positive and reasonable
        assert Q > 0, "Heat transfer rate should be positive"
        
        # Verify against effectiveness method
        Q_max = hx.C_min * (T_hot_in - T_cold_in)
        Q_expected = hx.effectiveness * Q_max
        
        assert abs(Q - Q_expected) < 1e-3, \
            f"Heat transfer rate mismatch: calculated {Q:.3f} W, expected {Q_expected:.3f} W"
    
    def test_oil_water_system(self, oil_water_heat_exchanger):
        """Test realistic oil-water heat exchanger (common in process industry)"""
        hx = oil_water_heat_exchanger
        
        # Typical oil cooling scenario
        T_hot_oil_in = 393.15   # 120°C hot oil
        T_cold_water_in = 298.15  # 25°C cooling water
        
        u = np.array([T_hot_oil_in, T_cold_water_in])
        T_hot_out, T_cold_out = hx.steady_state(u)
        
        # Verify energy balance
        Q_oil = hx.C_hot * (T_hot_oil_in - T_hot_out)
        Q_water = hx.C_cold * (T_cold_out - T_cold_water_in)
        
        assert abs(Q_oil - Q_water) < 1e-3, \
            f"Energy balance error in oil-water system: Q_oil = {Q_oil:.3f}, Q_water = {Q_water:.3f}"
        
        # Verify reasonable outlet temperatures
        assert T_hot_out > T_cold_out, "Oil outlet should be hotter than water outlet"
        assert T_hot_out < T_hot_oil_in, "Oil should cool down"
        assert T_cold_out > T_cold_water_in, "Water should heat up"
    
    def test_dynamics_convergence(self, default_heat_exchanger):
        """Test that dynamics converge to steady-state values"""
        hx = default_heat_exchanger
        
        # Operating conditions
        T_hot_in = 353.15   # 80°C
        T_cold_in = 293.15  # 20°C
        u = np.array([T_hot_in, T_cold_in])
        
        # Get steady-state values
        T_ss = hx.steady_state(u)
        
        # Start from different initial conditions
        x_initial = np.array([T_hot_in, T_cold_in])  # Start at inlet temperatures
        
        # Calculate derivatives
        dxdt = hx.dynamics(0, x_initial, u)
        
        # Verify derivatives point towards steady state
        if x_initial[0] > T_ss[0]:
            assert dxdt[0] < 0, "Hot outlet temperature should decrease"
        else:
            assert dxdt[0] > 0, "Hot outlet temperature should increase"
            
        if x_initial[1] < T_ss[1]:
            assert dxdt[1] > 0, "Cold outlet temperature should increase"
        else:
            assert dxdt[1] < 0, "Cold outlet temperature should decrease"
    
    def test_edge_cases(self, default_heat_exchanger):
        """Test edge cases and boundary conditions"""
        hx = default_heat_exchanger
        
        # Test case: Equal inlet temperatures (no driving force)
        T_equal = 323.15  # 50°C
        u_equal = np.array([T_equal, T_equal])
        T_out_equal = hx.steady_state(u_equal)
        
        # Outlet temperatures should equal inlet temperatures
        assert abs(T_out_equal[0] - T_equal) < 1e-6, "Hot outlet should equal inlet when no driving force"
        assert abs(T_out_equal[1] - T_equal) < 1e-6, "Cold outlet should equal inlet when no driving force"
        
        # Test case: Very small temperature difference
        T_hot_in = 323.16  # 50.01°C
        T_cold_in = 323.15  # 50.00°C
        u_small = np.array([T_hot_in, T_cold_in])
        T_out_small = hx.steady_state(u_small)
        
        # Should still maintain heat balance
        Q_hot = hx.C_hot * (T_hot_in - T_out_small[0])
        Q_cold = hx.C_cold * (T_out_small[1] - T_cold_in)
        assert abs(Q_hot - Q_cold) < 1e-6, "Heat balance should hold for small temperature differences"
    
    def test_performance_metrics(self, default_heat_exchanger):
        """Test performance metrics calculation"""
        hx = default_heat_exchanger
        
        # Operating conditions
        T_hot_in = 363.15   # 90°C
        T_cold_in = 288.15  # 15°C
        u = np.array([T_hot_in, T_cold_in])
        
        # Get steady-state outlet temperatures
        x = hx.steady_state(u)
        
        # Get performance metrics
        metrics = hx.get_performance_metrics(x, u)
        
        # Verify all expected metrics are present
        expected_keys = ['heat_transfer_rate', 'effectiveness', 'lmtd', 'ntu', 
                        'hot_outlet_temp', 'cold_outlet_temp', 'temperature_approach']
        
        for key in expected_keys:
            assert key in metrics, f"Performance metric '{key}' is missing"
        
        # Verify reasonable values
        assert metrics['heat_transfer_rate'] > 0, "Heat transfer rate should be positive"
        assert 0 < metrics['effectiveness'] < 1, "Effectiveness should be between 0 and 1"
        assert metrics['lmtd'] > 0, "LMTD should be positive"
        assert metrics['ntu'] > 0, "NTU should be positive"
        assert metrics['temperature_approach'] > 0, "Temperature approach should be positive"
    
    def test_describe_method(self, default_heat_exchanger):
        """Test the describe method returns proper metadata"""
        hx = default_heat_exchanger
        metadata = hx.describe()
        
        # Verify required fields are present
        required_fields = ['type', 'description', 'category', 'algorithms', 'parameters', 
                          'state_variables', 'inputs', 'outputs', 'valid_ranges', 
                          'applications', 'limitations']
        
        for field in required_fields:
            assert field in metadata, f"Required field '{field}' missing from describe() output"
        
        # Verify field types and content
        assert metadata['type'] == 'HeatExchanger', "Type should be 'HeatExchanger'"
        assert metadata['category'] == 'unit/heat_transfer', "Category should be 'unit/heat_transfer'"
        assert len(metadata['applications']) > 0, "Should have at least one application listed"
        assert len(metadata['limitations']) > 0, "Should have at least one limitation listed"
        
        # Verify parameter metadata includes units
        for param_name, param_info in metadata['parameters'].items():
            assert 'units' in param_info, f"Parameter {param_name} missing units"
            assert 'description' in param_info, f"Parameter {param_name} missing description"
            assert 'value' in param_info, f"Parameter {param_name} missing value"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
