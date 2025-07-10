# Tank Model Documentation

## Overview

The Tank class implements a gravity-drained tank model based on material balance principles and Torricelli's law. This model is fundamental in process control applications, particularly for level control systems and process dynamics studies.

## Use Cases

- **Level Control Systems**: Primary building block for tank level control applications
- **Process Dynamics Studies**: Understanding first-order nonlinear system behavior
- **Controller Tuning**: Provides realistic plant dynamics for PID and advanced controller design
- **Educational Demonstrations**: Teaching process control fundamentals

## Algorithm

The tank model is based on a material balance around the tank volume:

```
Accumulation = Inflow - Outflow
A * dh/dt = q_in - q_out
```

The outlet flow follows Torricelli's law for gravity discharge:
```
q_out = C * sqrt(h)
```

Combining these equations yields the fundamental tank dynamics:
```
dh/dt = (q_in - C * sqrt(h)) / A
```

## Mathematical Model

### State Variables
- `h`: Tank height [m]

### Input Variables  
- `q_in`: Inlet flow rate [m³/min]

### Parameters
- `A`: Cross-sectional area [m²]
- `C`: Discharge coefficient [m²/min]

### Governing Equations

**Dynamic equation:**
```
dh/dt = (q_in - C*sqrt(h))/A
```

**Outlet flow:**
```
q_out = C*sqrt(h)
```

**Tank volume:**
```
V = A*h
```

**Steady-state height:**
```
h_ss = (q_in/C)²
```

**Linearized time constant:**
```
τ = 2*A*sqrt(h)/C
```

## Parameters and Working Ranges

### Cross-sectional Area (A)
- **Range**: 0.1 - 10 m²
- **Typical**: 1.0 m²
- **Effect**: Larger area reduces response speed

### Discharge Coefficient (C)
- **Range**: 0.01 - 1.0 m²/min
- **Typical**: 0.1 - 0.5 m²/min
- **Effect**: Higher values increase discharge rate and reduce steady-state height

### Operating Ranges
- **Height**: 0 - 10 m
- **Flow rate**: 0 - 5 m³/min
- **Time constant**: 1 - 100 min (typical)

## Implementation Notes

### Numerical Considerations
- Height is constrained to non-negative values
- Square root function requires h ≥ 0
- Discharge coefficient should be positive

### Physical Assumptions
- Incompressible fluid
- Constant cross-sectional area
- Gravity-driven discharge
- Turbulent flow through outlet (Reynolds number > 4000)
- Negligible fluid acceleration effects

### Limitations
- Cannot model negative tank heights
- Assumes constant discharge coefficient
- Does not account for varying cross-sections
- Neglects entrance/exit losses in detail

## Literature References

1. Seborg, D.E., Edgar, T.F., Mellichamp, D.A., & Doyle III, F.J. (2016). *Process Dynamics and Control* (4th ed.). Wiley.

2. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.

3. Luyben, W.L. (1990). *Process Modeling, Simulation, and Control for Chemical Engineers* (2nd ed.). McGraw-Hill.

4. Ogunnaike, B.A., & Ray, W.H. (1994). *Process Dynamics, Modeling, and Control*. Oxford University Press.

5. Bequette, B.W. (2003). *Process Control: Modeling, Design, and Simulation*. Prentice Hall.

## Typical Applications in Industry

### Water Treatment
- Clarifier tanks
- Storage tanks
- Equalization basins

### Chemical Processing
- Reactor vessels
- Buffer tanks
- Settling tanks

### Petroleum Refining
- Surge tanks
- Product storage
- Separation vessels

## Control System Design

### PID Controller Tuning
The linearized time constant τ = 2*A*sqrt(h)/C provides guidance for controller tuning:
- **Proportional gain**: Start with Kc = 1/τ
- **Integral time**: Ti = τ
- **Derivative time**: Td = τ/4

### Process Characteristics
- **Process gain**: Kp = 2*sqrt(h_ss)/C
- **Dead time**: Typically negligible for well-mixed tanks
- **Nonlinearity**: Moderate due to square root relationship
