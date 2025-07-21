import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, curve_fit
from scipy.stats import t

def main():
    """
    Parameter Estimation Example: Reaction Kinetics for Catalytic Process
    
    This example demonstrates parameter estimation for a catalytic reaction
    using experimental data from a batch reactor study.
    """
    
    print("=== Parameter Estimation Example: Catalytic Reaction Kinetics ===")
    print()
    
    # ==============================================
    # STEP 1: EXPERIMENTAL DATA
    # ==============================================
    print("1. Experimental Data from Batch Reactor")
    print("-" * 50)
    
    # Simulated experimental data for A → B catalytic reaction
    # Temperature study at different conditions
    temperatures = np.array([313, 323, 333, 343, 353])  # K
    time_data = np.linspace(0, 3600, 13)  # seconds (0 to 1 hour)
    
    print(f"Reaction: A → B (catalytic)")
    print(f"Reactor Type: Batch")
    print(f"Temperature Range: {temperatures.min()-273.15:.0f}-{temperatures.max()-273.15:.0f}°C")
    print(f"Time Range: 0-{time_data.max()/60:.0f} minutes")
    print(f"Initial Concentration: 2.0 mol/L")
    print()
    
    # True parameters (unknown in real experiment)
    k0_true = 1e8  # Pre-exponential factor (1/s)
    Ea_true = 75000  # Activation energy (J/mol)
    R = 8.314  # Gas constant (J/(mol·K))
    
    # Generate experimental data with noise
    np.random.seed(42)  # For reproducible results
    
    experimental_data = {}
    for T in temperatures:
        # True rate constant at this temperature
        k_true = k0_true * np.exp(-Ea_true / (R * T))
        
        # First-order kinetics: C = C0 * exp(-k*t)
        C0 = 2.0  # mol/L
        C_true = C0 * np.exp(-k_true * time_data)
        
        # Add experimental noise (±3% relative error)
        noise = np.random.normal(0, 0.03 * C_true)
        C_experimental = C_true + noise
        C_experimental = np.maximum(C_experimental, 0.01)  # Ensure positive
        
        experimental_data[T] = {
            'time': time_data,
            'concentration': C_experimental,
            'initial_conc': C0
        }
    
    print(f"Experimental Data Summary:")
    for T in temperatures:
        data = experimental_data[T]
        final_conc = data['concentration'][-1]
        conversion = (data['initial_conc'] - final_conc) / data['initial_conc'] * 100
        print(f"  T = {T-273.15:.0f}°C: Final conversion = {conversion:.1f}%")
    print()
    
    # ==============================================
    # STEP 2: MODEL DEFINITION
    # ==============================================
    print("2. Kinetic Model Definition")
    print("-" * 50)
    
    def arrhenius_model(T, k0, Ea):
        """Arrhenius equation for temperature dependence"""
        return k0 * np.exp(-Ea / (R * T))
    
    def first_order_kinetics(t, C0, k):
        """First-order reaction kinetics"""
        return C0 * np.exp(-k * t)
    
    def objective_function(params, experimental_data):
        """Objective function for parameter estimation"""
        k0, Ea = params
        
        sse = 0.0  # Sum of squared errors
        
        for T in temperatures:
            data = experimental_data[T]
            k_pred = arrhenius_model(T, k0, Ea)
            
            # Predicted concentrations
            C_pred = first_order_kinetics(data['time'], data['initial_conc'], k_pred)
            
            # Sum of squared errors
            sse += np.sum((data['concentration'] - C_pred)**2)
        
        return sse
    
    print(f"Kinetic Model:")
    print(f"  Rate equation: r = k·C_A")
    print(f"  Mass balance: dC_A/dt = -k·C_A")
    print(f"  Solution: C_A(t) = C_A0·exp(-k·t)")
    print(f"  Temperature dependence: k = k0·exp(-Ea/RT)")
    print()
    
    print(f"Parameters to estimate:")
    print(f"  k0 = Pre-exponential factor (1/s)")
    print(f"  Ea = Activation energy (J/mol)")
    print()
    
    # ==============================================
    # STEP 3: PARAMETER ESTIMATION
    # ==============================================
    print("3. Parameter Estimation")
    print("-" * 50)
    
    # Initial guess
    k0_guess = 1e6  # 1/s
    Ea_guess = 60000  # J/mol
    initial_guess = [k0_guess, Ea_guess]
    
    print(f"Initial Parameter Guess:")
    print(f"  k0_guess = {k0_guess:.2e} 1/s")
    print(f"  Ea_guess = {Ea_guess/1000:.0f} kJ/mol")
    print()
    
    # Optimization
    result = minimize(
        objective_function,
        initial_guess,
        args=(experimental_data,),
        method='Nelder-Mead',
        options={'maxiter': 10000}
    )
    
    k0_estimated, Ea_estimated = result.x
    
    print(f"Optimization Results:")
    print(f"  Convergence: {'✓' if result.success else '✗'}")
    print(f"  Function evaluations: {result.nfev}")
    print(f"  Final SSE: {result.fun:.6f}")
    print()
    
    print(f"Estimated Parameters:")
    print(f"  k0 = {k0_estimated:.2e} 1/s")
    print(f"  Ea = {Ea_estimated/1000:.1f} kJ/mol")
    print()
    
    # ==============================================
    # STEP 4: PARAMETER UNCERTAINTY
    # ==============================================
    print("4. Parameter Uncertainty Analysis")
    print("-" * 50)
    
    # Calculate confidence intervals using linear approximation
    n_data = sum(len(experimental_data[T]['concentration']) for T in temperatures)
    n_params = 2
    degrees_freedom = n_data - n_params
    
    # Estimate parameter covariance (simplified)
    # In practice, use more sophisticated methods
    delta = 1e-6
    
    # Numerical Hessian approximation
    def hessian_element(i, j, params):
        h = delta * abs(params[i]) if params[i] != 0 else delta
        h2 = delta * abs(params[j]) if params[j] != 0 else delta
        
        params_pp = params.copy()
        params_pp[i] += h
        params_pp[j] += h2
        
        params_pm = params.copy()
        params_pm[i] += h
        params_pm[j] -= h2
        
        params_mp = params.copy()
        params_mp[i] -= h
        params_mp[j] += h2
        
        params_mm = params.copy()
        params_mm[i] -= h
        params_mm[j] -= h2
        
        return (objective_function(params_pp, experimental_data) - 
                objective_function(params_pm, experimental_data) -
                objective_function(params_mp, experimental_data) + 
                objective_function(params_mm, experimental_data)) / (4 * h * h2)
    
    # Calculate Hessian matrix
    hessian = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            hessian[i, j] = hessian_element(i, j, result.x)
    
    # Parameter covariance matrix
    try:
        covariance = np.linalg.inv(hessian) * 2 * result.fun / degrees_freedom
        
        # Standard errors
        std_errors = np.sqrt(np.diag(covariance))
        
        # 95% confidence intervals
        t_value = t.ppf(0.975, degrees_freedom)
        
        k0_ci = t_value * std_errors[0]
        Ea_ci = t_value * std_errors[1]
        
        print(f"95% Confidence Intervals:")
        print(f"  k0 = {k0_estimated:.2e} ± {k0_ci:.2e} 1/s")
        print(f"  Ea = {Ea_estimated/1000:.1f} ± {Ea_ci/1000:.1f} kJ/mol")
        print()
        
        # Parameter correlation
        correlation = covariance / np.outer(std_errors, std_errors)
        print(f"Parameter Correlation:")
        print(f"  Corr(k0, Ea) = {correlation[0,1]:.3f}")
        
    except np.linalg.LinAlgError:
        print("  Warning: Could not calculate confidence intervals")
        print("  (Hessian matrix is singular)")
        k0_ci = np.nan
        Ea_ci = np.nan
    
    print()
    
    # ==============================================
    # STEP 5: MODEL VALIDATION
    # ==============================================
    print("5. Model Validation")
    print("-" * 50)
    
    # Calculate model predictions with estimated parameters
    predictions = {}
    residuals_all = []
    
    for T in temperatures:
        data = experimental_data[T]
        k_pred = arrhenius_model(T, k0_estimated, Ea_estimated)
        C_pred = first_order_kinetics(data['time'], data['initial_conc'], k_pred)
        
        predictions[T] = {
            'time': data['time'],
            'concentration': C_pred,
            'rate_constant': k_pred
        }
        
        # Calculate residuals
        residuals = data['concentration'] - C_pred
        residuals_all.extend(residuals)
    
    # Model statistics
    residuals_array = np.array(residuals_all)
    rmse = np.sqrt(np.mean(residuals_array**2))
    mae = np.mean(np.abs(residuals_array))
    r_squared = 1 - np.var(residuals_array) / np.var([data['concentration'] for T in temperatures for data in [experimental_data[T]]])
    
    print(f"Model Fit Statistics:")
    print(f"  RMSE = {rmse:.4f} mol/L")
    print(f"  MAE = {mae:.4f} mol/L")
    print(f"  R² = {r_squared:.4f}")
    print()
    
    print(f"Rate Constants at Different Temperatures:")
    for T in temperatures:
        k_pred = predictions[T]['rate_constant']
        print(f"  T = {T-273.15:.0f}°C: k = {k_pred:.2e} 1/s")
    print()
    
    # ==============================================
    # STEP 6: PHYSICAL INTERPRETATION
    # ==============================================
    print("6. Physical Interpretation")
    print("-" * 50)
    
    print(f"Parameter Comparison with True Values:")
    k0_error = abs(k0_estimated - k0_true) / k0_true * 100
    Ea_error = abs(Ea_estimated - Ea_true) / Ea_true * 100
    
    print(f"  Pre-exponential factor:")
    print(f"    True: {k0_true:.2e} 1/s")
    print(f"    Estimated: {k0_estimated:.2e} 1/s")
    print(f"    Error: {k0_error:.1f}%")
    print()
    
    print(f"  Activation energy:")
    print(f"    True: {Ea_true/1000:.1f} kJ/mol")
    print(f"    Estimated: {Ea_estimated/1000:.1f} kJ/mol")
    print(f"    Error: {Ea_error:.1f}%")
    print()
    
    # Temperature dependence analysis
    T_range = np.linspace(300, 370, 100)
    k_true_range = arrhenius_model(T_range, k0_true, Ea_true)
    k_estimated_range = arrhenius_model(T_range, k0_estimated, Ea_estimated)
    
    print(f"Rate Constant Temperature Sensitivity:")
    T_ref = 333.15  # K (60°C)
    k_ref_true = arrhenius_model(T_ref, k0_true, Ea_true)
    k_ref_est = arrhenius_model(T_ref, k0_estimated, Ea_estimated)
    
    # 10K temperature increase effect
    T_high = T_ref + 10
    k_high_true = arrhenius_model(T_high, k0_true, Ea_true)
    k_high_est = arrhenius_model(T_high, k0_estimated, Ea_estimated)
    
    factor_true = k_high_true / k_ref_true
    factor_est = k_high_est / k_ref_est
    
    print(f"  10K temperature increase (60→70°C):")
    print(f"    True rate increase factor: {factor_true:.2f}")
    print(f"    Estimated rate increase factor: {factor_est:.2f}")
    print()
    
    # ==============================================
    # STEP 7: ECONOMIC IMPLICATIONS
    # ==============================================
    print("7. Economic Implications")
    print("-" * 50)
    
    # Economic analysis based on improved kinetic understanding
    operating_temp = 343.15  # K (70°C)
    k_operating = arrhenius_model(operating_temp, k0_estimated, Ea_estimated)
    
    # Reactor sizing implications
    target_conversion = 0.95  # 95% conversion
    residence_time = -np.log(1 - target_conversion) / k_operating / 3600  # hours
    
    # Production rate calculation
    feed_rate = 1000  # mol/h
    reactor_volume = feed_rate * residence_time / 2.0  # L (assuming 2 mol/L)
    
    print(f"Process Design Implications:")
    print(f"  Operating Temperature: {operating_temp-273.15:.0f}°C")
    print(f"  Rate Constant: {k_operating:.2e} 1/s")
    print(f"  Required Residence Time: {residence_time:.2f} hours")
    print(f"  Reactor Volume: {reactor_volume:.0f} L")
    print()
    
    # Cost comparison
    reactor_cost_per_liter = 500  # $/L
    reactor_cost = reactor_volume * reactor_cost_per_liter
    
    # Alternative: higher temperature operation
    T_alt = operating_temp + 20  # K
    k_alt = arrhenius_model(T_alt, k0_estimated, Ea_estimated)
    residence_time_alt = -np.log(1 - target_conversion) / k_alt / 3600
    reactor_volume_alt = feed_rate * residence_time_alt / 2.0
    reactor_cost_alt = reactor_volume_alt * reactor_cost_per_liter
    
    heating_cost_increase = 10000  # $/year additional heating cost
    
    print(f"Alternative High-Temperature Operation:")
    print(f"  Temperature: {T_alt-273.15:.0f}°C")
    print(f"  Residence Time: {residence_time_alt:.2f} hours")
    print(f"  Reactor Volume: {reactor_volume_alt:.0f} L")
    print(f"  Capital Savings: ${reactor_cost - reactor_cost_alt:,.0f}")
    print(f"  Additional Heating Cost: ${heating_cost_increase:,.0f}/year")
    print()
    
    # Payback calculation
    if reactor_cost > reactor_cost_alt:
        payback_years = (reactor_cost - reactor_cost_alt) / heating_cost_increase
        print(f"  Payback Period: {payback_years:.1f} years")
    
    return {
        'parameters': {
            'k0_estimated': k0_estimated,
            'Ea_estimated': Ea_estimated,
            'k0_true': k0_true,
            'Ea_true': Ea_true
        },
        'statistics': {
            'rmse': rmse,
            'mae': mae,
            'r_squared': r_squared
        },
        'experimental_data': experimental_data,
        'predictions': predictions,
        'economics': {
            'reactor_volume': reactor_volume,
            'reactor_cost': reactor_cost,
            'operating_temp': operating_temp
        }
    }

if __name__ == "__main__":
    results = main()
    print("✓ Parameter estimation example completed successfully!")
    print(f"✓ Estimated activation energy: {results['parameters']['Ea_estimated']/1000:.1f} kJ/mol")
    print(f"✓ Model R²: {results['statistics']['r_squared']:.4f}")
    print(f"✓ Reactor volume: {results['economics']['reactor_volume']:.0f} L")
