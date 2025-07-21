# Economic Optimization Quick Start Guide

## Getting Started

This guide provides a practical introduction to using the EconomicOptimization class for chemical engineering economic analysis and optimization.

## Installation Requirements

```python
# Required packages
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

# From sproclib
from sproclib.optimization.economic_optimization import EconomicOptimization
```

## Basic Usage

### 1. Simple Production Planning

```python
from sproclib.optimization.economic_optimization import EconomicOptimization

# Create optimizer
optimizer = EconomicOptimization("Chemical Plant Production")

# Production data for 3 products
costs = np.array([150, 200, 180])      # $/unit production cost
prices = np.array([300, 400, 350])     # $/unit selling price
capacities = np.array([1000, 800, 600]) # units/day capacity

# Optimize production for maximum profit
result = optimizer.production_optimization(
    production_rates=np.zeros(3),  # Starting production
    costs=costs,
    prices=prices,
    capacity_constraints=capacities
)

print(f"Optimal production: {result['optimal_production']}")
print(f"Daily profit: ${result['total_profit']:,.0f}")
print(f"Profit margin: {result['profit_margin']:.1f}%")
```

### 2. Utility Cost Optimization

```python
# Define utility system
utility_costs = {
    'steam': 15.0,        # $/GJ
    'electricity': 0.08,  # $/kWh
    'cooling': 0.05       # $/m³
}

# 8-hour demand profile
utility_demands = {
    'steam': np.array([80, 85, 90, 95, 100, 95, 90, 85]),      # GJ/h
    'electricity': np.array([12, 13, 14, 15, 16, 15, 14, 13]),  # MWh/h
    'cooling': np.array([1500, 1600, 1700, 1800, 1900, 1800, 1700, 1600])  # m³/h
}

# System capacities
utility_capacities = {
    'steam': 120.0,     # GJ/h
    'electricity': 20.0, # MWh/h
    'cooling': 2500.0   # m³/h
}

# Optimize utility schedule
result = optimizer.utility_optimization(
    utility_costs=utility_costs,
    utility_demands=utility_demands,
    utility_capacities=utility_capacities,
    time_horizon=8
)

print(f"Total utility cost: ${result['total_cost']:,.0f}")
print(f"Annual savings potential: ${result['total_cost'] * 365 * 0.1:,.0f}")
```

### 3. Investment Portfolio Optimization

```python
# Define investment projects
projects = [
    {
        'name': 'Heat Recovery System',
        'initial_cost': 2_000_000,    # $2M
        'annual_return': 400_000      # $400k/year
    },
    {
        'name': 'Process Control Upgrade', 
        'initial_cost': 1_500_000,    # $1.5M
        'annual_return': 350_000      # $350k/year
    },
    {
        'name': 'Energy Efficiency Project',
        'initial_cost': 3_000_000,    # $3M
        'annual_return': 550_000      # $550k/year
    }
]

# Optimize investment portfolio
result = optimizer.investment_optimization(
    investment_options=projects,
    budget_constraint=5_000_000,  # $5M budget
    time_horizon=15,              # 15 years
    discount_rate=0.10            # 10% discount rate
)

print(f"Selected projects: {result['selected_options']}")
print(f"Total NPV: ${result['total_npv']:,.0f}")
print(f"ROI: {result['roi_percent']:.1f}%")
```

## Intermediate Examples

### Multi-Product Chemical Plant

```python
# Petrochemical complex with 5 products
products = ['Ethylene', 'Propylene', 'Benzene', 'Toluene', 'Xylene']

# Economic data ($/metric ton)
production_costs = np.array([850, 720, 980, 820, 900])
market_prices = np.array([1350, 1200, 1450, 1180, 1400])
daily_capacities = np.array([500, 400, 200, 300, 250])  # tons/day
contract_demands = np.array([200, 150, 80, 120, 100])   # minimum tons/day

# Calculate profit margins
profit_margins = ((market_prices - production_costs) / market_prices) * 100
print("Product profit margins:")
for product, margin in zip(products, profit_margins):
    print(f"{product}: {margin:.1f}%")

# Optimize production
result = optimizer.production_optimization(
    production_rates=np.zeros(5),
    costs=production_costs,
    prices=market_prices,
    capacity_constraints=daily_capacities,
    demand_constraints=contract_demands
)

if result['success']:
    print(f"\nOptimal Production Schedule:")
    for i, product in enumerate(products):
        production = result['optimal_production'][i]
        utilization = (production / daily_capacities[i]) * 100
        daily_profit = (market_prices[i] - production_costs[i]) * production
        print(f"{product:12}: {production:6.0f} tons/day ({utilization:5.1f}%) = ${daily_profit:8,.0f}/day")
    
    print(f"\nTotal daily profit: ${result['total_profit']:,.0f}")
    print(f"Annual profit: ${result['total_profit'] * 365:,.0f}")
```

### Integrated Steam System Optimization

