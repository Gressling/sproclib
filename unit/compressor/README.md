# Compressor Models

This directory contains gas compressor models for gas compression operations.

## Contents

- `__init__.py`: Contains the `Compressor` class for gas compression

## Compressor Class

Models a gas compressor with the following features:

- Isentropic compression efficiency
- Thermodynamic calculations for temperature rise
- Power requirement calculations
- Multi-component gas support via gas properties
- Dynamic response modeling

### Key Parameters
- `eta_isentropic`: Isentropic efficiency (typically 0.7-0.85)
- `P_suction`: Suction pressure (Pa)
- `P_discharge`: Discharge pressure (Pa) 
- `T_suction`: Suction temperature (K)
- `gamma`: Heat capacity ratio (Cp/Cv)
- `R`: Gas constant (J/mol·K)
- `M`: Molar mass (kg/mol)

### State Variables
- Outlet temperature

### Inputs
- Suction pressure
- Suction temperature
- Discharge pressure
- Molar flow rate

### Outputs
- Outlet temperature
- Power requirement

## Usage Example

```python
from paramus.chemistry.process_control.unit.compressor import Compressor
import numpy as np

# Create compressor for air compression
compressor = Compressor(
    eta_isentropic=0.78,         # Isentropic efficiency
    P_suction=101325,            # Atmospheric pressure (Pa)
    P_discharge=500000,          # 5 bar discharge (Pa)
    T_suction=298.15,            # Ambient temperature (K)
    gamma=1.4,                   # Air heat capacity ratio
    R=8.314,                     # Universal gas constant
    M=0.0289,                    # Air molar mass (kg/mol)
    name="AirCompressor"
)

# Steady-state calculation
u = np.array([101325, 298.15, 500000, 2.0])  # [P_suc, T_suc, P_dis, flow]
result = compressor.steady_state(u)
print(f"Outlet temperature: {result[0]:.1f} K ({result[0]-273.15:.1f} °C)")
print(f"Power required: {result[1]/1000:.1f} kW")

# Dynamic simulation
t_span = (0, 30)  # 30 seconds
x0 = np.array([298.15])  # Initial outlet temperature
result = compressor.simulate(
    t_span=t_span,
    x0=x0,
    input_func=lambda t: u
)
```

## Applications

### Process Industries
- Natural gas compression
- Refrigeration cycles
- Air compression for pneumatic systems
- Chemical process gas handling

### Power Generation
- Gas turbine cycles
- Combined cycle power plants
- Energy storage systems

### Petrochemical
- Gas processing plants
- Pipeline compression
- Refinery operations

## For Contributors

When extending compressor models:

### Additional Features to Consider:
- **Multi-stage compression** with intercooling
- **Variable speed drives** and control
- **Surge protection** and antisurge control
- **Fouling and degradation** effects
- **Vibration and mechanical** limitations
- **Different compressor types**:
  - Centrifugal compressors
  - Reciprocating compressors
  - Rotary screw compressors
  - Axial compressors

### Thermodynamic Enhancements:
- Real gas equations of state (e.g., Peng-Robinson)
- Variable gas properties with temperature
- Multi-component gas mixtures
- Heat transfer effects during compression

### Control System Integration:
- Antisurge control logic
- Load sharing between multiple compressors
- Process optimization strategies
- Energy efficiency monitoring

### Example Extension Structure:
```
unit/compressor/
├── __init__.py              # Base Compressor class
├── centrifugal/            # Centrifugal compressor models
├── reciprocating/          # Reciprocating compressor models
├── rotary_screw/           # Rotary screw compressor models
└── multi_stage/            # Multi-stage compression systems
```
