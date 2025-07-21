# Economic Optimization for Chemical Engineering

## Overview

The `EconomicOptimization` class provides comprehensive economic optimization capabilities specifically designed for chemical engineering applications. It enables engineers to optimize production planning, utility systems, investment decisions, and implement economic model predictive control for maximum profitability and cost efficiency.

## Key Features

- **Linear Programming (LP)**: Efficient solution of large-scale linear optimization problems
- **Production Planning**: Multi-product manufacturing optimization with capacity and demand constraints
- **Utility Optimization**: Cost-effective scheduling of steam, electricity, and cooling systems
- **Investment Analysis**: Capital allocation optimization using NPV and ROI metrics
- **Economic MPC**: Real-time economic optimization for process control
- **Multi-objective**: Balance between cost, profit, and operational constraints

## Applications

### Production Planning and Scheduling
- Multi-product chemical plant optimization
- Resource allocation across product lines
- Capacity utilization optimization
- Demand fulfillment strategies
- Supply chain optimization

### Utility System Optimization
- Steam system cost minimization
- Electrical load management
- Cooling water optimization
- Compressed air system efficiency
- Cogeneration planning

### Investment Decision Making
- Capital project portfolio optimization
- Equipment replacement analysis
- Technology upgrade evaluations
- Expansion project prioritization
- Risk-adjusted return analysis

### Economic Model Predictive Control
- Real-time profit optimization
- Dynamic pricing response
- Energy cost minimization
- Production rate optimization
- Quality vs. cost trade-offs

## Technical Specifications

### Optimization Algorithms
- **Linear Programming**: HIGHS solver (default), Simplex method
- **Nonlinear Programming**: SLSQP, Interior Point methods
- **Integer Programming**: Branch and bound for discrete decisions
- **Economic MPC**: Receding horizon optimization

### Economic Models
- **Net Present Value (NPV)**: Time value of money calculations
- **Internal Rate of Return (IRR)**: Profitability assessment
- **Payback Period**: Investment recovery analysis
- **Life Cycle Cost (LCC)**: Total ownership cost evaluation
- **Operating Expense (OPEX)**: Variable cost optimization
- **Capital Expense (CAPEX)**: Fixed cost planning

### Financial Parameters
- **Discount Rate**: Cost of capital (typically 8-15% for chemical industry)
- **Time Horizon**: Project evaluation period (1-30 years)
- **Tax Considerations**: Depreciation and tax effects
- **Inflation Adjustment**: Real vs. nominal cash flows
- **Risk Assessment**: Uncertainty and sensitivity analysis

## Mathematical Foundation

### Linear Programming Formulation
```
minimize: c^T x
subject to: A_ub x ≤ b_ub    (inequality constraints)
           A_eq x = b_eq     (equality constraints)
           x_min ≤ x ≤ x_max (bounds)
```

Where:
- `x`: Decision variables (production rates, utility usage, investments)
- `c`: Cost coefficients (operating costs, prices, utility rates)
- `A_ub, b_ub`: Inequality constraints (capacity limits, demand requirements)
- `A_eq, b_eq`: Equality constraints (material balances, energy balances)

### Economic Objective Functions

#### Profit Maximization
```
maximize: Profit = Revenue - Operating_Cost - Fixed_Cost
        = Σ(price_i × production_i) - Σ(cost_i × production_i) - Fixed_Costs
```

#### Cost Minimization
```
minimize: Total_Cost = Operating_Cost + Utility_Cost + Labor_Cost
        = Σ(unit_cost_i × usage_i) + Σ(utility_rate_j × consumption_j) + Labor
```

#### NPV Maximization
```
maximize: NPV = Σ(Cash_Flow_t / (1 + r)^t) - Initial_Investment
```

## Usage Examples

### Basic Production Optimization
```python
from sproclib.optimization.economic_optimization import EconomicOptimization

# Create optimizer
optimizer = EconomicOptimization("Chemical Plant Production")

# Production data
costs = np.array([150, 200, 180])      # $/unit production cost
prices = np.array([300, 400, 350])     # $/unit selling price
capacities = np.array([1000, 800, 600]) # units/day capacity

# Optimize production
result = optimizer.production_optimization(
    production_rates=np.zeros(3),  # Initial production
    costs=costs,
    prices=prices,
    capacity_constraints=capacities
)

print(f"Optimal production: {result['optimal_production']}")
print(f"Daily profit: ${result['total_profit']:,.0f}")
```

