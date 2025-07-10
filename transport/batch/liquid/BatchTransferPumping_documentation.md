# Batch Transfer Pumping Documentation

## Overview

The `BatchTransferPumping` class models batch liquid transfer operations using pumps, incorporating pump characteristics, system hydraulics, and fluid dynamics. This model is essential for batch processing operations where liquids need to be transferred from one tank to another in discrete quantities.

## Use Case

Batch transfer pumping is commonly used in:
- Chemical batch processing plants
- Pharmaceutical manufacturing
- Food and beverage production
- Water treatment facilities
- Laboratory-scale operations

The model helps predict transfer times, optimize pump sizing, and ensure proper system design for efficient batch operations.

## Algorithm Description

The model implements two main calculation modes:

### Steady-State Algorithm
1. **Hydraulic Head Calculation**: Determines static head based on level difference
2. **Flow Rate Estimation**: Uses pump curve with speed and efficiency factors
3. **System Resistance**: Calculates friction losses using Darcy-Weisbach equation
4. **Flow Rate Adjustment**: Reduces flow if pump head is insufficient
5. **Transfer Time Prediction**: Estimates remaining transfer time based on volume and flow rate

### Dynamic Algorithm
1. **Pump Response Dynamics**: Models pump startup/shutdown with time constant
2. **Tank Level Dynamics**: Implements mass balance for source tank
3. **Flow Rate Evolution**: Tracks flow rate changes over time
4. **System Constraints**: Enforces physical limits (empty tank stops flow)

## Parameters

| Parameter | Unit | Range | Description |
|-----------|------|-------|-------------|
| pump_capacity | m³/s | 0.001 - 0.1 | Maximum pump flow capacity at rated conditions |
| pump_head_max | m | 10 - 100 | Maximum pump head at zero flow |
| tank_volume | m³ | 0.1 - 10 | Source tank volume for batch calculations |
| pipe_length | m | 1 - 100 | Transfer line length affecting friction |
| pipe_diameter | m | 0.01 - 0.2 | Transfer line internal diameter |
| fluid_density | kg/m³ | 500 - 2000 | Fluid density at operating temperature |
| fluid_viscosity | Pa·s | 1e-6 - 1e-1 | Dynamic viscosity at operating temperature |
| transfer_efficiency | - | 0.5 - 0.95 | Overall pump transfer efficiency |

## Mathematical Equations

### Reynolds Number
```
Re = ρ * v * D / μ
```
Where:
- ρ = fluid density [kg/m³]
- v = fluid velocity [m/s]
- D = pipe diameter [m]
- μ = dynamic viscosity [Pa·s]

### Friction Factor
For laminar flow (Re < 2300):
```
f = 64 / Re
```

For turbulent flow (Re ≥ 2300):
```
f = 0.316 / Re^0.25
```

### Friction Head Loss
```
h_f = f * (L/D) * (v²/2g)
```
Where:
- L = pipe length [m]
- g = gravitational acceleration [m/s²]

### Total Head Required
```
H_total = H_static + H_friction
```

### Mass Balance (Dynamic)
```
dV/dt = Q_in - Q_out
```

### Pump Characteristic
```
Q = Q_max * speed_fraction * efficiency
```

## Working Ranges

### Flow Conditions
- **Reynolds Number**: 10 - 100,000 (laminar to turbulent)
- **Velocity**: 0.1 - 5 m/s (typical industrial range)
- **Flow Rate**: 10% - 100% of pump capacity

### System Pressures
- **Static Head**: -10 to +50 m (suction to discharge)
- **Friction Losses**: 0.1 - 20 m (depending on system design)
- **Pump Operating Point**: 20% - 100% of rated head

### Operational Limits
- **Tank Level**: 5% - 95% of tank height
- **Transfer Time**: 1 minute - 8 hours typical
- **Temperature**: 5°C - 80°C (affects fluid properties)

## Usage Guidelines

1. **Parameter Selection**: Choose pump capacity 20-30% above required flow rate
2. **Pipe Sizing**: Maintain velocity between 1-3 m/s for efficiency
3. **Head Calculations**: Include safety factor of 10-20% for head requirements
4. **Dynamic Response**: Consider pump time constant for control system design

## Literature References

1. Perry, R.H., Green, D.W. (2019). "Perry's Chemical Engineers' Handbook", 9th Edition, McGraw-Hill.
2. Crane Co. (2013). "Flow of Fluids Through Valves, Fittings, and Pipe", Technical Paper 410.
3. Karassik, I.J., et al. (2008). "Pump Handbook", 4th Edition, McGraw-Hill.
4. Coulson, J.M., Richardson, J.F. (2017). "Chemical Engineering Design", Volume 6, 5th Edition.
5. Sinnott, R., Towler, G. (2019). "Chemical Engineering Design", 6th Edition, Butterworth-Heinemann.
6. White, F.M. (2016). "Fluid Mechanics", 8th Edition, McGraw-Hill.
7. Munson, B.R., et al. (2016). "Fundamentals of Fluid Mechanics", 8th Edition, Wiley.
