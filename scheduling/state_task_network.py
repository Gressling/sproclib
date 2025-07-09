"""
State-Task Network for SPROCLIB

This module implements State-Task Network (STN) scheduling for batch processes
with material balances, equipment constraints, and optimization.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)


class StateTaskNetwork:
    """State-Task Network for batch process scheduling."""
    
    def __init__(self, name: str = "STN"):
        """
        Initialize State-Task Network.
        
        Args:
            name: Network name
        """
        self.name = name
        self.states = {}  # Materials/intermediates
        self.tasks = {}   # Process tasks
        self.units = {}   # Equipment units
        self.schedule = {}
        
        logger.info(f"State-Task Network '{name}' initialized")
    
    def add_state(
        self,
        name: str,
        capacity: float = float('inf'),
        initial_amount: float = 0.0,
        price: float = 0.0,
        is_product: bool = False
    ):
        """
        Add a state (material) to the network.
        
        Args:
            name: State name
            capacity: Storage capacity
            initial_amount: Initial inventory
            price: Unit price/cost
            is_product: Whether this is a final product
        """
        self.states[name] = {
            'capacity': capacity,
            'initial_amount': initial_amount,
            'price': price,
            'is_product': is_product
        }
        
        logger.info(f"Added state '{name}' to STN")
    
    def add_task(
        self,
        name: str,
        duration: float,
        inputs: Dict[str, float],
        outputs: Dict[str, float],
        suitable_units: List[str],
        variable_cost: float = 0.0
    ):
        """
        Add a task to the network.
        
        Args:
            name: Task name
            duration: Task duration
            inputs: Input materials {state: amount}
            outputs: Output materials {state: amount}
            suitable_units: List of units that can perform this task
            variable_cost: Variable cost per batch
        """
        self.tasks[name] = {
            'duration': duration,
            'inputs': inputs,
            'outputs': outputs,
            'suitable_units': suitable_units,
            'variable_cost': variable_cost
        }
        
        logger.info(f"Added task '{name}' to STN")
    
    def add_unit(
        self,
        name: str,
        capacity: float = 1.0,
        unit_cost: float = 0.0,
        availability: float = 1.0
    ):
        """
        Add an equipment unit to the network.
        
        Args:
            name: Unit name
            capacity: Unit capacity multiplier
            unit_cost: Operating cost per time unit
            availability: Unit availability (0-1)
        """
        self.units[name] = {
            'capacity': capacity,
            'unit_cost': unit_cost,
            'availability': availability
        }
        
        logger.info(f"Added unit '{name}' to STN")
    
    def optimize_schedule(
        self,
        time_horizon: int,
        objective: str = 'profit',
        demand: Optional[Dict[str, float]] = None,
        method: str = 'greedy'
    ) -> Dict[str, Any]:
        """
        Optimize production schedule.
        
        Args:
            time_horizon: Scheduling horizon [time units]
            objective: Optimization objective ('profit', 'production', 'makespan')
            demand: Product demand requirements
            method: Solution method ('greedy', 'milp')
            
        Returns:
            Optimized schedule
        """
        if method == 'greedy':
            return self._greedy_scheduling(time_horizon, objective, demand)
        elif method == 'milp':
            return self._milp_scheduling(time_horizon, objective, demand)
        else:
            raise ValueError(f"Unknown scheduling method: {method}")
    
    def _greedy_scheduling(
        self,
        time_horizon: int,
        objective: str,
        demand: Optional[Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Greedy heuristic scheduling algorithm.
        
        Args:
            time_horizon: Time horizon
            objective: Objective function
            demand: Demand requirements
            
        Returns:
            Schedule solution
        """
        schedule = {}
        time_slots = list(range(time_horizon))
        
        # Initialize unit schedules
        for unit in self.units:
            schedule[unit] = [None] * time_horizon
        
        # Track material inventories
        inventories = {state: info['initial_amount'] 
                      for state, info in self.states.items()}
        
        # Track metrics
        total_profit = 0.0
        total_production = {state: 0.0 for state, info in self.states.items() 
                           if info.get('is_product', False)}
        
        # Task priority based on objective
        tasks_by_priority = self._calculate_task_priorities(objective, demand)
        
        # Greedy scheduling loop
        for t in time_slots:
            for task_name in tasks_by_priority:
                task_info = self.tasks[task_name]
                
                # Find available unit
                available_unit = None
                for unit in task_info['suitable_units']:
                    if unit in self.units and schedule[unit][t] is None:
                        # Check unit availability
                        if np.random.random() <= self.units[unit]['availability']:
                            available_unit = unit
                            break
                
                if available_unit is None:
                    continue
                
                # Check material availability
                can_start = True
                for input_state, amount in task_info['inputs'].items():
                    required_amount = amount * self.units[available_unit]['capacity']
                    if inventories.get(input_state, 0) < required_amount:
                        can_start = False
                        break
                
                if not can_start:
                    continue
                
                # Schedule task
                duration = int(task_info['duration'])
                end_time = min(t + duration, time_horizon)
                
                # Reserve unit
                for tt in range(t, end_time):
                    if tt < time_horizon:
                        schedule[available_unit][tt] = task_name
                
                # Update inventories
                unit_capacity = self.units[available_unit]['capacity']
                
                # Consume inputs
                for input_state, amount in task_info['inputs'].items():
                    inventories[input_state] -= amount * unit_capacity
                
                # Produce outputs
                for output_state, amount in task_info['outputs'].items():
                    produced = amount * unit_capacity
                    inventories[output_state] = inventories.get(output_state, 0) + produced
                    
                    # Calculate profit/revenue
                    if output_state in self.states:
                        state_info = self.states[output_state]
                        revenue = produced * state_info['price']
                        total_profit += revenue
                        
                        # Track production
                        if state_info.get('is_product', False):
                            total_production[output_state] += produced
                
                # Subtract variable costs
                total_profit -= task_info['variable_cost']
                total_profit -= self.units[available_unit]['unit_cost'] * duration
                
                # Break to next time slot (greedy: one task per time slot per unit)
                break
        
        # Calculate performance metrics
        demand_satisfaction = {}
        if demand:
            for product, required in demand.items():
                produced = total_production.get(product, 0)
                satisfaction = min(produced / required, 1.0) if required > 0 else 1.0
                demand_satisfaction[product] = satisfaction
        
        self.schedule = {
            'unit_schedules': schedule,
            'final_inventories': inventories,
            'total_profit': total_profit,
            'total_production': total_production,
            'demand_satisfaction': demand_satisfaction,
            'time_horizon': time_horizon,
            'method': 'greedy'
        }
        
        logger.info(f"Greedy scheduling completed: profit = {total_profit:.2f}")
        return self.schedule
    
    def _calculate_task_priorities(
        self,
        objective: str,
        demand: Optional[Dict[str, float]]
    ) -> List[str]:
        """
        Calculate task priorities based on objective.
        
        Args:
            objective: Objective function
            demand: Demand requirements
            
        Returns:
            List of tasks ordered by priority (highest first)
        """
        task_scores = {}
        
        for task_name, task_info in self.tasks.items():
            score = 0.0
            
            if objective == 'profit':
                # Calculate profit potential
                revenue = 0.0
                cost = task_info['variable_cost']
                
                for output_state, amount in task_info['outputs'].items():
                    if output_state in self.states:
                        revenue += amount * self.states[output_state]['price']
                
                score = revenue - cost
            
            elif objective == 'production':
                # Prioritize tasks that produce final products
                for output_state, amount in task_info['outputs'].items():
                    if output_state in self.states and self.states[output_state].get('is_product', False):
                        score += amount
            
            elif objective == 'makespan':
                # Prioritize shorter tasks
                score = -task_info['duration']  # Negative for shorter = better
            
            # Apply demand weighting
            if demand:
                demand_weight = 1.0
                for output_state, amount in task_info['outputs'].items():
                    if output_state in demand:
                        demand_weight = max(demand_weight, demand[output_state] / 10.0)
                score *= demand_weight
            
            task_scores[task_name] = score
        
        # Sort by score (descending)
        sorted_tasks = sorted(task_scores.keys(), key=lambda x: task_scores[x], reverse=True)
        return sorted_tasks
    
    def _milp_scheduling(
        self,
        time_horizon: int,
        objective: str,
        demand: Optional[Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Mixed-Integer Linear Programming scheduling (simplified implementation).
        
        Args:
            time_horizon: Time horizon
            objective: Objective function
            demand: Demand requirements
            
        Returns:
            Schedule solution
        """
        # This is a placeholder for MILP implementation
        # In practice, this would use specialized MILP solvers like Gurobi or CPLEX
        
        logger.warning("MILP scheduling not fully implemented, falling back to greedy")
        return self._greedy_scheduling(time_horizon, objective, demand)
    
    def plot_schedule(
        self,
        figsize: Tuple[int, int] = (12, 6),
        show_inventories: bool = True
    ):
        """
        Plot Gantt chart of the schedule.
        
        Args:
            figsize: Figure size
            show_inventories: Whether to show inventory plots
        """
        if not self.schedule:
            logger.error("No schedule to plot")
            return
        
        n_plots = 2 if show_inventories else 1
        fig, axes = plt.subplots(n_plots, 1, figsize=(figsize[0], figsize[1] * n_plots))
        
        if n_plots == 1:
            axes = [axes]
        
        # Gantt chart
        ax = axes[0]
        units = list(self.schedule['unit_schedules'].keys())
        time_horizon = self.schedule['time_horizon']
        
        # Color map for tasks
        task_names = list(self.tasks.keys())
        colors = plt.cm.Set3(np.linspace(0, 1, len(task_names)))
        task_colors = dict(zip(task_names, colors))
        
        # Create Gantt chart
        for i, unit in enumerate(units):
            schedule_unit = self.schedule['unit_schedules'][unit]
            
            current_task = None
            start_time = 0
            
            for t, task in enumerate(schedule_unit):
                if task != current_task:
                    if current_task is not None:
                        # Plot previous task
                        color = task_colors.get(current_task, 'gray')
                        ax.barh(i, t - start_time, left=start_time, 
                               height=0.6, alpha=0.8, color=color,
                               label=current_task if current_task not in [t.get_text() for t in ax.get_legend().get_texts()] else "")
                    current_task = task
                    start_time = t
            
            # Plot last task
            if current_task is not None:
                color = task_colors.get(current_task, 'gray')
                ax.barh(i, len(schedule_unit) - start_time, left=start_time,
                       height=0.6, alpha=0.8, color=color,
                       label=current_task if current_task not in [t.get_text() for t in ax.get_legend().get_texts()] else "")
        
        ax.set_yticks(range(len(units)))
        ax.set_yticklabels(units)
        ax.set_xlabel('Time')
        ax.set_ylabel('Units')
        ax.set_title(f'{self.name} - Production Schedule')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Inventory plot
        if show_inventories and n_plots > 1:
            ax2 = axes[1]
            
            # Simulate inventory evolution (simplified)
            time_points = range(time_horizon + 1)
            inventories = {state: [info['initial_amount']] for state, info in self.states.items()}
            
            # Simple inventory tracking
            for t in range(time_horizon):
                # Copy previous inventories
                for state in inventories:
                    inventories[state].append(inventories[state][-1])
            
            # Plot inventories
            for state, inventory_history in inventories.items():
                if self.states[state].get('is_product', False) or state in ['FeedA', 'FeedB']:  # Show key materials
                    ax2.plot(time_points, inventory_history, marker='o', label=state)
            
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Inventory')
            ax2.set_title('Material Inventories')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def get_schedule_metrics(self) -> Dict[str, Any]:
        """
        Calculate schedule performance metrics.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.schedule:
            return {}
        
        # Basic metrics
        metrics = {
            'total_profit': self.schedule.get('total_profit', 0),
            'total_production': self.schedule.get('total_production', {}),
            'demand_satisfaction': self.schedule.get('demand_satisfaction', {}),
            'time_horizon': self.schedule.get('time_horizon', 0)
        }
        
        # Unit utilization
        unit_utilization = {}
        for unit, schedule_unit in self.schedule['unit_schedules'].items():
            busy_slots = sum(1 for slot in schedule_unit if slot is not None)
            utilization = busy_slots / len(schedule_unit) if len(schedule_unit) > 0 else 0
            unit_utilization[unit] = utilization
        
        metrics['unit_utilization'] = unit_utilization
        metrics['average_utilization'] = np.mean(list(unit_utilization.values())) if unit_utilization else 0
        
        # Task distribution
        task_counts = {}
        for unit, schedule_unit in self.schedule['unit_schedules'].items():
            for task in schedule_unit:
                if task is not None:
                    task_counts[task] = task_counts.get(task, 0) + 1
        
        metrics['task_distribution'] = task_counts
        
        return metrics
