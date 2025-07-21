# Process Optimization Quick Start Guide

## Getting Started

This guide provides a practical introduction to using the ProcessOptimization class for chemical engineering applications.

## Installation Requirements

```python
# Required packages
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

# From sproclib
from sproclib.optimization.process_optimization import ProcessOptimization
```

## Basic Usage

### 1. Simple Reactor Volume Optimization

```python
from sproclib.optimization.process_optimization import ProcessOptimization

# Create optimizer
optimizer = ProcessOptimization("CSTR Volume Optimization")

# Define objective function
def reactor_cost(x):
    volume = x[0]  # m³
    
    # Capital cost (equipment scaling)
    capital = 50000 * (volume ** 0.6)
    
    # Operating cost (utilities)
    flow_rate = 0.5  # m³/s
    residence_time = volume / flow_rate
    conversion = 0.8 * (1 - np.exp(-0.1 * residence_time))
    
    if conversion < 0.75:  # Minimum conversion requirement
        return 1e10
    
    operating_annual = 10000 * volume
    
    return capital + 10 * operating_annual

# Set bounds
from scipy.optimize import Bounds
bounds = Bounds([1.0], [50.0])  # 1-50 m³

# Optimize
result = optimizer.optimize(reactor_cost, [10.0], bounds=bounds)

print(f"Optimal volume: {result['x'][0]:.2f} m³")
print(f"Minimum cost: ${result['fun']:,.0f}")
```

### 2. Heat Exchanger Design Optimization

```python
# Multi-variable optimization
def heat_exchanger_cost(x):
    area, tube_passes = x
    
    # Heat transfer calculations
    U = 800  # Overall heat transfer coefficient
    LMTD = 50  # Log mean temperature difference
    Q_required = 2e6  # Heat duty (W)
    Q_actual = U * area * LMTD
    
    if Q_actual < Q_required:
        return 1e10  # Insufficient heat transfer
    
    # Costs
    capital = 20000 + 600 * area + 3000 * tube_passes
    
    # Pressure drop penalty (increases with tube passes)
    pressure_drop_cost = 1000 * tube_passes * tube_passes
    
    return capital + 15 * pressure_drop_cost

# Bounds: area 50-1000 m², tube passes 1-4
bounds = Bounds([50, 1], [1000, 4])
initial_guess = [200, 2]

result = optimizer.optimize(heat_exchanger_cost, initial_guess, bounds=bounds)

optimal_area = result['x'][0]
optimal_passes = int(result['x'][1])
print(f"Optimal area: {optimal_area:.0f} m²")
print(f"Optimal tube passes: {optimal_passes}")
```

## Advanced Features

### Constraint Handling

```python
# Optimization with constraints
def distillation_cost(x):
    reflux_ratio, stages = x
    return reflux_ratio * 1000 + stages * 500

# Inequality constraints
def conversion_constraint(x):
    reflux_ratio, stages = x
    # Simplified conversion model
    conversion = 0.9 * (1 - np.exp(-0.1 * stages * reflux_ratio))
    return conversion - 0.85  # Must be >= 0.85

# Constraints list
constraints = [
    {'type': 'ineq', 'fun': conversion_constraint}
]

bounds = Bounds([1.2, 5], [5.0, 50])
result = optimizer.optimize(distillation_cost, [2.0, 20], 
                          bounds=bounds, constraints=constraints)
```

### Sensitivity Analysis

```python
# Perform sensitivity analysis
def sensitivity_analysis(optimizer, objective_func, base_point, variable_names):
    """Simple finite difference sensitivity analysis."""
    base_cost = objective_func(base_point)
    sensitivities = []
    
    for i, var_name in enumerate(variable_names):
        # Small perturbation
        delta = 0.01 * base_point[i]
        perturbed_point = base_point.copy()
        perturbed_point[i] += delta
        
        perturbed_cost = objective_func(perturbed_point)
        sensitivity = (perturbed_cost - base_cost) / delta
        sensitivities.append(sensitivity)
        
        print(f"{var_name}: {sensitivity:.3f}")
    
    return sensitivities

# Example usage
base_design = [200, 2]  # area, tube_passes
var_names = ["Area (m²)", "Tube Passes"]
sensitivities = sensitivity_analysis(optimizer, heat_exchanger_cost, 
                                   base_design, var_names)
```

## Economic Analysis Integration

### Life Cycle Cost Optimization

```python
def life_cycle_cost(x, project_years=15, discount_rate=0.08):
    """
    Calculate life cycle cost with time value of money.
    """
    equipment_size = x[0]
    
    # Capital cost (year 0)
    capital = 100000 * (equipment_size ** 0.6)
    
    # Annual operating costs
    operating_annual = 5000 * equipment_size
    
    # Calculate present value of operating costs
    pv_factor = (1 - (1 + discount_rate) ** (-project_years)) / discount_rate
    pv_operating = operating_annual * pv_factor
    
    return capital + pv_operating

# Optimize considering time value of money
bounds = Bounds([1.0], [100.0])
result = optimizer.optimize(life_cycle_cost, [10.0], bounds=bounds)

print(f"Economic optimal size: {result['x'][0]:.2f}")
```

