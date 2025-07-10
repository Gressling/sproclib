# Valve Units

This directory contains valve process unit models for flow control and switching.

## Contents

- `control/`: Control valve models for flow regulation
- `three_way/`: Three-way valve models for flow diverting/mixing

## Available Valve Models

### ControlValve (`control/`)
Control valve model with:
- Flow coefficient (Cv) based flow calculation
- Valve position dynamics
- Pressure drop effects
- Equal percentage or linear characteristics
- Cavitation and choked flow limits

### ThreeWayValve (`three_way/`)
Three-way valve model with:
- Mixing or diverting configurations
- Flow splitting based on valve position
- Independent Cv characteristics for each port
- Pressure-dependent flow distribution

## Usage Examples

```python
# Control valve
from paramus.chemistry.process_control.unit.valve.control import ControlValve

valve = ControlValve(
    Cv_max=10.0,         # maximum flow coefficient
    time_constant=5.0,   # valve response time
    valve_char="equal"   # valve characteristic
)

# Three-way valve (mixing)
from paramus.chemistry.process_control.unit.valve.three_way import ThreeWayValve

valve_3way = ThreeWayValve(
    Cv_max=10.0,              # maximum flow coefficient
    time_constant=3.0,        # valve response time
    valve_config="mixing"     # mixing configuration
)
```

## For Contributors

When adding valve models:
- Include detailed valve characteristics (linear, equal percentage, quick opening)
- Add hysteresis and deadband effects
- Model valve stiction and backlash
- Include safety valve and relief valve models
- Add check valve functionality
- Consider temperature and pressure effects on materials
