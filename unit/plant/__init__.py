"""
SPROCLIB Plant Package - Semantic Plant Design API
=================================================

This package provides a TensorFlow/Keras-style API for chemical plant design,
optimization, and simulation.

Classes:
    ProcessUnit: Base class for all process units
    ChemicalPlant: Main plant class with semantic API
    PlantConfiguration: Plant-wide configuration parameters
"""

from .process_unit import ProcessUnit
from .chemical_plant import ChemicalPlant, PlantConfiguration

__all__ = [
    'ProcessUnit',
    'ChemicalPlant', 
    'PlantConfiguration'
    'Stream', 
    'PlantOptimizer'
]

__version__ = '1.0.0'
__author__ = 'SPROCLIB Development Team'