### Multi-objective Optimization Setup

```python
# Trade-off between cost and environmental impact
def multi_objective_example(x):
    size = x[0]
    
    # Economic objective
    cost = 50000 * (size ** 0.6) + 1000 * size
    
    # Environmental objective (CO2 emissions)
    emissions = 100 * size + 500  # kg CO2/year
    
    return [cost, emissions]

# For Pareto optimization, you would use specialized algorithms
# or weighted sum approach:
def weighted_objective(x, w_cost=0.7, w_emissions=0.3):
    objectives = multi_objective_example(x)
    # Normalize and weight
    normalized_cost = objectives[0] / 100000
    normalized_emissions = objectives[1] / 10000
    
    return w_cost * normalized_cost + w_emissions * normalized_emissions
```

## Visualization and Analysis

### Plot Optimization Results

```python
import matplotlib.pyplot as plt

# Plot objective function landscape
def plot_objective_surface(objective_func, x_range, y_range):
    x = np.linspace(x_range[0], x_range[1], 50)
    y = np.linspace(y_range[0], y_range[1], 50)
    X, Y = np.meshgrid(x, y)
    
    Z = np.zeros_like(X)
    for i in range(len(x)):
        for j in range(len(y)):
            Z[j, i] = objective_func([X[j, i], Y[j, i]])
    
    plt.figure(figsize=(10, 8))
    contour = plt.contourf(X, Y, Z, levels=20, cmap='viridis')
    plt.colorbar(contour)
    plt.xlabel('Variable 1')
    plt.ylabel('Variable 2')
    plt.title('Objective Function Landscape')
    plt.show()

# Example usage
plot_objective_surface(heat_exchanger_cost, (50, 500), (1, 4))
```

## Best Practices

### 1. Problem Scaling
```python
# Scale variables to similar orders of magnitude
def scaled_objective(x_scaled):
    # Convert scaled variables back to physical units
    area = x_scaled[0] * 1000  # Scale factor 1000
    passes = x_scaled[1] * 4   # Scale factor 4
    
    return heat_exchanger_cost([area, passes]) / 100000  # Scale objective

# Use scaled bounds
scaled_bounds = Bounds([0.05, 0.25], [1.0, 1.0])  # [0.05*1000, 0.25*4] to [1.0*1000, 1.0*4]
```

### 2. Multiple Starting Points
```python
# Try multiple starting points to find global optimum
starting_points = [[100, 1], [300, 2], [500, 3], [700, 4]]
best_result = None
best_cost = float('inf')

for start_point in starting_points:
    result = optimizer.optimize(heat_exchanger_cost, start_point, bounds=bounds)
    if result['success'] and result['fun'] < best_cost:
        best_cost = result['fun']
        best_result = result

print(f"Best solution: {best_result['x']}")
```

### 3. Robust Design
```python
# Optimize considering uncertainty
def robust_objective(x, uncertainty_factor=0.1):
    # Nominal cost
    nominal_cost = heat_exchanger_cost(x)
    
    # Add penalty for sensitivity to uncertainty
    area, passes = x
    
    # Sample uncertain parameters
    U_variations = [800 * (1 + uncertainty_factor * np.random.normal()) for _ in range(10)]
    cost_variations = []
    
    for U_var in U_variations:
        # Recalculate with varied parameter
        varied_cost = nominal_cost * (800 / U_var)  # Simplified
        cost_variations.append(varied_cost)
    
    # Add robustness penalty (prefer low variance)
    robustness_penalty = np.std(cost_variations)
    
    return nominal_cost + 0.1 * robustness_penalty
```

## Common Problems and Solutions

### Convergence Issues
- **Problem**: Optimizer doesn't converge
- **Solutions**: 
  - Check bounds and constraints for feasibility
  - Try different starting points
  - Scale variables appropriately
  - Use gradient-free methods for noisy functions

### Poor Local Optima
- **Problem**: Different starting points give different results
- **Solutions**:
  - Use global optimization algorithms
  - Multiple random starting points
  - Physical understanding to guide search

### Constraint Violations
- **Problem**: Optimal solution violates physical constraints
- **Solutions**:
  - Add penalty terms to objective function
  - Use constraint optimization methods
  - Check constraint formulation

## Integration Examples

### With Process Simulation
```python
# Integrate with external simulation
def simulation_based_objective(x):
    # Set design variables in external simulator
    # (This would call your process simulation software)
    
    design_vars = {'reactor_volume': x[0], 'temperature': x[1]}
    
    # Simulate process (placeholder)
    # results = external_simulator.run(design_vars)
    
    # Extract economic metrics
    # return results.total_annual_cost
    
    # Simplified example
    return x[0] * 1000 + x[1] * 10
```

This quick start guide covers the essential features and best practices for using ProcessOptimization in chemical engineering applications. Start with simple examples and gradually add complexity as needed for your specific applications.
