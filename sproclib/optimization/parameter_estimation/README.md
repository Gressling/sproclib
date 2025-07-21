# Parameter Estimation

## Overview

The parameter estimation module provides comprehensive tools for identifying model parameters from experimental data in chemical process applications. This module supports linear and nonlinear regression, maximum likelihood estimation, and Bayesian inference methods specifically designed for chemical engineering applications.

## Key Features

### Estimation Methods
- **Linear Regression**: Least squares estimation for linear-in-parameters models
- **Nonlinear Optimization**: Robust algorithms for nonlinear parameter estimation
- **Maximum Likelihood**: Statistical estimation with uncertainty quantification
- **Bayesian Inference**: Prior knowledge incorporation and posterior distributions

### Statistical Analysis
- **Confidence Intervals**: Parameter uncertainty quantification
- **Correlation Analysis**: Parameter interdependence assessment
- **Model Validation**: Goodness-of-fit metrics and residual analysis
- **Sensitivity Analysis**: Parameter influence on model predictions

### Chemical Process Applications
- **Reaction Kinetics**: Arrhenius parameter estimation, rate constant determination
- **Heat Transfer**: Overall heat transfer coefficients, fouling factors
- **Mass Transfer**: Diffusivity, mass transfer coefficients
- **Thermodynamics**: Equilibrium constants, activity coefficients

## Core Classes

### ParameterEstimation
Main class for parameter estimation with multiple algorithms:

```python
from sproclib.optimization.parameter_estimation import ParameterEstimation

# Initialize estimator
estimator = ParameterEstimation(
    model_function=arrhenius_model,
    experimental_data=kinetic_data,
    initial_guess=[1e8, 75000]
)

# Perform estimation
results = estimator.estimate_parameters(
    method='least_squares',
    confidence_level=0.95
)

# Access results
parameters = results.parameters
confidence_intervals = results.confidence_intervals
statistics = results.fit_statistics
```

## Applications

### Reaction Kinetics
```python
# Arrhenius parameter estimation
def arrhenius_model(T, k0, Ea):
    R = 8.314  # J/(mol·K)
    return k0 * np.exp(-Ea / (R * T))

# Temperature-dependent rate data
temperatures = [313, 323, 333, 343, 353]  # K
rate_constants = [1e-3, 2e-3, 4e-3, 7e-3, 1.2e-2]  # 1/s

# Estimate pre-exponential factor and activation energy
estimator = ParameterEstimation(arrhenius_model, (temperatures, rate_constants))
results = estimator.fit()
```

### Heat Transfer
```python
# Overall heat transfer coefficient estimation
def heat_transfer_model(flow_rate, U, area):
    return U * area * flow_rate**0.8

# Pilot plant data
flow_rates = np.array([10, 20, 30, 40, 50])  # m³/h
heat_duties = np.array([150, 280, 400, 510, 620])  # kW

# Estimate U and area parameters
estimator = ParameterEstimation(heat_transfer_model, (flow_rates, heat_duties))
results = estimator.fit(bounds=[(100, 1000), (10, 100)])
```

### Mass Transfer
```python
# Diffusivity estimation from concentration profiles
def diffusion_model(time, position, D, boundary_conc):
    # Analytical solution for 1D diffusion
    return boundary_conc * erfc(position / (2 * np.sqrt(D * time)))

# Experimental concentration data
time_points = np.linspace(0, 3600, 25)  # seconds
positions = np.linspace(0, 0.1, 20)  # meters
concentration_data = measured_concentrations

# Estimate diffusivity
estimator = ParameterEstimation(diffusion_model, concentration_data)
results = estimator.fit()
```

## Data Requirements

### Experimental Data Format
```python
# Single response variable
data = {
    'independent_vars': np.array([[x1_1, x2_1], [x1_2, x2_2], ...]),
    'response_var': np.array([y1, y2, ...]),
    'weights': np.array([w1, w2, ...])  # Optional
}

# Multiple response variables
data = {
    'conditions': temperature_conditions,
    'responses': {
        'concentration': concentration_data,
        'temperature': temperature_data
    },
    'uncertainties': measurement_uncertainties
}
```

### Data Quality Requirements
- **Minimum Data Points**: At least 3 times the number of parameters
- **Experimental Range**: Cover expected operating conditions
- **Replication**: Multiple measurements for uncertainty assessment
- **Independence**: Avoid correlated measurement errors

## Validation Methods

