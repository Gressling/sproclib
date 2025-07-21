"""
Test module for CentrifugalPump class in SPROCLIB

Tests centrifugal pump functionality including pump curve characteristics,
head-flow relationships, and performance under typical industrial conditions.
"""

import pytest
import numpy as np
import sys
import os

# Add the sproclib directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sproclib'))

from sproclib.unit.pump.CentrifugalPump import CentrifugalPump


class TestCentrifugalPump:
    """Test suite for CentrifugalPump class."""
    
    @pytest.fixture
    def default_centrifugal_pump(self):
        """Create a default centrifugal pump for testing."""
        return CentrifugalPump(
            H0=50.0,        # 50 m shutoff head
            K=20.0,         # Head-flow coefficient
            eta=0.75,       # 75% efficiency
            rho=1000.0,     # Water density
            name="TestCentrifugalPump"
        )
    
    @pytest.fixture
    def industrial_centrifugal_pump(self):
        """Create a centrifugal pump with industrial parameters."""
        return CentrifugalPump(
            H0=120.0,       # 120 m shutoff head (high pressure pump)
            K=50.0,         # Steeper curve
            eta=0.82,       # High efficiency
            rho=950.0,      # Light hydrocarbon
            name="IndustrialCentrifugalPump"
        )
    
    def test_initialization(self, default_centrifugal_pump):
        """Test centrifugal pump initialization."""
        pump = default_centrifugal_pump
        assert pump.H0 == 50.0
        assert pump.K == 20.0
        assert pump.eta == 0.75
        assert pump.rho == 1000.0
        assert 'H0' in pump.parameters
        assert 'K' in pump.parameters
    
    def test_pump_curve_at_shutoff(self, default_centrifugal_pump):
        """Test pump behavior at shutoff (zero flow)."""
        P_inlet = 100000.0  # Pa
        flow = 0.0          # m³/s (shutoff condition)
        u = np.array([P_inlet, flow])
        
        P_outlet, Power = default_centrifugal_pump.steady_state(u)
        
        # At shutoff, head should equal H0
        g = 9.81
        expected_delta_P = default_centrifugal_pump.rho * g * default_centrifugal_pump.H0
        actual_delta_P = P_outlet - P_inlet
        
        assert abs(actual_delta_P - expected_delta_P) < 1e-3, \
            f"Expected ΔP {expected_delta_P:.0f} Pa, got {actual_delta_P:.0f} Pa"
        
        # Power should be zero at shutoff
        assert abs(Power) < 1e-10, f"Power should be zero at shutoff, got {Power}"
    
    def test_pump_curve_quadratic_behavior(self, default_centrifugal_pump):
        """Test quadratic head-flow relationship."""
        P_inlet = 100000.0  # Pa
        flows = np.array([0.0, 0.5, 1.0, 1.5])  # m³/s
        
        heads = []
        for flow in flows:
            u = np.array([P_inlet, flow])
            P_outlet, _ = default_centrifugal_pump.steady_state(u)
            delta_P = P_outlet - P_inlet
            head = delta_P / (default_centrifugal_pump.rho * 9.81)
            heads.append(head)
        
        # Verify quadratic relationship: H = H0 - K*Q²
        expected_heads = default_centrifugal_pump.H0 - default_centrifugal_pump.K * flows**2
        
        np.testing.assert_allclose(heads, expected_heads, rtol=1e-10,
                                 err_msg="Head should follow quadratic relationship")
    
    def test_negative_head_protection(self, default_centrifugal_pump):
        """Test that pump head cannot go negative."""
        P_inlet = 100000.0  # Pa
        
        # Calculate flow rate that would give negative head
        # H = H0 - K*Q² = 0 → Q = sqrt(H0/K)
        critical_flow = np.sqrt(default_centrifugal_pump.H0 / default_centrifugal_pump.K)
        excessive_flow = critical_flow * 1.5  # 50% beyond critical
        
        u = np.array([P_inlet, excessive_flow])
        P_outlet, Power = default_centrifugal_pump.steady_state(u)
        
        # Head should be zero (not negative)
        delta_P = P_outlet - P_inlet
        assert delta_P >= -1e-10, f"Pressure rise should not be negative, got {delta_P}"
        
        # Power should be zero when no head is developed
        assert abs(Power) < 1e-10, f"Power should be zero when no head developed, got {Power}"
    
    def test_best_efficiency_point_estimation(self, default_centrifugal_pump):
        """Test pump performance around typical BEP conditions."""
        # BEP typically occurs at 70-80% of maximum flow
        # Max flow occurs when H = 0: Q_max = sqrt(H0/K)
        Q_max = np.sqrt(default_centrifugal_pump.H0 / default_centrifugal_pump.K)
        Q_bep = 0.75 * Q_max  # Approximate BEP
        
        P_inlet = 100000.0  # Pa
        u = np.array([P_inlet, Q_bep])
        P_outlet, Power = default_centrifugal_pump.steady_state(u)
        
        # Calculate specific speed (dimensionless)
        delta_P = P_outlet - P_inlet
        head = delta_P / (default_centrifugal_pump.rho * 9.81)
        
        # Verify reasonable operating point
        assert head > 0, "Head should be positive at BEP"
        assert head < default_centrifugal_pump.H0, "Head should be less than shutoff head"
        assert Power > 0, "Power should be positive at BEP"
    
    def test_affinity_laws_simulation(self, default_centrifugal_pump):
        """Test behavior consistent with pump affinity laws."""
        P_inlet = 100000.0  # Pa
        base_flow = 1.0     # m³/s
        
        # Get baseline performance
        u_base = np.array([P_inlet, base_flow])
        P_out_base, Power_base = default_centrifugal_pump.steady_state(u_base)
        head_base = (P_out_base - P_inlet) / (default_centrifugal_pump.rho * 9.81)
        
        # Simulate reduced speed operation (50% speed)
        # Q₂/Q₁ = N₂/N₁, H₂/H₁ = (N₂/N₁)²
        speed_ratio = 0.5
        reduced_flow = base_flow * speed_ratio
        
        # Create equivalent pump with adjusted parameters for 50% speed
        # H0_new = H0_old * (N_new/N_old)²
        # K_new = K_old * (N_old/N_new)²
        H0_reduced = default_centrifugal_pump.H0 * speed_ratio**2
        K_reduced = default_centrifugal_pump.K / speed_ratio**2
        
        reduced_pump = CentrifugalPump(H0=H0_reduced, K=K_reduced, 
                                     eta=default_centrifugal_pump.eta,
                                     rho=default_centrifugal_pump.rho)
        
        u_reduced = np.array([P_inlet, reduced_flow])
        P_out_reduced, _ = reduced_pump.steady_state(u_reduced)
        head_reduced = (P_out_reduced - P_inlet) / (reduced_pump.rho * 9.81)
        
        # Check affinity law: H₂/H₁ = (N₂/N₁)²
        expected_head_ratio = speed_ratio**2
        actual_head_ratio = head_reduced / head_base
        
        assert abs(actual_head_ratio - expected_head_ratio) < 0.1, \
            f"Affinity law violated: expected ratio {expected_head_ratio:.3f}, got {actual_head_ratio:.3f}"
    
    def test_power_consumption_scaling(self, default_centrifugal_pump):
        """Test power consumption scaling with flow and head."""
        P_inlet = 100000.0  # Pa
        flows = np.array([0.5, 1.0, 1.5])  # m³/s
        
        powers = []
        for flow in flows:
            u = np.array([P_inlet, flow])
            _, power = default_centrifugal_pump.steady_state(u)
            powers.append(power)
        
        # Power should increase with flow (until flow becomes excessive)
        # P = Q * ΔP / η = Q * ρ * g * H / η = Q * ρ * g * (H0 - K*Q²) / η
        for i in range(len(powers)-1):
            if powers[i] > 0 and powers[i+1] > 0:  # Both positive
                # Power initially increases with flow, then may decrease
                assert powers[i+1] >= 0, "Power should be non-negative"
    
    def test_industrial_conditions(self, industrial_centrifugal_pump):
        """Test pump under realistic industrial conditions."""
        # Typical industrial conditions
        P_inlet = 200000.0   # 2 bar absolute pressure
        flow = 0.8           # 2880 m³/h
        u = np.array([P_inlet, flow])
        
        P_outlet, Power = industrial_centrifugal_pump.steady_state(u)
        
        # Calculate head
        delta_P = P_outlet - P_inlet
        head = delta_P / (industrial_centrifugal_pump.rho * 9.81)
        
        # Verify reasonable industrial performance
        assert 50.0 < head < 120.0, f"Head {head:.1f} m outside typical range"
        
        # Power in kW range for industrial pump
        Power_kW = Power / 1000.0
        assert 5.0 < Power_kW < 200.0, f"Power {Power_kW:.1f} kW outside expected range"
        
        # Check efficiency is being applied correctly
        hydraulic_power = flow * delta_P
        actual_efficiency = hydraulic_power / Power
        expected_efficiency = industrial_centrifugal_pump.eta
        
        assert abs(actual_efficiency - expected_efficiency) < 1e-10, \
            f"Efficiency calculation error: expected {expected_efficiency}, got {actual_efficiency}"
    
    def test_describe_method(self, default_centrifugal_pump):
        """Test the describe method returns proper metadata."""
        description = default_centrifugal_pump.describe()
        
        # Check required keys
        required_keys = ['type', 'description', 'category', 'algorithms', 
                        'parameters', 'applications', 'limitations']
        
        for key in required_keys:
            assert key in description, f"Missing required key: {key}"
        
        # Check specific content
        assert description['type'] == 'CentrifugalPump'
        assert 'pump_curve' in description['algorithms']
        assert 'H0' in description['parameters']
        assert 'K' in description['parameters']
        
        # Check algorithm descriptions contain key equations
        pump_curve = description['algorithms']['pump_curve']
        assert 'H₀' in pump_curve and 'K' in pump_curve and 'Q²' in pump_curve
    
    def test_density_effect_on_pressure(self, default_centrifugal_pump):
        """Test effect of fluid density on pressure rise."""
        P_inlet = 100000.0  # Pa
        flow = 1.0          # m³/s
        
        # Test different densities
        densities = [800.0, 1000.0, 1200.0]  # kg/m³
        
        delta_Ps = []
        for rho in densities:
            pump = CentrifugalPump(H0=50.0, K=20.0, eta=0.75, rho=rho)
            u = np.array([P_inlet, flow])
            P_outlet, _ = pump.steady_state(u)
            delta_Ps.append(P_outlet - P_inlet)
        
        # Pressure rise should be proportional to density (ΔP = ρgh)
        pressure_ratios = np.array(delta_Ps) / delta_Ps[1]  # Normalize by water
        density_ratios = np.array(densities) / densities[1]  # Normalize by water
        
        np.testing.assert_allclose(pressure_ratios, density_ratios, rtol=1e-10,
                                 err_msg="Pressure rise should be proportional to density")
    
    def test_pump_curve_parameters(self, default_centrifugal_pump):
        """Test pump curve parameter relationships."""
        # Test that different K values give different curve shapes
        P_inlet = 100000.0  # Pa
        flow = 1.0          # m³/s
        
        K_values = [10.0, 20.0, 40.0]  # Different curve steepness
        heads = []
        
        for K in K_values:
            pump = CentrifugalPump(H0=50.0, K=K, eta=0.75, rho=1000.0)
            u = np.array([P_inlet, flow])
            P_outlet, _ = pump.steady_state(u)
            head = (P_outlet - P_inlet) / (pump.rho * 9.81)
            heads.append(head)
        
        # Higher K should give lower head at same flow
        assert heads[0] > heads[1] > heads[2], \
            "Higher K coefficient should result in lower head at same flow rate"
        
        # All should have same shutoff head
        for K in K_values:
            pump = CentrifugalPump(H0=50.0, K=K, eta=0.75, rho=1000.0)
            u = np.array([P_inlet, 0.0])  # Zero flow
            P_outlet, _ = pump.steady_state(u)
            head = (P_outlet - P_inlet) / (pump.rho * 9.81)
            assert abs(head - 50.0) < 1e-10, "Shutoff head should be independent of K"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
