"""
Base Process Unit Class for SPROCLIB Plant Design
================================================

This module provides the base ProcessUnit class that all process equipment
inherits from, enabling semantic plant design API.
"""

import numpy as np
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class ProcessUnit(ABC):
    """
    Abstract base class for all process units in a chemical plant.
    
    Provides common functionality for:
    - Unit identification and naming
    - Performance calculation
    - Economic evaluation
    - Connection management
    """
    
    def __init__(self, name: Optional[str] = None):
        """
        Initialize process unit.
        
        Args:
            name: Optional name for the unit
        """
        self.name = name or f"{self.__class__.__name__}_{id(self)}"
        self.inputs = {}
        self.outputs = {}
        self.parameters = {}
        self.performance_data = {}
        
    @abstractmethod
    def calculate_performance(self) -> Dict[str, float]:
        """
        Calculate unit performance metrics.
        
        Returns:
            Dictionary containing performance metrics
        """
        pass
    
    def get_economic_data(self) -> Dict[str, float]:
        """
        Get economic data for the unit.
        
        Returns:
            Dictionary containing economic metrics
        """
        return {
            "capital_cost": 0.0,
            "operating_cost": 0.0,
            "maintenance_cost": 0.0
        }
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get unit configuration.
        
        Returns:
            Dictionary containing unit configuration
        """
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "parameters": self.parameters.copy()
        }
    
    def set_operating_conditions(self, conditions: Dict[str, float]) -> None:
        """
        Set operating conditions for the unit.
        
        Args:
            conditions: Dictionary of operating conditions
        """
        for key, value in conditions.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
