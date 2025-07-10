# Plug Flow Reactor (PFR) Model

This module provides a plug flow reactor model with axial discretization, reaction kinetics, and thermal dynamics.

## Features

- Axial discretization for distributed parameter representation
- Arrhenius reaction kinetics
- Energy balance with heat transfer
- Concentration and temperature profiles along reactor length
- Conversion calculations

## Usage

```python
from unit.reactor.pfr import PlugFlowReactor
import numpy as np

# Create PFR model
pfr = PlugFlowReactor(
    L=10.0,           # Reactor length [m]
    A_cross=0.1,      # Cross-sectional area [m²]
    n_segments=20,    # Number of discretization segments
    k0=7.2e10,        # Pre-exponential factor [1/min]
    Ea=72750.0,       # Activation energy [J/mol]
    name="PFR"
)

# Simulate dynamics
t_span = (0, 10)
# Initial conditions: [CA_segments, T_segments]
x0 = np.concatenate([
    np.ones(pfr.n_segments) * 1.0,    # Initial concentrations [mol/L]
    np.ones(pfr.n_segments) * 300.0   # Initial temperatures [K]
])

# Inputs: [flow_rate, inlet_conc, inlet_temp, coolant_temp]
u_func = lambda t: np.array([10.0, 1.0, 350.0, 300.0])

result = pfr.simulate(t_span, x0, u_func)

# Calculate conversion
conversion = pfr.calculate_conversion(result['x'][:, -1])
print(f"Final conversion: {conversion:.2%}")
```

## State Variables

- `x[0:n_segments]`: Concentration in each segment [mol/L]
- `x[n_segments:2*n_segments]`: Temperature in each segment [K]

## Input Variables

- `u[0]`: Inlet flow rate [L/min]
- `u[1]`: Inlet concentration [mol/L]
- `u[2]`: Inlet temperature [K]
- `u[3]`: Coolant temperature [K]

## Parameters

- `L`: Reactor length [m]
- `A_cross`: Cross-sectional area [m²]
- `n_segments`: Number of axial segments
- `k0`: Pre-exponential factor [1/min]
- `Ea`: Activation energy [J/mol]
- `delta_H`: Heat of reaction [J/mol]
- `rho`: Density [kg/m³]
- `cp`: Heat capacity [J/kg·K]
- `U`: Heat transfer coefficient [W/m²·K]
- `D_tube`: Tube diameter [m]

## For Contributors

To add a new reactor model:

1. Create a new directory under `/unit/reactor/your_reactor_type/`
2. Implement your reactor class inheriting from `ProcessModel`
3. Implement the required methods: `dynamics()` and `steady_state()`
4. Add reaction kinetics and energy balance equations
5. Include helper methods for conversion calculations
6. Add appropriate documentation and examples
7. Create unit tests in `tests.py`

See the existing PFR implementation as a template for your new reactor model.
