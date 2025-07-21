# Parameter Estimation - Quick Start Guide

## Installation & Import

```python
# Import parameter estimation module
from sproclib.optimization.parameter_estimation import (
    ParameterEstimation, 
    BayesianParameterEstimation,
    MultiObjectiveEstimation
)
import numpy as np
import matplotlib.pyplot as plt
```

## 1. Basic Linear Regression (5 minutes)

### Simple Linear Model
```python
# Generate synthetic data
x = np.linspace(0, 10, 20)
y_true = 2.5 * x + 1.3
y_data = y_true + np.random.normal(0, 0.5, len(x))

# Define linear model
def linear_model(x, slope, intercept):
    return slope * x + intercept

# Estimate parameters
estimator = ParameterEstimation(
    model_function=linear_model,
    experimental_data=(x, y_data)
)

results = estimator.estimate_parameters(method='linear')

print(f"Slope: {results.parameters[0]:.3f} ± {results.uncertainties[0]:.3f}")
print(f"Intercept: {results.parameters[1]:.3f} ± {results.uncertainties[1]:.3f}")
print(f"R²: {results.r_squared:.4f}")
```

## 2. Arrhenius Parameter Estimation (10 minutes)

### Temperature-Dependent Kinetics
```python
# Experimental data: temperature vs rate constant
temperatures = np.array([300, 310, 320, 330, 340, 350])  # K
rate_constants = np.array([0.001, 0.002, 0.004, 0.008, 0.015, 0.028])  # 1/s

# Arrhenius model: k = k0 * exp(-Ea/(R*T))
def arrhenius_model(T, k0, Ea):
    R = 8.314  # J/(mol·K)
    return k0 * np.exp(-Ea / (R * T))

# Initial guess
initial_guess = [1e6, 50000]  # k0 [1/s], Ea [J/mol]

# Estimate parameters
estimator = ParameterEstimation(
    model_function=arrhenius_model,
    experimental_data=(temperatures, rate_constants),
    initial_guess=initial_guess
)

results = estimator.estimate_parameters(
    method='least_squares',
    confidence_level=0.95
)

print(f"Pre-exponential factor: {results.parameters[0]:.2e} ± {results.uncertainties[0]:.2e} 1/s")
print(f"Activation energy: {results.parameters[1]/1000:.1f} ± {results.uncertainties[1]/1000:.1f} kJ/mol")

# Plot results
T_plot = np.linspace(295, 355, 100)
k_plot = arrhenius_model(T_plot, *results.parameters)

plt.figure(figsize=(10, 6))
plt.semilogy(temperatures, rate_constants, 'ro', label='Experimental data')
plt.semilogy(T_plot, k_plot, 'b-', label='Fitted model')
plt.xlabel('Temperature (K)')
plt.ylabel('Rate constant (1/s)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.title('Arrhenius Parameter Estimation')
plt.show()
```

## 3. Heat Transfer Coefficient (15 minutes)

### Overall Heat Transfer Correlation
```python
# Pilot plant data
flow_rates = np.array([10, 15, 20, 25, 30, 35, 40])  # m³/h
heat_transfer_coefficients = np.array([250, 290, 320, 345, 365, 380, 395])  # W/(m²·K)

# Heat transfer correlation: U = a * Re^b
# Re = flow_rate * density / viscosity / area (simplified as flow_rate for demo)
def heat_transfer_correlation(flow_rate, a, b):
    return a * flow_rate**b

# Estimate parameters
estimator = ParameterEstimation(
    model_function=heat_transfer_correlation,
    experimental_data=(flow_rates, heat_transfer_coefficients),
    initial_guess=[100, 0.5]
)

results = estimator.estimate_parameters()

print(f"Coefficient a: {results.parameters[0]:.1f} ± {results.uncertainties[0]:.1f}")
print(f"Exponent b: {results.parameters[1]:.3f} ± {results.uncertainties[1]:.3f}")
print(f"R²: {results.r_squared:.4f}")

# Validation
flow_validation = np.array([12, 22, 32])
U_validation = np.array([275, 330, 370])
U_predicted = heat_transfer_correlation(flow_validation, *results.parameters)

print(f"\\nValidation RMSE: {np.sqrt(np.mean((U_validation - U_predicted)**2)):.1f} W/(m²·K)")
```