### Utility System Optimization
```python
# Utility cost data
utility_costs = {
    'steam_hp': 15.0,    # $/GJ
    'electricity': 0.08,  # $/kWh
    'cooling': 0.05      # $/m³
}

# 24-hour demand profiles
utility_demands = {
    'steam_hp': np.array([80, 85, 90, ...]),     # GJ/h for 24 hours
    'electricity': np.array([12000, 13000, ...]), # kWh/h
    'cooling': np.array([1500, 1600, ...])       # m³/h
}

# Capacity limits
utility_capacities = {
    'steam_hp': 120.0,    # GJ/h
    'electricity': 18000.0, # kWh/h
    'cooling': 2000.0     # m³/h
}

# Optimize utility schedule
result = optimizer.utility_optimization(
    utility_costs=utility_costs,
    utility_demands=utility_demands,
    utility_capacities=utility_capacities,
    time_horizon=24
)

print(f"Daily utility cost: ${result['total_cost']:,.0f}")
```

### Investment Portfolio Optimization
```python
# Investment options
projects = [
    {'initial_cost': 2_000_000, 'annual_return': 400_000},  # Heat recovery
    {'initial_cost': 5_000_000, 'annual_return': 800_000},  # Process upgrade
    {'initial_cost': 1_500_000, 'annual_return': 350_000}   # Control system
]

# Optimize investment portfolio
result = optimizer.investment_optimization(
    investment_options=projects,
    budget_constraint=6_000_000,  # $6M budget
    time_horizon=15,              # 15 years
    discount_rate=0.10            # 10% discount rate
)

print(f"Selected projects: {result['selected_options']}")
print(f"Total NPV: ${result['total_npv']:,.0f}")
print(f"ROI: {result['roi_percent']:.1f}%")
```

### Economic Model Predictive Control
```python
# Process model
class ReactorModel:
    def __init__(self):
        self.n_inputs = 2  # Temperature, flow rate

# Economic objective function
def economic_objective(u, k):
    temp, flow = u
    # Production revenue
    production_rate = reaction_rate(temp, flow)
    revenue = production_rate * product_price
    
    # Operating costs
    heating_cost = heating_energy(temp) * energy_price
    raw_material_cost = flow * material_price
    
    return -(revenue - heating_cost - raw_material_cost)  # Minimize negative profit

# Constraints
constraints = [
    {'type': 'ineq', 'fun': lambda u: 450 - u[0]},  # Max temperature
    {'type': 'ineq', 'fun': lambda u: u[0] - 350},   # Min temperature
    {'type': 'ineq', 'fun': lambda u: 100 - u[1]},   # Max flow
    {'type': 'ineq', 'fun': lambda u: u[1] - 10}     # Min flow
]

# Economic MPC
result = optimizer.economic_mpc(
    process_model=ReactorModel(),
    economic_objective=economic_objective,
    constraints=constraints,
    prediction_horizon=8,
    control_horizon=4
)

optimal_action = result['first_control_action']
print(f"Optimal temperature: {optimal_action[0]:.1f} K")
print(f"Optimal flow rate: {optimal_action[1]:.1f} kg/h")
```

## Advanced Features

### Multi-Period Optimization
Handle time-varying prices and demands:
```python
# Weekly production planning with varying prices
for week in range(52):
    weekly_prices = base_prices * price_factors[week]
    weekly_demands = base_demands * demand_factors[week]
    
    result = optimizer.production_optimization(
        production_rates=current_production,
        costs=costs,
        prices=weekly_prices,
        capacity_constraints=capacities,
        demand_constraints=weekly_demands
    )
    
    weekly_schedule.append(result['optimal_production'])
```

### Stochastic Optimization
Incorporate uncertainty in prices and demands:
```python
# Monte Carlo approach for uncertain parameters
n_scenarios = 1000
scenario_results = []

for scenario in range(n_scenarios):
    # Sample uncertain parameters
    uncertain_prices = np.random.normal(base_prices, price_std)
    uncertain_demands = np.random.normal(base_demands, demand_std)
    
    result = optimizer.production_optimization(...)
    scenario_results.append(result)

# Analyze risk metrics
mean_profit = np.mean([r['total_profit'] for r in scenario_results])
profit_std = np.std([r['total_profit'] for r in scenario_results])
var_95 = np.percentile([r['total_profit'] for r in scenario_results], 5)
```