```python
# Industrial steam system with multiple pressure levels
steam_system = {
    'costs': {
        'steam_600psig': 18.5,  # $/GJ (high pressure)
        'steam_150psig': 15.2,  # $/GJ (medium pressure)  
        'steam_50psig': 12.8    # $/GJ (low pressure)
    },
    'capacities': {
        'steam_600psig': 200.0,  # GJ/h
        'steam_150psig': 250.0,  # GJ/h
        'steam_50psig': 300.0    # GJ/h
    }
}

# 24-hour demand profiles
hours = np.arange(24)
base_600 = 120  # GJ/h
base_150 = 180  # GJ/h
base_50 = 150   # GJ/h

# Realistic demand variations
steam_demands = {
    'steam_600psig': base_600 * (1 + 0.2 * np.sin(2 * np.pi * hours / 24)),
    'steam_150psig': base_150 * (1 + 0.15 * np.sin(2 * np.pi * hours / 24 - np.pi/4)),
    'steam_50psig': base_50 * (1 + 0.3 * np.sin(2 * np.pi * hours / 24 - np.pi/2))
}

# Optimize steam system
result = optimizer.utility_optimization(
    utility_costs=steam_system['costs'],
    utility_demands=steam_demands,
    utility_capacities=steam_system['capacities'],
    time_horizon=24
)

if result['success']:
    print("Steam System Optimization Results:")
    print(f"Daily steam cost: ${result['total_cost']:,.0f}")
    
    # Analyze each steam level
    for steam_level in steam_system['costs'].keys():
        schedule = result['utility_schedules'][steam_level]
        demand = steam_demands[steam_level]
        
        avg_utilization = np.mean(schedule) / steam_system['capacities'][steam_level] * 100
        daily_cost = np.sum(schedule) * steam_system['costs'][steam_level]
        
        print(f"{steam_level:15}: {avg_utilization:5.1f}% avg utilization, ${daily_cost:6,.0f}/day")
```

## Advanced Features

### Economic Model Predictive Control

```python
# Economic MPC for reactor optimization
class ReactorModel:
    def __init__(self):
        self.n_inputs = 2  # Temperature, catalyst rate

def economic_objective(u, k):
    """Economic objective for reactor operation."""
    temp, catalyst_rate = u if len(u) >= 2 else (u[0], 2.0)
    
    # Production rate (Arrhenius kinetics)
    rate_constant = np.exp(-5000 / max(temp, 300))
    production_rate = rate_constant * catalyst_rate * 100  # kg/h
    
    # Economic calculations
    product_value = 2.5  # $/kg
    revenue = production_rate * product_value
    
    # Operating costs
    heating_cost = max(0, temp - 298) * 0.05  # $/h
    catalyst_cost = catalyst_rate * 12.0      # $/h
    
    return -(revenue - heating_cost - catalyst_cost)  # Minimize negative profit

# Process constraints
constraints = [
    {'type': 'ineq', 'fun': lambda u: 450 - u[0]},  # Max temperature
    {'type': 'ineq', 'fun': lambda u: u[0] - 350},   # Min temperature
    {'type': 'ineq', 'fun': lambda u: 5.0 - u[1]},   # Max catalyst rate
    {'type': 'ineq', 'fun': lambda u: u[1] - 0.5}    # Min catalyst rate
]

# Run economic MPC
result = optimizer.economic_mpc(
    process_model=ReactorModel(),
    economic_objective=economic_objective,
    constraints=constraints,
    prediction_horizon=6,
    control_horizon=3
)

if result['success']:
    temp_opt, catalyst_opt = result['first_control_action']
    profit_rate = -result['optimal_cost']
    
    print(f"Optimal reactor conditions:")
    print(f"Temperature: {temp_opt:.1f} K")
    print(f"Catalyst rate: {catalyst_opt:.2f} kg/h")
    print(f"Profit rate: ${profit_rate:.2f}/h")
    print(f"Daily profit: ${profit_rate * 24:,.0f}")
```

### Multi-Period Planning

```python
# Weekly production planning with price variations
weeks = 4
products = ['Product_A', 'Product_B', 'Product_C']

# Base economics
base_costs = np.array([100, 150, 120])
base_prices = np.array([200, 280, 220])
capacities = np.array([500, 400, 600])

# Price variations over weeks
price_factors = np.array([
    [1.0, 1.05, 0.95],   # Week 1
    [1.02, 1.08, 0.98],  # Week 2
    [0.98, 1.10, 1.02],  # Week 3
    [0.95, 1.12, 1.05]   # Week 4
])

total_profit = 0
weekly_schedules = []

print("Weekly Production Planning:")
print("Week  Product_A  Product_B  Product_C  Weekly_Profit")
print("-" * 50)

for week in range(weeks):
    weekly_prices = base_prices * price_factors[week]
    
    result = optimizer.production_optimization(
        production_rates=np.zeros(3),
        costs=base_costs,
        prices=weekly_prices,
        capacity_constraints=capacities
    )
    
    if result['success']:
        production = result['optimal_production']
        weekly_profit = result['total_profit'] * 7  # Convert to weekly
        total_profit += weekly_profit
        weekly_schedules.append(production)
        
        print(f"  {week+1}   {production[0]:8.0f}  {production[1]:8.0f}  {production[2]:8.0f}  ${weekly_profit:10,.0f}")

print(f"\nTotal monthly profit: ${total_profit:,.0f}")

# Analyze production variations
weekly_schedules = np.array(weekly_schedules)
for i, product in enumerate(products):
    variation = np.std(weekly_schedules[:, i])
    avg_production = np.mean(weekly_schedules[:, i])
    cv = (variation / avg_production) * 100 if avg_production > 0 else 0
    print(f"{product} coefficient of variation: {cv:.1f}%")
```