## 4. Multi-Parameter System (20 minutes)

### Reactor Performance Model
```python
# Reactor data: temperature, pressure, concentration -> conversion
data = {
    'temperature': np.array([350, 360, 370, 350, 360, 370, 350, 360, 370]),  # K
    'pressure': np.array([2, 2, 2, 3, 3, 3, 4, 4, 4]),  # bar
    'conversion': np.array([0.65, 0.72, 0.78, 0.70, 0.77, 0.83, 0.74, 0.81, 0.87])
}

# Complex kinetic model
def reactor_model(conditions, k0, Ea, pressure_order):
    T, P = conditions
    R = 8.314
    k = k0 * np.exp(-Ea / (R * T))
    return 1 - np.exp(-k * P**pressure_order * 100)  # Simplified conversion model

# Prepare data for estimation
conditions = np.column_stack([data['temperature'], data['pressure']])
conversions = data['conversion']

# Multi-parameter estimation
estimator = ParameterEstimation(
    model_function=reactor_model,
    experimental_data=(conditions, conversions),
    initial_guess=[1e8, 75000, 0.5]
)

results = estimator.estimate_parameters(
    bounds=[(1e5, 1e12), (50000, 150000), (0, 2)],
    confidence_level=0.95
)

print(f"Pre-exponential factor: {results.parameters[0]:.2e}")
print(f"Activation energy: {results.parameters[1]/1000:.1f} kJ/mol")
print(f"Pressure order: {results.parameters[2]:.3f}")
print(f"Model R²: {results.r_squared:.4f}")

# Parameter correlation matrix
correlation_matrix = results.parameter_correlation
print(f"\\nParameter correlations:")
print(f"k0-Ea: {correlation_matrix[0,1]:.3f}")
print(f"k0-n: {correlation_matrix[0,2]:.3f}")
print(f"Ea-n: {correlation_matrix[1,2]:.3f}")
```

## 5. Bayesian Estimation with Priors (25 minutes)

### Incorporating Prior Knowledge
```python
# Previous studies suggest activation energy around 80 kJ/mol
prior_knowledge = {
    'pre_exponential': ('lognormal', 1e8, 0.8),    # median, shape
    'activation_energy': ('normal', 80000, 10000), # mean, std
}

# Bayesian estimation
bayesian_estimator = BayesianParameterEstimation(
    model_function=arrhenius_model,
    experimental_data=(temperatures, rate_constants),
    prior_distributions=prior_knowledge
)

# Sample posterior distribution
posterior_samples = bayesian_estimator.sample_posterior(
    n_samples=5000,
    burn_in=1000,
    chains=4
)

# Analyze posterior
print("Bayesian Results:")
print(f"Ea posterior mean: {np.mean(posterior_samples['activation_energy'])/1000:.1f} kJ/mol")
print(f"Ea 95% credible interval: [{np.percentile(posterior_samples['activation_energy'], 2.5)/1000:.1f}, "
      f"{np.percentile(posterior_samples['activation_energy'], 97.5)/1000:.1f}] kJ/mol")

# Plot posterior distributions
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(posterior_samples['pre_exponential'], bins=50, alpha=0.7, density=True)
axes[0].set_xlabel('Pre-exponential factor (1/s)')
axes[0].set_ylabel('Posterior density')
axes[0].set_title('k₀ Posterior Distribution')

axes[1].hist(posterior_samples['activation_energy']/1000, bins=50, alpha=0.7, density=True)
axes[1].set_xlabel('Activation energy (kJ/mol)')
axes[1].set_ylabel('Posterior density')
axes[1].set_title('Ea Posterior Distribution')

plt.tight_layout()
plt.show()
```

## 6. Model Validation & Diagnostics (30 minutes)

