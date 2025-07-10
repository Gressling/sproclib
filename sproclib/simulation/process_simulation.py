"""
Process Simulation for SPROCLIB

This module provides dynamic simulation capabilities for process control systems
with integrated control loops, disturbances, and performance monitoring.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any, List, Callable, Union
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import logging

logger = logging.getLogger(__name__)


class ProcessSimulation:
    """Dynamic process simulation with control loops."""
    
    def __init__(self, process_model, controller=None, name: str = "Process Simulation"):
        """
        Initialize process simulation.
        
        Args:
            process_model: Process model with dynamics(t, x, u) method
            controller: Controller object (optional)
            name: Simulation name
        """
        self.process_model = process_model
        self.controller = controller
        self.name = name
        self.results = {}
        self.disturbances = []
        self.setpoint_profile = None
        
        logger.info(f"Process simulation '{name}' initialized")
    
    def add_disturbance(
        self,
        disturbance_func: Callable[[float], np.ndarray],
        name: str = "Disturbance"
    ):
        """
        Add disturbance to simulation.
        
        Args:
            disturbance_func: Function d(t) returning disturbance vector
            name: Disturbance name
        """
        self.disturbances.append({
            'function': disturbance_func,
            'name': name
        })
        
        logger.info(f"Added disturbance '{name}' to simulation")
    
    def set_setpoint_profile(
        self,
        setpoint_func: Callable[[float], Union[float, np.ndarray]]
    ):
        """
        Set setpoint profile for closed-loop simulation.
        
        Args:
            setpoint_func: Function sp(t) returning setpoint value(s)
        """
        self.setpoint_profile = setpoint_func
        logger.info("Setpoint profile configured")
    
    def run(
        self,
        t_span: Tuple[float, float],
        x0: np.ndarray,
        u_profile: Optional[Callable[[float], np.ndarray]] = None,
        solver: str = 'RK45',
        rtol: float = 1e-6,
        atol: float = 1e-9,
        max_step: Optional[float] = None
    ) -> Dict[str, np.ndarray]:
        """
        Run simulation with specified conditions.
        
        Args:
            t_span: Time span (start, end)
            x0: Initial conditions
            u_profile: Input profile function (for open-loop) or None (for closed-loop)
            solver: ODE solver method
            rtol: Relative tolerance
            atol: Absolute tolerance
            max_step: Maximum step size
            
        Returns:
            Simulation results
        """
        # Initialize controller state if present
        if self.controller is not None:
            self.controller.reset()
        
        # Store control history for closed-loop
        control_history = []
        setpoint_history = []
        output_history = []
        
        def dynamics(t, x):
            """Combined process and control dynamics."""
            # Calculate process output
            if hasattr(self.process_model, 'output'):
                y = self.process_model.output(x)
            else:
                y = x[0] if len(x) > 0 else 0.0  # Default to first state
            
            # Determine control input
            if u_profile is not None:
                # Open-loop simulation
                u = u_profile(t)
            elif self.controller is not None and self.setpoint_profile is not None:
                # Closed-loop simulation
                setpoint = self.setpoint_profile(t)
                u = self.controller.update(t, setpoint, y)
                
                # Store history
                control_history.append(u)
                setpoint_history.append(setpoint)
                output_history.append(y)
            else:
                # No control input
                u = np.zeros(getattr(self.process_model, 'n_inputs', 1))
            
            # Add disturbances
            d_total = np.zeros_like(x)
            for disturbance in self.disturbances:
                d = disturbance['function'](t)
                if len(d) == len(x):
                    d_total += d
            
            # Calculate process dynamics
            if hasattr(self.process_model, 'dynamics'):
                dx_dt = self.process_model.dynamics(t, x, u) + d_total
            else:
                # Simple default dynamics
                dx_dt = -0.1 * x + 0.1 * u
            
            return dx_dt
        
        # Run simulation
        try:
            sol = solve_ivp(
                dynamics, t_span, x0, 
                method=solver, rtol=rtol, atol=atol,
                max_step=max_step, dense_output=True
            )
            
            if not sol.success:
                logger.error(f"Simulation failed: {sol.message}")
                return {}
            
            # Extract results at regular intervals
            t_eval = np.linspace(t_span[0], t_span[1], 1000)
            x_results = sol.sol(t_eval)
            
            # Reconstruct control inputs and outputs
            u_results = []
            y_results = []
            
            for t in t_eval:
                # Calculate output
                x_t = sol.sol(t)
                if hasattr(self.process_model, 'output'):
                    y_t = self.process_model.output(x_t)
                else:
                    y_t = x_t[0] if len(x_t) > 0 else 0.0
                y_results.append(y_t)
                
                # Calculate control input
                if u_profile is not None:
                    u_t = u_profile(t)
                elif self.controller is not None and self.setpoint_profile is not None:
                    setpoint_t = self.setpoint_profile(t)
                    u_t = self.controller.update(t, setpoint_t, y_t)
                else:
                    u_t = 0.0
                
                u_results.append(u_t)
            
            u_results = np.array(u_results)
            y_results = np.array(y_results)
            
            # Store results
            self.results = {
                't': t_eval,
                'x': x_results,
                'u': u_results.T if u_results.ndim > 1 else u_results,
                'y': y_results,
                'success': sol.success,
                'message': sol.message
            }
            
            # Add setpoint history for closed-loop
            if self.setpoint_profile is not None:
                sp_results = [self.setpoint_profile(t) for t in t_eval]
                self.results['setpoint'] = np.array(sp_results)
            
            logger.info(f"Simulation completed successfully over {t_span[1]-t_span[0]:.2f} time units")
            return self.results
            
        except Exception as e:
            logger.error(f"Simulation error: {e}")
            return {'success': False, 'error': str(e)}
    
    def plot_results(
        self,
        variables: Optional[List[str]] = None,
        figsize: Tuple[int, int] = (12, 10)
    ):
        """
        Plot simulation results.
        
        Args:
            variables: List of variables to plot
            figsize: Figure size
        """
        if not self.results or not self.results.get('success', False):
            logger.error("No valid simulation results to plot")
            return
        
        t = self.results['t']
        x = self.results['x']
        u = self.results['u']
        y = self.results['y']
        
        # Determine number of subplots
        n_plots = 3
        if 'setpoint' in self.results:
            n_plots = 4
        
        fig, axes = plt.subplots(n_plots, 1, figsize=figsize)
        if n_plots == 1:
            axes = [axes]
        
        # Plot states
        if x.ndim > 1:
            for i in range(x.shape[0]):
                axes[0].plot(t, x[i, :], label=f'x{i+1}')
        else:
            axes[0].plot(t, x, label='x')
        axes[0].set_ylabel('States')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        axes[0].set_title(f'{self.name} - State Variables')
        
        # Plot inputs
        if u.ndim > 1:
            for i in range(u.shape[0]):
                axes[1].plot(t, u[i, :], label=f'u{i+1}')
        else:
            axes[1].plot(t, u, label='u')
        axes[1].set_ylabel('Inputs')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        axes[1].set_title('Control Inputs')
        
        # Plot outputs
        axes[2].plot(t, y, 'b-', label='Output', linewidth=2)
        if 'setpoint' in self.results:
            axes[2].plot(t, self.results['setpoint'], 'r--', label='Setpoint', linewidth=2)
            axes[2].set_title('Process Output vs Setpoint')
        else:
            axes[2].set_title('Process Output')
        axes[2].set_ylabel('Output')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # Plot control performance if closed-loop
        if 'setpoint' in self.results and n_plots >= 4:
            error = self.results['setpoint'] - y
            axes[3].plot(t, error, 'g-', label='Error')
            axes[3].set_ylabel('Control Error')
            axes[3].set_xlabel('Time')
            axes[3].legend()
            axes[3].grid(True, alpha=0.3)
            axes[3].set_title('Control Error')
        else:
            axes[-1].set_xlabel('Time')
        
        plt.tight_layout()
        plt.show()
    
    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Calculate performance metrics for closed-loop simulation.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.results or 'setpoint' not in self.results:
            logger.warning("Cannot calculate performance metrics without setpoint data")
            return {}
        
        t = self.results['t']
        y = self.results['y']
        setpoint = self.results['setpoint']
        
        # Control error
        error = setpoint - y
        
        # Performance metrics
        mae = np.mean(np.abs(error))
        mse = np.mean(error**2)
        rmse = np.sqrt(mse)
        
        # Settling time (2% criterion)
        final_setpoint = setpoint[-1] if len(setpoint) > 0 else 0
        settling_time = t[-1]
        
        for i in range(len(error)-1, 0, -1):
            if abs(error[i]) > 0.02 * abs(final_setpoint):
                settling_time = t[i]
                break
        
        # Overshoot
        if len(y) > 0:
            max_output = np.max(y)
            overshoot = ((max_output - final_setpoint) / final_setpoint * 100) if final_setpoint != 0 else 0
        else:
            overshoot = 0
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'settling_time': settling_time,
            'overshoot_percent': overshoot,
            'steady_state_error': abs(error[-1]) if len(error) > 0 else 0
        }
    
    def compare_scenarios(
        self,
        scenarios: List[Dict[str, Any]],
        metric: str = 'mae'
    ) -> Dict[str, Any]:
        """
        Compare multiple simulation scenarios.
        
        Args:
            scenarios: List of scenario dictionaries
            metric: Performance metric for comparison
            
        Returns:
            Comparison results
        """
        results = {}
        
        for i, scenario in enumerate(scenarios):
            scenario_name = scenario.get('name', f'Scenario_{i+1}')
            
            # Run scenario
            scenario_results = self.run(**scenario.get('simulation_params', {}))
            
            if scenario_results.get('success', False):
                # Calculate performance metrics
                metrics = self.get_performance_metrics()
                results[scenario_name] = {
                    'results': scenario_results,
                    'metrics': metrics,
                    'metric_value': metrics.get(metric, np.inf)
                }
            else:
                results[scenario_name] = {
                    'results': scenario_results,
                    'metrics': {},
                    'metric_value': np.inf
                }
        
        # Find best scenario
        best_scenario = min(results.keys(), key=lambda k: results[k]['metric_value'])
        
        return {
            'scenarios': results,
            'best_scenario': best_scenario,
            'comparison_metric': metric
        }
