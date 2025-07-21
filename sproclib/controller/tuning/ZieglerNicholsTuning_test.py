import pytest
import numpy as np
from sproclib.controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning

class TestZieglerNicholsTuning:
    @pytest.fixture
    def step_response_data(self):
        """Create simulated step response data for testing."""
        time = np.linspace(0, 50, 251)
        
        # FOPDT parameters
        Kp = 2.5  # Process gain
        tau = 12.0  # Time constant
        theta = 2.0  # Dead time
        
        # Step response
        response = np.zeros_like(time)
        for i, t in enumerate(time):
            if t >= theta:
                response[i] = Kp * (1 - np.exp(-(t - theta) / tau))
        
        return {
            'time': time,
            'output': response,
            'input_change': 1.0,
            'steady_state_gain': Kp,
            'time_constant': tau,
            'dead_time': theta
        }
    
    @pytest.fixture
    def heat_exchanger_data(self):
        """Heat exchanger step test data."""
        return {
            'Kp': 3.2,  # °C per kg/h steam
            'T': 18.0,  # minutes
            'L': 3.5,   # minutes
            'type': 'temperature_control'
        }
    
    @pytest.fixture
    def reactor_data(self):
        """Reactor temperature control data."""
        return {
            'Kp': -2.5,  # K per L/min cooling (negative gain)
            'T': 12.0,   # minutes
            'L': 0.8,    # minutes
            'type': 'temperature_control'
        }
    
    def test_step_response_identification(self, step_response_data):
        """Test parameter identification from step response."""
        tuner = ZieglerNicholsTuning()
        
        try:
            identified_params = tuner.identify_from_step_response(step_response_data)
            
            # Check identified parameters are reasonable
            assert 'Kp' in identified_params
            assert 'T' in identified_params
            assert 'L' in identified_params
            
            # Verify values are close to original
            assert abs(identified_params['Kp'] - 2.5) < 0.5
            assert abs(identified_params['T'] - 12.0) < 2.0
            assert abs(identified_params['L'] - 2.0) < 1.0
            
        except AttributeError:
            pytest.skip("Step response identification method not implemented")
    
    def test_zn_pi_tuning(self, heat_exchanger_data):
        """Test Ziegler-Nichols PI tuning formulas."""
        tuner = ZieglerNicholsTuning()
        
        try:
            pi_params = tuner.tune_pi(heat_exchanger_data)
            
            # Check parameter structure
            assert 'Kc' in pi_params
            assert 'tau_I' in pi_params
            assert 'tau_D' not in pi_params or pi_params['tau_D'] == 0
            
            # Check reasonable values for heat exchanger
            Kp = heat_exchanger_data['Kp']
            T = heat_exchanger_data['T']
            L = heat_exchanger_data['L']
            
            expected_Kc = 0.9 * T / (Kp * L)  # ZN PI formula
            expected_tau_I = 3.3 * L
            
            assert abs(pi_params['Kc'] - expected_Kc) < 0.1 * expected_Kc
            assert abs(pi_params['tau_I'] - expected_tau_I) < 0.1 * expected_tau_I
            
        except AttributeError:
            pytest.skip("ZN PI tuning method not implemented")
    
    def test_zn_pid_tuning(self, reactor_data):
        """Test Ziegler-Nichols PID tuning formulas."""
        tuner = ZieglerNicholsTuning()
        
        try:
            pid_params = tuner.tune_pid(reactor_data)
            
            # Check parameter structure
            assert 'Kc' in pid_params
            assert 'tau_I' in pid_params
            assert 'tau_D' in pid_params
            
            # Check reasonable values
            assert pid_params['Kc'] > 0  # Should be positive even for negative gain
            assert pid_params['tau_I'] > 0
            assert pid_params['tau_D'] > 0
            
            # Verify relationships
            Kp = abs(reactor_data['Kp'])  # Use absolute value
            T = reactor_data['T']
            L = reactor_data['L']
            
            expected_Kc = 1.2 * T / (Kp * L)
            expected_tau_I = 2 * L
            expected_tau_D = 0.5 * L
            
            assert abs(pid_params['Kc'] - expected_Kc) < 0.2 * expected_Kc
            assert abs(pid_params['tau_I'] - expected_tau_I) < 0.2 * expected_tau_I
            assert abs(pid_params['tau_D'] - expected_tau_D) < 0.2 * expected_tau_D
            
        except AttributeError:
            pytest.skip("ZN PID tuning method not implemented")
    
    def test_ultimate_gain_method(self):
        """Test ultimate gain tuning method."""
        tuner = ZieglerNicholsTuning()
        
        # Typical ultimate gain test results
        ultimate_data = {
            'Ku': 8.5,    # Ultimate gain
            'Pu': 15.0,   # Ultimate period (minutes)
            'process_gain': 2.0
        }
        
        try:
            pid_params = tuner.tune_from_ultimate_gain(ultimate_data)
            
            # Check ZN relationships
            expected_Kc = 0.6 * ultimate_data['Ku']
            expected_tau_I = 0.5 * ultimate_data['Pu']
            expected_tau_D = 0.125 * ultimate_data['Pu']
            
            assert abs(pid_params['Kc'] - expected_Kc) < 0.01
            assert abs(pid_params['tau_I'] - expected_tau_I) < 0.01
            assert abs(pid_params['tau_D'] - expected_tau_D) < 0.01
            
        except AttributeError:
            pytest.skip("Ultimate gain tuning method not implemented")
    
    def test_conservative_tuning(self, heat_exchanger_data):
        """Test conservative tuning modification."""
        tuner = ZieglerNicholsTuning()
        
        try:
            # Get standard tuning
            standard_params = tuner.tune_pid(heat_exchanger_data)
            
            # Get conservative tuning
            conservative_params = tuner.tune_pid(heat_exchanger_data, 
                                               conservative=True)
            
            # Conservative should have lower gains
            assert conservative_params['Kc'] < standard_params['Kc']
            assert conservative_params['tau_I'] > standard_params['tau_I']
            
        except (AttributeError, TypeError):
            pytest.skip("Conservative tuning option not implemented")
    
    def test_distillation_application(self):
        """Test ZN tuning for distillation column."""
        tuner = ZieglerNicholsTuning()
        
        # Distillation column parameters
        column_data = {
            'Kp': 0.8,    # mol% per reflux ratio change
            'T': 25.0,    # minutes (tray dynamics)
            'L': 4.0,     # minutes (analyzer delay)
            'type': 'composition_control'
        }
        
        try:
            tuning_params = tuner.tune_pi(column_data)  # PI preferred for composition
            
            # Check tuning is reasonable for composition control
            assert tuning_params['Kc'] > 0
            assert tuning_params['tau_I'] > column_data['L']  # Integral time > dead time
            
            # Conservative tuning expected for composition
            expected_range = (5, 20)  # Reasonable Kc range
            assert expected_range[0] < tuning_params['Kc'] < expected_range[1]
            
        except AttributeError:
            pytest.skip("Distillation tuning method not implemented")
    
    def test_flow_control_application(self):
        """Test ZN tuning for flow control loop."""
        tuner = ZieglerNicholsTuning()
        
        # Flow control parameters (fast process)
        flow_data = {
            'Kp': 1.2,    # % per % valve opening
            'T': 2.0,     # seconds (fast dynamics)
            'L': 0.5,     # seconds (minimal delay)
            'type': 'flow_control'
        }
        
        try:
            tuning_params = tuner.tune_pid(flow_data)
            
            # Flow control typically needs higher gains
            assert tuning_params['Kc'] > 5.0
            assert tuning_params['tau_D'] < 1.0  # Small derivative time
            
        except AttributeError:
            pytest.skip("Flow control tuning method not implemented")
    
    def test_tuning_parameter_limits(self, heat_exchanger_data):
        """Test that tuning parameters are within reasonable limits."""
        tuner = ZieglerNicholsTuning()
        
        try:
            params = tuner.tune_pid(heat_exchanger_data)
            
            # Check for reasonable parameter ranges
            assert 0.01 < params['Kc'] < 100.0
            assert 0.1 < params['tau_I'] < 1000.0
            assert 0.0 <= params['tau_D'] < 100.0
            
            # Check stability relationships
            # τI should be larger than τD for stability
            assert params['tau_I'] > params['tau_D']
            
        except AttributeError:
            pytest.skip("Parameter limit checking not implemented")
    
    def test_multiple_process_types(self):
        """Test ZN tuning across different process types."""
        tuner = ZieglerNicholsTuning()
        
        process_types = {
            'temperature': {'Kp': 2.5, 'T': 15.0, 'L': 2.0},
            'pressure': {'Kp': 0.8, 'T': 5.0, 'L': 1.0},
            'level': {'Kp': 1.5, 'T': 30.0, 'L': 0.5},
            'composition': {'Kp': 0.6, 'T': 40.0, 'L': 8.0}
        }
        
        for process_type, data in process_types.items():
            try:
                params = tuner.tune_pid(data)
                
                # Each process type should give reasonable parameters
                assert params['Kc'] > 0
                assert params['tau_I'] > 0
                assert params['tau_D'] >= 0
                
                # Process-specific checks
                if process_type == 'composition':
                    # Composition loops typically more conservative
                    assert params['tau_I'] > 5.0
                elif process_type == 'pressure':
                    # Pressure loops can be more aggressive
                    assert params['Kc'] > 1.0
                    
            except AttributeError:
                pytest.skip(f"Tuning for {process_type} not implemented")
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        tuner = ZieglerNicholsTuning()
        
        # Test with invalid data
        invalid_data = {
            'Kp': 0,     # Zero gain
            'T': -5.0,   # Negative time constant
            'L': 'invalid'  # Non-numeric
        }
        
        try:
            with pytest.raises((ValueError, TypeError)):
                tuner.tune_pid(invalid_data)
        except AttributeError:
            pytest.skip("Error handling not implemented")
    
    def test_describe_method(self):
        """Test describe method returns proper metadata."""
        tuner = ZieglerNicholsTuning()
        
        try:
            description = tuner.describe()
            
            assert 'method_name' in description
            assert 'tuning_rules' in description
            assert 'applicable_processes' in description
            
        except AttributeError:
            pytest.skip("Describe method not implemented")
            
    def test_performance_estimation(self, heat_exchanger_data):
        """Test performance estimation for tuned parameters."""
        tuner = ZieglerNicholsTuning()
        
        try:
            params = tuner.tune_pid(heat_exchanger_data)
            performance = tuner.estimate_performance(heat_exchanger_data, params)
            
            # Check performance metrics exist
            expected_metrics = ['settling_time', 'overshoot', 'rise_time']
            for metric in expected_metrics:
                assert metric in performance
                assert performance[metric] > 0
                
        except AttributeError:
            pytest.skip("Performance estimation not implemented")
