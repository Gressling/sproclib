import pytest
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add the module path for importing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestParameterEstimation:
    """
    Comprehensive test suite for parameter estimation methods.
    
    Tests linear regression, nonlinear optimization, and statistical analysis
    for chemical process parameter identification.
    """
    
    @pytest.fixture
    def kinetic_data(self):
        """Generate synthetic kinetic data for testing"""
        # Arrhenius parameters (true values)
        k0_true = 1e8  # 1/s
        Ea_true = 75000  # J/mol
        R = 8.314  # J/(mol·K)
        
        temperatures = np.array([313, 323, 333, 343, 353])  # K
        time_points = np.linspace(0, 3600, 13)  # seconds
        
        data = {}
        np.random.seed(42)  # Reproducible results
        
        for T in temperatures:
            k = k0_true * np.exp(-Ea_true / (R * T))
            C0 = 2.0  # mol/L
            
            # First-order kinetics with noise
            C_true = C0 * np.exp(-k * time_points)
            noise = np.random.normal(0, 0.02 * C_true)
            C_exp = C_true + noise
            C_exp = np.maximum(C_exp, 0.01)  # Ensure positive
            
            data[T] = {
                'time': time_points,
                'concentration': C_exp,
                'initial_conc': C0,
                'true_k': k
            }
        
        return {
            'data': data,
            'true_params': {'k0': k0_true, 'Ea': Ea_true},
            'temperatures': temperatures
        }
    
    def test_linear_regression_basic(self):
        """Test basic linear regression functionality"""
        # Simple linear relationship: y = a*x + b
        np.random.seed(42)
        x = np.linspace(0, 10, 50)
        a_true, b_true = 2.5, 1.2
        y_true = a_true * x + b_true
        noise = np.random.normal(0, 0.1, len(x))
        y_exp = y_true + noise
        
        # Linear regression
        X = np.column_stack([x, np.ones(len(x))])
        params = np.linalg.lstsq(X, y_exp, rcond=None)[0]
        a_est, b_est = params
        
        # Validate estimates
        assert abs(a_est - a_true) < 0.1, f"Slope error too high: {abs(a_est - a_true)}"
        assert abs(b_est - b_true) < 0.1, f"Intercept error too high: {abs(b_est - b_true)}"
        
        # R-squared calculation
        y_pred = a_est * x + b_est
        ss_res = np.sum((y_exp - y_pred)**2)
        ss_tot = np.sum((y_exp - np.mean(y_exp))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        assert r_squared > 0.95, f"R-squared too low: {r_squared}"
    
    def test_arrhenius_parameter_estimation(self, kinetic_data):
        """Test Arrhenius parameter estimation from kinetic data"""
        from scipy.optimize import minimize
        
        data = kinetic_data['data']
        temperatures = kinetic_data['temperatures']
        true_params = kinetic_data['true_params']
        R = 8.314  # J/(mol·K)
        
        def arrhenius_model(T, k0, Ea):
            return k0 * np.exp(-Ea / (R * T))
        
        def first_order_model(t, C0, k):
            return C0 * np.exp(-k * t)
        
        def objective_function(params):
            k0, Ea = params
            sse = 0.0
            
            for T in temperatures:
                k_pred = arrhenius_model(T, k0, Ea)
                C_pred = first_order_model(
                    data[T]['time'], 
                    data[T]['initial_conc'], 
                    k_pred
                )
                sse += np.sum((data[T]['concentration'] - C_pred)**2)
            
            return sse
        
        # Parameter estimation
        initial_guess = [1e6, 60000]  # k0, Ea
        result = minimize(objective_function, initial_guess, method='Nelder-Mead')
        
        k0_est, Ea_est = result.x
        
        # Validate convergence
        assert result.success, "Optimization did not converge"
        
        # Validate parameter estimates (allow 15% error due to noise)
        k0_error = abs(k0_est - true_params['k0']) / true_params['k0']
        Ea_error = abs(Ea_est - true_params['Ea']) / true_params['Ea']
        
        assert k0_error < 0.2, f"k0 estimation error too high: {k0_error:.3f}"
        assert Ea_error < 0.15, f"Ea estimation error too high: {Ea_error:.3f}"
        
        # Validate physical reasonableness
        assert 1e6 <= k0_est <= 1e12, f"k0 estimate outside reasonable range: {k0_est:.2e}"
        assert 50000 <= Ea_est <= 100000, f"Ea estimate outside reasonable range: {Ea_est}"
    
    def test_confidence_intervals(self, kinetic_data):
        """Test confidence interval calculation for parameters"""
        from scipy.stats import t
        
        # Simplified confidence interval calculation
        n_data = 65  # Total data points (5 temps × 13 time points)
        n_params = 2
        degrees_freedom = n_data - n_params
        
        # Mock parameter estimates and standard errors
        k0_est = 8.5e7
        Ea_est = 73500
        
        # Estimated standard errors (from covariance matrix)
        std_k0 = 1.2e7
        std_Ea = 3500
        
        # 95% confidence intervals
        t_value = t.ppf(0.975, degrees_freedom)
        
        k0_ci = t_value * std_k0
        Ea_ci = t_value * std_Ea
        
        # Validate confidence interval calculation
        assert t_value > 1.9, "t-value too small for 95% confidence"
        assert k0_ci > 0, "Confidence interval must be positive"
        assert Ea_ci > 0, "Confidence interval must be positive"
        
        # Relative confidence intervals should be reasonable
        rel_ci_k0 = k0_ci / k0_est
        rel_ci_Ea = Ea_ci / Ea_est
        
        assert rel_ci_k0 < 0.5, f"k0 confidence interval too wide: {rel_ci_k0:.3f}"
        assert rel_ci_Ea < 0.2, f"Ea confidence interval too wide: {rel_ci_Ea:.3f}"
    
    def test_model_validation_statistics(self, kinetic_data):
        """Test model validation statistics calculation"""
        data = kinetic_data['data']
        temperatures = kinetic_data['temperatures']
        
        # Mock predictions vs experimental data
        all_residuals = []
        all_experimental = []
        
        for T in temperatures:
            exp_data = data[T]['concentration']
            # Simulate predictions with small error
            predictions = exp_data + np.random.normal(0, 0.01, len(exp_data))
            residuals = exp_data - predictions
            
            all_residuals.extend(residuals)
            all_experimental.extend(exp_data)
        
        residuals_array = np.array(all_residuals)
        experimental_array = np.array(all_experimental)
        
        # Calculate statistics
        rmse = np.sqrt(np.mean(residuals_array**2))
        mae = np.mean(np.abs(residuals_array))
        
        # R-squared calculation
        ss_res = np.sum(residuals_array**2)
        ss_tot = np.sum((experimental_array - np.mean(experimental_array))**2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # Validate statistics
        assert rmse > 0, "RMSE must be positive"
        assert mae > 0, "MAE must be positive"
        assert 0 <= r_squared <= 1, f"R-squared outside valid range: {r_squared}"
        assert r_squared > 0.9, f"R-squared too low for good fit: {r_squared}"
        assert rmse < 0.1, f"RMSE too high: {rmse}"
    
    def test_parameter_correlation_analysis(self):
        """Test parameter correlation matrix calculation"""
        # Mock covariance matrix for 2 parameters
        variance_k0 = (1e7)**2
        variance_Ea = (2500)**2
        covariance_k0_Ea = 1e7 * 2500 * 0.8  # 80% correlation
        
        cov_matrix = np.array([
            [variance_k0, covariance_k0_Ea],
            [covariance_k0_Ea, variance_Ea]
        ])
        
        # Calculate correlation matrix
        std_devs = np.sqrt(np.diag(cov_matrix))
        correlation_matrix = cov_matrix / np.outer(std_devs, std_devs)
        
        # Validate correlation matrix properties
        assert np.allclose(np.diag(correlation_matrix), 1.0), "Diagonal should be 1"
        assert np.allclose(correlation_matrix, correlation_matrix.T), "Should be symmetric"
        
        # Check correlation value
        correlation_k0_Ea = correlation_matrix[0, 1]
        assert -1 <= correlation_k0_Ea <= 1, "Correlation outside valid range"
        assert abs(correlation_k0_Ea - 0.8) < 0.01, "Correlation calculation error"
    
    def test_physical_parameter_validation(self):
        """Test validation of physically reasonable parameters"""
        # Test cases with expected validity
        test_cases = [
            {'k0': 1e8, 'Ea': 75000, 'valid': True},    # Typical values
            {'k0': 1e15, 'Ea': 200000, 'valid': True},  # High energy reaction
            {'k0': 1e3, 'Ea': 25000, 'valid': True},    # Low energy reaction
            {'k0': -1e8, 'Ea': 75000, 'valid': False},  # Negative k0
            {'k0': 1e8, 'Ea': -10000, 'valid': False},  # Negative Ea
            {'k0': 1e20, 'Ea': 500000, 'valid': False}, # Unreasonably high
        ]
        
        for case in test_cases:
            k0, Ea = case['k0'], case['Ea']
            expected_valid = case['valid']
            
            # Physical validation criteria
            k0_valid = k0 > 0 and k0 < 1e18
            Ea_valid = Ea > 0 and Ea < 300000  # J/mol
            
            is_valid = k0_valid and Ea_valid
            
            if expected_valid:
                assert is_valid, f"Parameters should be valid: k0={k0:.2e}, Ea={Ea}"
            else:
                assert not is_valid, f"Parameters should be invalid: k0={k0:.2e}, Ea={Ea}"
    
    def test_temperature_sensitivity_analysis(self):
        """Test temperature sensitivity of rate constants"""
        k0 = 1e8  # 1/s
        Ea = 75000  # J/mol
        R = 8.314  # J/(mol·K)
        
        def arrhenius(T):
            return k0 * np.exp(-Ea / (R * T))
        
        # Reference conditions
        T_ref = 333.15  # K (60°C)
        k_ref = arrhenius(T_ref)
        
        # Temperature sensitivity tests
        delta_T = 10  # K temperature change
        T_high = T_ref + delta_T
        T_low = T_ref - delta_T
        
        k_high = arrhenius(T_high)
        k_low = arrhenius(T_low)
        
        # Calculate sensitivity factors
        factor_high = k_high / k_ref
        factor_low = k_ref / k_low
        
        # For typical activation energies, 10K change should give 1.5-3x rate change
        assert 1.5 <= factor_high <= 4.0, f"High temp factor outside expected range: {factor_high:.2f}"
        assert 1.5 <= factor_low <= 4.0, f"Low temp factor outside expected range: {factor_low:.2f}"
        
        # Temperature coefficient (approximate)
        temp_coeff = Ea / (R * T_ref**2)  # d(ln k)/dT
        expected_factor = np.exp(temp_coeff * delta_T)
        
        # Should match analytical expectation within 5%
        assert abs(factor_high - expected_factor) / expected_factor < 0.05
    
    def test_data_quality_assessment(self):
        """Test data quality metrics for parameter estimation"""
        # Generate data with different noise levels
        np.random.seed(42)
        x = np.linspace(0, 10, 50)
        y_true = 2 * x + 1
        
        noise_levels = [0.01, 0.1, 0.5, 1.0]  # Different noise levels
        
        for noise_level in noise_levels:
            y_noisy = y_true + np.random.normal(0, noise_level, len(x))
            
            # Signal-to-noise ratio
            signal_power = np.var(y_true)
            noise_power = noise_level**2
            snr = signal_power / noise_power
            snr_db = 10 * np.log10(snr)
            
            # Data quality assessment
            if noise_level <= 0.1:
                assert snr_db >= 20, f"SNR too low for good estimation: {snr_db:.1f} dB"
                data_quality = "Excellent"
            elif noise_level <= 0.5:
                assert snr_db >= 5, f"SNR marginal: {snr_db:.1f} dB"
                data_quality = "Good"
            else:
                data_quality = "Poor"
            
            # Validate data quality classification
            assert data_quality in ["Excellent", "Good", "Poor"]
    
    def test_economic_impact_calculation(self):
        """Test economic impact calculations from parameter estimates"""
        # Reactor design parameters
        k_estimated = 2.5e-3  # 1/s at operating temperature
        target_conversion = 0.95
        feed_rate = 1000  # mol/h
        feed_concentration = 2.0  # mol/L
        
        # Required residence time for first-order reaction
        residence_time = -np.log(1 - target_conversion) / k_estimated / 3600  # hours
        
        # Reactor volume
        reactor_volume = feed_rate * residence_time / feed_concentration  # L
        
        # Economic calculations
        reactor_cost_per_liter = 500  # $/L
        total_reactor_cost = reactor_volume * reactor_cost_per_liter
        
        # Validate calculations
        assert residence_time > 0, "Residence time must be positive"
        assert reactor_volume > 0, "Reactor volume must be positive"
        assert total_reactor_cost > 0, "Reactor cost must be positive"
        
        # Reasonable ranges for chemical reactors
        assert 0.1 <= residence_time <= 10, f"Residence time outside typical range: {residence_time:.2f} h"
        assert 100 <= reactor_volume <= 10000, f"Reactor volume outside typical range: {reactor_volume:.0f} L"
        
        # Sensitivity analysis for ±20% parameter uncertainty
        k_high = k_estimated * 1.2
        k_low = k_estimated * 0.8
        
        residence_time_low = -np.log(1 - target_conversion) / k_high / 3600
        residence_time_high = -np.log(1 - target_conversion) / k_low / 3600
        
        volume_sensitivity = (residence_time_high - residence_time_low) / residence_time
        
        # Parameter uncertainty should have significant economic impact
        assert volume_sensitivity > 0.2, f"Parameter sensitivity too low: {volume_sensitivity:.3f}"