### Statistical Validation
```python
# Model validation metrics
validation_results = estimator.validate_model(
    validation_data=independent_dataset,
    cross_validation=True,
    bootstrap_samples=1000
)

print(f"R²: {validation_results.r_squared:.4f}")
print(f"RMSE: {validation_results.rmse:.4f}")
print(f"AIC: {validation_results.aic:.2f}")
print(f"BIC: {validation_results.bic:.2f}")
```

### Physical Validation
```python
# Check parameter physical reasonableness
if results.parameters['activation_energy'] < 0:
    warnings.warn("Negative activation energy - check model formulation")

if results.parameters['pre_exponential'] < 1e6:
    warnings.warn("Unusually low pre-exponential factor")

# Temperature extrapolation limits
max_temp_extrapolation = 50  # K beyond experimental range
if operating_temp > max(experimental_temps) + max_temp_extrapolation:
    warnings.warn("Operating temperature beyond reliable extrapolation range")
```

## Economic Integration

### Process Design Impact
```python
# Calculate economic impact of parameter uncertainty
base_design = calculate_reactor_volume(parameters_mean)
uncertainty_impact = calculate_design_uncertainty(
    parameters=results.parameters,
    confidence_intervals=results.confidence_intervals
)

print(f"Reactor volume: {base_design['volume']:.0f} ± {uncertainty_impact['volume_uncertainty']:.0f} L")
print(f"Capital cost impact: ±${uncertainty_impact['cost_uncertainty']:,.0f}")
```

### Optimization Integration
```python
# Use estimated parameters in process optimization
from sproclib.optimization.process_optimization import ProcessOptimization

# Economic objective with parameter uncertainty
optimizer = ProcessOptimization(
    parameters=results.parameters,
    parameter_uncertainty=results.confidence_intervals,
    economic_model=profit_function
)

optimal_conditions = optimizer.optimize_robust(
    uncertainty_level=0.95,
    risk_tolerance=0.1
)
```

## Advanced Features

### Bayesian Estimation
```python
# Incorporate prior knowledge
prior_distributions = {
    'activation_energy': ('normal', 75000, 5000),  # Mean, std
    'pre_exponential': ('lognormal', 1e8, 0.5)    # Median, shape
}

bayesian_estimator = BayesianParameterEstimation(
    model=arrhenius_model,
    data=experimental_data,
    priors=prior_distributions
)

posterior_samples = bayesian_estimator.sample_posterior(n_samples=10000)
```

### Multi-objective Estimation
```python
# Simultaneous fitting of multiple datasets
multi_estimator = MultiObjectiveEstimation(
    models=[kinetic_model, thermodynamic_model],
    datasets=[kinetic_data, equilibrium_data],
    shared_parameters=['activation_energy']
)

results = multi_estimator.fit(
    weights=[0.7, 0.3],  # Relative importance
    constraint_functions=physical_constraints
)
```

## Performance Guidelines

### Computational Efficiency
- Use analytical gradients when available
- Initialize with physically reasonable parameter values
- Scale parameters to similar magnitudes
- Use parallel processing for large datasets

### Numerical Stability
- Check for parameter identifiability before estimation
- Use regularization for ill-conditioned problems
- Validate convergence with multiple initial guesses
- Monitor condition number of information matrix

## Industrial Examples

The module includes comprehensive examples for:
- **Pharmaceutical**: Drug dissolution kinetics, stability studies
- **Petrochemical**: Catalyst deactivation, reaction selectivity
- **Food Processing**: Heat treatment kinetics, mass transfer
- **Environmental**: Biodegradation rates, adsorption isotherms

## References

1. Bard, Y. (1974). *Nonlinear Parameter Estimation*. Academic Press.
2. Englezos, P. & Kalogerakis, N. (2001). *Applied Parameter Estimation for Chemical Engineers*. Marcel Dekker.
3. Rawlings, J.B. & Ekerdt, J.G. (2002). *Chemical Reactor Analysis and Design Fundamentals*. Nob Hill Publishing.
4. Himmelblau, D.M. & Riggs, J.B. (2012). *Basic Principles and Calculations in Chemical Engineering*, 8th Edition. Prentice Hall.

## See Also

- [Process Optimization](../process_optimization/README.md): Integration with optimization workflows
- [Economic Optimization](../economic_optimization/README.md): Economic objective functions
- [Unit Operations](../../unit/README.md): Process models for parameter estimation
