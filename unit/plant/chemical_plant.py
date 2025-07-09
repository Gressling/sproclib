"""
Chemical Plant - Main Plant Design and Orchestration Class

This module provides the main ChemicalPlant class that enables semantic
plant design similar to TensorFlow/Keras Sequential models.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PlantConfiguration:
    """Plant-wide configuration parameters."""
    name: str = "Chemical Plant"
    operating_hours: float = 8760.0  # hours/year
    electricity_cost: float = 0.10   # $/kWh
    steam_cost: float = 15.0         # $/ton
    cooling_water_cost: float = 0.05 # $/m³
    labor_cost: float = 50.0         # $/hour
    maintenance_factor: float = 0.03  # fraction of capital cost


class ChemicalPlant:
    """
    Main chemical plant class enabling semantic plant design.
    
    Similar to keras.Sequential, this class allows adding process units
    in sequence and provides plant-wide optimization and analysis.
    """
    
    def __init__(self, name: str = "Chemical Plant", config: Optional[PlantConfiguration] = None):
        """
        Initialize chemical plant.
        
        Args:
            name: Plant name
            config: Plant configuration parameters
        """
        self.name = name
        self.config = config or PlantConfiguration(name=name)
        self.units: List = []
        self.streams: Dict[str, Any] = {}
        self.connections: List[Tuple[str, str, str]] = []
        self.is_compiled = False
        self.optimizer = None
        self.metrics = []
        
        logger.info(f"Initialized chemical plant: {self.name}")
    
    def add(self, unit, name: Optional[str] = None):
        """
        Add a process unit to the plant (similar to model.add()).
        
        Args:
            unit: Process unit instance (reactor, pump, etc.)
            name: Optional name for the unit
        """
        if name:
            unit.name = name
        
        # Auto-generate name if not provided
        if not hasattr(unit, 'name') or not unit.name:
            unit_type = type(unit).__name__
            unit_count = len([u for u in self.units if type(u).__name__ == unit_type])
            unit.name = f"{unit_type}_{unit_count + 1}"
        
        self.units.append(unit)
        logger.info(f"Added unit: {unit.name} ({type(unit).__name__})")
        
        return self
    
    def connect(self, from_unit: str, to_unit: str, stream_name: str = None):
        """
        Connect two units with a stream.
        
        Args:
            from_unit: Name of source unit
            to_unit: Name of destination unit  
            stream_name: Optional name for connecting stream
        """
        if not stream_name:
            stream_name = f"{from_unit}_to_{to_unit}"
        
        self.connections.append((from_unit, to_unit, stream_name))
        logger.info(f"Connected {from_unit} → {to_unit} via {stream_name}")
        
        return self
    
    def compile(self, optimizer="economic", loss="total_cost", metrics=None):
        """
        Compile the plant for optimization (similar to model.compile()).
        
        Args:
            optimizer: Optimization strategy ("economic", "environmental", "safety")
            loss: Loss function to minimize ("total_cost", "emissions", "risk")
            metrics: List of metrics to track
        """
        if metrics is None:
            metrics = ["total_cost", "energy_consumption", "conversion", "profit"]
        
        self.optimizer = optimizer
        self.loss_function = loss
        self.metrics = metrics
        self.is_compiled = True
        
        # Validate plant configuration
        self._validate_plant()
        
        logger.info(f"Plant compiled with optimizer={optimizer}, loss={loss}")
        return self
    
    def summary(self):
        """Print plant summary (similar to model.summary())."""
        print(f"\n{'='*60}")
        print(f"Chemical Plant: {self.name}")
        print(f"{'='*60}")
        
        print(f"Configuration:")
        print(f"  Operating hours: {self.config.operating_hours:,.0f} h/year")
        print(f"  Electricity cost: ${self.config.electricity_cost:.3f}/kWh")
        print(f"  Steam cost: ${self.config.steam_cost:.2f}/ton")
        print(f"  Cooling water cost: ${self.config.cooling_water_cost:.3f}/m³")
        
        print(f"\nProcess Units ({len(self.units)} total):")
        print(f"{'Unit Name':<20} {'Type':<20} {'Parameters':<30}")
        print(f"{'-'*70}")
        
        for i, unit in enumerate(self.units, 1):
            unit_type = type(unit).__name__
            params = self._get_unit_params(unit)
            print(f"{unit.name:<20} {unit_type:<20} {params:<30}")
        
        print(f"\nConnections ({len(self.connections)} total):")
        for from_unit, to_unit, stream in self.connections:
            print(f"  {from_unit} → {to_unit} ({stream})")
        
        if self.is_compiled:
            print(f"\nOptimization:")
            print(f"  Optimizer: {self.optimizer}")
            print(f"  Loss function: {self.loss_function}")
            print(f"  Metrics: {', '.join(self.metrics)}")
        else:
            print(f"\n⚠️  Plant not compiled yet. Call plant.compile() to enable optimization.")
        
        print(f"{'='*60}\n")
    
    def optimize(self, target_production: float = None, constraints: Dict = None):
        """
        Optimize plant operations.
        
        Args:
            target_production: Target production rate
            constraints: Operating constraints dictionary
        """
        if not self.is_compiled:
            raise RuntimeError("Plant must be compiled before optimization. Call plant.compile().")
        
        constraints = constraints or {}
        
        print(f"Optimizing plant: {self.name}")
        print(f"Optimizer: {self.optimizer}")
        print(f"Loss function: {self.loss_function}")
        
        # Plant-wide optimization logic
        results = self._run_optimization(target_production, constraints)
        
        return results
    
    def simulate(self, duration: float = 24.0, time_step: float = 0.1):
        """
        Run dynamic plant simulation.
        
        Args:
            duration: Simulation duration (hours)
            time_step: Time step (hours)
        """
        if not self.is_compiled:
            raise RuntimeError("Plant must be compiled before simulation. Call plant.compile().")
        
        print(f"Running plant simulation for {duration} hours...")
        
        # Dynamic simulation logic
        time_points = np.arange(0, duration + time_step, time_step)
        results = {
            'time': time_points,
            'units': {unit.name: [] for unit in self.units},
            'streams': {},
            'economics': []
        }
        
        # Simulate each time step
        for t in time_points:
            # Unit operations at time t
            for unit in self.units:
                unit_result = self._simulate_unit_step(unit, t, time_step)
                results['units'][unit.name].append(unit_result)
            
            # Economic calculation
            economics = self._calculate_economics(t)
            results['economics'].append(economics)
        
        return results
    
    def evaluate(self, operating_conditions: Dict):
        """
        Evaluate plant performance at given operating conditions.
        
        Args:
            operating_conditions: Dictionary of operating conditions
        """
        if not self.is_compiled:
            raise RuntimeError("Plant must be compiled before evaluation. Call plant.compile().")
        
        # Calculate steady-state performance
        performance = {}
        
        # Unit-wise evaluation
        for unit in self.units:
            unit_performance = self._evaluate_unit(unit, operating_conditions)
            performance[unit.name] = unit_performance
        
        # Plant-wide metrics
        performance['plant'] = self._calculate_plant_metrics(performance)
        
        return performance
    
    def get_config(self):
        """Get plant configuration."""
        return {
            'name': self.name,
            'config': self.config,
            'units': [(unit.name, type(unit).__name__) for unit in self.units],
            'connections': self.connections,
            'optimizer': self.optimizer if self.is_compiled else None,
            'metrics': self.metrics
        }
    
    def save_plant(self, filepath: str):
        """Save plant configuration to file."""
        import json
        
        config = self.get_config()
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2, default=str)
        
        print(f"Plant saved to {filepath}")
    
    def _get_unit_params(self, unit) -> str:
        """Get unit parameters summary."""
        if hasattr(unit, 'V'):
            return f"V={unit.V:.1f}L"
        elif hasattr(unit, 'length'):
            return f"L={unit.length:.1f}m"
        elif hasattr(unit, 'H0'):
            return f"H0={unit.H0:.1f}m"
        elif hasattr(unit, 'N_trays'):
            return f"Trays={unit.N_trays}"
        else:
            return "Custom"
    
    def _validate_plant(self):
        """Validate plant configuration."""
        if len(self.units) == 0:
            raise ValueError("Plant has no units. Add units with plant.add().")
        
        # Check for disconnected units
        connected_units = set()
        for from_unit, to_unit, _ in self.connections:
            connected_units.add(from_unit)
            connected_units.add(to_unit)
        
        unit_names = {unit.name for unit in self.units}
        
        # Validate connection references
        for from_unit, to_unit, stream in self.connections:
            if from_unit not in unit_names:
                raise ValueError(f"Connection references unknown unit: {from_unit}")
            if to_unit not in unit_names:
                raise ValueError(f"Connection references unknown unit: {to_unit}")
    
    def _run_optimization(self, target_production, constraints):
        """Run plant optimization."""
        from scipy.optimize import minimize
        
        # Objective function for economic optimization
        def objective(x):
            # x contains operating variables for all units
            total_cost = 0
            
            # Operating costs
            energy_cost = sum(self._calculate_unit_energy_cost(unit, x) for unit in self.units)
            raw_material_cost = self._calculate_raw_material_cost(x)
            utilities_cost = self._calculate_utilities_cost(x)
            
            total_cost = energy_cost + raw_material_cost + utilities_cost
            
            return total_cost
        
        # Initial guess
        x0 = np.ones(len(self.units) * 3)  # 3 variables per unit
        
        # Bounds and constraints
        bounds = [(0.1, 10.0)] * len(x0)  # Example bounds
        
        # Optimize
        result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')
        
        return {
            'success': result.success,
            'optimal_cost': result.fun,
            'optimal_variables': result.x,
            'message': result.message
        }
    
    def _simulate_unit_step(self, unit, t, dt):
        """Simulate one time step for a unit."""
        # Placeholder - would call unit's dynamics method
        return {'t': t, 'state': np.random.random(2)}
    
    def _calculate_economics(self, t):
        """Calculate economic metrics at time t."""
        return {
            'operating_cost': np.random.random() * 1000,
            'revenue': np.random.random() * 2000,
            'profit': np.random.random() * 500
        }
    
    def _evaluate_unit(self, unit, conditions):
        """Evaluate unit performance."""
        return {'efficiency': 0.85, 'conversion': 0.92}
    
    def _calculate_plant_metrics(self, unit_performance):
        """Calculate plant-wide metrics."""
        return {
            'overall_efficiency': 0.80,
            'total_energy': 1500.0,  # kW
            'production_rate': 1000.0,  # kg/h
            'profit_rate': 500.0  # $/h
        }
    
    def _calculate_unit_energy_cost(self, unit, variables):
        """Calculate energy cost for a unit."""
        return np.random.random() * 100  # Placeholder
    
    def _calculate_raw_material_cost(self, variables):
        """Calculate raw material costs."""
        return np.random.random() * 500  # Placeholder
    
    def _calculate_utilities_cost(self, variables):
        """Calculate utilities costs."""
        return np.random.random() * 200  # Placeholder