## Financial Analysis Integration

### NPV and ROI Calculations

```python
def calculate_project_npv(initial_cost, annual_returns, years, discount_rate):
    """Calculate Net Present Value of a project."""
    npv = -initial_cost
    for year in range(1, years + 1):
        npv += annual_returns / (1 + discount_rate) ** year
    return npv

def calculate_irr(initial_cost, annual_returns, years):
    """Estimate Internal Rate of Return."""
    # Simple approximation
    return (annual_returns / initial_cost) * 100

# Analyze multiple projects
projects = [
    ("Heat Recovery", 2_000_000, 400_000),
    ("Process Control", 1_500_000, 350_000),
    ("Energy Efficiency", 3_000_000, 550_000),
    ("Waste Reduction", 1_200_000, 280_000)
]

years = 15
discount_rate = 0.10

print("Project Financial Analysis:")
print("Project           Cost ($M)  Return ($K/yr)  NPV ($M)  IRR (%)  Payback (yr)")
print("-" * 80)

for name, cost, return_annual in projects:
    npv = calculate_project_npv(cost, return_annual, years, discount_rate)
    irr = calculate_irr(cost, return_annual, years)
    payback = cost / return_annual
    
    print(f"{name:15} {cost/1e6:8.1f}    {return_annual/1e3:8.0f}     {npv/1e6:6.2f}  {irr:6.1f}    {payback:6.1f}")
```

## Best Practices

### Data Validation

```python
def validate_production_data(costs, prices, capacities):
    """Validate production optimization inputs."""
    assert len(costs) == len(prices) == len(capacities), "Array lengths must match"
    assert np.all(costs > 0), "All costs must be positive"
    assert np.all(prices > 0), "All prices must be positive"
    assert np.all(capacities > 0), "All capacities must be positive"
    assert np.all(prices > costs), "Prices should exceed costs for profitability"

# Example usage
try:
    validate_production_data(costs, prices, capacities)
    print("✓ Production data validation passed")
except AssertionError as e:
    print(f"✗ Validation failed: {e}")
```

### Sensitivity Analysis

```python
def sensitivity_analysis(optimizer, base_params, param_name, variations):
    """Perform sensitivity analysis on optimization parameters."""
    results = []
    
    for variation in variations:
        params = base_params.copy()
        params[param_name] = base_params[param_name] * (1 + variation)
        
        result = optimizer.production_optimization(**params)
        if result['success']:
            results.append(result['total_profit'])
        else:
            results.append(0)
    
    return results

# Example: Price sensitivity
base_params = {
    'production_rates': np.zeros(3),
    'costs': np.array([150, 200, 180]),
    'prices': np.array([300, 400, 350]),
    'capacity_constraints': np.array([1000, 800, 600])
}

price_variations = [-0.2, -0.1, -0.05, 0, 0.05, 0.1, 0.2]
profit_results = sensitivity_analysis(optimizer, base_params, 'prices', price_variations)

print("Price Sensitivity Analysis:")
for var, profit in zip(price_variations, profit_results):
    print(f"Price change: {var*100:+5.0f}% → Profit: ${profit:,.0f}")
```

## Troubleshooting

### Common Issues and Solutions

```python
# Issue 1: Infeasible optimization
result = optimizer.production_optimization(...)
if not result['success']:
    print("Optimization failed. Check:")
    print("- Demand constraints vs. capacities")
    print("- Cost and price data validity")
    print("- Constraint compatibility")

# Issue 2: Unrealistic results
if result['success']:
    total_capacity = np.sum(capacity_constraints)
    total_production = np.sum(result['optimal_production'])
    
    if total_production > total_capacity * 1.01:  # 1% tolerance
        print("Warning: Production exceeds capacity")
    
    if result['total_profit'] < 0:
        print("Warning: Negative profit - check cost/price data")

# Issue 3: Performance monitoring
import time

start_time = time.time()
result = optimizer.production_optimization(...)
solve_time = time.time() - start_time

print(f"Optimization solved in {solve_time:.3f} seconds")
if solve_time > 10:
    print("Consider reducing problem size or using simpler constraints")
```

This quick start guide covers the essential features of EconomicOptimization. Start with simple examples and gradually build complexity as you become familiar with the optimization capabilities.
