# Base Classes

This directory contains the abstract base classes for the SPROCLIB process units.

## Contents

- `__init__.py`: Contains the `ProcessModel` abstract base class that all process units inherit from

## ProcessModel Base Class

The `ProcessModel` class provides the fundamental interface that all process units must implement:

- Abstract `dynamics()` method for defining process dynamics
- Common attributes for parameters, state variables, inputs, and outputs
- Standardized simulation interface
- Logging support

## Usage

```python
from paramus.chemistry.process_control.unit.base import ProcessModel

# All process units inherit from ProcessModel
class MyCustomUnit(ProcessModel):
    def dynamics(self, t, x, u):
        # Define your process dynamics here
        return dx_dt
```

## For Contributors

When creating new process units:
1. Always inherit from `ProcessModel`
2. Implement the abstract `dynamics()` method
3. Follow the established naming conventions
4. Add docstrings and type hints
