"""
Model-Based Controllers for SPROCLIB

This package contains model-based control algorithms that use process models
to design and tune controllers.

Available Controllers:
- IMCController: Internal Model Control using process model inverse
- FOPDTModel: First Order Plus Dead Time model for IMC
- SOPDTModel: Second Order Plus Dead Time model for IMC

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

from .IMCController import (
    IMCController,
    ProcessModelInterface,
    FOPDTModel,
    SOPDTModel,
    tune_imc_lambda
)

__all__ = [
    'IMCController',
    'ProcessModelInterface', 
    'FOPDTModel',
    'SOPDTModel',
    'tune_imc_lambda'
]
