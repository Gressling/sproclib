#!/usr/bin/env python3
"""
Comprehensive Test Suite for Economic Optimization

This test suite covers all economic optimization capabilities with realistic
industrial examples including production planning, utility optimization,
investment analysis, and economic model predictive control.

Chemical engineering focus with typical plant-scale operations.
"""

import pytest
import numpy as np
import numpy.testing as npt
from economic_optimization import EconomicOptimization


class TestEconomicOptimization:
    """Comprehensive test suite for economic optimization functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.optimizer = EconomicOptimization("Test Economic Optimizer")
        
        # Typical chemical plant data
        self.production_costs = np.array([150, 200, 180])  # $/unit (A, B, C products)
        self.product_prices = np.array([300, 400, 350])   # $/unit
        self.capacity_constraints = np.array([1000, 800, 600])  # units/day
        
        # Utility data for chemical plant
        self.utility_costs = {
            'steam_hp': 15.0,      # $/GJ (high pressure steam)
            'steam_lp': 12.0,      # $/GJ (low pressure steam)  
            'electricity': 0.08,   # $/kWh
            'cooling_water': 0.05, # $/m³
            'compressed_air': 0.15 # $/m³ (standard)
        }
        
    def test_class_initialization(self):
        """Test proper initialization of EconomicOptimization class."""
        optimizer = EconomicOptimization("Petrochemical Plant Optimizer")
        assert optimizer.name == "Petrochemical Plant Optimizer"
        assert isinstance(optimizer.results, dict)
        
        # Test describe method
        description = optimizer.describe()
        assert description['class'] == 'EconomicOptimization'
        assert 'Linear Programming (LP)' in description['algorithms']
        assert 'Production planning and scheduling' in description['applications']
        assert 'cost_minimization' in description['optimization_types']
    
    def test_linear_programming_basic(self):
        """Test basic linear programming functionality."""
        # Simple LP problem: minimize 2x1 + 3x2
        # subject to: x1 + x2 <= 4, 2x1 + x2 <= 6, x1,x2 >= 0
        
        c = np.array([2, 3])  # Objective coefficients
        A_ub = np.array([[1, 1], [2, 1]])  # Inequality constraint matrix
        b_ub = np.array([4, 6])  # Inequality constraint bounds
        bounds = [(0, None), (0, None)]  # Variable bounds
        
        result = self.optimizer.linear_programming(c, A_ub, b_ub, bounds=bounds)
        
        assert result['success'] is True
        assert result['problem_type'] == 'linear_programming'
        npt.assert_allclose(result['x'], [2.0, 2.0], rtol=1e-6)
        npt.assert_allclose(result['fun'], 10.0, rtol=1e-6)
    
    def test_production_optimization_basic(self):
        """Test production planning optimization for chemical plant."""
        # Chemical plant producing three products: A, B, C
        production_rates = np.array([500, 400, 300])  # Current production
        
        result = self.optimizer.production_optimization(
            production_rates=production_rates,
            costs=self.production_costs,
            prices=self.product_prices,
            capacity_constraints=self.capacity_constraints
        )
        
        assert result['success'] is True
        assert 'optimal_production' in result
        assert 'total_profit' in result
        assert 'profit_margin' in result
        
        # Should maximize production given capacity constraints
        optimal_production = result['optimal_production']
        assert np.all(optimal_production <= self.capacity_constraints)
        assert result['total_profit'] > 0
        
        # Verify profit calculation
        expected_revenue = np.dot(self.product_prices, optimal_production)
        expected_cost = np.dot(self.production_costs, optimal_production)
        expected_profit = expected_revenue - expected_cost
        npt.assert_allclose(result['total_profit'], expected_profit, rtol=1e-6)
    
    def test_production_optimization_with_demand(self):
        """Test production optimization with minimum demand constraints."""
        production_rates = np.array([500, 400, 300])
        demand_constraints = np.array([300, 200, 150])  # Minimum production required
        
        result = self.optimizer.production_optimization(
            production_rates=production_rates,
            costs=self.production_costs,
            prices=self.product_prices,
            capacity_constraints=self.capacity_constraints,
            demand_constraints=demand_constraints
        )
        
        assert result['success'] is True
        optimal_production = result['optimal_production']
        
        # All demand constraints should be satisfied
        assert np.all(optimal_production >= demand_constraints)
        assert np.all(optimal_production <= self.capacity_constraints)
    
    def test_utility_optimization_steam_system(self):
        """Test utility optimization for industrial steam system."""
        # 24-hour operation with varying steam demands
        time_horizon = 24  # hours
        
        # Steam demand profile (typical chemical plant)
        steam_hp_demand = np.array([
            80, 75, 70, 65, 70, 85, 95, 100,  # Night to morning ramp-up
            110, 115, 120, 118, 115, 120, 125, 120,  # Day shift peak
            115, 110, 105, 100, 95, 90, 85, 82  # Evening ramp-down
        ])  # GJ/h
        
        steam_lp_demand = np.array([
            60, 55, 50, 45, 50, 65, 75, 80,
            90, 95, 100, 98, 95, 100, 105, 100,
            95, 90, 85, 80, 75, 70, 65, 62
        ])  # GJ/h
        
        utility_demands = {
            'steam_hp': steam_hp_demand,
            'steam_lp': steam_lp_demand
        }
        
        utility_capacities = {
            'steam_hp': 150.0,  # GJ/h maximum capacity
            'steam_lp': 120.0   # GJ/h maximum capacity
        }
        
        utility_costs_subset = {
            'steam_hp': self.utility_costs['steam_hp'],
            'steam_lp': self.utility_costs['steam_lp']
        }
        
        result = self.optimizer.utility_optimization(
            utility_costs=utility_costs_subset,
            utility_demands=utility_demands,
            utility_capacities=utility_capacities,
            time_horizon=time_horizon
        )
        
        assert result['success'] is True
        assert 'utility_schedules' in result
        assert 'total_cost' in result
        
        schedules = result['utility_schedules']
        assert 'steam_hp' in schedules
        assert 'steam_lp' in schedules
        
        # Verify demand satisfaction
        assert np.all(schedules['steam_hp'] >= steam_hp_demand)
        assert np.all(schedules['steam_lp'] >= steam_lp_demand)
        
        # Verify capacity constraints
        assert np.all(schedules['steam_hp'] <= utility_capacities['steam_hp'])
        assert np.all(schedules['steam_lp'] <= utility_capacities['steam_lp'])
    
    def test_investment_optimization_plant_expansion(self):
        """Test investment optimization for plant expansion projects."""
        # Chemical plant expansion options
        investment_options = [
            {
                'name': 'Reactor Upgrade',
                'initial_cost': 2_000_000,  # $2M
                'annual_return': 400_000    # $400k/year
            },
            {
                'name': 'Heat Recovery System',
                'initial_cost': 1_500_000,  # $1.5M
                'annual_return': 350_000    # $350k/year
            },
            {
                'name': 'Distillation Column Revamp',
                'initial_cost': 3_000_000,  # $3M
                'annual_return': 550_000    # $550k/year
            },
            {
                'name': 'Process Control Upgrade',
                'initial_cost': 800_000,    # $800k
                'annual_return': 200_000    # $200k/year
            },
            {
                'name': 'Utility System Optimization',
                'initial_cost': 1_200_000,  # $1.2M
                'annual_return': 280_000    # $280k/year
            }
        ]
        
        budget_constraint = 5_000_000  # $5M available budget
        time_horizon = 15  # 15-year project life
        discount_rate = 0.08  # 8% discount rate
        
        result = self.optimizer.investment_optimization(
            investment_options=investment_options,
            budget_constraint=budget_constraint,
            time_horizon=time_horizon,
            discount_rate=discount_rate
        )
        
        assert result['success'] is True
        assert 'selected_options' in result
        assert 'total_npv' in result
        assert 'roi_percent' in result
        
        # Verify budget constraint
        total_cost = result['total_investment_cost']
        assert total_cost <= budget_constraint
        
        # NPV should be positive for profitable investments
        assert result['total_npv'] > 0
        
        # ROI should be reasonable
        assert result['roi_percent'] > 0
    
    def test_economic_mpc_simple(self):
        """Test basic economic model predictive control functionality."""
        # Simplified economic MPC for reactor temperature control
        
        class SimpleProcessModel:
            """Simple process model for testing."""
            def __init__(self):
                self.n_inputs = 1  # Temperature setpoint
                self.current_state = [350.0]  # Initial temperature (K)
        
        def economic_objective(u, k):
            """Economic objective: minimize heating cost + product loss."""
            temperature_setpoint = u[0] if hasattr(u, '__len__') else u
            
            # Heating cost (proportional to temperature above ambient)
            heating_cost = 0.1 * max(0, temperature_setpoint - 298)  # $/h
            
            # Product loss cost (deviation from optimal 380K)
            product_loss = 0.5 * abs(temperature_setpoint - 380) ** 2  # $/h
            
            return heating_cost + product_loss
        
        process_model = SimpleProcessModel()
        
        constraints = [
            {
                'type': 'ineq',
                'fun': lambda u: 450 - u[0]  # Temperature upper limit
            },
            {
                'type': 'ineq', 
                'fun': lambda u: u[0] - 320   # Temperature lower limit
            }
        ]
        
        result = self.optimizer.economic_mpc(
            process_model=process_model,
            economic_objective=economic_objective,
            constraints=constraints,
            prediction_horizon=8,
            control_horizon=4
        )
        
        assert result['success'] is True
        assert 'optimal_control_sequence' in result
        assert 'first_control_action' in result
        assert result['problem_type'] == 'economic_mpc'
        
        # First control action should be within bounds
        first_action = result['first_control_action'][0]
        assert 320 <= first_action <= 450
    
    def test_multi_product_chemical_plant(self):
        """Test comprehensive production optimization for multi-product chemical plant."""
        # Petrochemical complex with multiple products
        n_products = 5
        
        # Product data (Ethylene, Propylene, Benzene, Toluene, Xylene)
        costs = np.array([800, 600, 900, 750, 850])  # $/ton
        prices = np.array([1200, 1000, 1400, 1100, 1300])  # $/ton
        capacities = np.array([500, 400, 300, 350, 250])  # tons/day
        demands = np.array([200, 150, 100, 120, 80])   # tons/day minimum
        
        production_rates = np.zeros(n_products)
        
        result = self.optimizer.production_optimization(
            production_rates=production_rates,
            costs=costs,
            prices=prices,
            capacity_constraints=capacities,
            demand_constraints=demands
        )
        
        assert result['success'] is True
        
        optimal_production = result['optimal_production']
        
        # Verify all constraints
        assert np.all(optimal_production >= demands)
        assert np.all(optimal_production <= capacities)
        
        # Calculate expected economics
        revenue = np.dot(prices, optimal_production)
        cost = np.dot(costs, optimal_production)
        profit = revenue - cost
        
        assert result['total_revenue'] == pytest.approx(revenue, rel=1e-6)
        assert result['total_cost'] == pytest.approx(cost, rel=1e-6)
        assert result['total_profit'] == pytest.approx(profit, rel=1e-6)
        
        # Should maximize production of most profitable products
        profit_margins = (prices - costs) / prices * 100
        most_profitable = np.argmax(profit_margins)
        
        # Most profitable product should be at capacity
        assert optimal_production[most_profitable] == pytest.approx(capacities[most_profitable], rel=1e-3)
    
    def test_integrated_utility_production_optimization(self):
        """Test integrated optimization of production and utilities."""
        # Chemical plant with coupled production and utility systems
        
        # Production data
        production_costs = np.array([200, 250, 180])  # $/unit (includes utilities)
        product_prices = np.array([400, 450, 350])    # $/unit
        production_capacities = np.array([800, 600, 1000])  # units/day
        
        # Utility requirements per unit production
        steam_per_unit = np.array([2.5, 3.2, 1.8])    # GJ/unit
        electricity_per_unit = np.array([150, 200, 120])  # kWh/unit
        
        # Test production optimization first
        result_production = self.optimizer.production_optimization(
            production_rates=np.zeros(3),
            costs=production_costs,
            prices=product_prices,
            capacity_constraints=production_capacities
        )
        
        assert result_production['success'] is True
        optimal_production = result_production['optimal_production']
        
        # Calculate utility requirements
        total_steam_required = np.dot(steam_per_unit, optimal_production)
        total_electricity_required = np.dot(electricity_per_unit, optimal_production)
        
        # Verify reasonable utility demands
        assert total_steam_required > 0
        assert total_electricity_required > 0
        
        # Test utility optimization for the required demands
        utility_demands = {
            'steam_hp': np.full(24, total_steam_required / 24),  # Distribute over 24 hours
            'electricity': np.full(24, total_electricity_required / 24)
        }
        
        utility_capacities = {
            'steam_hp': total_steam_required / 20,  # 120% capacity margin
            'electricity': total_electricity_required / 20
        }
        
        utility_costs_subset = {
            'steam_hp': self.utility_costs['steam_hp'],
            'electricity': self.utility_costs['electricity']
        }
        
        result_utility = self.optimizer.utility_optimization(
            utility_costs=utility_costs_subset,
            utility_demands=utility_demands,
            utility_capacities=utility_capacities,
            time_horizon=24
        )
        
        assert result_utility['success'] is True
        assert result_utility['total_cost'] > 0
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with invalid production data
        with pytest.raises((ValueError, Exception)):
            self.optimizer.production_optimization(
                production_rates=np.array([]),  # Empty array
                costs=self.production_costs,
                prices=self.product_prices,
                capacity_constraints=self.capacity_constraints
            )
        
        # Test with mismatched array sizes
        with pytest.raises((ValueError, Exception)):
            self.optimizer.production_optimization(
                production_rates=np.array([100, 200]),  # Wrong size
                costs=self.production_costs,           # Size 3
                prices=self.product_prices,            # Size 3
                capacity_constraints=self.capacity_constraints  # Size 3
            )
    
    def test_economic_metrics_calculation(self):
        """Test accurate calculation of economic metrics."""
        # Test with known values
        costs = np.array([100])
        prices = np.array([150])
        capacities = np.array([1000])
        
        result = self.optimizer.production_optimization(
            production_rates=np.array([0]),
            costs=costs,
            prices=prices,
            capacity_constraints=capacities
        )
        
        assert result['success'] is True
        
        # Should produce at maximum capacity
        expected_production = 1000
        expected_revenue = 150 * 1000  # $150,000
        expected_cost = 100 * 1000     # $100,000
        expected_profit = 50 * 1000    # $50,000
        expected_margin = 33.33        # %
        
        assert result['optimal_production'][0] == pytest.approx(expected_production, rel=1e-6)
        assert result['total_revenue'] == pytest.approx(expected_revenue, rel=1e-6)
        assert result['total_cost'] == pytest.approx(expected_cost, rel=1e-6)
        assert result['total_profit'] == pytest.approx(expected_profit, rel=1e-6)
        assert result['profit_margin'] == pytest.approx(expected_margin, rel=1e-3)


def test_integration_example():
    """Integration test with realistic chemical plant scenario."""
    optimizer = EconomicOptimization("Integrated Chemical Plant")
    
    # Multi-period production planning
    n_periods = 7  # Weekly planning
    n_products = 3
    
    # Varying prices over the week
    base_prices = np.array([300, 400, 350])
    price_variations = np.array([
        [1.0, 1.05, 0.95],   # Monday
        [1.02, 1.03, 0.98],  # Tuesday  
        [1.01, 1.08, 1.00],  # Wednesday
        [0.98, 1.10, 1.02],  # Thursday
        [0.95, 1.05, 1.05],  # Friday
        [0.92, 0.95, 1.08],  # Saturday
        [0.90, 0.90, 1.10]   # Sunday
    ])
    
    costs = np.array([150, 200, 180])
    capacities = np.array([1000, 800, 600])
    
    total_profit = 0
    optimal_schedules = []
    
    # Optimize for each day
    for day in range(n_periods):
        daily_prices = base_prices * price_variations[day]
        
        result = optimizer.production_optimization(
            production_rates=np.zeros(n_products),
            costs=costs,
            prices=daily_prices,
            capacity_constraints=capacities
        )
        
        assert result['success'] is True
        total_profit += result['total_profit']
        optimal_schedules.append(result['optimal_production'])
    
    # Verify weekly optimization results
    assert total_profit > 0
    assert len(optimal_schedules) == n_periods
    
    # Check that production varies with price changes
    optimal_schedules = np.array(optimal_schedules)
    
    # Product 2 (index 1) has highest price variation, should show most variation
    product_2_variation = np.std(optimal_schedules[:, 1])
    assert product_2_variation > 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
