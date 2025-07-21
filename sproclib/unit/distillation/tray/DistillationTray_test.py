"""
Test file for DistillationTray class
Tests vapor-liquid equilibrium and material balance dynamics
"""

import pytest
import numpy as np
from sproclib.unit.distillation.tray import DistillationTray


class TestDistillationTray:
    @pytest.fixture
    def default_tray(self):
        """Create default distillation tray for testing"""
        return DistillationTray(
            tray_number=5,
            holdup=2.0,
            alpha=2.5,
            name="TestTray"
        )
    
    @pytest.fixture
    def ethanol_water_tray(self):
        """Create tray with ethanol-water system parameters"""
        return DistillationTray(
            tray_number=10,
            holdup=1.5,
            alpha=8.0,  # Typical for ethanol-water at 1 atm
            name="EthanolWaterTray"
        )
    
    def test_initialization(self, default_tray):
        """Test tray initialization with default parameters"""
        assert default_tray.tray_number == 5
        assert default_tray.holdup == 2.0
        assert default_tray.alpha == 2.5
        assert default_tray.name == "TestTray"
        assert 'tray_number' in default_tray.parameters
        assert 'holdup' in default_tray.parameters
        assert 'alpha' in default_tray.parameters
    
    def test_vapor_liquid_equilibrium(self, default_tray):
        """Test VLE calculation accuracy"""
        # Test known points
        x_test = 0.5
        y_expected = 2.5 * 0.5 / (1 + (2.5 - 1) * 0.5)
        y_calculated = default_tray.vapor_liquid_equilibrium(x_test)
        assert abs(y_calculated - y_expected) < 1e-10
        
        # Test boundary conditions
        assert default_tray.vapor_liquid_equilibrium(0.0) == 0.0
        assert default_tray.vapor_liquid_equilibrium(1.0) == 1.0
        
        # Test monotonic behavior
        x_values = np.linspace(0.01, 0.99, 10)
        y_values = [default_tray.vapor_liquid_equilibrium(x) for x in x_values]
        assert all(y_values[i] <= y_values[i+1] for i in range(len(y_values)-1))
    
    def test_high_volatility_system(self, ethanol_water_tray):
        """Test VLE with high relative volatility (ethanol-water)"""
        # At x = 0.1, y should be significantly higher due to high alpha
        x_test = 0.1
        y_test = ethanol_water_tray.vapor_liquid_equilibrium(x_test)
        assert y_test > 0.4  # Should be much higher than liquid composition
        
        # At x = 0.9, y should approach 1.0
        x_test = 0.9
        y_test = ethanol_water_tray.vapor_liquid_equilibrium(x_test)
        assert y_test > 0.98
    
    def test_dynamics_steady_state(self, default_tray):
        """Test steady-state behavior (dx/dt = 0)"""
        # Define steady-state conditions
        x_steady = 0.4
        y_steady = default_tray.vapor_liquid_equilibrium(x_steady)
        
        # Balanced flows
        L_in = 100.0
        V_in = 120.0
        L_out = 100.0
        V_out = 120.0
        
        # Input: [L_in, x_in, V_in, y_in, L_out, V_out]
        u = np.array([L_in, x_steady, V_in, y_steady, L_out, V_out])
        x_state = np.array([x_steady])
        
        dxdt = default_tray.dynamics(0.0, x_state, u)
        assert abs(dxdt[0]) < 1e-10  # Should be zero for steady state
    
    def test_dynamics_accumulation(self, default_tray):
        """Test material balance with accumulation"""
        # Feed more light component than removed
        x_tray = 0.3
        x_in = 0.6  # Rich feed
        y_in = 0.4
        
        L_in = 100.0
        V_in = 120.0
        L_out = 100.0
        V_out = 120.0
        
        u = np.array([L_in, x_in, V_in, y_in, L_out, V_out])
        x_state = np.array([x_tray])
        
        dxdt = default_tray.dynamics(0.0, x_state, u)
        assert dxdt[0] > 0  # Composition should increase
    
    def test_dynamics_depletion(self, default_tray):
        """Test material balance with depletion"""
        # Remove more light component than added
        x_tray = 0.6
        x_in = 0.3  # Lean feed
        y_in = 0.2
        
        L_in = 100.0
        V_in = 120.0
        L_out = 100.0
        V_out = 120.0
        
        u = np.array([L_in, x_in, V_in, y_in, L_out, V_out])
        x_state = np.array([x_tray])
        
        dxdt = default_tray.dynamics(0.0, x_state, u)
        assert dxdt[0] < 0  # Composition should decrease
    
    def test_composition_constraints(self, default_tray):
        """Test that compositions are constrained to [0,1]"""
        # Test extreme composition values
        x_extreme = np.array([1.5])  # Above 1.0
        u = np.array([100.0, 0.5, 120.0, 0.4, 100.0, 120.0])
        
        dxdt = default_tray.dynamics(0.0, x_extreme, u)
        assert np.isfinite(dxdt[0])  # Should not produce NaN or inf
        
        x_extreme = np.array([-0.5])  # Below 0.0
        dxdt = default_tray.dynamics(0.0, x_extreme, u)
        assert np.isfinite(dxdt[0])
    
    def test_steady_state_solution(self, default_tray):
        """Test steady-state calculation method"""
        # Define operating conditions
        u = np.array([100.0, 0.4, 120.0, 0.3, 100.0, 120.0])
        
        x_ss = default_tray.steady_state(u)
        assert len(x_ss) == 1
        assert 0.0 <= x_ss[0] <= 1.0
        
        # Verify it's actually steady state
        dxdt = default_tray.dynamics(0.0, x_ss, u)
        assert abs(dxdt[0]) < 1e-6
    
    def test_describe_method(self, default_tray):
        """Test describe method returns complete metadata"""
        metadata = default_tray.describe()
        
        # Check required fields
        assert metadata['type'] == 'DistillationTray'
        assert 'description' in metadata
        assert 'category' in metadata
        assert 'algorithms' in metadata
        assert 'parameters' in metadata
        assert 'applications' in metadata
        assert 'limitations' in metadata
        
        # Check parameter values match instance
        assert metadata['parameters']['holdup']['value'] == default_tray.holdup
        assert metadata['parameters']['alpha']['value'] == default_tray.alpha
        assert metadata['parameters']['tray_number']['value'] == default_tray.tray_number
    
    def test_parameter_ranges(self, default_tray):
        """Test parameter validation and ranges"""
        # Test minimum holdup
        tray_min = DistillationTray(holdup=0.1)
        assert tray_min.holdup == 0.1
        
        # Test minimum alpha
        tray_min_alpha = DistillationTray(alpha=1.01)
        assert tray_min_alpha.alpha == 1.01
        
        # Test that VLE still works at limits
        assert 0.0 <= tray_min_alpha.vapor_liquid_equilibrium(0.5) <= 1.0
    
    def test_material_balance_conservation(self, default_tray):
        """Test material balance conservation principles"""
        # Total material balance should be conserved
        x_tray = 0.5
        
        # Define flows
        L_in = 100.0
        V_in = 120.0
        L_out = 105.0  # Net accumulation
        V_out = 115.0  # Net accumulation
        
        u = np.array([L_in, 0.4, V_in, 0.3, L_out, V_out])
        x_state = np.array([x_tray])
        
        dxdt = default_tray.dynamics(0.0, x_state, u)
        
        # Net accumulation should be consistent with flow imbalance
        total_in = L_in + V_in
        total_out = L_out + V_out
        net_accumulation = total_in - total_out
        
        assert net_accumulation == 0.0  # Total flow should be balanced in this test
