# CSTR (Continuous Stirred Tank Reactor) Model

## Overview

The CSTR module provides a model for a continuous stirred tank reactor with:
- Arrhenius kinetics
- Energy balance with heat transfer
- Steady-state and dynamic simulation capabilities

## Features

- **Material Balance**: Component mass balance with reaction
- **Energy Balance**: Temperature dynamics with heat generation and removal
- **Arrhenius Kinetics**: Temperature-dependent reaction rate
- **Heat Transfer**: Cooling/heating through reactor jacket
- **Performance Metrics**: Conversion, selectivity, productivity calculations

## State Variables

| Variable | Description | Units |
|----------|-------------|-------|
| CA | Concentration | mol/L |
| T | Temperature | K |

## Input Variables

| Variable | Description | Units |
|----------|-------------|-------|
| q | Flow rate | L/min |
| CAi | Inlet concentration | mol/L |
| Ti | Inlet temperature | K |
| Tc | Coolant temperature | K |

## Parameters

| Parameter | Description | Default | Units |
|-----------|-------------|---------|-------|
| V | Reactor volume | 100.0 | L |
| k0 | Pre-exponential factor | 7.2e10 | 1/min |
| Ea | Activation energy | 72750.0 | J/mol |
| R | Gas constant | 8.314 | J/mol/K |
| rho | Density | 1000.0 | g/L |
| Cp | Heat capacity | 0.239 | J/g/K |
| dHr | Heat of reaction | -50000.0 | J/mol |
| UA | Heat transfer coefficient | 50000.0 | J/min/K |

## Usage Example

```python
from unit.reactor.cstr import CSTR
import numpy as np

# Create CSTR instance
reactor = CSTR(
    V=100.0,           # 100 L reactor
    k0=7.2e10,         # Pre-exponential factor
    Ea=72750.0,        # Activation energy
    UA=50000.0         # Heat transfer coefficient
)

# Define operating conditions
u = np.array([10.0, 1.0, 350.0, 300.0])  # [q, CAi, Ti, Tc]

# Calculate steady state
x_ss = reactor.steady_state(u)
print(f"Steady-state: CA = {x_ss[0]:.3f} mol/L, T = {x_ss[1]:.1f} K")

# Simulate dynamic response
t_span = (0, 60)  # 60 minutes
x0 = np.array([0.0, 300.0])  # Initial conditions

def u_func(t):
    return u  # Constant inputs

result = reactor.simulate(t_span, x0, u_func)

# Calculate performance metrics
metrics = reactor.get_performance_metrics(x_ss, u)
print(f"Conversion: {metrics['conversion']:.1%}")
print(f"Residence time: {metrics['residence_time']:.1f} min")
```

## Mathematical Model

### Material Balance
```
dCA/dt = q/V * (CAi - CA) - k(T) * CA
```

### Energy Balance
```
dT/dt = q/V * (Ti - T) + (-ΔHr) * k(T) * CA / (ρ * Cp) + UA * (Tc - T) / (V * ρ * Cp)
```

### Reaction Rate
```
k(T) = k0 * exp(-Ea / (R * T))
```

## References

1. Fogler, H.S. (2016). *Elements of Chemical Reaction Engineering*, 5th Edition
2. Levenspiel, O. (1999). *Chemical Reaction Engineering*, 3rd Edition
3. Seborg, D.E. et al. (2016). *Process Dynamics and Control*, 4th Edition
