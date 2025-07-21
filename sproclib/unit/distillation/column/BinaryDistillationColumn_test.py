"""
Test file for BinaryDistillationColumn class
Tests multi-tray dynamics, separation performance, and control behavior
"""

import pytest
import numpy as np
from sproclib.unit.distillation.column import BinaryDistillationColumn


class TestBinaryDistillationColumn:
    @pytest.fixture
    def default_column(self):
        """Create default binary distillation column for testing"""
        return BinaryDistillationColumn(
            N_trays=20,
            feed_tray=10,
            alpha=2.5,
            tray_holdup=1.0,
            reflux_drum_holdup=5.0,
            reboiler_holdup=10.0,
            feed_flow=100.0,
            feed_composition=0.5,
            name="TestColumn"
        )
    
    @pytest.fixture
    def ethanol_column(self):
        """Create column for ethanol-water separation"""
        return BinaryDistillationColumn(
            N_trays=30,
            feed_tray=15,
            alpha=8.0,  # Ethanol-water at 1 atm
            tray_holdup=2.0,
            reflux_drum_holdup=8.0,
            reboiler_holdup=15.0,
            feed_flow=200.0,
            feed_composition=0.12,  # Typical fermentation composition
            name="EthanolColumn"
        )
    
    def test_initialization(self, default_column):
        """Test column initialization with default parameters"""
        assert default_column.N_trays == 20
        assert default_column.feed_tray == 10
        assert default_column.alpha == 2.5
        assert default_column.tray_holdup == 1.0
        assert default_column.feed_flow == 100.0
        assert default_column.feed_composition == 0.5
        assert len(default_column.trays) == 20
        
        # Check that all trays have correct parameters
        for i, tray in enumerate(default_column.trays):
            assert tray.tray_number == i + 1
            assert tray.alpha == 2.5
            assert tray.holdup == 1.0
    
    def test_vapor_liquid_equilibrium(self, default_column):
        """Test VLE calculation consistency"""
        # Test known points
        x_test = 0.4
        y_expected = 2.5 * 0.4 / (1 + (2.5 - 1) * 0.4)
        y_calculated = default_column.vapor_liquid_equilibrium(x_test)
        assert abs(y_calculated - y_expected) < 1e-10
        
        # Test boundary conditions
        assert default_column.vapor_liquid_equilibrium(0.0) == 0.0
        assert default_column.vapor_liquid_equilibrium(1.0) == 1.0
    
    def test_steady_state_solution(self, default_column):
        """Test steady-state calculation"""
        # Define operating conditions
        R = 3.0  # Reflux ratio
        Q_reb = 1000.0  # Reboiler duty
        D = 45.0  # Distillate flow
        B = 55.0  # Bottoms flow
        
        u = np.array([R, Q_reb, D, B])
        x_ss = default_column.steady_state(u)
        
        # Check dimensions
        assert len(x_ss) == default_column.N_trays + 2
        
        # Check all compositions are valid
        assert all(0.0 <= x <= 1.0 for x in x_ss)
        
        # Check separation: distillate should be richer than bottoms
        x_distillate = x_ss[default_column.N_trays]
        x_bottoms = x_ss[default_column.N_trays + 1]
        assert x_distillate > x_bottoms
        assert x_distillate > default_column.feed_composition
        assert x_bottoms < default_column.feed_composition
    
    def test_dynamics_steady_state(self, default_column):
        """Test that steady-state solution gives zero derivatives"""
        # Get steady-state solution
        u = np.array([2.0, 800.0, 45.0, 55.0])
        x_ss = default_column.steady_state(u)
        
        # Check that derivatives are zero (or very small)
        dxdt = default_column.dynamics(0.0, x_ss, u)
        assert all(abs(dx) < 1e-3 for dx in dxdt)  # Allow small numerical errors
    
    def test_separation_metrics(self, default_column):
        """Test separation performance metrics"""
        # Create composition profile
        compositions = np.linspace(0.1, 0.9, default_column.N_trays + 2)
        compositions[default_column.N_trays] = 0.95  # Distillate
        compositions[default_column.N_trays + 1] = 0.05  # Bottoms
        
        metrics = default_column.calculate_separation_metrics(compositions)
        
        # Check required metrics exist
        assert 'distillate_composition' in metrics
        assert 'bottoms_composition' in metrics
        assert 'light_recovery' in metrics
        assert 'separation_factor' in metrics
        
        # Check values are reasonable
        assert metrics['distillate_composition'] == 0.95
        assert metrics['bottoms_composition'] == 0.05
        assert metrics['separation_factor'] > 1.0
    
    def test_minimum_reflux_calculation(self, default_column):
        """Test minimum reflux ratio calculation"""
        R_min = default_column.calculate_minimum_reflux()
        
        assert R_min > 0.1  # Should be positive
        assert R_min < 100.0  # Should be reasonable
        assert isinstance(R_min, float)
    
    def test_ethanol_column_separation(self, ethanol_column):
        """Test ethanol column with realistic parameters"""
        # Operating conditions for ethanol purification
        R = 5.0  # High reflux for high purity
        Q_reb = 2000.0
        D = 24.0  # 12% recovery as 95% ethanol
        B = 176.0  # Remaining as bottoms
        
        u = np.array([R, Q_reb, D, B])
        x_ss = ethanol_column.steady_state(u)
        
        # Check separation performance
        x_distillate = x_ss[ethanol_column.N_trays]
        x_bottoms = x_ss[ethanol_column.N_trays + 1]
        
        assert x_distillate > 0.8  # Should achieve good purity
        assert x_bottoms < 0.05  # Should have low ethanol in bottoms
        
        # Check minimum reflux for ethanol system
        R_min = ethanol_column.calculate_minimum_reflux()
        assert R_min > 0.5  # Should be reasonable for ethanol-water
    
    def test_parameter_update(self, default_column):
        """Test parameter updating functionality"""
        original_alpha = default_column.alpha
        
        # Update alpha
        default_column.update_parameters(alpha=3.0)
        assert default_column.alpha == 3.0
        assert default_column.parameters['alpha'] == 3.0
        
        # Check that tray models are updated
        for tray in default_column.trays:
            assert tray.alpha == 3.0
        
        # Test multiple parameter update
        default_column.update_parameters(
            feed_flow=150.0,
            feed_composition=0.6
        )
        assert default_column.feed_flow == 150.0
        assert default_column.feed_composition == 0.6
    
    def test_dynamics_composition_constraints(self, default_column):
        """Test that dynamics handle composition constraints properly"""
        # Create state with extreme compositions
        x_extreme = np.zeros(default_column.N_trays + 2)
        x_extreme[0] = 1.5  # Above 1.0
        x_extreme[1] = -0.5  # Below 0.0
        x_extreme[2:] = 0.5  # Normal values
        
        u = np.array([2.0, 800.0, 45.0, 55.0])
        
        dxdt = default_column.dynamics(0.0, x_extreme, u)
        
        # Should not produce NaN or inf
        assert all(np.isfinite(dx) for dx in dxdt)
    
    def test_dynamics_flow_constraints(self, default_column):
        """Test that dynamics handle flow constraints properly"""
        # Normal state
        x_normal = np.full(default_column.N_trays + 2, 0.5)
        
        # Extreme flow conditions
        u_extreme = np.array([0.0, 800.0, 0.0, 0.0])  # Zero flows
        
        dxdt = default_column.dynamics(0.0, x_normal, u_extreme)
        
        # Should not crash and should produce finite values
        assert all(np.isfinite(dx) for dx in dxdt)
    
    def test_describe_method(self, default_column):
        """Test describe method returns complete metadata"""
        metadata = default_column.describe()
        
        # Check required fields
        assert metadata['type'] == 'BinaryDistillationColumn'
        assert 'description' in metadata
        assert 'category' in metadata
        assert 'algorithms' in metadata
        assert 'parameters' in metadata
        assert 'applications' in metadata
        assert 'limitations' in metadata
        
        # Check parameter values match instance
        assert metadata['parameters']['N_trays']['value'] == default_column.N_trays
        assert metadata['parameters']['alpha']['value'] == default_column.alpha
        assert metadata['parameters']['feed_tray']['value'] == default_column.feed_tray
    
    def test_feed_tray_location_effect(self, default_column):
        """Test effect of feed tray location on separation"""
        # Test different feed tray locations
        feed_locations = [5, 10, 15]
        separations = []
        
        for feed_tray in feed_locations:
            column = BinaryDistillationColumn(
                N_trays=20,
                feed_tray=feed_tray,
                alpha=2.5,
                feed_composition=0.5
            )
            
            u = np.array([2.0, 800.0, 45.0, 55.0])
            x_ss = column.steady_state(u)
            
            x_distillate = x_ss[column.N_trays]
            x_bottoms = x_ss[column.N_trays + 1]
            separation = x_distillate - x_bottoms
            separations.append(separation)
        
        # Should achieve reasonable separation for all feed locations
        assert all(sep > 0.3 for sep in separations)
    
    def test_mass_balance_consistency(self, default_column):
        """Test overall mass balance consistency"""
        # Define balanced flows
        R = 2.0
        D = 50.0
        B = 50.0  # Feed = D + B = 100
        Q_reb = 1000.0
        
        u = np.array([R, Q_reb, D, B])
        
        # Check that feed flow equals product flows
        assert abs(default_column.feed_flow - (D + B)) < 1e-10
        
        # Get steady state
        x_ss = default_column.steady_state(u)
        
        # Calculate component balance
        x_distillate = x_ss[default_column.N_trays]
        x_bottoms = x_ss[default_column.N_trays + 1]
        
        # Overall component balance: F*x_F = D*x_D + B*x_B
        feed_light = default_column.feed_flow * default_column.feed_composition
        product_light = D * x_distillate + B * x_bottoms
        
        # Should be approximately balanced (within numerical error)
        relative_error = abs(feed_light - product_light) / feed_light
        assert relative_error < 0.1  # Allow 10% error for approximate steady-state method
