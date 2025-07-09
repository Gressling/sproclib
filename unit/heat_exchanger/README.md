# Heat Exchanger Units

This directory contains heat exchanger process unit models.

## Contents

- `__init__.py`: Contains the `HeatExchanger` class for modeling heat exchange processes

## HeatExchanger Class

Models a counter-current heat exchanger with the following features:

- Hot and cold side temperature dynamics
- Heat transfer coefficient modeling
- Thermal capacity effects
- Flow rate dependencies
- Temperature-dependent properties

### Key Parameters
- `area`: Heat transfer area (m²)
- `U`: Overall heat transfer coefficient (W/m²·K)
- `mc_hot`: Thermal capacity of hot side (J/K)
- `mc_cold`: Thermal capacity of cold side (J/K)

### State Variables
- Hot side temperature
- Cold side temperature

### Inputs
- Hot side inlet temperature
- Cold side inlet temperature
- Hot side flow rate
- Cold side flow rate

## Usage Example

```python
from paramus.chemistry.process_control.unit.heat_exchanger import HeatExchanger

# Create heat exchanger
hx = HeatExchanger(
    area=10.0,          # m²
    U=500.0,            # W/m²·K
    mc_hot=1000.0,      # J/K
    mc_cold=800.0       # J/K
)

# Simulate
result = hx.simulate(...)
```

## For Contributors

When extending heat exchanger models:
- Consider different heat exchanger configurations (parallel flow, cross flow)
- Add validation for physical constraints
- Include pressure drop effects if needed
- Add fouling factor modeling capabilities
