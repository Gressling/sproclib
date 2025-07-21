#!/usr/bin/env python3
"""
Visualization tools for Process Optimization

This module provides comprehensive plotting and visualization capabilities
for process optimization problems in chemical engineering applications.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from typing import List, Tuple, Dict, Optional, Callable
import os

# Set matplotlib style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class ProcessOptimizationPlots:
    """
    Visualization class for process optimization results and analysis.
    
    Provides methods for creating professional-quality plots for:
    - Objective function landscapes
    - Optimization convergence
    - Pareto frontiers
    - Sensitivity analysis
    - Economic trade-offs
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
    
    def plot_objective_landscape_2d(self, 
                                   objective_func: Callable,
                                   x_range: Tuple[float, float],
                                   y_range: Tuple[float, float],
                                   x_label: str = "Variable 1",
                                   y_label: str = "Variable 2",
                                   title: str = "Objective Function Landscape",
                                   optimal_point: Optional[Tuple[float, float]] = None,
                                   n_points: int = 100) -> None:
        """
        Create 2D contour plot of objective function landscape.
        
        Parameters
        ----------
        objective_func : Callable
            Objective function to plot
        x_range : Tuple[float, float]
            Range for first variable (min, max)
        y_range : Tuple[float, float]
            Range for second variable (min, max)
        x_label : str
            Label for x-axis
        y_label : str
            Label for y-axis
        title : str
            Plot title
        optimal_point : Tuple[float, float], optional
            Coordinates of optimal point to highlight
        n_points : int
            Number of grid points per dimension
        """
        # Create grid
        x = np.linspace(x_range[0], x_range[1], n_points)
        y = np.linspace(y_range[0], y_range[1], n_points)
        X, Y = np.meshgrid(x, y)
        
        # Evaluate objective function
        Z = np.zeros_like(X)
        for i in range(n_points):
            for j in range(n_points):
                try:
                    Z[i, j] = objective_func([X[i, j], Y[i, j]])
                except:
                    Z[i, j] = np.inf
        
        # Replace inf values with large number for plotting
        Z[Z == np.inf] = np.nanmax(Z[Z != np.inf]) * 2
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Contour plot
        contour = ax.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
        contour_lines = ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.3, linewidths=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(contour, ax=ax)
        cbar.set_label('Objective Function Value', rotation=270, labelpad=20)
        
        # Highlight optimal point if provided
        if optimal_point:
            ax.plot(optimal_point[0], optimal_point[1], 'r*', markersize=15, 
                   label=f'Optimum: ({optimal_point[0]:.2f}, {optimal_point[1]:.2f})')
            ax.legend()
        
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'objective_landscape_2d.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_objective_landscape_3d(self,
                                   objective_func: Callable,
                                   x_range: Tuple[float, float],
                                   y_range: Tuple[float, float],
                                   x_label: str = "Variable 1",
                                   y_label: str = "Variable 2",
                                   z_label: str = "Objective Value",
                                   title: str = "3D Objective Function Surface",
                                   optimal_point: Optional[Tuple[float, float]] = None,
                                   n_points: int = 50) -> None:
        """Create 3D surface plot of objective function."""
        # Create grid
        x = np.linspace(x_range[0], x_range[1], n_points)
        y = np.linspace(y_range[0], y_range[1], n_points)
        X, Y = np.meshgrid(x, y)
        
        # Evaluate objective function
        Z = np.zeros_like(X)
        for i in range(n_points):
            for j in range(n_points):
                try:
                    Z[i, j] = objective_func([X[i, j], Y[i, j]])
                except:
                    Z[i, j] = np.inf
        
        # Replace inf values
        Z[Z == np.inf] = np.nanmax(Z[Z != np.inf]) * 2
        
        # Create 3D plot
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        # Surface plot
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8, 
                              linewidth=0, antialiased=True)
        
        # Add contour projections
        ax.contour(X, Y, Z, zdir='z', offset=np.min(Z), cmap='viridis', alpha=0.5)
        
        # Highlight optimal point
        if optimal_point:
            z_opt = objective_func(optimal_point)
            ax.scatter([optimal_point[0]], [optimal_point[1]], [z_opt], 
                      color='red', s=100, label='Optimum')
            ax.legend()
        
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.set_zlabel(z_label, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        # Add colorbar
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'objective_landscape_3d.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_convergence_history(self,
                               iteration_history: List[int],
                               objective_history: List[float],
                               title: str = "Optimization Convergence History") -> None:
        """
        Plot optimization convergence history.
        
        Parameters
        ----------
        iteration_history : List[int]
            List of iteration numbers
        objective_history : List[float]
            List of objective function values
        title : str
            Plot title
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Main convergence plot
        ax1.plot(iteration_history, objective_history, 'b-', linewidth=2, marker='o', markersize=4)
        ax1.set_xlabel('Iteration', fontsize=12)
        ax1.set_ylabel('Objective Function Value', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Log scale convergence (if values are positive)
        if all(val > 0 for val in objective_history):
            ax2.semilogy(iteration_history, objective_history, 'g-', linewidth=2, marker='s', markersize=4)
            ax2.set_xlabel('Iteration', fontsize=12)
            ax2.set_ylabel('Objective Function Value (log scale)', fontsize=12)
            ax2.set_title('Convergence History (Log Scale)', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3)
        else:
            # Show improvement per iteration
            improvements = [-abs(objective_history[i] - objective_history[i-1]) 
                          for i in range(1, len(objective_history))]
            ax2.bar(iteration_history[1:], improvements, alpha=0.7, color='orange')
            ax2.set_xlabel('Iteration', fontsize=12)
            ax2.set_ylabel('Objective Improvement', fontsize=12)
            ax2.set_title('Per-Iteration Improvement', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'convergence_history.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_pareto_frontier(self,
                           pareto_points: List[Tuple[float, float]],
                           all_points: Optional[List[Tuple[float, float]]] = None,
                           x_label: str = "Objective 1",
                           y_label: str = "Objective 2",
                           title: str = "Pareto Frontier") -> None:
        """
        Plot Pareto frontier for multi-objective optimization.
        
        Parameters
        ----------
        pareto_points : List[Tuple[float, float]]
            List of (obj1, obj2) values on Pareto frontier
        all_points : List[Tuple[float, float]], optional
            All evaluated points for context
        x_label : str
            Label for first objective
        y_label : str
            Label for second objective
        title : str
            Plot title
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot all points if provided
        if all_points:
            all_x, all_y = zip(*all_points)
            ax.scatter(all_x, all_y, c='lightblue', alpha=0.6, s=20, label='All Solutions')
        
        # Plot Pareto frontier
        pareto_x, pareto_y = zip(*pareto_points)
        ax.scatter(pareto_x, pareto_y, c='red', s=50, marker='o', 
                  label='Pareto Frontier', zorder=5)
        
        # Connect Pareto points
        sorted_indices = np.argsort(pareto_x)
        sorted_x = [pareto_x[i] for i in sorted_indices]
        sorted_y = [pareto_y[i] for i in sorted_indices]
        ax.plot(sorted_x, sorted_y, 'r--', alpha=0.7, linewidth=2)
        
        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'pareto_frontier.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_sensitivity_analysis(self,
                                variables: List[str],
                                sensitivity_values: List[float],
                                title: str = "Sensitivity Analysis") -> None:
        """
        Plot sensitivity analysis results.
        
        Parameters
        ----------
        variables : List[str]
            List of variable names
        sensitivity_values : List[float]
            Sensitivity values for each variable
        title : str
            Plot title
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create horizontal bar plot
        y_pos = np.arange(len(variables))
        colors = ['red' if val < 0 else 'green' for val in sensitivity_values]
        
        bars = ax.barh(y_pos, sensitivity_values, color=colors, alpha=0.7)
        
        # Customize plot
        ax.set_yticks(y_pos)
        ax.set_yticklabels(variables)
        ax.set_xlabel('Sensitivity (∂f/∂x)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, sensitivity_values)):
            ax.text(val + (0.01 * max(abs(v) for v in sensitivity_values) if val >= 0 else -0.01 * max(abs(v) for v in sensitivity_values)), 
                   i, f'{val:.3f}', va='center', fontsize=10)
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'sensitivity_analysis.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_economic_tradeoff(self,
                             design_variables: List[float],
                             capital_costs: List[float],
                             operating_costs: List[float],
                             total_costs: List[float],
                             x_label: str = "Design Variable",
                             title: str = "Economic Trade-off Analysis") -> None:
        """
        Plot economic trade-off between capital and operating costs.
        
        Parameters
        ----------
        design_variables : List[float]
            Values of the design variable
        capital_costs : List[float]
            Capital cost for each design
        operating_costs : List[float]
            Annual operating cost for each design
        total_costs : List[float]
            Total cost (NPV) for each design
        x_label : str
            Label for design variable
        title : str
            Plot title
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # Top plot: Cost components
        ax1.plot(design_variables, capital_costs, 'b-', linewidth=2, marker='o', 
                label='Capital Cost', markersize=6)
        ax1.plot(design_variables, operating_costs, 'r-', linewidth=2, marker='s', 
                label='Operating Cost (Annual)', markersize=6)
        ax1.plot(design_variables, total_costs, 'g-', linewidth=3, marker='^', 
                label='Total Cost (NPV)', markersize=8)
        
        # Find and mark minimum
        min_idx = np.argmin(total_costs)
        ax1.plot(design_variables[min_idx], total_costs[min_idx], 'k*', 
                markersize=15, label=f'Optimum: {design_variables[min_idx]:.2f}')
        
        ax1.set_xlabel(x_label, fontsize=12)
        ax1.set_ylabel('Cost ($)', fontsize=12)
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Bottom plot: Cost breakdown pie chart at optimum
        optimal_capital = capital_costs[min_idx]
        optimal_operating_annual = operating_costs[min_idx]
        optimal_operating_total = optimal_operating_annual * 10  # Assume 10-year period
        
        labels = ['Capital Cost', 'Operating Cost (10-year)']
        sizes = [optimal_capital, optimal_operating_total]
        colors = ['lightblue', 'lightcoral']
        explode = (0.05, 0)  # Slightly separate slices
        
        ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax2.set_title(f'Cost Breakdown at Optimum ({x_label} = {design_variables[min_idx]:.2f})', 
                     fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        
        if self.save_path:
            plt.savefig(os.path.join(self.save_path, 'economic_tradeoff.png'), 
                       dpi=300, bbox_inches='tight')
        plt.show()

def demonstrate_process_optimization_plots():
    """Demonstrate the plotting capabilities with example data."""
    
    print("Creating Process Optimization Visualization Examples...")
    print("=" * 60)
    
    # Create plotter instance
    plotter = ProcessOptimizationPlots()
    
    # Example 1: Reactor volume optimization landscape
    print("\n1. Creating objective function landscape for reactor optimization...")
    
    def reactor_cost_function(x):
        """Example reactor cost function."""
        volume, temp = x
        if volume <= 0 or temp <= 0:
            return 1e10
        
        # Capital cost scales with volume^0.6
        capital = 50000 * (volume ** 0.6)
        
        # Operating cost increases with temperature
        operating = volume * (temp - 300) * 100
        
        return capital + 10 * operating
    
    plotter.plot_objective_landscape_2d(
        reactor_cost_function,
        x_range=(1, 50),
        y_range=(300, 500),
        x_label="Reactor Volume (m³)",
        y_label="Temperature (K)",
        title="Reactor Design Optimization Landscape",
        optimal_point=(15.2, 350)
    )
    
    # Example 2: Convergence history
    print("\n2. Creating convergence history plot...")
    
    # Simulate convergence data
    iterations = list(range(1, 51))
    obj_values = [1000 * np.exp(-0.1 * i) + 100 + 10 * np.random.random() for i in iterations]
    
    plotter.plot_convergence_history(iterations, obj_values, 
                                    "Heat Exchanger Optimization Convergence")
    
    # Example 3: Pareto frontier
    print("\n3. Creating Pareto frontier plot...")
    
    # Generate example Pareto data
    np.random.seed(42)
    all_points = [(np.random.uniform(100, 1000), np.random.uniform(10, 100)) for _ in range(100)]
    pareto_points = [(150, 80), (200, 60), (300, 40), (500, 25), (800, 15)]
    
    plotter.plot_pareto_frontier(pareto_points, all_points,
                                "Cost ($1000)", "CO₂ Emissions (kg/h)",
                                "Cost vs Environmental Impact Trade-off")
    
    # Example 4: Sensitivity analysis
    print("\n4. Creating sensitivity analysis plot...")
    
    variables = ["Temperature", "Pressure", "Flow Rate", "Concentration", "Catalyst Loading"]
    sensitivities = [0.45, -0.23, 0.78, -0.56, 0.34]
    
    plotter.plot_sensitivity_analysis(variables, sensitivities,
                                     "Reactor Performance Sensitivity Analysis")
    
    # Example 5: Economic trade-off
    print("\n5. Creating economic trade-off plot...")
    
    # Heat exchanger area optimization example
    areas = np.linspace(50, 500, 20)
    capital_costs = [15000 + 600 * area for area in areas]
    operating_costs = [50000 / area for area in areas]  # Inversely related to area
    total_costs = [cap + 10 * op for cap, op in zip(capital_costs, operating_costs)]
    
    plotter.plot_economic_tradeoff(areas, capital_costs, operating_costs, total_costs,
                                  "Heat Exchanger Area (m²)",
                                  "Heat Exchanger Economic Optimization")
    
    print("\n" + "=" * 60)
    print("All visualization examples completed!")
    print("These plots demonstrate typical process optimization visualizations")
    print("for chemical engineering applications.")

if __name__ == "__main__":
    demonstrate_process_optimization_plots()
