"""
Base Classes for SPROCLIB Controller Package

This module provides abstract base classes for controllers and tuning rules.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from abc import ABC, abstractmethod
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class TuningRule(ABC):
    """Abstract base class for PID tuning rules."""
    
    @abstractmethod
    def calculate_parameters(self, model_params: Dict[str, float]) -> Dict[str, float]:
        """Calculate PID parameters from process model parameters."""
        pass
