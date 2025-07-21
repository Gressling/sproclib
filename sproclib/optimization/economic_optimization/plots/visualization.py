#!/usr/bin/env python3
"""
Visualization tools for Economic Optimization

This module provides comprehensive plotting and visualization capabilities
for economic optimization problems in chemical engineering applications.
Focus on production planning, utility optimization, investment analysis,
and economic performance metrics.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict, Optional
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# Set matplotlib style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class EconomicOptimizationPlots:
    """
    Visualization class for economic optimization results and analysis.
    
    Provides methods for creating professional-quality plots for:
    - Production planning results
    - Utility cost analysis
    - Investment portfolio visualization
    - Economic performance metrics
    - Sensitivity analysis
    """
    
    def __init__(self, save_path: str = None):
        """
        Initialize the plotting class.
        
        Parameters
        ----------
        save_path : str, optional
            Directory path to save plots. If None, plots are only displayed.
        """
        self.save_path = save_path
        if save_path and not os.path.exists(save_path):
            os.makedirs(save_path)
    
    def plot_production_optimization(self,
                                   products: List[str],
                                   optimal_production: np.ndarray,
                                   capacity_constraints: np.ndarray,
                                   demand_constraints: Optional[np.ndarray] = None,
                                   costs: Optional[np.ndarray] = None,
                                   prices: Optional[np.ndarray] = None,
                                   title: str = "Production Optimization Results") -> None:
        """
        Create comprehensive production optimization visualization.
        
        Parameters
        ----------
        products : List[str]
            Product names
        optimal_production : np.ndarray
            Optimal production rates
        capacity_constraints : np.ndarray
            Maximum production capacities
        demand_constraints : np.ndarray, optional
            Minimum demand requirements
        costs : np.ndarray, optional
            Production costs per unit
        prices : np.ndarray, optional
            Product prices per unit
        title : str
            Plot title
        """
        fig = plt.figure(figsize=(15, 10))
        
        # Create subplot layout
        gs = fig.add_gridspec(2, 2, height_ratios=[2, 1], width_ratios=[2, 1])
        
        # Main production chart
        ax1 = fig.add_subplot(gs[0, 0])
        
        x = np.arange(len(products))
        width = 0.35
        
        # Production bars
        bars1 = ax1.bar(x - width/2, optimal_production, width, 
                       label='Optimal Production', color='steelblue', alpha=0.8)
        bars2 = ax1.bar(x + width/2, capacity_constraints, width,
                       label='Capacity Limit', color='lightcoral', alpha=0.6)
        
        # Add demand constraints if provided
        if demand_constraints is not None:
            ax1.plot(x, demand_constraints, 'go--', linewidth=2, markersize=8,
                    label='Minimum Demand')
        
        # Add value labels on bars
        for i, (prod, cap) in enumerate(zip(optimal_production, capacity_constraints)):
            utilization = (prod / cap) * 100
            ax1.text(i - width/2, prod + cap*0.02, f'{prod:.0f}', 
                    ha='center', va='bottom', fontweight='bold')
            ax1.text(i + width/2, cap + cap*0.02, f'{cap:.0f}', 
                    ha='center', va='bottom', fontweight='bold')
            ax1.text(i, cap*0.5, f'{utilization:.1f}%', 
                    ha='center', va='center', fontsize=10, 
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax1.set_xlabel('Products', fontsize=12)
        ax1.set_ylabel('Production Rate (units/day)', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(products, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Capacity utilization chart
        ax2 = fig.add_subplot(gs[0, 1])
        
        utilization = (optimal_production / capacity_constraints) * 100
        colors = ['red' if u > 95 else 'orange' if u > 80 else 'green' for u in utilization]
        
        bars = ax2.barh(products, utilization, color=colors, alpha=0.7)
        ax2.set_xlabel('Capacity Utilization (%)', fontsize=12)
        ax2.set_title('Capacity Utilization', fontsize=12, fontweight='bold')
        ax2.axvline(x=80, color='orange', linestyle='--', alpha=0.7, label='80% Threshold')
        ax2.axvline(x=95, color='red', linestyle='--', alpha=0.7, label='95% Threshold')
        ax2.legend()
        
        # Add percentage labels
        for i, (bar, util) in enumerate(zip(bars, utilization)):
            ax2.text(util + 2, i, f'{util:.1f}%', va='center', fontsize=10)
        
        # Economic analysis (if cost and price data available)
        if costs is not None and prices is not None:
            ax3 = fig.add_subplot(gs[1, :])
            
            # Calculate economics
            revenues = optimal_production * prices
            production_costs = optimal_production * costs
            profits = revenues - production_costs
            profit_margins = (profits / revenues) * 100
            
            # Economic bar chart
            x_eco = np.arange(len(products))
            width_eco = 0.25
            
            bars_rev = ax3.bar(x_eco - width_eco, revenues, width_eco, 
                             label='Revenue', color='green', alpha=0.7)
            bars_cost = ax3.bar(x_eco, production_costs, width_eco,
                              label='Cost', color='red', alpha=0.7)
            bars_profit = ax3.bar(x_eco + width_eco, profits, width_eco,
                                 label='Profit', color='blue', alpha=0.7)
            
            ax3.set_xlabel('Products', fontsize=12)
            ax3.set_ylabel('Value ($/day)', fontsize=12)
            ax3.set_title('Economic Analysis', fontsize=12, fontweight='bold')
            ax3.set_xticks(x_eco)
            ax3.set_xticklabels(products, rotation=45, ha='right')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Add profit margin annotations
            for i, margin in enumerate(profit_margins):
                ax3.text(i + width_eco, profits[i] + max(profits)*0.02, 
                        f'{margin:.1f}%', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'production_optimization.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_utility_optimization(self,
                                utilities: List[str],
                                utility_schedules: Dict[str, np.ndarray],
                                utility_demands: Dict[str, np.ndarray],
                                utility_costs: Dict[str, float],
                                time_horizon: int = 24,
                                title: str = "Utility System Optimization") -> None:
        """
        Create utility optimization visualization showing schedules and costs.
        
        Parameters
        ----------
        utilities : List[str]
            Utility names
        utility_schedules : Dict[str, np.ndarray]
            Optimal utility schedules
        utility_demands : Dict[str, np.ndarray]
            Utility demand profiles
        utility_costs : Dict[str, float]
            Cost per unit for each utility
        time_horizon : int
            Time horizon in hours
        title : str
            Plot title
        """
        n_utilities = len(utilities)
        fig, axes = plt.subplots(n_utilities + 1, 1, figsize=(14, 3 * (n_utilities + 1)))
        
        if n_utilities == 1:
            axes = [axes]
        
        hours = np.arange(time_horizon)
        
        # Plot each utility
        for i, utility in enumerate(utilities):
            ax = axes[i]
            
            demand = utility_demands[utility]
            schedule = utility_schedules[utility]
            
            # Plot demand and supply
            ax.plot(hours, demand, 'r--', linewidth=2, label='Demand', marker='o', markersize=4)
            ax.plot(hours, schedule, 'b-', linewidth=2, label='Supply', marker='s', markersize=4)
            
            # Fill areas
            ax.fill_between(hours, 0, demand, alpha=0.3, color='red', label='Required')
            ax.fill_between(hours, demand, schedule, alpha=0.3, color='green', 
                          where=(schedule >= demand), label='Excess')
            
            ax.set_xlabel('Time (hours)' if i == n_utilities - 1 else '', fontsize=12)
            ax.set_ylabel(f'{utility}\n(units/h)', fontsize=11)
            ax.set_title(f'{utility} - Cost: ${utility_costs[utility]:.3f}/unit', 
                        fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add statistics
            total_demand = np.sum(demand)
            total_supply = np.sum(schedule)
            daily_cost = total_supply * utility_costs[utility]
            
            ax.text(0.02, 0.98, f'Daily Total: {total_supply:.0f} units\nCost: ${daily_cost:.0f}',
                   transform=ax.transAxes, va='top', ha='left',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Cost breakdown pie chart
        ax_pie = axes[-1]
        
        # Calculate daily costs for each utility
        daily_costs = []
        labels = []
        for utility in utilities:
            if utility in utility_schedules:
                total_usage = np.sum(utility_schedules[utility])
                daily_cost = total_usage * utility_costs[utility]
                daily_costs.append(daily_cost)
                labels.append(f'{utility}\n${daily_cost:.0f}')
        
        # Create pie chart
        colors = plt.cm.Set3(np.linspace(0, 1, len(daily_costs)))
        wedges, texts, autotexts = ax_pie.pie(daily_costs, labels=labels, autopct='%1.1f%%',
                                             colors=colors, startangle=90)
        
        ax_pie.set_title('Daily Utility Cost Breakdown', fontsize=12, fontweight='bold')
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_fontweight('bold')
            autotext.set_color('white')
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'utility_optimization.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_investment_portfolio(self,
                                investment_options: List[Dict],
                                selected_options: List[int],
                                budget_constraint: float,
                                total_npv: float,
                                title: str = "Investment Portfolio Optimization") -> None:
        """
        Create investment portfolio visualization.
        
        Parameters
        ----------
        investment_options : List[Dict]
            List of investment options with cost and return data
        selected_options : List[int]
            Indices of selected investment options
        budget_constraint : float
            Total available budget
        total_npv : float
            Total NPV of selected portfolio
        title : str
            Plot title
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Extract data
        project_names = [opt.get('name', f'Project {i}') for i, opt in enumerate(investment_options)]
        initial_costs = [opt['initial_cost'] for opt in investment_options]
        annual_returns = [opt['annual_return'] for opt in investment_options]
        
        # Calculate metrics
        payback_periods = [cost / return_rate for cost, return_rate in zip(initial_costs, annual_returns)]
        roi_rates = [(return_rate / cost) * 100 for cost, return_rate in zip(initial_costs, annual_returns)]
        
        # Colors for selected vs not selected
        colors = ['green' if i in selected_options else 'lightgray' for i in range(len(investment_options))]
        alphas = [0.8 if i in selected_options else 0.4 for i in range(len(investment_options))]
        
        # Plot 1: Cost vs Return scatter
        scatter = ax1.scatter(initial_costs, annual_returns, c=colors, s=100, alpha=0.7)
        
        # Add project labels
        for i, name in enumerate(project_names):
            if i in selected_options:
                ax1.annotate(name, (initial_costs[i], annual_returns[i]), 
                           xytext=(5, 5), textcoords='offset points', fontsize=9,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        ax1.set_xlabel('Initial Cost ($)', fontsize=12)
        ax1.set_ylabel('Annual Return ($)', fontsize=12)
        ax1.set_title('Investment Cost vs Annual Return', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Add diagonal ROI lines
        x_max = max(initial_costs)
        for roi in [10, 15, 20, 25]:
            y_line = np.array([0, x_max]) * (roi / 100)
            ax1.plot([0, x_max], y_line, '--', alpha=0.3, label=f'{roi}% ROI')
        ax1.legend()
        
        # Plot 2: ROI comparison
        bars = ax2.bar(range(len(project_names)), roi_rates, color=colors, alpha=alphas)
        ax2.set_xlabel('Projects', fontsize=12)
        ax2.set_ylabel('ROI (%)', fontsize=12)
        ax2.set_title('Return on Investment Comparison', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(len(project_names)))
        ax2.set_xticklabels([name[:15] + '...' if len(name) > 15 else name 
                           for name in project_names], rotation=45, ha='right')
        ax2.grid(True, alpha=0.3)
        
        # Add ROI values on bars
        for i, (bar, roi) in enumerate(zip(bars, roi_rates)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{roi:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # Plot 3: Budget allocation
        selected_costs = [initial_costs[i] for i in selected_options]
        selected_names = [project_names[i] for i in selected_options]
        
        if selected_costs:
            # Pie chart of selected investments
            wedges, texts, autotexts = ax3.pie(selected_costs, labels=selected_names, 
                                             autopct='%1.1f%%', startangle=90)
            ax3.set_title(f'Budget Allocation\nTotal: ${sum(selected_costs):,.0f}', 
                         fontsize=12, fontweight='bold')
            
            # Budget utilization bar
            used_budget = sum(selected_costs)
            remaining_budget = budget_constraint - used_budget
            
            ax3.text(0, -1.3, f'Budget Utilization: {used_budget/budget_constraint*100:.1f}%', 
                    ha='center', fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        else:
            ax3.text(0.5, 0.5, 'No Projects Selected', ha='center', va='center',
                    transform=ax3.transAxes, fontsize=14)
        
        # Plot 4: Financial summary
        ax4.axis('off')
        
        # Create financial summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Budget', f'${budget_constraint:,.0f}'],
            ['Invested Amount', f'${sum(selected_costs):,.0f}'],
            ['Remaining Budget', f'${budget_constraint - sum(selected_costs):,.0f}'],
            ['Total NPV', f'${total_npv:,.0f}'],
            ['Number of Projects', f'{len(selected_options)}'],
            ['Avg. Payback Period', f'{np.mean([payback_periods[i] for i in selected_options]):.1f} years' if selected_options else 'N/A'],
            ['Portfolio ROI', f'{np.mean([roi_rates[i] for i in selected_options]):.1f}%' if selected_options else 'N/A']
        ]
        
        # Create table
        table = ax4.table(cellText=summary_data[1:], colLabels=summary_data[0],
                         cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 2)
        
        # Style table
        for i in range(len(summary_data)):
            for j in range(2):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
        
        ax4.set_title('Investment Portfolio Summary', fontsize=12, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'investment_portfolio.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_economic_performance(self,
                                time_periods: List[str],
                                revenues: np.ndarray,
                                costs: np.ndarray,
                                profits: np.ndarray,
                                title: str = "Economic Performance Analysis") -> None:
        """
        Create economic performance visualization over time.
        
        Parameters
        ----------
        time_periods : List[str]
            Time period labels
        revenues : np.ndarray
            Revenue values for each period
        costs : np.ndarray
            Cost values for each period
        profits : np.ndarray
            Profit values for each period
        title : str
            Plot title
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        
        x = np.arange(len(time_periods))
        
        # Plot 1: Revenue, Cost, Profit trends
        ax1.plot(x, revenues, 'g-', linewidth=3, marker='o', markersize=6, label='Revenue')
        ax1.plot(x, costs, 'r-', linewidth=3, marker='s', markersize=6, label='Costs')
        ax1.plot(x, profits, 'b-', linewidth=3, marker='^', markersize=6, label='Profit')
        
        ax1.set_xlabel('Time Period', fontsize=12)
        ax1.set_ylabel('Value ($)', fontsize=12)
        ax1.set_title('Economic Trends', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(time_periods, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Fill areas
        ax1.fill_between(x, 0, revenues, alpha=0.3, color='green')
        ax1.fill_between(x, 0, costs, alpha=0.3, color='red')
        
        # Plot 2: Profit margins
        profit_margins = (profits / revenues) * 100
        bars = ax2.bar(x, profit_margins, color='blue', alpha=0.7)
        ax2.set_xlabel('Time Period', fontsize=12)
        ax2.set_ylabel('Profit Margin (%)', fontsize=12)
        ax2.set_title('Profit Margin Trends', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(time_periods, rotation=45, ha='right')
        ax2.grid(True, alpha=0.3)
        
        # Add margin values on bars
        for i, (bar, margin) in enumerate(zip(bars, profit_margins)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{margin:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # Plot 3: Cumulative profit
        cumulative_profit = np.cumsum(profits)
        ax3.plot(x, cumulative_profit, 'purple', linewidth=3, marker='D', markersize=6)
        ax3.fill_between(x, 0, cumulative_profit, alpha=0.3, color='purple')
        ax3.set_xlabel('Time Period', fontsize=12)
        ax3.set_ylabel('Cumulative Profit ($)', fontsize=12)
        ax3.set_title('Cumulative Profit', fontsize=12, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(time_periods, rotation=45, ha='right')
        ax3.grid(True, alpha=0.3)
        
        # Add final cumulative value
        ax3.text(x[-1], cumulative_profit[-1], f'${cumulative_profit[-1]:,.0f}',
                ha='right', va='bottom', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # Plot 4: Economic metrics summary
        ax4.axis('off')
        
        # Calculate summary statistics
        avg_revenue = np.mean(revenues)
        avg_cost = np.mean(costs)
        avg_profit = np.mean(profits)
        avg_margin = np.mean(profit_margins)
        total_profit = np.sum(profits)
        
        # Create metrics display
        metrics_text = f"""
        ECONOMIC PERFORMANCE SUMMARY
        
        Average Revenue:     ${avg_revenue:,.0f}
        Average Costs:       ${avg_cost:,.0f}
        Average Profit:      ${avg_profit:,.0f}
        Average Margin:      {avg_margin:.1f}%
        
        Total Profit:        ${total_profit:,.0f}
        Best Period:         {time_periods[np.argmax(profits)]}
        Worst Period:        {time_periods[np.argmin(profits)]}
        
        Growth Rate:         {((profits[-1]/profits[0])**(1/len(profits))-1)*100:.1f}%/period
        """
        
        ax4.text(0.1, 0.9, metrics_text, transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'economic_performance.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()

def demonstrate_economic_optimization_plots():
    """Demonstrate the economic optimization plotting capabilities."""
    
    print("Creating Economic Optimization Visualization Examples...")
    print("=" * 60)
    
    # Create plotter instance
    plotter = EconomicOptimizationPlots()
    
    # Example 1: Production optimization visualization
    print("\n1. Creating production optimization visualization...")
    
    products = ['Ethylene', 'Propylene', 'Benzene', 'Toluene', 'BTX Mix']
    optimal_production = np.array([950, 750, 480, 720, 380])
    capacity_constraints = np.array([1000, 800, 500, 800, 400])
    demand_constraints = np.array([600, 400, 200, 300, 150])
    costs = np.array([850, 720, 980, 820, 750])
    prices = np.array([1350, 1200, 1450, 1180, 1100])
    
    plotter.plot_production_optimization(
        products=products,
        optimal_production=optimal_production,
        capacity_constraints=capacity_constraints,
        demand_constraints=demand_constraints,
        costs=costs,
        prices=prices,
        title="Petrochemical Complex Production Optimization"
    )
    
    # Example 2: Utility optimization visualization
    print("\n2. Creating utility optimization visualization...")
    
    utilities = ['Steam HP', 'Steam LP', 'Electricity']
    time_horizon = 24
    hours = np.arange(time_horizon)
    
    # Generate realistic utility profiles
    steam_hp_demand = 120 + 20 * np.sin(2 * np.pi * hours / 24) + 5 * np.random.random(24)
    steam_lp_demand = 180 + 30 * np.sin(2 * np.pi * hours / 24 - np.pi/4) + 8 * np.random.random(24)
    electricity_demand = 15000 + 3000 * np.sin(2 * np.pi * hours / 24) + 500 * np.random.random(24)
    
    utility_demands = {
        'Steam HP': steam_hp_demand,
        'Steam LP': steam_lp_demand,
        'Electricity': electricity_demand
    }
    
    # Optimal schedules (slightly above demand)
    utility_schedules = {
        'Steam HP': steam_hp_demand + 5,
        'Steam LP': steam_lp_demand + 8,
        'Electricity': electricity_demand + 200
    }
    
    utility_costs = {
        'Steam HP': 18.5,     # $/GJ
        'Steam LP': 15.2,     # $/GJ
        'Electricity': 0.085  # $/kWh
    }
    
    plotter.plot_utility_optimization(
        utilities=utilities,
        utility_schedules=utility_schedules,
        utility_demands=utility_demands,
        utility_costs=utility_costs,
        time_horizon=time_horizon,
        title="Chemical Plant Utility System Optimization"
    )
    
    # Example 3: Investment portfolio visualization
    print("\n3. Creating investment portfolio visualization...")
    
    investment_options = [
        {'name': 'New Reactor', 'initial_cost': 85_000_000, 'annual_return': 12_500_000},
        {'name': 'Cogeneration', 'initial_cost': 35_000_000, 'annual_return': 6_200_000},
        {'name': 'Process Control', 'initial_cost': 8_500_000, 'annual_return': 2_100_000},
        {'name': 'Heat Integration', 'initial_cost': 22_000_000, 'annual_return': 4_800_000},
        {'name': 'Wastewater Treatment', 'initial_cost': 15_000_000, 'annual_return': 2_800_000},
        {'name': 'Catalyst Upgrade', 'initial_cost': 12_000_000, 'annual_return': 3_500_000}
    ]
    
    selected_options = [0, 2, 3, 5]  # Selected project indices
    budget_constraint = 120_000_000
    total_npv = 45_000_000
    
    plotter.plot_investment_portfolio(
        investment_options=investment_options,
        selected_options=selected_options,
        budget_constraint=budget_constraint,
        total_npv=total_npv,
        title="Chemical Plant Investment Portfolio Optimization"
    )
    
    # Example 4: Economic performance analysis
    print("\n4. Creating economic performance analysis...")
    
    time_periods = ['Q1', 'Q2', 'Q3', 'Q4', 'Q1+1', 'Q2+1', 'Q3+1', 'Q4+1']
    revenues = np.array([12.5, 13.2, 14.1, 13.8, 14.5, 15.2, 15.8, 16.1]) * 1e6
    costs = np.array([8.2, 8.5, 8.9, 8.7, 9.1, 9.3, 9.6, 9.8]) * 1e6
    profits = revenues - costs
    
    plotter.plot_economic_performance(
        time_periods=time_periods,
        revenues=revenues,
        costs=costs,
        profits=profits,
        title="Chemical Plant Economic Performance (2-Year Analysis)"
    )
    
    print("\n" + "=" * 60)
    print("All economic optimization visualizations completed!")
    print("These plots demonstrate comprehensive economic analysis")
    print("for chemical engineering applications.")

if __name__ == "__main__":
    demonstrate_economic_optimization_plots()
