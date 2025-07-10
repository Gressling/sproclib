# Interacting Tanks Model

This module provides a model for two interacting tanks in series, commonly used for studying process dynamics and control.

## Features

- Two gravity-drained tanks in series
- Configurable tank cross-sectional areas and discharge coefficients
- Material balance dynamics
- Steady-state calculations

## Usage

```python
from unit.tank.interacting import InteractingTanks
import numpy as np

# Create interacting tanks model
tanks = InteractingTanks(
    A1=1.0,    # Tank 1 cross-sectional area [m²]
    A2=1.5,    # Tank 2 cross-sectional area [m²]
    C1=0.5,    # Tank 1 discharge coefficient [m²/min]
    C2=0.3,    # Tank 2 discharge coefficient [m²/min]
    name="InteractingTanks"
)

# Simulate dynamics
t_span = (0, 20)
x0 = np.array([2.0, 1.0])  # Initial heights [m]
u_func = lambda t: np.array([1.0])  # Constant inlet flow [m³/min]

result = tanks.simulate(t_span, x0, u_func)
```

## State Variables

- `x[0]`: Height of tank 1 [m]
- `x[1]`: Height of tank 2 [m]

## Input Variables

- `u[0]`: Inlet flow rate to tank 1 [m³/min]

## Parameters

- `A1`, `A2`: Cross-sectional areas [m²]
- `C1`, `C2`: Discharge coefficients [m²/min]

## For Contributors

To add a new tank model:

1. Create a new directory under `/unit/tank/your_tank_type/`
2. Implement your tank class inheriting from `ProcessModel`
3. Implement the required methods: `dynamics()` and `steady_state()`
4. Add appropriate documentation and examples
5. Create unit tests in `tests.py`

See the existing implementation as a template for your new tank model.