### Comprehensive Model Assessment
```python
# Extended validation workflow
def comprehensive_validation(estimator, results):
    # 1. Residual analysis
    y_pred = estimator.predict(results.parameters)
    residuals = estimator.y_data - y_pred
    
    # 2. Normality test
    from scipy.stats import shapiro
    normality_p = shapiro(residuals).pvalue
    
    # 3. Autocorrelation check
    autocorr = np.corrcoef(residuals[:-1], residuals[1:])[0,1]
    
    # 4. Bootstrap confidence intervals
    bootstrap_params = []
    n_bootstrap = 1000
    
    for i in range(n_bootstrap):
        # Resample residuals
        bootstrap_residuals = np.random.choice(residuals, len(residuals))
        y_bootstrap = y_pred + bootstrap_residuals
        
        # Re-estimate parameters
        estimator_boot = ParameterEstimation(
            model_function=estimator.model_function,
            experimental_data=(estimator.x_data, y_bootstrap)
        )
        try:
            results_boot = estimator_boot.estimate_parameters(method='least_squares')
            bootstrap_params.append(results_boot.parameters)
        except:
            continue
    
    bootstrap_params = np.array(bootstrap_params)
    
    # Results summary
    print("=== Model Validation Summary ===")
    print(f"R²: {results.r_squared:.4f}")
    print(f"Adjusted R²: {results.adjusted_r_squared:.4f}")
    print(f"RMSE: {np.sqrt(np.mean(residuals**2)):.4f}")
    print(f"Residual normality p-value: {normality_p:.4f}")
    print(f"Residual autocorrelation: {autocorr:.4f}")
    
    print(f"\\nBootstrap parameter confidence intervals (95%):")
    for i, param in enumerate(['k0', 'Ea']):
        ci_low = np.percentile(bootstrap_params[:, i], 2.5)
        ci_high = np.percentile(bootstrap_params[:, i], 97.5)
        print(f"{param}: [{ci_low:.2e}, {ci_high:.2e}]")
    
    # Residual plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Residuals vs fitted
    axes[0,0].scatter(y_pred, residuals)
    axes[0,0].axhline(y=0, color='r', linestyle='--')
    axes[0,0].set_xlabel('Fitted values')
    axes[0,0].set_ylabel('Residuals')
    axes[0,0].set_title('Residuals vs Fitted')
    
    # Q-Q plot
    from scipy.stats import probplot
    probplot(residuals, dist="norm", plot=axes[0,1])
    axes[0,1].set_title('Q-Q Plot')
    
    # Residuals histogram
    axes[1,0].hist(residuals, bins=15, alpha=0.7, density=True)
    axes[1,0].set_xlabel('Residuals')
    axes[1,0].set_ylabel('Density')
    axes[1,0].set_title('Residual Distribution')
    
    # Bootstrap parameter distribution
    axes[1,1].scatter(bootstrap_params[:, 0], bootstrap_params[:, 1], alpha=0.5)
    axes[1,1].set_xlabel('k0')
    axes[1,1].set_ylabel('Ea')
    axes[1,1].set_title('Parameter Bootstrap Distribution')
    
    plt.tight_layout()
    plt.show()

# Apply validation
comprehensive_validation(estimator, results)
```

## 7. Economic Integration (35 minutes)

