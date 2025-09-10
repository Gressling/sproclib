# Mixer Models

This directory contains stream mixer models for combining multiple input streams.

## Contents

- `__init__.py`: Contains the `Mixer` class for stream mixing operations

## Mixer Class

Models a stream mixer with the following features:

- Multiple inlet stream mixing
- Mass and energy balance calculations
- Heat transfer to environment
- Pressure drop considerations
- Dynamic response modeling with volume accumulation

### Key Parameters
- `n_inlets`: Number of inlet streams (typically 2-6)
- `mixing_efficiency`: Mixing efficiency (0.90-0.99 for good mixing)
- `volume`: Mixer volume for dynamic calculations (m³)
- `heat_transfer_coeff`: Heat transfer coefficient to environment (W/K)
- `ambient_temp`: Ambient temperature for heat transfer (K)
- `pressure_drop`: Pressure drop across mixer (Pa)

### State Variables
- Total mass in mixer (kg)
- Total thermal energy in mixer (J)

### Inputs
For each inlet stream:
- Flow rate (kg/s)
- Temperature (K)
- Pressure (Pa)

### Outputs
- Total outlet flow rate (kg/s)
- Outlet temperature (K)
- Outlet pressure (Pa)

## Usage Example

```python
from sproclib.unit.mixer import Mixer
import numpy as np

# Create mixer for 3 inlet streams
mixer = Mixer(
    n_inlets=3,                  # Three inlet streams
    mixing_efficiency=0.95,      # Good mixing efficiency
    volume=2.0,                  # 2 m³ mixer volume
    heat_transfer_coeff=500.0,   # Heat transfer to environment
    ambient_temp=298.15,         # Room temperature
    pressure_drop=5000.0         # 5 kPa pressure drop
)

# Define inlet conditions
# Stream 1: Hot water
flow_1 = 10.0    # kg/s
temp_1 = 353.15  # 80°C
pres_1 = 300000  # 3 bar

# Stream 2: Cold water  
flow_2 = 15.0    # kg/s
temp_2 = 283.15  # 10°C
pres_2 = 310000  # 3.1 bar

# Stream 3: Ambient water
flow_3 = 5.0     # kg/s
temp_3 = 298.15  # 25°C
pres_3 = 305000  # 3.05 bar

# Input array: [flow_1, T_1, P_1, flow_2, T_2, P_2, flow_3, T_3, P_3]
u = np.array([flow_1, temp_1, pres_1, 
              flow_2, temp_2, pres_2,
              flow_3, temp_3, pres_3])

# Calculate steady-state outlet conditions
result = mixer.steady_state(u)
flow_out, temp_out, pres_out = result

print(f"Outlet flow rate: {flow_out:.1f} kg/s")
print(f"Outlet temperature: {temp_out:.1f} K ({temp_out-273.15:.1f}°C)")
print(f"Outlet pressure: {pres_out/1000:.1f} kPa")

# Dynamic simulation
from scipy.integrate import solve_ivp

# Initial conditions: empty mixer
x0 = np.array([0.0, 0.0])  # [mass, energy]

# Time span
t_span = (0, 60)  # 60 seconds
t_eval = np.linspace(0, 60, 100)

# Solve dynamic model
def dynamics_wrapper(t, x):
    return mixer.dynamics(t, x, u)

sol = solve_ivp(dynamics_wrapper, t_span, x0, t_eval=t_eval)

# Calculate temperature profile
mass_profile = sol.y[0]
energy_profile = sol.y[1]
cp = 4186.0  # J/kg/K

temp_profile = np.zeros_like(mass_profile)
for i, (m, e) in enumerate(zip(mass_profile, energy_profile)):
    if m > 0:
        temp_profile[i] = e / (m * cp)
    else:
        temp_profile[i] = mixer.ambient_temp

print(f"Final mixer temperature: {temp_profile[-1]:.1f} K")
```

## Applications

- **Chemical Processing**: Combining reactant streams before reactors
- **Water Treatment**: Blending water streams with different qualities
- **Food Processing**: Mixing ingredients with different temperatures
- **Pharmaceutical**: Combining API solutions with excipients
- **HVAC Systems**: Mixing hot and cold air/water streams
- **Petroleum Refining**: Combining process streams

## Design Considerations

1. **Mixing Efficiency**: Higher efficiency means better temperature homogenization
2. **Volume**: Larger volume provides more residence time for mixing
3. **Heat Transfer**: Important for temperature-sensitive processes
4. **Pressure Drop**: Must be considered for pump sizing
5. **Number of Inlets**: More inlets increase complexity but flexibility

## Engineering Notes

- The model assumes perfect mixing (no temperature or concentration gradients)
- Single-phase liquid operation only
- Constant specific heat capacity assumption
- Pressure is determined by minimum inlet pressure minus pressure drop
- Heat transfer follows Newton's law of cooling

## Related Models

- **Splitter**: For dividing streams (opposite operation)
- **Heat Exchanger**: For temperature control with separate utility streams
- **Tank**: For mixing with significant residence time and level control
