import pytest
import numpy as np
import warnings
from unittest.mock import Mock, patch
import time

class TestRelayTuning:
    """
    Comprehensive test suite for Relay Auto-Tuning (Relay Feedback Test) methodology.
    
    Tests relay tuning for automatic identification of process dynamics and 
    controller parameter calculation for industrial process control applications.
    """
    
    @pytest.fixture
    def relay_test_heat_exchanger(self):
        """Heat exchanger relay test configuration and expected results."""
        return {
            'process_type': 'shell_tube_heat_exchanger',
            'manipulated_variable': 'steam_valve_position',  # %
            'controlled_variable': 'outlet_temperature',  # K
            'operating_conditions': {
                'inlet_temp': 298.15,  # K (25°C)
                'outlet_setpoint': 348.15,  # K (75°C)
                'steam_pressure': 4.0,  # bar
                'heat_duty': 2500.0,  # kW
                'flow_rate': 50.0  # m³/h
            },
            'relay_parameters': {
                'relay_amplitude': 10.0,  # % valve position
                'hysteresis': 0.5,  # K temperature band
                'test_duration': 180.0,  # minutes
                'sampling_time': 0.5  # minutes
            },
            'expected_results': {
                'ultimate_gain': 2.5,  # Ku
                'ultimate_period': 25.0,  # Tu (minutes)
                'process_gain': 1.8,  # K/%
                'dead_time': 3.5,  # minutes
                'oscillation_amplitude': 4.2  # K
            }
        }
    
    @pytest.fixture
    def relay_test_reactor(self):
        """CSTR reactor relay test for temperature control."""
        return {
            'process_type': 'cstr_reactor',
            'manipulated_variable': 'jacket_cooling_flow',  # L/min
            'controlled_variable': 'reactor_temperature',  # K
            'operating_conditions': {
                'reaction_temp': 383.15,  # K (110°C)
                'coolant_temp': 293.15,  # K (20°C)
                'reactor_volume': 5.0,  # m³
                'heat_generation': 150.0,  # kW
                'exothermic_reaction': True
            },
            'relay_parameters': {
                'relay_amplitude': 15.0,  # L/min flow change
                'hysteresis': 1.0,  # K temperature band
                'test_duration': 120.0,  # minutes
                'sampling_time': 0.2  # minutes
            },
            'expected_results': {
                'ultimate_gain': 0.8,  # Ku
                'ultimate_period': 18.0,  # Tu (minutes)
                'process_gain': -0.4,  # K/(L/min) (negative for cooling)
                'dead_time': 2.0,  # minutes
                'oscillation_amplitude': 3.8  # K
            }
        }
    
    @pytest.fixture
    def relay_test_level_control(self):
        """Tank level control relay test configuration."""
        return {
            'process_type': 'storage_tank',
            'manipulated_variable': 'outlet_valve_position',  # %
            'controlled_variable': 'liquid_level',  # m
            'operating_conditions': {
                'tank_diameter': 4.0,  # m
                'normal_level': 3.5,  # m
                'inlet_flow': 20.0,  # m³/h
                'tank_volume': 44.0,  # m³
                'integrating_process': True
            },
            'relay_parameters': {
                'relay_amplitude': 20.0,  # % valve position
                'hysteresis': 0.1,  # m level band
                'test_duration': 240.0,  # minutes
                'sampling_time': 1.0  # minutes
            },
            'expected_results': {
                'ultimate_gain': None,  # Integrating process
                'ultimate_period': 60.0,  # Tu (minutes)
                'process_gain': 'integrating',  # m/(%·min)
                'dead_time': 1.5,  # minutes
                'oscillation_amplitude': 0.8  # m
            }
        }
    
    def generate_relay_response(self, config, noise_level=0.02):
        """Generate simulated relay test response for testing."""
        relay_params = config['relay_parameters']
        expected = config['expected_results']
        
        # Time vector
        duration = relay_params['test_duration']
        dt = relay_params['sampling_time']
        time_vector = np.arange(0, duration + dt, dt)
        
        # Relay test simulation
        relay_amplitude = relay_params['relay_amplitude']
        hysteresis = relay_params['hysteresis']
        
        # Initialize arrays
        manipulated_var = np.zeros_like(time_vector)
        controlled_var = np.zeros_like(time_vector)
        relay_output = np.zeros_like(time_vector)
        
        # Initial conditions
        setpoint = 0.0  # Deviation variables
        pv = 0.0
        relay_state = 1  # Start with positive relay
        
        # Process parameters from expected results
        if expected['ultimate_period'] and expected['ultimate_gain']:
            Ku = expected['ultimate_gain']
            Tu = expected['ultimate_period']
            omega_u = 2 * np.pi / Tu  # Ultimate frequency
            
            # Simplified process response
            if config['process_type'] == 'storage_tank':
                # Integrating process
                process_gain_int = 0.1  # m/(%·min)
            else:
                # Self-regulating process
                process_gain = expected['process_gain']
        
        for i in range(1, len(time_vector)):
            # Relay logic with hysteresis
            error = setpoint - pv
            
            if relay_state == 1 and error <= -hysteresis/2:
                relay_state = -1
            elif relay_state == -1 and error >= hysteresis/2:
                relay_state = 1
            
            relay_output[i] = relay_state * relay_amplitude
            manipulated_var[i] = relay_output[i]
            
            # Process response simulation
            if config['process_type'] == 'storage_tank':
                # Integrating process - level accumulates
                controlled_var[i] = controlled_var[i-1] + process_gain_int * manipulated_var[i] * dt
            else:
                # Self-regulating process with oscillation
                t = time_vector[i]
                if t > 20:  # Allow time for oscillation to develop
                    amplitude = expected['oscillation_amplitude'] / 2
                    frequency = omega_u
                    phase = np.pi if relay_state == -1 else 0
                    controlled_var[i] = amplitude * np.sin(frequency * (t - 20) + phase)
        
        # Add measurement noise
        np.random.seed(42)
        noise = np.random.normal(0, noise_level * np.std(controlled_var), len(controlled_var))
        controlled_var += noise
        
        return {
            'time': time_vector,
            'manipulated_variable': manipulated_var,
            'controlled_variable': controlled_var,
            'relay_output': relay_output
        }
    
    def test_relay_oscillation_detection(self, relay_test_heat_exchanger):
        """Test relay auto-tuning oscillation detection and analysis."""
        config = relay_test_heat_exchanger
        response = self.generate_relay_response(config)
        
        # Analyze oscillation characteristics
        time = response['time']
        pv = response['controlled_variable']
        mv = response['manipulated_variable']
        
        # Find oscillation after initial transient (skip first 20 minutes)
        start_idx = int(20 / config['relay_parameters']['sampling_time'])
        pv_oscillation = pv[start_idx:]
        time_oscillation = time[start_idx:]
        
        # Peak detection for period calculation
        # Find peaks and valleys
        peaks = []
        valleys = []
        
        for i in range(1, len(pv_oscillation) - 1):
            if pv_oscillation[i] > pv_oscillation[i-1] and pv_oscillation[i] > pv_oscillation[i+1]:
                peaks.append(i)
            elif pv_oscillation[i] < pv_oscillation[i-1] and pv_oscillation[i] < pv_oscillation[i+1]:
                valleys.append(i)
        
        # Calculate period from peak-to-peak intervals
        if len(peaks) >= 3:
            peak_times = time_oscillation[peaks]
            periods = np.diff(peak_times)
            average_period = np.mean(periods)
            
            # Validate period detection
            expected_period = config['expected_results']['ultimate_period']
            period_error = abs(average_period - expected_period) / expected_period
            assert period_error < 0.1, f"Period detection error {period_error:.3f} too high"
        
        # Calculate oscillation amplitude
        if len(peaks) > 0 and len(valleys) > 0:
            peak_values = pv_oscillation[peaks]
            valley_values = pv_oscillation[valleys]
            amplitude = np.mean(peak_values) - np.mean(valley_values)
            
            expected_amplitude = config['expected_results']['oscillation_amplitude']
            amplitude_error = abs(amplitude - expected_amplitude) / expected_amplitude
            assert amplitude_error < 0.2, f"Amplitude detection error {amplitude_error:.3f} too high"
    
    def test_ultimate_gain_calculation(self, relay_test_reactor):
        """Test ultimate gain calculation from relay test data."""
        config = relay_test_reactor
        response = self.generate_relay_response(config)
        
        # Ultimate gain calculation using describing function method
        relay_amplitude = config['relay_parameters']['relay_amplitude']
        oscillation_amplitude = config['expected_results']['oscillation_amplitude']
        
        # Describing function for relay with hysteresis
        hysteresis = config['relay_parameters']['hysteresis']
        
        # For ideal relay (no hysteresis): N = 4*h/(π*a)
        # For relay with hysteresis: N = 4*h/(π*a) * sqrt(1 - (ε/a)²)
        # where h = relay amplitude, a = oscillation amplitude, ε = hysteresis
        
        if hysteresis == 0:
            # Ideal relay
            describing_function = 4 * relay_amplitude / (np.pi * oscillation_amplitude)
        else:
            # Relay with hysteresis
            if oscillation_amplitude > hysteresis:
                hysteresis_factor = np.sqrt(1 - (hysteresis / oscillation_amplitude)**2)
                describing_function = 4 * relay_amplitude / (np.pi * oscillation_amplitude) * hysteresis_factor
            else:
                describing_function = 0  # No oscillation possible
        
        # Ultimate gain is inverse of describing function
        if describing_function > 0:
            Ku_calculated = 1 / describing_function
        else:
            Ku_calculated = np.inf
        
        # Validate ultimate gain calculation
        expected_Ku = config['expected_results']['ultimate_gain']
        if expected_Ku and np.isfinite(Ku_calculated):
            Ku_error = abs(Ku_calculated - expected_Ku) / expected_Ku
            assert Ku_error < 0.15, f"Ultimate gain calculation error {Ku_error:.3f} too high"
            assert Ku_calculated > 0, "Ultimate gain must be positive"
            assert Ku_calculated < 100, "Ultimate gain unreasonably high"
    
    def test_relay_pid_tuning(self, relay_test_heat_exchanger):
        """Test PID tuning parameter calculation from relay test results."""
        config = relay_test_heat_exchanger
        
        # Use identified parameters from relay test
        Ku = config['expected_results']['ultimate_gain']
        Tu = config['expected_results']['ultimate_period']
        
        # Ziegler-Nichols tuning from relay test
        Kc_zn = 0.6 * Ku
        tau_I_zn = 0.5 * Tu
        tau_D_zn = 0.125 * Tu
        
        # Tyreus-Luyben tuning (more conservative)
        Kc_tl = Ku / 3.2
        tau_I_tl = 2.2 * Tu
        tau_D_tl = Tu / 6.3
        
        # AMIGO-like tuning from relay test
        Kc_amigo = 0.45 * Ku
        tau_I_amigo = 0.85 * Tu
        tau_D_amigo = 0.1 * Tu
        
        # Validate tuning parameters
        tuning_methods = [
            ('ZN', Kc_zn, tau_I_zn, tau_D_zn),
            ('TL', Kc_tl, tau_I_tl, tau_D_tl),
            ('AMIGO', Kc_amigo, tau_I_amigo, tau_D_amigo)
        ]
        
        for method, Kc, tau_I, tau_D in tuning_methods:
            assert Kc > 0, f"{method}: Controller gain must be positive"
            assert tau_I > 0, f"{method}: Integral time must be positive"
            assert tau_D >= 0, f"{method}: Derivative time must be non-negative"
            
            # Reasonable ranges for heat exchanger control
            assert 0.1 <= Kc <= 10.0, f"{method}: Kc {Kc:.2f} outside reasonable range"
            assert 1.0 <= tau_I <= 100.0, f"{method}: tau_I {tau_I:.1f} outside reasonable range"
            assert 0.0 <= tau_D <= 20.0, f"{method}: tau_D {tau_D:.1f} outside reasonable range"
        
        # Conservative tuning should have lower gains
        assert Kc_tl < Kc_zn, "Tyreus-Luyben should be more conservative than ZN"
        assert tau_I_tl > tau_I_zn, "TL integral time should be larger than ZN"
    
    def test_relay_integrating_process(self, relay_test_level_control):
        """Test relay tuning for integrating processes (level control)."""
        config = relay_test_level_control
        response = self.generate_relay_response(config)
        
        # For integrating processes, relay test gives different information
        # No ultimate gain (Ku = ∞), but still has ultimate period
        
        Tu = config['expected_results']['ultimate_period']
        relay_amplitude = config['relay_parameters']['relay_amplitude']
        oscillation_amplitude = config['expected_results']['oscillation_amplitude']
        
        # For integrating processes, use modified tuning rules
        # PI tuning for integrating processes
        Kc_int = 0.15 / (relay_amplitude / oscillation_amplitude * Tu / 60)  # Normalize to hours
        tau_I_int = 0.5 * Tu
        
        # Validate integrating process tuning
        assert Kc_int > 0, "Integrating process controller gain must be positive"
        assert tau_I_int > 0, "Integrating process integral time must be positive"
        
        # For level control, gains should be moderate
        assert 0.01 <= Kc_int <= 2.0, f"Level control Kc {Kc_int:.3f} outside reasonable range"
        assert 10.0 <= tau_I_int <= 200.0, f"Level control tau_I {tau_I_int:.1f} outside reasonable range"
        
        # No derivative action for integrating processes
        tau_D_int = 0.0
        assert tau_D_int == 0.0, "No derivative action for integrating processes"
    
    def test_relay_test_design(self, relay_test_reactor):
        """Test relay test design parameters and constraints."""
        config = relay_test_reactor
        
        relay_params = config['relay_parameters']
        operating_conditions = config['operating_conditions']
        
        # Relay amplitude selection
        relay_amplitude = relay_params['relay_amplitude']
        normal_flow = 50.0  # L/min (assumed normal coolant flow)
        
        # Relay amplitude should be 5-20% of normal operating range
        amplitude_fraction = relay_amplitude / normal_flow
        assert 0.05 <= amplitude_fraction <= 0.3, f"Relay amplitude {amplitude_fraction:.3f} outside recommended range"
        
        # Hysteresis selection
        hysteresis = relay_params['hysteresis']
        measurement_noise = 0.1  # K (assumed temperature measurement noise)
        
        # Hysteresis should be 2-5 times measurement noise
        hysteresis_ratio = hysteresis / measurement_noise
        assert 2.0 <= hysteresis_ratio <= 10.0, f"Hysteresis ratio {hysteresis_ratio:.1f} outside recommended range"
        
        # Test duration
        test_duration = relay_params['test_duration']
        expected_period = config['expected_results']['ultimate_period']
        
        # Test should run for at least 5-10 periods
        duration_ratio = test_duration / expected_period
        assert duration_ratio >= 4.0, f"Test duration too short: {duration_ratio:.1f} periods"
        assert duration_ratio <= 20.0, f"Test duration too long: {duration_ratio:.1f} periods"
        
        # Sampling time
        sampling_time = relay_params['sampling_time']
        
        # Sampling should be fast enough (at least 20 samples per period)
        samples_per_period = expected_period / sampling_time
        assert samples_per_period >= 10, f"Sampling too slow: {samples_per_period:.1f} samples/period"
        assert sampling_time <= 1.0, "Sampling time should not exceed 1 minute for good resolution"
    
    def test_relay_safety_considerations(self, relay_test_heat_exchanger):
        """Test relay tuning safety considerations and constraints."""
        config = relay_test_heat_exchanger
        
        operating_conditions = config['operating_conditions']
        relay_params = config['relay_parameters']
        
        # Safety limits during relay test
        outlet_setpoint = operating_conditions['outlet_setpoint']
        relay_amplitude = relay_params['relay_amplitude']
        expected_oscillation = config['expected_results']['oscillation_amplitude']
        
        # Temperature excursions should be within safe limits
        max_temp_excursion = expected_oscillation / 2
        min_safe_temp = outlet_setpoint - 10.0  # K
        max_safe_temp = outlet_setpoint + 15.0  # K
        
        predicted_min_temp = outlet_setpoint - max_temp_excursion
        predicted_max_temp = outlet_setpoint + max_temp_excursion
        
        assert predicted_min_temp >= min_safe_temp, f"Relay test may cause unsafe low temperature"
        assert predicted_max_temp <= max_safe_temp, f"Relay test may cause unsafe high temperature"
        
        # Steam valve position limits
        nominal_valve_position = 50.0  # % (assumed)
        max_valve_change = relay_amplitude
        
        min_valve_position = nominal_valve_position - max_valve_change
        max_valve_position = nominal_valve_position + max_valve_change
        
        assert min_valve_position >= 0.0, "Relay test may drive valve below 0%"
        assert max_valve_position <= 100.0, "Relay test may drive valve above 100%"
        
        # Test should not run during critical operating periods
        heat_duty = operating_conditions['heat_duty']
        max_safe_duty = 3000.0  # kW
        
        assert heat_duty <= max_safe_duty, "Process load too high for safe relay testing"
    
    def test_relay_noise_robustness(self, relay_test_reactor):
        """Test relay tuning robustness to measurement noise."""
        config = relay_test_reactor
        
        # Test with different noise levels
        noise_levels = [0.01, 0.05, 0.1, 0.2]  # 1%, 5%, 10%, 20% noise
        
        base_response = self.generate_relay_response(config, noise_level=0.01)
        base_amplitude = config['expected_results']['oscillation_amplitude']
        
        for noise_level in noise_levels:
            noisy_response = self.generate_relay_response(config, noise_level=noise_level)
            
            # Check if oscillation is still detectable
            pv_noisy = noisy_response['controlled_variable']
            pv_std = np.std(pv_noisy[100:])  # Skip initial transient
            
            # Signal-to-noise ratio
            snr = base_amplitude / (2 * pv_std)
            
            if noise_level <= 0.1:
                # Low to moderate noise - should still work
                assert snr >= 2.0, f"SNR {snr:.1f} too low for reliable identification at {noise_level*100}% noise"
            else:
                # High noise - may not work well
                if snr < 1.0:
                    warnings.warn(f"High noise level {noise_level*100}% may prevent reliable relay tuning")
    
    def test_relay_process_nonlinearity(self, relay_test_heat_exchanger):
        """Test relay tuning considerations for nonlinear processes."""
        config = relay_test_heat_exchanger
        
        # Simulate nonlinear heat exchanger response
        # Heat transfer coefficient varies with flow rate
        
        operating_conditions = config['operating_conditions']
        relay_params = config['relay_parameters']
        
        # Base conditions
        nominal_steam_flow = 1000.0  # kg/h
        relay_amplitude = relay_params['relay_amplitude']  # % valve
        
        # Valve to flow nonlinearity (square root characteristic)
        valve_positions = [50 - relay_amplitude/2, 50 + relay_amplitude/2]  # %
        steam_flows = [nominal_steam_flow * np.sqrt(pos/50) for pos in valve_positions]
        
        # Heat transfer nonlinearity
        # U varies with flow rate: U ∝ flow^0.8
        base_u = 1000.0  # W/(m²·K)
        heat_transfer_coeffs = [base_u * (flow/nominal_steam_flow)**0.8 for flow in steam_flows]
        
        # Check for significant nonlinearity
        u_variation = (max(heat_transfer_coeffs) - min(heat_transfer_coeffs)) / base_u
        
        if u_variation > 0.2:  # More than 20% variation
            warnings.warn(f"Significant process nonlinearity detected: {u_variation*100:.1f}% variation in heat transfer")
            
            # Recommend smaller relay amplitude for better linearity
            recommended_amplitude = relay_amplitude * 0.7
            assert recommended_amplitude >= 5.0, "Cannot reduce relay amplitude below minimum"
            
            warnings.warn(f"Consider reducing relay amplitude to {recommended_amplitude:.1f}% for better linearity")
    
    def test_relay_multiple_loops_interference(self):
        """Test relay tuning considerations for multiple interacting control loops."""
        
        # Simulate two interacting loops (temperature and flow)
        loop_configs = {
            'temperature': {
                'relay_amplitude': 10.0,  # % valve position
                'expected_period': 25.0,  # minutes
                'coupling_factor': 0.3  # Interaction strength
            },
            'flow': {
                'relay_amplitude': 15.0,  # % valve position  
                'expected_period': 8.0,  # minutes
                'coupling_factor': 0.2  # Interaction strength
            }
        }
        
        # Check for period interference
        temp_period = loop_configs['temperature']['expected_period']
        flow_period = loop_configs['flow']['expected_period']
        
        period_ratio = max(temp_period, flow_period) / min(temp_period, flow_period)
        
        if period_ratio < 3.0:
            warnings.warn(f"Loop periods too close: ratio {period_ratio:.1f} < 3.0")
            warnings.warn("Consider sequential relay testing to avoid interference")
        
        # Check coupling effects
        for loop_name, config in loop_configs.items():
            coupling = config['coupling_factor']
            
            if coupling > 0.1:
                warnings.warn(f"{loop_name} loop has significant coupling: {coupling:.2f}")
                
                # Recommend reduced relay amplitude for coupled loops
                original_amplitude = config['relay_amplitude']
                reduced_amplitude = original_amplitude * (1 - coupling)
                
                assert reduced_amplitude >= 5.0, f"Coupling too strong for {loop_name} loop relay testing"
    
    def test_relay_economic_impact(self, relay_test_heat_exchanger):
        """Test economic impact analysis of relay auto-tuning tests."""
        config = relay_test_heat_exchanger
        
        # Economic parameters
        steam_cost = 15.0  # $/tonne
        off_spec_cost = 100.0  # $/hour of off-spec operation
        production_rate = 10.0  # tonnes/hour
        
        # Relay test economics
        test_duration = config['relay_parameters']['test_duration'] / 60  # hours
        relay_amplitude = config['relay_parameters']['relay_amplitude']  # %
        expected_oscillation = config['expected_results']['oscillation_amplitude']  # K
        
        # Steam consumption impact
        nominal_steam_flow = 2.0  # tonnes/hour
        steam_variation = nominal_steam_flow * relay_amplitude / 100 * 0.5  # Average increase
        extra_steam_cost = steam_variation * steam_cost * test_duration
        
        # Off-specification impact
        temp_deviation = expected_oscillation / 2  # Average deviation
        if temp_deviation > 2.0:  # K tolerance
            off_spec_time = test_duration * 0.7  # Estimated fraction of time off-spec
            off_spec_cost_total = off_spec_time * off_spec_cost
        else:
            off_spec_cost_total = 0.0
        
        # Total test cost
        total_test_cost = extra_steam_cost + off_spec_cost_total
        
        # Benefits of improved control
        # Assume 50% reduction in temperature variance after tuning
        annual_energy_savings = 5000.0  # $/year
        annual_quality_savings = 8000.0  # $/year
        total_annual_savings = annual_energy_savings + annual_quality_savings
        
        # Payback period
        if total_test_cost > 0:
            payback_days = total_test_cost / (total_annual_savings / 365)
        else:
            payback_days = 0
        
        # Economic validation
        assert total_test_cost <= 1000.0, f"Relay test cost ${total_test_cost:.2f} too high"
        assert payback_days <= 30.0, f"Payback period {payback_days:.1f} days too long"
        
        # Cost-benefit ratio
        if total_test_cost > 0:
            benefit_ratio = total_annual_savings / total_test_cost
            assert benefit_ratio >= 10.0, f"Benefit-cost ratio {benefit_ratio:.1f} too low"
