"""
Plant Package for SPROCLIB - Process Plant Design and Optimization

This package provides high-level plant design capabilities with semantic APIs
similar to TensorFlow/Keras for intuitive chemical plant construction.

Classes:
    ChemicalPlant: Main plant container and orchestrator
    ProcessUnit: Base class for all process equipment
    Stream: Material and energy stream connections
    PlantOptimizer: Plant-wide optimization framework
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .chemical_plant import ChemicalPlant
from .process_unit import ProcessUnit  
from .stream import Stream
from .plant_optimizer import PlantOptimizer

__all__ = [
    'ChemicalPlant',
    'ProcessUnit',
    'Stream', 
    'PlantOptimizer'
]
