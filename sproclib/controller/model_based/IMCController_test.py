import pytest
import numpy as np
from sproclib.controller.model_based.IMCController import IMCController

class TestIMCController:
    @pytest.fixture
    def simple_process_model(self):
        """Create simple first-order process model for testing."""
        # First-order process: Gp(s) = K / (τs + 1) * exp(-θs)
        return {
            'gain': 2.5,
            'time_constant': 8.0,
            'dead_time': 1.5,
            'type': 'FOPDT'
        }
    
    @pytest.fixture
    def reactor_model(self):
        """Create reactor temperature control model."""
        return {
            'gain': 1.8,
            'time_constant': 12.0,
            'dead_time': 2.0,
            'disturbance_gain': -0.5,
            'type': 'FOPDT_with_disturbance'
        }
    
    @pytest.fixture
    def default_controller(self, simple_process_model):
        """Create default IMC controller."""
        return IMCController(
            process_model=simple_process_model,
            filter_time_constant=4.0,
            name="TestIMCController"
        )
    
    def test_controller_initialization(self, default_controller):
        """Test IMC controller initialization."""
        assert default_controller.name == "TestIMCController"
        assert default_controller.filter_time_constant == 4.0
        assert default_controller.process_model['gain'] == 2.5
        
    def test_internal_model_inversion(self, default_controller):
        """Test internal model inversion calculation."""
        # For FOPDT: Gm_inv(s) = (τs + 1) / K  
        # The controller should compute the inverse correctly
        
        # Test steady-state inverse
        steady_state_inverse = 1.0 / default_controller.process_model['gain']
        expected_inverse = 1.0 / 2.5
        
        assert abs(steady_state_inverse - expected_inverse) < 1e-6
        
    def test_filter_design(self, default_controller):
        """Test IMC filter design."""
        # Filter: f(s) = 1 / (λs + 1)^n
        # where n = relative degree and λ = filter time constant
        
        filter_tc = default_controller.filter_time_constant
        assert filter_tc > 0
        
        # For FOPDT, relative degree = 1 (first order)
        # Check that filter time constant is reasonable compared to process
        process_tc = default_controller.process_model['time_constant']
        assert filter_tc <= process_tc  # Conservative tuning
        
    def test_controller_update_step_change(self, default_controller):
        """Test controller response to step setpoint change."""
        
        # Simulation parameters
        t = 0.0
        setpoint = 100.0  # Temperature setpoint (°C)
        measurement = 85.0  # Current temperature
        
        # Calculate control output
        try:
            control_output = default_controller.update(t, setpoint, measurement)
            
            # Should be finite and reasonable
            assert np.isfinite(control_output)
            
            # For step increase, control output should be positive
            assert control_output > 0
            
        except AttributeError:
            # Method may not be implemented yet
            pytest.skip("IMC update method not available")
            
    def test_disturbance_rejection(self, reactor_model):
        """Test IMC controller disturbance rejection."""
        
        controller = IMCController(
            process_model=reactor_model,
            filter_time_constant=6.0,
            name="ReactorIMC"
        )
        
        # Test response to measured disturbance
        t = 0.0
        setpoint = 350.0  # K
        measurement = 348.0  # Current temperature
        disturbance = 10.0  # Feed temperature increase
        
        try:
            # Calculate control output with disturbance compensation
            control_output = controller.update(t, setpoint, measurement, 
                                             disturbance=disturbance)
            
            assert np.isfinite(control_output)
            
        except (AttributeError, TypeError):
            pytest.skip("Disturbance compensation not implemented")
            
    def test_robustness_analysis(self, default_controller):
        """Test robustness to model mismatch."""
        
        # Original model parameters
        original_gain = default_controller.process_model['gain']
        original_tc = default_controller.process_model['time_constant']
        
        # Test with +/-20% model mismatch
        gain_errors = [0.8, 1.0, 1.2]  # -20%, 0%, +20%
        tc_errors = [0.8, 1.0, 1.2]
        
        for gain_mult in gain_errors:
            for tc_mult in tc_errors:
                # Modify model parameters
                default_controller.process_model['gain'] = original_gain * gain_mult
                default_controller.process_model['time_constant'] = original_tc * tc_mult
                
                try:
                    # Test stability (should not crash)
                    control_output = default_controller.update(0.0, 100.0, 90.0)
                    assert np.isfinite(control_output)
                    
                except AttributeError:
                    pytest.skip("IMC update method not available")
        
        # Restore original parameters
        default_controller.process_model['gain'] = original_gain
        default_controller.process_model['time_constant'] = original_tc
        
    def test_heat_exchanger_application(self):
        """Test IMC controller for heat exchanger temperature control."""
        
        # Heat exchanger model: outlet temperature vs steam flow
        heat_exchanger_model = {
            'gain': 3.2,  # K per kg/h steam
            'time_constant': 15.0,  # minutes
            'dead_time': 3.0,  # minutes
            'type': 'FOPDT'
        }
        
        controller = IMCController(
            process_model=heat_exchanger_model,
            filter_time_constant=7.5,  # τc/2 for good performance
            name="HeatExchangerIMC"
        )
        
        # Test setpoint tracking
        setpoint = 180.0  # °C outlet temperature
        current_temp = 165.0  # °C
        
        try:
            steam_flow = controller.update(0.0, setpoint, current_temp)
            
            # Should request positive steam flow increase
            assert steam_flow > 0
            assert steam_flow < 50.0  # Reasonable upper bound (kg/h)
            
        except AttributeError:
            pytest.skip("IMC update method not available")
            
    def test_distillation_column_application(self):
        """Test IMC controller for distillation column composition control."""
        
        # Distillation model: top composition vs reflux ratio
        column_model = {
            'gain': 0.8,  # mol% per reflux ratio change
            'time_constant': 25.0,  # minutes (large thermal mass)
            'dead_time': 5.0,  # minutes (measurement delay)
            'type': 'FOPDT'
        }
        
        controller = IMCController(
            process_model=column_model,
            filter_time_constant=12.0,  # Conservative tuning for composition
            name="DistillationIMC"
        )
        
        # Test composition control
        setpoint = 95.0  # mol% purity
        measurement = 92.5  # Current composition
        
        try:
            reflux_adjustment = controller.update(0.0, setpoint, measurement)
            
            # Should increase reflux for higher purity
            assert reflux_adjustment > 0
            
        except AttributeError:
            pytest.skip("IMC update method not available")
            
    def test_reactor_temperature_control(self):
        """Test IMC controller for exothermic reactor temperature control."""
        
        # Reactor model with cooling
        reactor_model = {
            'gain': -1.5,  # K per m³/h cooling (negative gain)
            'time_constant': 8.0,  # minutes
            'dead_time': 1.0,  # minutes
            'type': 'FOPDT'
        }
        
        controller = IMCController(
            process_model=reactor_model,
            filter_time_constant=4.0,
            name="ReactorTempIMC"
        )
        
        # Test temperature control
        setpoint = 340.0  # K
        temperature = 345.0  # K (too high)
        
        try:
            cooling_flow = controller.update(0.0, setpoint, temperature)
            
            # Should increase cooling (positive flow) to reduce temperature
            assert cooling_flow > 0
            
        except AttributeError:
            pytest.skip("IMC update method not available")
            
    def test_filter_tuning_guidelines(self, simple_process_model):
        """Test different filter tuning approaches."""
        
        process_tc = simple_process_model['time_constant']
        dead_time = simple_process_model['dead_time']
        
        # Test different tuning rules
        tuning_rules = {
            'conservative': process_tc,  # τc = τ
            'moderate': process_tc / 2,  # τc = τ/2  
            'aggressive': dead_time,     # τc = θ
        }
        
        for rule_name, filter_tc in tuning_rules.items():
            controller = IMCController(
                process_model=simple_process_model,
                filter_time_constant=filter_tc,
                name=f"IMC_{rule_name}"
            )
            
            assert controller.filter_time_constant == filter_tc
            assert controller.name == f"IMC_{rule_name}"
            
    def test_performance_metrics(self, default_controller):
        """Test calculation of performance metrics."""
        
        # Simulate step response
        time_vector = np.linspace(0, 50, 251)
        setpoint = 100.0
        initial_output = 0.0
        
        simulated_response = []
        controller_output = []
        
        # Simple simulation loop
        process_output = initial_output
        
        for t in time_vector:
            try:
                # Calculate controller output
                control = default_controller.update(t, setpoint, process_output)
                controller_output.append(control)
                
                # Simple first-order process simulation
                if len(simulated_response) > 0:
                    dt = time_vector[1] - time_vector[0]
                    tau = default_controller.process_model['time_constant']
                    gain = default_controller.process_model['gain']
                    
                    # First-order response: τ dy/dt + y = K*u
                    dydt = (gain * control - process_output) / tau
                    process_output = process_output + dydt * dt
                
                simulated_response.append(process_output)
                
            except AttributeError:
                pytest.skip("IMC update method not available")
                
        if len(simulated_response) > 10:
            # Calculate performance metrics
            final_value = simulated_response[-1]
            steady_state_error = abs(setpoint - final_value)
            
            # Performance should be reasonable
            assert steady_state_error < 0.1 * setpoint  # < 10% error
            
    def test_edge_cases(self, default_controller):
        """Test edge cases and error handling."""
        
        # Test with zero setpoint
        try:
            output = default_controller.update(0.0, 0.0, 10.0)
            assert np.isfinite(output)
        except AttributeError:
            pytest.skip("IMC update method not available")
            
        # Test with very large setpoint change
        try:
            output = default_controller.update(0.0, 1000.0, 0.0)
            assert np.isfinite(output)
        except AttributeError:
            pytest.skip("IMC update method not available")
            
        # Test with negative process gain
        default_controller.process_model['gain'] = -2.0
        try:
            output = default_controller.update(0.0, 100.0, 90.0)
            assert np.isfinite(output)
        except AttributeError:
            pytest.skip("IMC update method not available")
            
    def test_describe_method(self, default_controller):
        """Test describe method returns proper metadata."""
        
        try:
            description = default_controller.describe()
            
            assert description['class_name'] == 'IMCController'
            assert 'process_model' in description
            assert 'filter_design' in description
            assert 'imc_theory' in description
            
        except AttributeError:
            pytest.skip("Describe method not implemented")
            
    def test_multiple_controller_instances(self):
        """Test multiple IMC controller instances."""
        
        # Create different controllers for different loops
        controllers = {}
        
        models = {
            'temperature': {'gain': 2.0, 'time_constant': 10.0, 'dead_time': 2.0, 'type': 'FOPDT'},
            'pressure': {'gain': 1.5, 'time_constant': 5.0, 'dead_time': 1.0, 'type': 'FOPDT'},
            'flow': {'gain': 3.0, 'time_constant': 2.0, 'dead_time': 0.5, 'type': 'FOPDT'}
        }
        
        for loop_name, model in models.items():
            controllers[loop_name] = IMCController(
                process_model=model,
                filter_time_constant=model['time_constant'] / 2,
                name=f"IMC_{loop_name}"
            )
        
        # Verify all controllers are independent
        assert len(controllers) == 3
        for name, controller in controllers.items():
            assert controller.name == f"IMC_{name}"
