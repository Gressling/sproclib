# Pump Models

This directory contains pump models for liquid pumping operations.

## Contents

- `base/`: Base pump class with generic pump functionality
- `centrifugal/`: Centrifugal pump with quadratic head-flow curve
- `positive_displacement/`: Positive displacement pump with constant flow

## Available Pump Models

### Pump (`base/`)
Generic liquid pump model with:
- Configurable efficiency and density
- Nominal flow rate and pressure rise
- Power calculation
- First-order dynamic response

### CentrifugalPump (`centrifugal/`)
Centrifugal pump model with:
- Quadratic head-flow characteristic curve
- Shutoff head and flow coefficient parameters
- Realistic pump curve behavior
- Variable flow and pressure operation

### PositiveDisplacementPump (`positive_displacement/`)
Positive displacement pump model with:
- Constant volumetric flow rate
- Variable pressure capability
- High efficiency operation
- Suitable for high-pressure applications

## Usage Examples

```python
# Generic pump
from paramus.chemistry.process_control.unit.pump.base import Pump

pump = Pump(
    eta=0.75,                    # Pump efficiency
    rho=1000.0,                  # Liquid density (kg/m³)
    flow_nominal=0.01,           # Nominal flow (m³/s)
    delta_P_nominal=200000       # Pressure rise (Pa)
)

# Simulate steady-state operation
import numpy as np
u = np.array([100000, 0.008])   # [inlet pressure (Pa), flow rate (m³/s)]
result = pump.steady_state(u)   # [outlet pressure, power]
print(f"Outlet pressure: {result[0]/1000:.0f} kPa")
print(f"Power required: {result[1]/1000:.1f} kW")

# Centrifugal pump
from paramus.chemistry.process_control.unit.pump.centrifugal import CentrifugalPump

centrifugal = CentrifugalPump(
    H0=50.0,                     # Shutoff head (m)
    K=20.0,                      # Head-flow coefficient
    eta=0.72                     # Efficiency
)

# Positive displacement pump
from paramus.chemistry.process_control.unit.pump.positive_displacement import PositiveDisplacementPump

pd_pump = PositiveDisplacementPump(
    flow_rate=0.005,             # Constant flow rate (m³/s)
    eta=0.85                     # Efficiency
)
```

## For Contributors

When adding pump models:
- Inherit from the base `Pump` class
- Include realistic pump characteristics and limitations
- Add cavitation and NPSH (Net Positive Suction Head) effects
- Model variable speed drive capabilities
- Include pump curve data fitting methods
- Add wear and aging effects
- Consider multi-stage pumps for high pressures

### Suggested Additional Pump Types:
- Axial flow pumps
- Mixed flow pumps
- Gear pumps
- Screw pumps
- Diaphragm pumps
- Peristaltic pumps
