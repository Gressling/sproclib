#!/usr/bin/env python3
"""
Industrial Economic Optimization Examples for Chemical Engineering

This example demonstrates comprehensive economic optimization for chemical
plant operations including production planning, utility cost optimization,
investment analysis, and economic model predictive control.

Realistic industrial scenarios with typical plant economics.
"""

import numpy as np
import matplotlib.pyplot as plt
from economic_optimization import EconomicOptimization

def main():
    print("=" * 70)
    print("ECONOMIC OPTIMIZATION - INDUSTRIAL CHEMICAL ENGINEERING EXAMPLES")
    print("=" * 70)
    
    # Create economic optimizer instance
    optimizer = EconomicOptimization("Petrochemical Complex Optimizer")
    
    print(f"\nOptimizer: {optimizer.name}")
    print(f"Capabilities: {len(optimizer.describe()['applications'])} application areas")
    
    # Example 1: Multi-Product Production Planning
    print("\n" + "="*50)
    print("EXAMPLE 1: MULTI-PRODUCT PRODUCTION PLANNING")
    print("="*50)
    
    # Petrochemical complex producing multiple products
    products = ['Ethylene', 'Propylene', 'Benzene', 'Toluene', 'BTX_Mix']
    n_products = len(products)
    
    # Production economics (realistic industrial data)
    production_costs = np.array([850, 720, 980, 820, 750])  # $/metric ton
    product_prices = np.array([1350, 1200, 1450, 1180, 1100])  # $/metric ton
    capacity_constraints = np.array([1200, 900, 600, 800, 400])  # metric tons/day
    demand_constraints = np.array([800, 500, 200, 300, 150])   # minimum contracts
    
    print("Production Planning Parameters:")
    print(f"Products: {products}")
    print(f"Production costs: {production_costs} $/ton")
    print(f"Market prices: {product_prices} $/ton")
    print(f"Plant capacities: {capacity_constraints} tons/day")
    print(f"Contract demands: {demand_constraints} tons/day")
    
    # Calculate profit margins
    profit_margins = ((product_prices - production_costs) / product_prices) * 100
    print(f"Profit margins: {profit_margins.round(1)} %")
    
    result = optimizer.production_optimization(
        production_rates=np.zeros(n_products),
        costs=production_costs,
        prices=product_prices,
        capacity_constraints=capacity_constraints,
        demand_constraints=demand_constraints
    )
    
    if result['success']:
        optimal_production = result['optimal_production']
        
        print(f"\nOptimal Production Schedule:")
        for i, product in enumerate(products):
            utilization = (optimal_production[i] / capacity_constraints[i]) * 100
            daily_profit = (product_prices[i] - production_costs[i]) * optimal_production[i]
            print(f"{product:12}: {optimal_production[i]:6.0f} tons/day ({utilization:5.1f}% capacity) - ${daily_profit:8,.0f}/day")
        
        print(f"\nEconomic Summary:")
        print(f"Total daily revenue: ${result['total_revenue']:,.0f}")
        print(f"Total daily costs:   ${result['total_cost']:,.0f}")
        print(f"Total daily profit:  ${result['total_profit']:,.0f}")
        print(f"Profit margin:       {result['profit_margin']:.1f}%")
        print(f"Annual profit:       ${result['total_profit'] * 365:,.0f}")
    
    # Example 2: Utility System Optimization
    print("\n" + "="*50)
    print("EXAMPLE 2: INTEGRATED UTILITY SYSTEM OPTIMIZATION")
    print("="*50)
    
    # Industrial utility system for chemical complex
    utility_costs = {
        'steam_600psig': 18.5,    # $/GJ (high pressure steam)
        'steam_150psig': 15.2,    # $/GJ (medium pressure steam)
        'steam_50psig': 12.8,     # $/GJ (low pressure steam)
        'electricity': 0.085,     # $/kWh
        'natural_gas': 8.5,       # $/GJ
        'cooling_water': 0.12,    # $/m³
        'chilled_water': 25.0,    # $/GJ (refrigeration)
        'compressed_air': 0.18    # $/m³ (standard conditions)
    }
    
    # 24-hour demand profiles (typical chemical plant operation)
    time_horizon = 24  # hours
    hours = np.arange(time_horizon)
    
    # Steam demands vary with production and ambient conditions
    base_steam_600 = 120  # GJ/h
    base_steam_150 = 180  # GJ/h
    base_steam_50 = 150   # GJ/h
    
    # Demand profiles with daily variations
    steam_600_demand = base_steam_600 * (1 + 0.2 * np.sin(2 * np.pi * hours / 24) + 0.1 * np.random.random(24))
    steam_150_demand = base_steam_150 * (1 + 0.15 * np.sin(2 * np.pi * hours / 24 - np.pi/4) + 0.1 * np.random.random(24))
    steam_50_demand = base_steam_50 * (1 + 0.3 * np.sin(2 * np.pi * hours / 24 - np.pi/2) + 0.1 * np.random.random(24))
    
    # Electricity demand follows production pattern
    electricity_demand = 15000 * (1 + 0.25 * np.sin(2 * np.pi * hours / 24) + 0.1 * np.random.random(24))  # kWh/h
    
    # Cooling demands higher during day (ambient temperature effect)
    cooling_water_demand = 2500 * (1 + 0.4 * np.sin(2 * np.pi * hours / 24 - np.pi/3) + 0.1 * np.random.random(24))  # m³/h
    
    utility_demands = {
        'steam_600psig': steam_600_demand,
        'steam_150psig': steam_150_demand,
        'steam_50psig': steam_50_demand,
        'electricity': electricity_demand,
        'cooling_water': cooling_water_demand
    }
    
    # Utility generation/supply capacities
    utility_capacities = {
        'steam_600psig': 200.0,   # GJ/h (boiler capacity)
        'steam_150psig': 250.0,   # GJ/h
        'steam_50psig': 300.0,    # GJ/h
        'electricity': 25000.0,   # kWh/h (grid + cogeneration)
        'cooling_water': 4000.0   # m³/h (cooling tower capacity)
    }
    
    print("Utility System Parameters:")
    for utility, cost in utility_costs.items():
        if utility in utility_demands:
            avg_demand = np.mean(utility_demands[utility])
            capacity = utility_capacities[utility]
            utilization = (avg_demand / capacity) * 100
            print(f"{utility:15}: ${cost:6.2f}/unit, Avg demand: {avg_demand:6.0f}, Capacity: {capacity:6.0f} ({utilization:5.1f}%)")
    
    result_utility = optimizer.utility_optimization(
        utility_costs={k: v for k, v in utility_costs.items() if k in utility_demands},
        utility_demands=utility_demands,
        utility_capacities=utility_capacities,
        time_horizon=time_horizon
    )
    
    if result_utility['success']:
        print(f"\nUtility Optimization Results:")
        print(f"Total daily utility cost: ${result_utility['total_cost']:,.0f}")
        print(f"Annual utility cost:      ${result_utility['total_cost'] * 365:,.0f}")
        
        schedules = result_utility['utility_schedules']
        
        # Calculate utilization statistics
        print(f"\nUtility Utilization Analysis:")
        for utility in utility_demands.keys():
            demand = utility_demands[utility]
            supply = schedules[utility]
            capacity = utility_capacities[utility]
            
            avg_utilization = np.mean(supply) / capacity * 100
            peak_utilization = np.max(supply) / capacity * 100
            excess_capacity = np.mean(supply - demand)
            
            print(f"{utility:15}: Avg {avg_utilization:5.1f}%, Peak {peak_utilization:5.1f}%, Excess {excess_capacity:6.0f} units/h")
    
    # Example 3: Capital Investment Optimization
    print("\n" + "="*50)
    print("EXAMPLE 3: CAPITAL INVESTMENT PORTFOLIO OPTIMIZATION")
    print("="*50)
    
    # Major capital projects for chemical plant expansion/modernization
    investment_options = [
        {
            'name': 'New Ethylene Cracker',
            'initial_cost': 85_000_000,    # $85M
            'annual_return': 12_500_000,   # $12.5M/year
            'description': 'Increase ethylene capacity by 400 kt/year'
        },
        {
            'name': 'Steam Turbine Cogeneration',
            'initial_cost': 35_000_000,    # $35M
            'annual_return': 6_200_000,    # $6.2M/year
            'description': 'Combined heat and power system'
        },
        {
            'name': 'Process Control Upgrade',
            'initial_cost': 8_500_000,     # $8.5M
            'annual_return': 2_100_000,    # $2.1M/year
            'description': 'Advanced process control and optimization'
        },
        {
            'name': 'Heat Integration Network',
            'initial_cost': 22_000_000,    # $22M
            'annual_return': 4_800_000,    # $4.8M/year
            'description': 'Energy recovery and heat exchanger network'
        },
        {
            'name': 'Wastewater Treatment Upgrade',
            'initial_cost': 15_000_000,    # $15M
            'annual_return': 2_800_000,    # $2.8M/year
            'description': 'Environmental compliance and water reuse'
        },
        {
            'name': 'Catalyst Technology Upgrade',
            'initial_cost': 12_000_000,    # $12M
            'annual_return': 3_500_000,    # $3.5M/year
            'description': 'Improved selectivity and yield'
        },
        {
            'name': 'Storage and Logistics',
            'initial_cost': 18_000_000,    # $18M
            'annual_return': 3_200_000,    # $3.2M/year
            'description': 'Additional storage and automated handling'
        }
    ]
    
    # Investment parameters
    budget_constraint = 120_000_000  # $120M available capital
    time_horizon = 20               # 20-year project evaluation
    discount_rate = 0.12            # 12% hurdle rate (typical for petrochemicals)
    
    print("Investment Options Analysis:")
    print("Project                     Cost ($M)  Return ($M/yr)  Payback (yr)  IRR (%)")
    print("-" * 80)
    
    for option in investment_options:
        cost_m = option['initial_cost'] / 1e6
        return_m = option['annual_return'] / 1e6
        payback = option['initial_cost'] / option['annual_return']
        
        # Simple IRR approximation
        irr_approx = (option['annual_return'] / option['initial_cost']) * 100
        
        print(f"{option['name']:25} {cost_m:8.1f}    {return_m:8.1f}      {payback:6.1f}     {irr_approx:6.1f}")
    
    print(f"\nBudget constraint: ${budget_constraint/1e6:.0f}M")
    print(f"Time horizon: {time_horizon} years")
    print(f"Discount rate: {discount_rate*100:.0f}%")
    
    result_investment = optimizer.investment_optimization(
        investment_options=investment_options,
        budget_constraint=budget_constraint,
        time_horizon=time_horizon,
        discount_rate=discount_rate
    )
    
    if result_investment['success']:
        selected_indices = result_investment['selected_options']
        
        print(f"\nOptimal Investment Portfolio:")
        print("Selected Projects:")
        print("-" * 50)
        
        total_cost = 0
        total_annual_return = 0
        
        for idx in selected_indices:
            project = investment_options[idx]
            cost_m = project['initial_cost'] / 1e6
            return_m = project['annual_return'] / 1e6
            
            print(f"✓ {project['name']:25} ${cost_m:6.1f}M → ${return_m:6.1f}M/year")
            print(f"  {project['description']}")
            
            total_cost += project['initial_cost']
            total_annual_return += project['annual_return']
        
        print(f"\nInvestment Summary:")
        print(f"Total investment:     ${result_investment['total_investment_cost']/1e6:6.1f}M")
        print(f"Budget utilization:   {result_investment['total_investment_cost']/budget_constraint*100:5.1f}%")
        print(f"Total NPV:           ${result_investment['total_npv']/1e6:6.1f}M")
        print(f"ROI:                 {result_investment['roi_percent']:5.1f}%")
        print(f"Total annual return: ${total_annual_return/1e6:6.1f}M/year")
        print(f"Simple payback:      {total_cost/total_annual_return:5.1f} years")
    
    # Example 4: Economic Model Predictive Control
    print("\n" + "="*50)
    print("EXAMPLE 4: ECONOMIC MODEL PREDICTIVE CONTROL")
    print("="*50)
    
    # Economic MPC for reactor temperature optimization
    class ReactorModel:
        """Simplified reactor model for economic MPC demonstration."""
        def __init__(self):
            self.n_inputs = 2  # Temperature setpoint, Catalyst feed rate
            self.current_state = [380.0, 2.5]  # [Temperature K, Catalyst kg/h]
    
    def reactor_economic_objective(u, k):
        """
        Economic objective for reactor optimization.
        Balances production rate, energy costs, and catalyst costs.
        """
        if hasattr(u, '__len__') and len(u) >= 2:
            temp_setpoint = u[0]
            catalyst_rate = u[1]
        else:
            temp_setpoint = u
            catalyst_rate = 2.5  # Default catalyst rate
        
        # Production rate (simplified Arrhenius-type relationship)
        # Higher temperature → higher reaction rate → more product
        activation_energy = 8000  # K (simplified)
        rate_constant = np.exp(-activation_energy / max(temp_setpoint, 300))
        production_rate = rate_constant * catalyst_rate * 1000  # kg/h
        
        # Revenue from production
        product_price = 2.5  # $/kg
        revenue = production_rate * product_price  # $/h
        
        # Energy cost (heating)
        ambient_temp = 298  # K
        heating_duty = max(0, temp_setpoint - ambient_temp) * 0.5  # kW (simplified)
        energy_cost = heating_duty * 0.08  # $/h (electricity cost)
        
        # Catalyst cost
        catalyst_price = 15.0  # $/kg
        catalyst_cost = catalyst_rate * catalyst_price  # $/h
        
        # Operating cost (maintenance, labor, etc.)
        operating_cost = 50.0  # $/h (fixed)
        
        # Total cost
        total_cost = energy_cost + catalyst_cost + operating_cost
        
        # Economic objective: maximize profit = minimize negative profit
        profit = revenue - total_cost
        
        return -profit  # Minimize negative profit
    
    reactor_model = ReactorModel()
    
    # Economic MPC constraints
    constraints = [
        {
            'type': 'ineq',
            'fun': lambda u: 450 - u[0]  # Temperature upper limit (K)
        },
        {
            'type': 'ineq',
            'fun': lambda u: u[0] - 350   # Temperature lower limit (K)
        },
        {
            'type': 'ineq',
            'fun': lambda u: 5.0 - u[1]   # Catalyst rate upper limit (kg/h)
        },
        {
            'type': 'ineq',
            'fun': lambda u: u[1] - 0.5   # Catalyst rate lower limit (kg/h)
        }
    ]
    
    print("Economic MPC for Reactor Optimization:")
    print("Variables: Temperature setpoint (K), Catalyst feed rate (kg/h)")
    print("Objective: Maximize profit (revenue - energy cost - catalyst cost - operating cost)")
    print("Constraints: 350-450 K, 0.5-5.0 kg/h catalyst")
    
    result_empc = optimizer.economic_mpc(
        process_model=reactor_model,
        economic_objective=reactor_economic_objective,
        constraints=constraints,
        prediction_horizon=8,  # 8-hour prediction
        control_horizon=4      # 4-hour control
    )
    
    if result_empc['success']:
        optimal_sequence = result_empc['optimal_control_sequence']
        first_action = result_empc['first_control_action']
        
        print(f"\nEconomic MPC Results:")
        print(f"Optimal first action:")
        print(f"  Temperature setpoint: {first_action[0]:.1f} K")
        print(f"  Catalyst feed rate:   {first_action[1]:.2f} kg/h")
        print(f"Economic cost:         ${-result_empc['optimal_cost']:.2f}/h profit")
        
        # Calculate economic metrics for the first action
        temp_opt = first_action[0]
        catalyst_opt = first_action[1]
        
        # Production rate
        rate_constant = np.exp(-8000 / temp_opt)
        production_rate = rate_constant * catalyst_opt * 1000
        
        # Costs and revenue
        revenue = production_rate * 2.5
        energy_cost = max(0, temp_opt - 298) * 0.5 * 0.08
        catalyst_cost = catalyst_opt * 15.0
        operating_cost = 50.0
        
        print(f"\nDetailed Economics:")
        print(f"Production rate:      {production_rate:.1f} kg/h")
        print(f"Revenue:             ${revenue:.2f}/h")
        print(f"Energy cost:         ${energy_cost:.2f}/h")
        print(f"Catalyst cost:       ${catalyst_cost:.2f}/h")
        print(f"Operating cost:      ${operating_cost:.2f}/h")
        print(f"Net profit:          ${revenue - energy_cost - catalyst_cost - operating_cost:.2f}/h")
    
    # Summary
    print("\n" + "="*70)
    print("ECONOMIC OPTIMIZATION SUMMARY")
    print("="*70)
    print("✓ Multi-product production planning optimized for maximum profit")
    print("✓ Integrated utility system optimized for minimum cost")
    print("✓ Capital investment portfolio optimized for maximum NPV")
    print("✓ Economic MPC for real-time profit optimization")
    print("\nKey Economic Benefits:")
    
    if result['success']:
        annual_production_profit = result['total_profit'] * 365
        print(f"• Production optimization: ${annual_production_profit:,.0f}/year")
    
    if result_utility['success']:
        annual_utility_savings = result_utility['total_cost'] * 365 * 0.15  # Assume 15% savings
        print(f"• Utility optimization savings: ${annual_utility_savings:,.0f}/year")
    
    if result_investment['success']:
        print(f"• Investment portfolio NPV: ${result_investment['total_npv']:,.0f}")
    
    if result_empc['success']:
        daily_empc_profit = -result_empc['optimal_cost'] * 24
        annual_empc_profit = daily_empc_profit * 365
        print(f"• Economic MPC profit: ${annual_empc_profit:,.0f}/year")

if __name__ == "__main__":
    main()
