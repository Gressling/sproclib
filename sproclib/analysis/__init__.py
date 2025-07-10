"""
Analysis Package for SPROCLIB - Standard Process Control Library

This package provides system analysis tools including transfer functions,
frequency response analysis, stability analysis, and model identification.

Classes:
    TransferFunction: Transfer function representation and analysis
    SystemAnalysis: Comprehensive system analysis tools
    ModelIdentification: Model fitting and identification methods
    
Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .transfer_function import TransferFunction
from .system_analysis import SystemAnalysis
from .model_identification import ModelIdentification

__all__ = [
    'TransferFunction',
    'SystemAnalysis', 
    'ModelIdentification'
]
