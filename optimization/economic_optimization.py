"""
Economic Optimization for SPROCLIB

This module provides economic optimization tools for process operations
including profit maximization, cost minimization, and production planning.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List
from scipy.optimize import linprog, minimize
import logging

logger = logging.getLogger(__name__)


class EconomicOptimization:
    """Economic optimization tools for process control."""
    
    def __init__(self, name: str = "Economic Optimization"):
        """
        Initialize economic optimization.
        
        Args:
            name: Optimization problem name
        """
        self.name = name
        self.results = {}
        
        logger.info(f"Economic optimization '{name}' initialized")
    
    def linear_programming(
        self,
        c: np.ndarray,
        A_ub: Optional[np.ndarray] = None,
        b_ub: Optional[np.ndarray] = None,
        A_eq: Optional[np.ndarray] = None,
        b_eq: Optional[np.ndarray] = None,
        bounds: Optional[List[Tuple]] = None,
        method: str = 'highs'
    ) -> Dict[str, Any]:
        """
        Solve linear programming problem: min c^T x subject to constraints.
        
        Args:
            c: Objective function coefficients
            A_ub, b_ub: Inequality constraints A_ub @ x <= b_ub
            A_eq, b_eq: Equality constraints A_eq @ x = b_eq
            bounds: Variable bounds [(min, max), ...]
            method: Solver method
            
        Returns:
            Optimization results
        """
        try:
            result = linprog(
                c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                bounds=bounds, method=method
            )
            
            self.results = {
                'x': result.x,
                'fun': result.fun,
                'success': result.success,
                'message': result.message,
                'slack': result.slack if hasattr(result, 'slack') else None,
                'problem_type': 'linear_programming'
            }
            
            if result.success:
                logger.info(f"Linear programming solved successfully: objective = {result.fun:.6f}")
            else:
                logger.error(f"Linear programming failed: {result.message}")
            
            return self.results
            
        except Exception as e:
            logger.error(f"Linear programming error: {e}")
            return {
                'success': False,
                'error': str(e),
                'problem_type': 'linear_programming'
            }
    
    def production_optimization(
        self,
        production_rates: np.ndarray,
        costs: np.ndarray,
        prices: np.ndarray,
        capacity_constraints: np.ndarray,
        demand_constraints: Optional[np.ndarray] = None,
        material_balances: Optional[Dict[str, np.ndarray]] = None
    ) -> Dict[str, Any]:
        """
        Optimize production planning for maximum profit.
        
        Args:
            production_rates: Production variables [units/time]
            costs: Unit production costs [$/unit]
            prices: Product prices [$/unit]
            capacity_constraints: Maximum production capacities [units/time]
            demand_constraints: Minimum demand requirements [units/time]
            material_balances: Material balance constraints
            
        Returns:
            Optimization results with profit analysis
        """
        n_products = len(production_rates)
        
        # Maximize profit = prices^T * x - costs^T * x
        c = -(prices - costs)  # Negative for minimization
        
        # Build constraint matrices
        A_ub = []
        b_ub = []
        
        # Capacity constraints: x <= capacity
        A_ub.append(np.eye(n_products))
        b_ub.extend(capacity_constraints)
        
        # Convert to arrays
        A_ub = np.array(A_ub).reshape(-1, n_products)
        b_ub = np.array(b_ub)
        
        # Demand constraints (if provided)
        bounds = []
        for i in range(n_products):
            min_demand = demand_constraints[i] if demand_constraints is not None else 0
            max_capacity = capacity_constraints[i]
            bounds.append((min_demand, max_capacity))
        
        # Material balance constraints (if provided)
        A_eq = None
        b_eq = None
        if material_balances:
            # Simple material balance implementation
            # In practice, this would be more sophisticated
            pass
        
        # Solve optimization
        result = self.linear_programming(c, A_ub, b_ub, A_eq, b_eq, bounds)
        
        if result.get('success', False):
            # Calculate profit metrics
            optimal_production = result['x']
            total_revenue = np.dot(prices, optimal_production)
            total_cost = np.dot(costs, optimal_production)
            total_profit = total_revenue - total_cost
            
            result.update({
                'optimal_production': optimal_production,
                'total_revenue': total_revenue,
                'total_cost': total_cost,
                'total_profit': total_profit,
                'profit_margin': (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            })
            
            logger.info(f"Production optimization: profit = ${total_profit:.2f}")
        
        return result
    
    def utility_optimization(
        self,
        utility_costs: Dict[str, float],
        utility_demands: Dict[str, np.ndarray],
        utility_capacities: Dict[str, float],
        time_horizon: int = 24
    ) -> Dict[str, Any]:
        """
        Optimize utility usage (steam, electricity, cooling water).
        
        Args:
            utility_costs: Cost per unit for each utility
            utility_demands: Demand profiles for each utility
            utility_capacities: Maximum capacity for each utility
            time_horizon: Planning horizon [hours]
            
        Returns:
            Optimization results for utility scheduling
        """
        utilities = list(utility_costs.keys())
        n_utilities = len(utilities)
        
        # Decision variables: utility usage at each time period
        n_vars = n_utilities * time_horizon
        
        # Objective: minimize total utility cost
        c = np.zeros(n_vars)
        for i, utility in enumerate(utilities):
            cost = utility_costs[utility]
            start_idx = i * time_horizon
            end_idx = (i + 1) * time_horizon
            c[start_idx:end_idx] = cost
        
        # Constraints
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        
        # Capacity constraints
        for i, utility in enumerate(utilities):
            capacity = utility_capacities[utility]
            for t in range(time_horizon):
                constraint = np.zeros(n_vars)
                constraint[i * time_horizon + t] = 1
                A_ub.append(constraint)
                b_ub.append(capacity)
        
        # Demand constraints (must meet minimum demand)
        for i, utility in enumerate(utilities):
            demand = utility_demands[utility]
            for t in range(min(time_horizon, len(demand))):
                constraint = np.zeros(n_vars)
                constraint[i * time_horizon + t] = 1
                A_ub.append(constraint)
                b_ub.append(-demand[t])  # Negative for >= constraint
        
        # Convert to arrays
        A_ub = np.array(A_ub) if A_ub else None
        b_ub = np.array(b_ub) if b_ub else None
        
        # Variable bounds (non-negative)
        bounds = [(0, None) for _ in range(n_vars)]
        
        # Solve optimization
        result = self.linear_programming(c, A_ub, b_ub, None, None, bounds)
        
        if result.get('success', False):
            # Reshape results by utility and time
            optimal_usage = result['x'].reshape(n_utilities, time_horizon)
            
            utility_schedules = {}
            for i, utility in enumerate(utilities):
                utility_schedules[utility] = optimal_usage[i, :]
            
            result.update({
                'utility_schedules': utility_schedules,
                'total_cost': result['fun'],
                'time_horizon': time_horizon
            })
            
            logger.info(f"Utility optimization: total cost = ${result['fun']:.2f}")
        
        return result
    
    def economic_mpc(
        self,
        process_model,
        economic_objective: callable,
        constraints: List[Dict],
        prediction_horizon: int = 10,
        control_horizon: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Economic Model Predictive Control optimization.
        
        Args:
            process_model: Process model for predictions
            economic_objective: Economic objective function
            constraints: List of constraint dictionaries
            prediction_horizon: Prediction horizon
            control_horizon: Control horizon
            
        Returns:
            Economic MPC solution
        """
        if control_horizon is None:
            control_horizon = prediction_horizon
        
        # This is a simplified implementation
        # Full economic MPC requires more sophisticated formulation
        
        def objective(u_sequence):
            """Economic objective over prediction horizon."""
            try:
                # Simulate process with control sequence
                total_cost = 0.0
                
                # Simple cost accumulation
                for k, u_k in enumerate(u_sequence):
                    cost_k = economic_objective(u_k, k)
                    total_cost += cost_k
                
                return total_cost
            
            except Exception as e:
                logger.error(f"Economic objective evaluation error: {e}")
                return 1e6  # Large penalty for infeasible solutions
        
        # Initial guess for control sequence
        n_inputs = getattr(process_model, 'n_inputs', 1)
        x0 = np.zeros(control_horizon * n_inputs)
        
        # Convert constraints to scipy format
        scipy_constraints = []
        for constraint in constraints:
            if constraint['type'] == 'ineq':
                scipy_constraints.append({
                    'type': 'ineq',
                    'fun': constraint['fun']
                })
            elif constraint['type'] == 'eq':
                scipy_constraints.append({
                    'type': 'eq',
                    'fun': constraint['fun']
                })
        
        try:
            # Solve optimization
            result = minimize(
                objective, x0, method='SLSQP',
                constraints=scipy_constraints
            )
            
            optimal_sequence = result.x.reshape(control_horizon, n_inputs)
            
            return {
                'success': result.success,
                'optimal_control_sequence': optimal_sequence,
                'optimal_cost': result.fun,
                'first_control_action': optimal_sequence[0, :],
                'message': result.message,
                'problem_type': 'economic_mpc'
            }
        
        except Exception as e:
            logger.error(f"Economic MPC optimization error: {e}")
            return {
                'success': False,
                'error': str(e),
                'problem_type': 'economic_mpc'
            }
    
    def investment_optimization(
        self,
        investment_options: List[Dict[str, float]],
        budget_constraint: float,
        time_horizon: int = 10,
        discount_rate: float = 0.1
    ) -> Dict[str, Any]:
        """
        Optimize capital investment decisions.
        
        Args:
            investment_options: List of investment options with costs and returns
            budget_constraint: Total available budget
            time_horizon: Investment time horizon [years]
            discount_rate: Discount rate for NPV calculation
            
        Returns:
            Investment optimization results
        """
        n_options = len(investment_options)
        
        # Decision variables: binary selection of investment options
        # For simplicity, treat as continuous [0, 1] and round
        
        # Calculate NPV for each option
        npvs = []
        costs = []
        
        for option in investment_options:
            initial_cost = option.get('initial_cost', 0)
            annual_return = option.get('annual_return', 0)
            
            # Calculate NPV
            npv = -initial_cost
            for year in range(1, time_horizon + 1):
                npv += annual_return / ((1 + discount_rate) ** year)
            
            npvs.append(npv)
            costs.append(initial_cost)
        
        # Objective: maximize total NPV
        c = -np.array(npvs)  # Negative for minimization
        
        # Budget constraint
        A_ub = np.array(costs).reshape(1, -1)
        b_ub = np.array([budget_constraint])
        
        # Variable bounds [0, 1] for selection
        bounds = [(0, 1) for _ in range(n_options)]
        
        # Solve optimization
        result = self.linear_programming(c, A_ub, b_ub, bounds=bounds)
        
        if result.get('success', False):
            # Round to get binary decisions (simplified)
            selections = np.round(result['x'])
            selected_options = [i for i, selected in enumerate(selections) if selected > 0.5]
            
            total_npv = -result['fun']  # Convert back to positive
            total_cost = np.sum([costs[i] for i in selected_options])
            
            result.update({
                'selected_options': selected_options,
                'selection_vector': selections,
                'total_npv': total_npv,
                'total_investment_cost': total_cost,
                'roi_percent': (total_npv / total_cost * 100) if total_cost > 0 else 0
            })
            
            logger.info(f"Investment optimization: NPV = ${total_npv:.2f}, ROI = {result['roi_percent']:.1f}%")
        
        return result

# Standalone function wrappers for backward compatibility
def optimize_operation(
    objective_func: callable,
    x0: np.ndarray,
    constraints: Optional[List[Dict]] = None,
    bounds: Optional[List[Tuple]] = None,
    method: str = 'SLSQP'
) -> Dict[str, Any]:
    """
    Optimize process operation using nonlinear programming.
    
    Args:
        objective_func: Objective function to minimize
        x0: Initial guess
        constraints: List of constraint dictionaries
        bounds: Variable bounds [(min, max), ...]
        method: Optimization method
        
    Returns:
        Optimization results
    """
    try:
        result = minimize(
            objective_func, x0, method=method,
            constraints=constraints, bounds=bounds
        )
        
        return {
            'x_optimal': result.x,
            'f_optimal': result.fun,
            'success': result.success,
            'message': result.message,
            'iterations': result.nit,
            'function_evaluations': result.nfev
        }
    
    except Exception as e:
        logger.error(f"Operation optimization error: {e}")
        return {
            'success': False,
            'error': str(e),
            'x_optimal': x0,
            'f_optimal': float('inf')
        }
