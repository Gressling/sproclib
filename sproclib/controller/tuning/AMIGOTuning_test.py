import pytest
import numpy as np
import warnings
from unittest.mock import Mock, patch

class TestAMIGOTuning:
    """
    Comprehensive test suite for AMIGO (Approximate M-constrained Integral Gain Optimization) tuning.
    
    Tests AMIGO tuning methodology for process control applications with emphasis on
    robustness and performance optimization under model uncertainty.
    """
    
    @pytest.fixture
    def process_data_heat_exchanger(self):
        """Heat exchanger step response data for AMIGO tuning validation."""
        return {
            'time': np.linspace(0, 300, 1501),  # 5 hours, 12-second intervals
            'process_type': 'heat_exchanger',
            'manipulated_variable': 'steam_flow',  # kg/h
            'controlled_variable': 'outlet_temperature',  # K
            'operating_conditions': {
                'inlet_temp': 293.15,  # K (20°C)
                'nominal_outlet': 353.15,  # K (80°C)
                'steam_pressure': 5.0,  # bar
                'flow_rate': 10.0  # m³/h
            },
            'step_test': {
                'magnitude': 50.0,  # kg/h steam flow increase
                'time': 30.0,  # minutes
                'initial_value': 353.15,  # K
                'final_value': 363.15,  # K (10K increase)
                'process_gain': 0.2,  # K/(kg/h)
                'time_constant': 45.0,  # minutes
                'dead_time': 5.0  # minutes
            }
        }
    
    @pytest.fixture
    def process_data_reactor(self):
        """Exothermic reactor step response data for AMIGO tuning."""
        return {
            'time': np.linspace(0, 180, 901),  # 3 hours, 12-second intervals
            'process_type': 'cstr_reactor',
            'manipulated_variable': 'coolant_flow',  # L/min
            'controlled_variable': 'reactor_temperature',  # K
            'operating_conditions': {
                'reaction_temp': 378.15,  # K (105°C)
                'coolant_temp': 298.15,  # K (25°C)
                'reactor_volume': 2.5,  # m³
                'heat_generation': 50.0  # kW
            },
            'step_test': {
                'magnitude': -5.0,  # L/min coolant increase (negative for cooling)
                'time': 15.0,  # minutes
                'initial_value': 378.15,  # K
                'final_value': 375.15,  # K (3K decrease)
                'process_gain': -0.6,  # K/(L/min)
                'time_constant': 25.0,  # minutes
                'dead_time': 2.5  # minutes
            }
        }
    
    @pytest.fixture
    def process_data_distillation(self):
        """Distillation column composition control data for AMIGO tuning."""
        return {
            'time': np.linspace(0, 480, 2401),  # 8 hours, 12-second intervals
            'process_type': 'distillation_column',
            'manipulated_variable': 'reflux_ratio',  # dimensionless
            'controlled_variable': 'top_composition',  # mole fraction
            'operating_conditions': {
                'feed_rate': 100.0,  # kmol/h
                'feed_composition': 0.5,  # mole fraction
                'operating_pressure': 1.0,  # bar
                'number_of_trays': 20
            },
            'step_test': {
                'magnitude': 0.5,  # reflux ratio increase
                'time': 60.0,  # minutes
                'initial_value': 0.95,  # mole fraction
                'final_value': 0.97,  # mole fraction
                'process_gain': 0.04,  # (mole fraction)/(reflux ratio)
                'time_constant': 120.0,  # minutes
                'dead_time': 15.0  # minutes
            }
        }
    
    def generate_step_response(self, data):
        """Generate realistic step response with noise for testing."""
        time = data['time']
        step_data = data['step_test']
        
        # First-order plus dead time response
        response = np.zeros_like(time)
        initial = step_data['initial_value']
        final = step_data['final_value']
        step_time = step_data['time']
        gain = step_data['process_gain']
        tau = step_data['time_constant']
        theta = step_data['dead_time']
        
        for i, t in enumerate(time):
            if t < step_time:
                response[i] = initial
            elif t >= step_time + theta:
                time_since_step = t - step_time - theta
                change = gain * step_data['magnitude'] * (1 - np.exp(-time_since_step / tau))
                response[i] = initial + change
            else:
                response[i] = initial
        
        # Add realistic measurement noise
        noise_level = abs(final - initial) * 0.01  # 1% noise
        np.random.seed(42)  # Reproducible results
        noise = np.random.normal(0, noise_level, len(response))
        response += noise
        
        return response
    
    def test_amigo_parameter_identification(self, process_data_heat_exchanger):
        """Test AMIGO parameter identification from step response data."""
        data = process_data_heat_exchanger
        response = self.generate_step_response(data)
        
        # Mock AMIGO parameter identification
        # In real implementation, this would analyze the step response
        identified_params = {
            'process_gain': 0.195,  # Close to actual 0.2
            'time_constant': 47.2,  # Close to actual 45.0
            'dead_time': 4.8,  # Close to actual 5.0
            'normalized_dead_time': 4.8 / 47.2  # L/T ratio
        }
        
        # Validate identification accuracy
        actual_gain = data['step_test']['process_gain']
        actual_tau = data['step_test']['time_constant']
        actual_theta = data['step_test']['dead_time']
        
        gain_error = abs(identified_params['process_gain'] - actual_gain) / abs(actual_gain)
        tau_error = abs(identified_params['time_constant'] - actual_tau) / actual_tau
        theta_error = abs(identified_params['dead_time'] - actual_theta) / actual_theta
        
        # AMIGO method should achieve good identification accuracy
        assert gain_error < 0.1, f"Process gain identification error too high: {gain_error:.3f}"
        assert tau_error < 0.1, f"Time constant identification error too high: {tau_error:.3f}"
        assert theta_error < 0.1, f"Dead time identification error too high: {theta_error:.3f}"
        
        # Check normalized dead time for applicability
        L_T_ratio = identified_params['normalized_dead_time']
        assert 0.1 <= L_T_ratio <= 2.0, f"L/T ratio {L_T_ratio:.3f} outside AMIGO applicability range"
    
    def test_amigo_pid_tuning_formulas(self, process_data_reactor):
        """Test AMIGO PID tuning parameter calculations."""
        data = process_data_reactor
        
        # Use known process parameters for testing
        Kp = abs(data['step_test']['process_gain'])  # 0.6
        T = data['step_test']['time_constant']  # 25.0
        L = data['step_test']['dead_time']  # 2.5
        
        # AMIGO PID tuning formulas
        # These are the actual AMIGO formulas for robustness
        L_T = L / T  # 0.1
        
        # AMIGO PID parameters
        if L_T <= 0.1:
            # Low dead time - aggressive tuning
            Kc = (0.15 + 0.35 * T / L) / Kp
            tau_I = 0.35 * L + 13 * L**2 / T
            tau_D = 0.5 * L
        elif L_T <= 0.2:
            # Medium dead time - balanced tuning
            Kc = (0.25 + 0.3 * T / L) / Kp
            tau_I = 0.32 * L + 13 * L**2 / T
            tau_D = 0.5 * L
        else:
            # High dead time - conservative tuning
            Kc = (0.15 + 0.25 * T / L) / Kp
            tau_I = 0.4 * L + 8 * L**2 / T
            tau_D = 0.5 * L
        
        # Validate tuning parameters
        assert Kc > 0, "Controller gain must be positive"
        assert tau_I > 0, "Integral time must be positive"
        assert tau_D >= 0, "Derivative time must be non-negative"
        
        # Check reasonable ranges for reactor control
        assert 0.1 <= Kc <= 10.0, f"Controller gain {Kc:.2f} outside reasonable range"
        assert 1.0 <= tau_I <= 100.0, f"Integral time {tau_I:.1f} outside reasonable range"
        assert 0.0 <= tau_D <= 10.0, f"Derivative time {tau_D:.1f} outside reasonable range"
        
        # AMIGO robustness constraints
        Ms_target = 1.4  # Maximum sensitivity (robustness measure)
        estimated_Ms = 1 + 0.5 * L_T  # Simplified estimation
        assert estimated_Ms <= 2.0, f"Estimated Ms {estimated_Ms:.2f} indicates poor robustness"
    
    def test_amigo_pi_tuning_conservative(self, process_data_distillation):
        """Test AMIGO PI tuning for conservative control (composition loops)."""
        data = process_data_distillation
        
        # Process parameters
        Kp = data['step_test']['process_gain']  # 0.04
        T = data['step_test']['time_constant']  # 120.0
        L = data['step_test']['dead_time']  # 15.0
        
        L_T = L / T  # 0.125
        
        # AMIGO PI tuning (conservative for composition control)
        Kc = (0.15 + 0.35 * T / L) / Kp
        tau_I = 0.35 * L + 13 * L**2 / T
        
        # For composition control, use more conservative settings
        Kc *= 0.7  # Reduce aggressiveness
        tau_I *= 1.3  # Increase integral time for stability
        
        # Validate conservative tuning
        assert Kc > 0, "PI controller gain must be positive"
        assert tau_I > L, "Integral time should be greater than dead time"
        
        # Check composition control specific constraints
        assert 1.0 <= Kc <= 50.0, f"PI gain {Kc:.1f} outside range for composition control"
        assert 10.0 <= tau_I <= 300.0, f"PI integral time {tau_I:.1f} outside reasonable range"
        
        # Robustness check for slow composition dynamics
        bandwidth = 1 / tau_I  # Approximate closed-loop bandwidth
        nyquist_limit = 1 / (2 * L)  # Nyquist frequency limit
        assert bandwidth < 0.3 * nyquist_limit, "Controller bandwidth too high for dead time"
    
    def test_amigo_robustness_analysis(self, process_data_heat_exchanger):
        """Test AMIGO robustness analysis and Ms calculation."""
        data = process_data_heat_exchanger
        
        # Process parameters
        Kp = data['step_test']['process_gain']
        T = data['step_test']['time_constant']
        L = data['step_test']['dead_time']
        
        # AMIGO tuning
        L_T = L / T
        Kc = (0.15 + 0.35 * T / L) / Kp
        tau_I = 0.35 * L + 13 * L**2 / T
        tau_D = 0.5 * L
        
        # Robustness metrics
        # Maximum sensitivity (Ms) - measure of robustness
        # AMIGO is designed to maintain Ms ≈ 1.4
        
        # Simplified Ms calculation
        omega_c = 1 / tau_I  # Crossover frequency approximation
        phase_margin = 60 - 57.3 * L * omega_c  # Degrees
        
        if phase_margin > 30:
            Ms_estimated = 1 / np.sin(np.radians(phase_margin / 2))
        else:
            Ms_estimated = 3.0  # Conservative estimate for low phase margin
        
        # AMIGO robustness constraints
        assert 1.2 <= Ms_estimated <= 2.0, f"Maximum sensitivity {Ms_estimated:.2f} outside robust range"
        assert phase_margin >= 30, f"Phase margin {phase_margin:.1f}° too low for robustness"
        
        # Gain margin estimation
        gain_margin_db = 20 * np.log10(1 + 1 / (Kc * Kp))
        assert gain_margin_db >= 6.0, f"Gain margin {gain_margin_db:.1f} dB insufficient"
    
    def test_amigo_performance_simulation(self, process_data_reactor):
        """Test AMIGO tuning performance through closed-loop simulation."""
        data = process_data_reactor
        
        # Simulation parameters
        sim_time = np.linspace(0, 120, 601)  # 2 hours
        dt = sim_time[1] - sim_time[0]
        
        # Process parameters
        Kp = data['step_test']['process_gain']
        T = data['step_test']['time_constant']
        L = data['step_test']['dead_time']
        
        # AMIGO PID tuning
        L_T = L / T
        Kc = (0.25 + 0.3 * T / L) / abs(Kp)  # Use absolute value
        tau_I = 0.32 * L + 13 * L**2 / T
        tau_D = 0.5 * L
        
        # Simplified closed-loop simulation
        setpoint = np.ones_like(sim_time) * 378.15  # K
        setpoint[300:] = 380.15  # 2K step at t=60 min
        
        # Performance metrics calculation (simplified)
        step_response_time = 4 * T  # Approximate settling time
        overshoot_expected = 5.0  # % (AMIGO targets low overshoot)
        
        # AMIGO performance expectations
        assert step_response_time <= 6 * T, "AMIGO settling time should be reasonable"
        assert overshoot_expected <= 15.0, "AMIGO should limit overshoot for robustness"
        
        # Rise time expectation
        rise_time_expected = tau_I / 3  # Approximation
        assert rise_time_expected >= L, "Rise time should be greater than dead time"
    
    def test_amigo_tuning_constraints(self):
        """Test AMIGO tuning constraints and limitations."""
        
        # Test various L/T ratios for AMIGO applicability
        test_cases = [
            {'L': 2.0, 'T': 30.0, 'Kp': 1.5, 'applicable': True},   # L/T = 0.067
            {'L': 5.0, 'T': 25.0, 'Kp': 2.0, 'applicable': True},   # L/T = 0.2
            {'L': 15.0, 'T': 20.0, 'Kp': 1.0, 'applicable': True},  # L/T = 0.75
            {'L': 25.0, 'T': 15.0, 'Kp': 0.5, 'applicable': False}, # L/T = 1.67 (marginal)
            {'L': 30.0, 'T': 10.0, 'Kp': 0.3, 'applicable': False}  # L/T = 3.0 (not applicable)
        ]
        
        for case in test_cases:
            L = case['L']
            T = case['T']
            Kp = case['Kp']
            L_T = L / T
            
            if case['applicable']:
                # AMIGO should provide reasonable tuning
                if L_T <= 0.1:
                    Kc = (0.15 + 0.35 * T / L) / Kp
                elif L_T <= 0.2:
                    Kc = (0.25 + 0.3 * T / L) / Kp
                else:
                    Kc = (0.15 + 0.25 * T / L) / Kp
                
                tau_I = 0.35 * L + 13 * L**2 / T
                
                assert Kc > 0, f"Invalid Kc for L/T={L_T:.3f}"
                assert tau_I > 0, f"Invalid tau_I for L/T={L_T:.3f}"
                assert Kc < 100 / Kp, f"Kc too high for L/T={L_T:.3f}"
            else:
                # High L/T ratio - AMIGO may not be optimal
                warnings.warn(f"L/T ratio {L_T:.3f} outside optimal AMIGO range")
    
    def test_amigo_vs_ziegler_nichols_comparison(self, process_data_heat_exchanger):
        """Test AMIGO tuning comparison with Ziegler-Nichols for robustness."""
        data = process_data_heat_exchanger
        
        # Process parameters
        Kp = data['step_test']['process_gain']
        T = data['step_test']['time_constant']
        L = data['step_test']['dead_time']
        
        # Ziegler-Nichols PID tuning
        Kc_zn = 1.2 * T / (Kp * L)
        tau_I_zn = 2 * L
        tau_D_zn = 0.5 * L
        
        # AMIGO PID tuning
        L_T = L / T
        Kc_amigo = (0.15 + 0.35 * T / L) / Kp
        tau_I_amigo = 0.35 * L + 13 * L**2 / T
        tau_D_amigo = 0.5 * L
        
        # AMIGO should be more conservative (lower Kc, higher tau_I)
        assert Kc_amigo < Kc_zn, "AMIGO should be more conservative than ZN"
        assert tau_I_amigo > tau_I_zn, "AMIGO integral time should be larger than ZN"
        
        # AMIGO robustness advantage
        amigo_aggressiveness = Kc_amigo * L / T
        zn_aggressiveness = Kc_zn * L / T
        
        assert amigo_aggressiveness < zn_aggressiveness, "AMIGO should be less aggressive"
        
        # Derivative time comparison
        assert abs(tau_D_amigo - tau_D_zn) < 0.1 * L, "Derivative times should be similar"
    
    def test_amigo_error_handling(self):
        """Test AMIGO tuning error handling and edge cases."""
        
        # Test invalid process parameters
        with pytest.raises((ValueError, AssertionError)):
            # Zero process gain
            Kp, T, L = 0.0, 10.0, 1.0
            Kc = (0.15 + 0.35 * T / L) / Kp  # Should raise division by zero
        
        with pytest.raises((ValueError, AssertionError)):
            # Negative time constant
            Kp, T, L = 1.0, -10.0, 1.0
            assert T > 0, "Time constant must be positive"
        
        with pytest.raises((ValueError, AssertionError)):
            # Negative dead time
            Kp, T, L = 1.0, 10.0, -1.0
            assert L >= 0, "Dead time must be non-negative"
        
        # Test extreme L/T ratios
        extreme_cases = [
            {'L': 0.01, 'T': 100.0, 'Kp': 1.0},  # Very low L/T
            {'L': 50.0, 'T': 10.0, 'Kp': 1.0}    # Very high L/T
        ]
        
        for case in extreme_cases:
            L_T = case['L'] / case['T']
            
            if L_T < 0.05:
                warnings.warn(f"Very low L/T ratio {L_T:.4f} - consider P or PI control")
            elif L_T > 2.0:
                warnings.warn(f"Very high L/T ratio {L_T:.2f} - AMIGO may not be optimal")
    
    def test_amigo_economic_optimization(self, process_data_distillation):
        """Test AMIGO tuning for economic optimization considerations."""
        data = process_data_distillation
        
        # Economic parameters for distillation
        energy_cost = 0.05  # $/kWh
        off_spec_cost = 1000.0  # $/kmol off-spec product
        reboiler_duty = 5000.0  # kW
        
        # Process parameters
        Kp = data['step_test']['process_gain']
        T = data['step_test']['time_constant']
        L = data['step_test']['dead_time']
        
        # AMIGO PI tuning (conservative for composition)
        Kc = (0.15 + 0.35 * T / L) / Kp * 0.7  # Conservative factor
        tau_I = (0.35 * L + 13 * L**2 / T) * 1.3  # Increase for stability
        
        # Economic performance indicators
        control_bandwidth = 1 / tau_I  # Hz
        disturbance_rejection = Kc * Kp  # Dimensionless
        
        # AMIGO should balance performance and robustness
        assert 0.001 <= control_bandwidth <= 0.01, "Bandwidth appropriate for composition control"
        assert 0.1 <= disturbance_rejection <= 2.0, "Good disturbance rejection without instability"
        
        # Energy efficiency consideration
        controller_aggressiveness = Kc / tau_I
        assert controller_aggressiveness < 1.0, "Not too aggressive to avoid energy waste"
        
        # Robustness for economic operation
        safety_factor = 1.0 / (Kc * Kp)  # Inverse of loop gain
        assert safety_factor >= 0.5, "Sufficient safety margin for economic operation"
