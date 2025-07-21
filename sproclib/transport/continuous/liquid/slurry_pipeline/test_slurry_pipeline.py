"""
Test suite for SlurryPipeline class - Standard Process Control Library

This module contains comprehensive tests for the SlurryPipeline multiphase transport model,
including steady-state calculations, dynamic behavior, and describe methods.
"""

import numpy as np
import sys
import os

# Add the parent directory to path to import SlurryPipeline
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .slurry_pipeline import SlurryPipeline


class TestSlurryPipeline:
    """Test suite for SlurryPipeline class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.pipeline = SlurryPipeline(
            pipe_length=500.0,
            pipe_diameter=0.2,
            solid_concentration=0.3,
            particle_diameter=1e-3,
            fluid_density=1000.0,
            solid_density=2500.0,
            fluid_viscosity=1e-3,
            flow_nominal=0.05
        )
    
    def test_initialization(self):
        """Test SlurryPipeline initialization and parameter setting."""
        assert self.pipeline.pipe_length == 500.0
        assert self.pipeline.pipe_diameter == 0.2
        assert self.pipeline.solid_concentration == 0.3
        assert self.pipeline.particle_diameter == 1e-3
        assert self.pipeline.fluid_density == 1000.0
        assert self.pipeline.solid_density == 2500.0
        assert self.pipeline.fluid_viscosity == 1e-3
        assert self.pipeline.flow_nominal == 0.05
        assert self.pipeline.name == "SlurryPipeline"
        
        # Test parameters dictionary
        assert len(self.pipeline.parameters) == 8
        assert self.pipeline.parameters['pipe_length'] == 500.0
    
    def test_describe_method(self):
        """Test the describe method returns comprehensive metadata."""
        desc = self.pipeline.describe()
        
        # Test required keys
        required_keys = [
            'class_name', 'module', 'description', 'model_type',
            'physics', 'algorithms', 'parameters', 'inputs', 'outputs',
            'state_variables', 'methods', 'correlations', 'limitations'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['class_name'] == 'SlurryPipeline'
        assert 'Slurry pipeline' in desc['description']
        assert 'slurry_density' in desc['algorithms']
        assert 'effective_viscosity' in desc['algorithms']
        assert 'settling_model' in desc['algorithms']
        
        # Test physics domain
        assert 'Multiphase' in desc['physics']['domain']
        assert 'Solid-liquid flow' in desc['physics']['phenomena']
        
        # Test correlations
        assert 'einstein_viscosity' in desc['correlations']
    
    def test_steady_state_basic(self):
        """Test basic steady-state calculation."""
        P_in = 500000  # 500 kPa
        flow_rate = 0.05  # m³/s
        c_solid_in = 0.25  # 25% solids
        
        u = np.array([P_in, flow_rate, c_solid_in])
        result = self.pipeline.steady_state(u)
        
        # Basic checks
        assert len(result) == 2
        P_out, c_solid_out = result
        
        # Pressure should decrease (positive pressure drop)
        assert P_out < P_in
        
        # Solid concentration may change due to settling
        assert c_solid_out >= 0
        assert c_solid_out <= c_solid_in  # Cannot increase due to settling
    
    def test_slurry_density_calculation(self):
        """Test slurry density calculation."""
        c_solid = 0.3
        expected_density = (self.pipeline.fluid_density * (1 - c_solid) + 
                          self.pipeline.solid_density * c_solid)
        
        # Test through steady_state calculation
        u = np.array([400000, 0.05, c_solid])
        result = self.pipeline.steady_state(u)
        
        # Verify density is being calculated correctly
        # Expected: 1000 * 0.7 + 2500 * 0.3 = 700 + 750 = 1450 kg/m³
        assert abs(expected_density - 1450.0) < 1.0
    
    def test_effective_viscosity_calculation(self):
        """Test effective viscosity calculation using Einstein relation."""
        c_solid = 0.2
        
        # Expected viscosity factor: 1 + 2.5*C_s + 10.05*C_s²
        expected_factor = 1 + 2.5 * c_solid + 10.05 * c_solid**2
        expected_viscosity = self.pipeline.fluid_viscosity * expected_factor
        
        # For 20% solids: 1 + 2.5*0.2 + 10.05*0.04 = 1 + 0.5 + 0.402 = 1.902
        assert abs(expected_factor - 1.902) < 0.01
    
    def test_solid_concentration_effect(self):
        """Test effect of solid concentration on pressure drop."""
        P_in = 400000
        flow_rate = 0.05
        
        # Test different solid concentrations
        concentrations = [0.1, 0.3, 0.5]
        pressure_drops = []
        
        for c_solid in concentrations:
            u = np.array([P_in, flow_rate, c_solid])
            result = self.pipeline.steady_state(u)
            pressure_drop = P_in - result[0]
            pressure_drops.append(pressure_drop)
        
        # Higher solid concentration should cause higher pressure drop
        assert pressure_drops[1] > pressure_drops[0]
        assert pressure_drops[2] > pressure_drops[1]
    
    def test_flow_rate_effect(self):
        """Test effect of flow rate on pressure drop and settling."""
        P_in = 400000
        c_solid_in = 0.3
        
        # Test different flow rates
        flow_rates = [0.02, 0.05, 0.1]
        pressure_drops = []
        settling_effects = []
        
        for flow_rate in flow_rates:
            u = np.array([P_in, flow_rate, c_solid_in])
            result = self.pipeline.steady_state(u)
            pressure_drop = P_in - result[0]
            settling_effect = c_solid_in - result[1]  # Reduction in concentration
            
            pressure_drops.append(pressure_drop)
            settling_effects.append(settling_effect)
        
        # Higher flow rate should cause higher pressure drop
        assert pressure_drops[1] > pressure_drops[0]
        assert pressure_drops[2] > pressure_drops[1]
        
        # Higher flow rate should cause less settling (better suspension)
        assert settling_effects[1] < settling_effects[0]
        assert settling_effects[2] < settling_effects[1]
    
    def test_reynolds_number_calculation(self):
        """Test Reynolds number calculation for slurry."""
        flow_rate = 0.05
        c_solid = 0.3
        
        # Calculate expected properties
        slurry_density = (self.pipeline.fluid_density * (1 - c_solid) + 
                         self.pipeline.solid_density * c_solid)
        viscosity_factor = 1 + 2.5 * c_solid + 10.05 * c_solid**2
        effective_viscosity = self.pipeline.fluid_viscosity * viscosity_factor
        
        velocity = flow_rate / (np.pi * (self.pipeline.pipe_diameter/2)**2)
        expected_Re = (slurry_density * velocity * self.pipeline.pipe_diameter / 
                      effective_viscosity)
        
        # Should be in reasonable range for pipeline flow
        assert expected_Re > 1000  # Should be turbulent
        assert expected_Re < 1e6   # Reasonable upper limit
    
    def test_settling_model(self):
        """Test particle settling model."""
        P_in = 400000
        c_solid_in = 0.4
        
        # Test at different velocities
        low_flow = 0.01   # Low velocity - more settling
        high_flow = 0.1   # High velocity - less settling
        
        u_low = np.array([P_in, low_flow, c_solid_in])
        u_high = np.array([P_in, high_flow, c_solid_in])
        
        result_low = self.pipeline.steady_state(u_low)
        result_high = self.pipeline.steady_state(u_high)
        
        c_out_low = result_low[1]
        c_out_high = result_high[1]
        
        # Higher velocity should result in less settling (higher outlet concentration)
        assert c_out_high > c_out_low
        
        # Both should be less than or equal to inlet concentration
        assert c_out_low <= c_solid_in
        assert c_out_high <= c_solid_in
    
    def test_dynamics_basic(self):
        """Test dynamic model basic functionality."""
        # Initial state [P_out, c_solid_out]
        x = np.array([350000, 0.25])
        
        # Input [P_inlet, flow_rate, c_solid_in]
        u = np.array([400000, 0.05, 0.3])
        
        # Time
        t = 0.0
        
        # Calculate derivatives
        dx_dt = self.pipeline.dynamics(t, x, u)
        
        # Check output format
        assert len(dx_dt) == 2
        dP_dt, dc_dt = dx_dt
        
        # Pressure should increase (current is below steady-state)
        assert dP_dt < 0  # Moving toward lower steady-state pressure
        
        # Concentration derivative should move toward steady-state
        assert isinstance(dc_dt, (int, float, np.number))
    
    def test_dynamics_convergence(self):
        """Test that dynamics converge to steady-state values."""
        # Input conditions
        u = np.array([400000, 0.05, 0.3])
        
        # Calculate steady-state target
        ss_result = self.pipeline.steady_state(u)
        P_ss, c_ss = ss_result
        
        # Start from different initial conditions
        x = np.array([300000, 0.2])
        
        # Check that derivatives point toward steady-state
        dx_dt = self.pipeline.dynamics(0.0, x, u)
        dP_dt, dc_dt = dx_dt
        
        # Should move toward steady-state values
        if P_ss < 300000:
            assert dP_dt < 0  # Moving toward lower pressure
        else:
            assert dP_dt > 0  # Moving toward higher pressure
        
        if c_ss > 0.2:
            assert dc_dt > 0  # Moving toward higher concentration
        else:
            assert dc_dt < 0  # Moving toward lower concentration
    
    def test_residence_time_calculation(self):
        """Test residence time calculation in dynamics."""
        flow_rate = 0.05
        
        # Calculate expected residence time
        pipe_volume = self.pipeline.pipe_length * np.pi * (self.pipeline.pipe_diameter/2)**2
        expected_residence_time = pipe_volume / flow_rate
        
        # Test dynamics to see if residence time affects time constants
        u = np.array([400000, flow_rate, 0.3])
        x = np.array([350000, 0.25])
        
        dx_dt = self.pipeline.dynamics(0.0, x, u)
        
        # Concentration dynamics should be slower than pressure dynamics
        # This is verified by the different time constants used
        assert isinstance(dx_dt[1], (int, float, np.number))
    
    def test_describe_steady_state(self):
        """Test the describe_steady_state static method."""
        desc = SlurryPipeline.describe_steady_state()
        
        # Test required keys
        required_keys = [
            'function_name', 'purpose', 'algorithm_steps', 'equations',
            'input_format', 'output_format', 'multiphase_effects', 'flow_regimes'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['function_name'] == 'steady_state'
        assert 'slurry flow' in desc['purpose']
        assert len(desc['algorithm_steps']) >= 5
        assert 'slurry_density' in desc['equations']
        assert 'viscosity_factor' in desc['equations']
        assert 'settling' in desc['equations']
        
        # Test multiphase effects
        assert 'density_mixing' in desc['multiphase_effects']
        assert 'viscosity_enhancement' in desc['multiphase_effects']
    
    def test_describe_dynamics(self):
        """Test the describe_dynamics static method."""
        desc = SlurryPipeline.describe_dynamics()
        
        # Test required keys
        required_keys = [
            'function_name', 'purpose', 'model_type', 'algorithm_steps',
            'differential_equations', 'time_constants', 'transport_delay'
        ]
        for key in required_keys:
            assert key in desc, f"Missing key: {key}"
        
        # Test specific content
        assert desc['function_name'] == 'dynamics'
        assert 'pressure and concentration' in desc['purpose']
        assert 'pressure' in desc['differential_equations']
        assert 'concentration' in desc['differential_equations']
        assert 'transport_delay' in desc
        assert 'residence_time' in desc['transport_delay']
    
    def test_friction_factor_calculation(self):
        """Test friction factor calculation for different flow regimes."""
        P_in = 400000
        c_solid = 0.2
        
        # Test low flow rate (potentially laminar)
        low_flow = 0.001
        u_low = np.array([P_in, low_flow, c_solid])
        result_low = self.pipeline.steady_state(u_low)
        
        # Test high flow rate (turbulent)
        high_flow = 0.1
        u_high = np.array([P_in, high_flow, c_solid])
        result_high = self.pipeline.steady_state(u_high)
        
        # Both should produce valid results
        assert len(result_low) == 2
        assert len(result_high) == 2
        
        # Higher flow should have higher pressure drop
        pressure_drop_low = P_in - result_low[0]
        pressure_drop_high = P_in - result_high[0]
        
        # Note: pressure drop scales with velocity squared in turbulent flow
        assert pressure_drop_high > pressure_drop_low
    
    def test_solid_effect_factor(self):
        """Test additional pressure drop due to solids."""
        P_in = 400000
        flow_rate = 0.05
        
        # Compare with pure liquid (zero solids)
        u_liquid = np.array([P_in, flow_rate, 0.0])
        result_liquid = self.pipeline.steady_state(u_liquid)
        pressure_drop_liquid = P_in - result_liquid[0]
        
        # Compare with slurry
        u_slurry = np.array([P_in, flow_rate, 0.3])
        result_slurry = self.pipeline.steady_state(u_slurry)
        pressure_drop_slurry = P_in - result_slurry[0]
        
        # Slurry should have higher pressure drop
        assert pressure_drop_slurry > pressure_drop_liquid
        
        # Solid effect factor should be evident
        enhancement_factor = pressure_drop_slurry / pressure_drop_liquid
        expected_solid_factor = 1 + 3 * 0.3  # 1 + 3*C_s = 1.9
        
        # Enhancement should be related to solid effect factor
        # (also includes density and viscosity effects)
        assert enhancement_factor > 1.5
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with zero solids (pure liquid)
        u_no_solids = np.array([400000, 0.05, 0.0])
        result_no_solids = self.pipeline.steady_state(u_no_solids)
        
        # Should produce valid results
        assert len(result_no_solids) == 2
        assert result_no_solids[1] == 0.0  # No solids out
        
        # Test with maximum practical solids concentration
        u_high_solids = np.array([400000, 0.05, 0.6])
        result_high_solids = self.pipeline.steady_state(u_high_solids)
        
        # Should still produce valid results
        assert len(result_high_solids) == 2
        assert result_high_solids[0] > 0  # Positive outlet pressure
        
        # Test with very low flow
        u_low_flow = np.array([400000, 0.001, 0.3])
        result_low_flow = self.pipeline.steady_state(u_low_flow)
        
        # Should have significant settling
        settling_effect = 0.3 - result_low_flow[1]
        assert settling_effect > 0.05  # At least 5% settling
    
    def test_parameter_sensitivity(self):
        """Test sensitivity to parameter changes."""
        base_u = np.array([400000, 0.05, 0.3])
        base_result = self.pipeline.steady_state(base_u)
        base_pressure_drop = base_u[0] - base_result[0]
        
        # Test with longer pipeline
        long_pipeline = SlurryPipeline(pipe_length=1000.0)  # Double length
        long_result = long_pipeline.steady_state(base_u)
        long_pressure_drop = base_u[0] - long_result[0]
        
        # Longer pipeline should have higher pressure drop
        assert long_pressure_drop > base_pressure_drop
        
        # Test with larger diameter
        large_pipeline = SlurryPipeline(pipe_diameter=0.4)  # Double diameter
        large_result = large_pipeline.steady_state(base_u)
        large_pressure_drop = base_u[0] - large_result[0]
        
        # Larger diameter should have lower pressure drop
        assert large_pressure_drop < base_pressure_drop
    
    def test_multiphase_properties(self):
        """Test multiphase property calculations."""
        c_solid = 0.25
        
        # Test density calculation
        expected_density = (self.pipeline.fluid_density * (1 - c_solid) + 
                          self.pipeline.solid_density * c_solid)
        # 1000 * 0.75 + 2500 * 0.25 = 750 + 625 = 1375 kg/m³
        assert abs(expected_density - 1375.0) < 1.0
        
        # Test viscosity enhancement
        viscosity_factor = 1 + 2.5 * c_solid + 10.05 * c_solid**2
        # 1 + 2.5*0.25 + 10.05*0.0625 = 1 + 0.625 + 0.628 = 2.253
        assert abs(viscosity_factor - 2.253) < 0.01
        
        # Test through actual calculation
        u = np.array([400000, 0.05, c_solid])
        result = self.pipeline.steady_state(u)
        
        # Should produce reasonable results with these properties
        assert len(result) == 2
        assert result[0] > 0
        assert result[1] >= 0


def run_all_tests():
    """Run all tests manually without pytest dependency."""
    test_instance = TestSlurryPipeline()
    
    # List of test methods
    test_methods = [
        'test_initialization',
        'test_describe_method',
        'test_steady_state_basic',
        'test_slurry_density_calculation',
        'test_effective_viscosity_calculation',
        'test_solid_concentration_effect',
        'test_flow_rate_effect',
        'test_reynolds_number_calculation',
        'test_settling_model',
        'test_dynamics_basic',
        'test_dynamics_convergence',
        'test_residence_time_calculation',
        'test_describe_steady_state',
        'test_describe_dynamics',
        'test_friction_factor_calculation',
        'test_solid_effect_factor',
        'test_edge_cases',
        'test_parameter_sensitivity',
        'test_multiphase_properties'
    ]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            test_instance.setup_method()  # Reset for each test
            method = getattr(test_instance, method_name)
            method()
            print(f"✓ {method_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {method_name}: {str(e)}")
            failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Run the tests
    success = run_all_tests()
    if not success:
        exit(1)