### Multi-objective Optimization
Balance competing objectives:
```python
def multi_objective_function(x, weights):
    """Weighted sum of profit and environmental impact."""
    profit = calculate_profit(x)
    emissions = calculate_emissions(x)
    
    # Normalize objectives
    norm_profit = profit / max_profit
    norm_emissions = emissions / max_emissions
    
    return -(weights[0] * norm_profit - weights[1] * norm_emissions)

# Pareto frontier analysis
pareto_points = []
for w_profit in np.linspace(0, 1, 11):
    w_emissions = 1 - w_profit
    weights = [w_profit, w_emissions]
    
    result = minimize(multi_objective_function, x0, args=(weights,))
    pareto_points.append((calculate_profit(result.x), calculate_emissions(result.x)))
```

## Integration with Other Systems

### ERP Integration
```python
# Connect with enterprise systems
from erp_connector import ProductionData, SalesData

# Get current production data
production_data = ProductionData.get_current_schedules()
sales_data = SalesData.get_price_forecasts()

# Update optimization parameters
result = optimizer.production_optimization(
    production_rates=production_data.current_rates,
    costs=production_data.unit_costs,
    prices=sales_data.forecasted_prices,
    capacity_constraints=production_data.capacities
)

# Send optimized schedule back to ERP
ProductionData.update_schedule(result['optimal_production'])
```

### Process Control Integration
```python
# Integration with DCS/SCADA systems
from process_interface import ControlSystem

control_system = ControlSystem("Plant_DCS")

# Get current process state
current_state = control_system.get_process_variables()

# Economic optimization
result = optimizer.economic_mpc(
    process_model=plant_model,
    economic_objective=profit_function,
    constraints=process_constraints,
    prediction_horizon=4
)

# Implement optimal control actions
control_system.set_setpoints(result['first_control_action'])
```

## Performance Benchmarks

### Problem Size Capabilities
- **Small problems** (< 100 variables): < 1 second
- **Medium problems** (100-1,000 variables): 1-10 seconds
- **Large problems** (1,000-10,000 variables): 10-60 seconds
- **Very large problems** (> 10,000 variables): 1-10 minutes

### Memory Requirements
- Linear scaling with problem size
- Typical: 1-10 MB for medium problems
- Large problems: 10-100 MB

### Accuracy
- Linear problems: Machine precision (1e-15)
- Nonlinear problems: User-specified tolerance (1e-6 typical)
- Economic calculations: Financial precision (1e-2)

## Industry Applications

### Petrochemical Complex
- Ethylene/propylene production optimization
- Aromatics (BTX) production planning
- Utility system integration
- Maintenance scheduling

### Pharmaceutical Manufacturing
- Multi-product batch scheduling
- Clean room utility optimization
- Equipment campaign planning
- Regulatory compliance optimization

### Specialty Chemicals
- Custom product scheduling
- Just-in-time production
- Quality-cost trade-offs
- Waste minimization

### Food and Beverage
- Seasonal demand planning
- Energy cost optimization
- Shelf-life considerations
- Supply chain coordination

## Best Practices

### Problem Formulation
1. **Clear Objectives**: Define economic goals explicitly
2. **Realistic Constraints**: Use engineering knowledge for bounds
3. **Data Quality**: Ensure accurate cost and price data
4. **Model Validation**: Verify optimization results make sense

### Implementation
1. **Incremental Deployment**: Start with simple problems
2. **Data Integration**: Connect to real-time plant data
3. **User Training**: Ensure operators understand economic drivers
4. **Continuous Improvement**: Regular model updates and calibration

### Maintenance
1. **Parameter Updates**: Keep costs and prices current
2. **Model Tuning**: Adjust based on actual performance
3. **Sensitivity Analysis**: Understand parameter impacts
4. **Backup Strategies**: Have fallback procedures

## Troubleshooting

### Common Issues
- **Infeasible Solutions**: Check constraint compatibility
- **Poor Performance**: Review problem scaling and bounds
- **Unrealistic Results**: Verify economic parameters
- **Slow Convergence**: Consider algorithm selection

### Diagnostic Tools
- Constraint analysis
- Sensitivity reporting
- Shadow price interpretation
- Dual variable analysis

## References

1. Williams, H.P. "Model Building in Mathematical Programming"
2. Edgar, T.F. "Optimization of Chemical Processes"
3. Biegler, L.T. "Nonlinear Programming: Concepts, Algorithms, and Applications"
4. Grossmann, I.E. "Enterprise-wide Optimization"

## See Also

- [Process Optimization](../process_optimization/README.md)
- [Parameter Estimation](../parameter_estimation/README.md)
- [Process Control](../../controller/README.md)
- [Process Simulation](../../simulation/README.md)