### Process Economics with Parameter Uncertainty
```python
def economic_analysis_with_uncertainty(kinetic_results):
    """Calculate economic impact of parameter uncertainty"""
    
    # Base case design
    def reactor_volume(k0, Ea, T_design=350):
        R = 8.314
        k = k0 * np.exp(-Ea / (R * T_design))
        # Simplified: V = F0 * X / k (CSTR design)
        F0 = 100  # mol/h feed rate
        X = 0.80   # target conversion
        return F0 * X / k  # L
    
    # Uncertainty propagation
    n_monte_carlo = 10000
    
    # Sample parameters from confidence intervals
    k0_samples = np.random.normal(
        kinetic_results.parameters[0], 
        kinetic_results.uncertainties[0], 
        n_monte_carlo
    )
    Ea_samples = np.random.normal(
        kinetic_results.parameters[1], 
        kinetic_results.uncertainties[1], 
        n_monte_carlo
    )
    
    # Calculate volume distribution
    volumes = []
    for k0_s, Ea_s in zip(k0_samples, Ea_samples):
        if k0_s > 0 and Ea_s > 0:  # Physical constraints
            vol = reactor_volume(k0_s, Ea_s)
            if vol > 0 and vol < 10000:  # Reasonable range
                volumes.append(vol)
    
    volumes = np.array(volumes)
    
    # Economic calculations
    reactor_cost_per_L = 1500  # $/L
    base_volume = reactor_volume(*kinetic_results.parameters)
    base_cost = base_volume * reactor_cost_per_L
    
    cost_distribution = volumes * reactor_cost_per_L
    
    # Risk assessment
    cost_95_percentile = np.percentile(cost_distribution, 95)
    cost_risk = cost_95_percentile - base_cost
    
    print("=== Economic Analysis ===")
    print(f"Base reactor volume: {base_volume:.0f} L")
    print(f"Base capital cost: ${base_cost:,.0f}")
    print(f"\\nUncertainty Analysis:")
    print(f"Volume 95% confidence interval: [{np.percentile(volumes, 2.5):.0f}, {np.percentile(volumes, 97.5):.0f}] L")
    print(f"Cost 95% confidence interval: [${np.percentile(cost_distribution, 2.5):,.0f}, ${np.percentile(cost_distribution, 97.5):,.0f}]")
    print(f"Cost risk (95th percentile): ${cost_risk:,.0f}")
    print(f"Relative cost uncertainty: ±{100*np.std(cost_distribution)/np.mean(cost_distribution):.1f}%")
    
    # Risk visualization
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(volumes, bins=50, alpha=0.7, density=True)
    plt.axvline(base_volume, color='r', linestyle='--', label='Base design')
    plt.axvline(np.percentile(volumes, 95), color='orange', linestyle='--', label='95th percentile')
    plt.xlabel('Reactor Volume (L)')
    plt.ylabel('Probability Density')
    plt.title('Volume Uncertainty Distribution')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.hist(cost_distribution/1000, bins=50, alpha=0.7, density=True)
    plt.axvline(base_cost/1000, color='r', linestyle='--', label='Base cost')
    plt.axvline(cost_95_percentile/1000, color='orange', linestyle='--', label='95th percentile')
    plt.xlabel('Capital Cost ($1000)')
    plt.ylabel('Probability Density')
    plt.title('Cost Risk Distribution')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return {
        'base_volume': base_volume,
        'volume_uncertainty': np.std(volumes),
        'base_cost': base_cost,
        'cost_risk': cost_risk
    }

# Apply economic analysis
economic_results = economic_analysis_with_uncertainty(results)
```

## Common Troubleshooting

### 1. Convergence Issues
```python
# Try different optimization algorithms
methods = ['least_squares', 'differential_evolution', 'basin_hopping']
for method in methods:
    try:
        results = estimator.estimate_parameters(method=method)
        print(f"{method}: Success, R² = {results.r_squared:.4f}")
        break
    except:
        print(f"{method}: Failed to converge")
```

### 2. Parameter Bounds
```python
# Add physical constraints
bounds = [
    (1e3, 1e12),   # k0: reasonable pre-exponential range
    (20000, 200000) # Ea: typical activation energy range
]
results = estimator.estimate_parameters(bounds=bounds)
```

### 3. Data Scaling
```python
# Scale parameters for better numerical conditioning
def scaled_arrhenius(T, log_k0, Ea_scaled):
    k0 = 10**log_k0
    Ea = Ea_scaled * 1000  # Scale to J/mol
    R = 8.314
    return k0 * np.exp(-Ea / (R * T))

# Use log(k0) and Ea/1000 as parameters
initial_guess_scaled = [8, 75]  # log10(k0), Ea in kJ/mol
```

## Next Steps

1. **Explore Advanced Methods**: Try Bayesian estimation for incorporating prior knowledge
2. **Model Selection**: Compare different model forms using information criteria
3. **Robust Estimation**: Handle outliers with robust regression methods
4. **Process Integration**: Connect with process optimization and economic analysis
5. **Industrial Application**: Apply to real plant data with proper validation

## Key Performance Tips

- Always plot data before fitting
- Check residuals for model adequacy
- Use cross-validation for model selection
- Consider parameter physical meaning
- Quantify and propagate uncertainty to design decisions
