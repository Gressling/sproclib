# SPROCLIB Process Unit Models

This directory contains the modular process unit models for SPROCLIB (Standard Process Control Library). Each process unit is implemented as its own class in a separate directory to enable easy contribution and maintenance.

## Directory Structure

```
unit/
├── base/                   # Abstract base classes
│   └── __init__.py        # ProcessModel base class
├── reactor/               # Reactor models
│   ├── cstr/             # Continuous Stirred Tank Reactor
│   ├── pfr/              # Plug Flow Reactor
│   ├── batch/            # Batch Reactor
│   └── fixed_bed/        # Fixed Bed Reactor
├── tank/                 # Tank models
│   ├── single/           # Single gravity-drained tank
│   └── interacting/      # Two interacting tanks
├── heat_exchanger/       # Heat exchanger models
├── distillation/         # Distillation models
│   ├── tray/            # Individual distillation tray
│   └── column/          # Binary distillation column
└── utilities/           # Analysis utilities
    └── __init__.py      # LinearApproximation
```

## Available Process Units

### Reactor Models (`/reactor/`)
- **CSTR**: Continuous Stirred Tank Reactor with reaction kinetics and thermal dynamics
- **PFR**: Plug Flow Reactor with axial discretization
- **BatchReactor**: Batch reactor with heating/cooling
- **FixedBedReactor**: Fixed bed catalytic reactor

### Tank Models (`/tank/`)
- **Tank**: Single gravity-drained tank
- **InteractingTanks**: Two tanks in series

### Heat Exchange (`/heat_exchanger/`)
- **HeatExchanger**: Counter-current heat exchanger with thermal dynamics

### Distillation (`/distillation/`)
- **DistillationTray**: Individual tray model for binary systems
- **BinaryDistillationColumn**: Complete column with multiple trays

### Utilities (`/utilities/`)
- **LinearApproximation**: Linearization utility for control design

## Usage

```python
# Import individual units
from unit.reactor.cstr import CSTR
from unit.tank.interacting import InteractingTanks
from unit.heat_exchanger import HeatExchanger

# Or import from main unit module
from unit import CSTR, InteractingTanks, HeatExchanger

# Create and use process units
cstr = CSTR(V=100.0, k0=7.2e10, Ea=72750.0)
tanks = InteractingTanks(A1=1.0, A2=1.5, C1=0.5, C2=0.3)
hx = HeatExchanger(U=500.0, A=10.0)
```

## For Contributors

### Adding a New Process Unit

1. **Create Directory Structure**
   ```
   unit/your_category/your_unit_name/
   ├── __init__.py      # Main implementation
   ├── README.md        # Documentation
   ├── examples.py      # Usage examples (optional)
   └── tests.py         # Unit tests (optional)
   ```

2. **Implement Your Unit Class**
   ```python
   from ...base import ProcessModel
   import numpy as np
   
   class YourUnit(ProcessModel):
       def __init__(self, param1, param2, name="YourUnit"):
           super().__init__(name)
           # Initialize parameters
           
       def dynamics(self, t, x, u):
           # Implement dx/dt = f(t, x, u)
           return dxdt
           
       def steady_state(self, u):
           # Calculate steady-state values
           return x_ss
   ```

3. **Required Methods**
   - `__init__()`: Initialize parameters and call `super().__init__(name)`
   - `dynamics()`: Implement process dynamics `dx/dt = f(t, x, u)`
   - `steady_state()`: Calculate steady-state for given inputs

4. **Documentation Requirements**
   - Clear docstrings for all methods
   - Parameter descriptions with units
   - State and input variable definitions
   - Usage examples in README.md

5. **Testing**
   - Create unit tests in `tests.py`
   - Test dynamics, steady-state, and edge cases
   - Verify physical consistency

### Guidelines

- **Naming**: Use descriptive names following Python conventions
- **Units**: Clearly specify units in docstrings and comments
- **Validation**: Include input validation and physical constraints
- **Error Handling**: Handle edge cases gracefully
- **Documentation**: Provide documentation and examples

### Integration

After implementing your unit:

1. Add import to relevant `__init__.py` files
2. Update the main unit `__init__.py` and `__all__` list
3. Create pull request with thorough description
4. Include tests and documentation

## Examples

See individual unit directories for specific usage examples. Each unit includes:
- Basic setup and configuration
- Simulation examples
- Steady-state calculations
- Parameter studies

## Dependencies

- `numpy`: Numerical computations
- `scipy`: Integration and optimization
- `typing`: Type hints
- `abc`: Abstract base classes
- `logging`: Error and warning messages

## Support

For questions or contributions, please refer to:
- Individual unit README files
- Main SPROCLIB documentation
- GitHub issues and discussions
