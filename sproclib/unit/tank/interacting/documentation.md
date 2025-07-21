# InteractingTanks Model Documentation

## Overview

The InteractingTanks class implements a two-tank system in series where the outlet of the first tank feeds the second tank. This configuration is widely used in process control education and industrial applications to study multi-variable dynamics and control strategies.

## Use Cases

- **Process Dynamics Studies**: Understanding second-order system behavior
- **Multi-variable Control**: Design of MIMO control systems
- **Educational Demonstrations**: Teaching advanced process control concepts
- **Industrial Applications**: Cascade tank systems, wastewater treatment

## Algorithm

The interacting tanks model consists of two coupled material balance equations:

**Tank 1:**
```
A1 * dh1/dt = q_in - q12
```

**Tank 2:**
```
A2 * dh2/dt = q12 - q_out
```

Where the inter-tank flow and outlet flow follow Torricelli's law:
```
q12 = C1 * sqrt(h1)
q_out = C2 * sqrt(h2)
```

## Mathematical Model

### State Variables
- `h1`: Tank 1 height [m]
- `h2`: Tank 2 height [m]

### Input Variables
- `q_in`: Inlet flow rate to tank 1 [m³/min]

### Parameters
- `A1`: Tank 1 cross-sectional area [m²]
- `A2`: Tank 2 cross-sectional area [m²]
- `C1`: Tank 1 discharge coefficient [m²/min]
- `C2`: Tank 2 discharge coefficient [m²/min]

### Governing Equations

**Tank 1 dynamics:**
```
dh1/dt = (q_in - C1*sqrt(h1))/A1
```

**Tank 2 dynamics:**
```
dh2/dt = (C1*sqrt(h1) - C2*sqrt(h2))/A2
```

**Inter-tank flow:**
```
q12 = C1*sqrt(h1)
```

**Outlet flow:**
```
q_out = C2*sqrt(h2)
```

**Steady-state heights:**
```
h1_ss = (q_in/C1)²
h2_ss = (q_in/C2)²
```

## Transfer Function Analysis

For small perturbations around steady-state, the system can be linearized to:

**Tank 1 time constant:**
```
τ1 = 2*A1*sqrt(h1_ss)/C1
```

**Tank 2 time constant:**
```
τ2 = 2*A2*sqrt(h2_ss)/C2
```

**Overall transfer function (h2/q_in):**
```
G(s) = K / ((τ1*s + 1)(τ2*s + 1))
```

Where K is the overall process gain.

## Parameters and Working Ranges

### Cross-sectional Areas (A1, A2)
- **Range**: 0.1 - 10 m²
- **Typical**: 1.0 m²
- **Effect**: Larger areas increase time constants

### Discharge Coefficients (C1, C2)
- **Range**: 0.01 - 1.0 m²/min
- **Typical**: 0.1 - 0.5 m²/min
- **Effect**: Higher values decrease time constants

### Operating Ranges
- **Heights**: 0 - 10 m
- **Flow rates**: 0 - 5 m³/min
- **Time constants**: 2 - 200 min (typical)

## System Characteristics

### Process Gain
The steady-state gain from inlet flow to tank 2 level:
```
K = 4*h2_ss/q_in_ss = 4/C2²
```

### Time Constants
- **Fast tank**: min(τ1, τ2)
- **Slow tank**: max(τ1, τ2)
- **Dominant pole**: Usually the slower tank

### Interaction Effects
- Strong interaction when τ1 ≈ τ2
- Weak interaction when τ1 >> τ2 or τ1 << τ2

## Implementation Notes

### Numerical Considerations
- Both heights constrained to non-negative values
- Square root functions require h1, h2 ≥ 0
- All discharge coefficients should be positive

### Physical Assumptions
- Incompressible fluid
- Constant cross-sectional areas
- Gravity-driven discharge
- Perfect mixing in each tank
- Negligible pipe dynamics between tanks
- Turbulent flow through outlets

### Limitations
- Cannot model negative tank heights
- Assumes constant discharge coefficients
- Does not account for pipe pressure drops
- Neglects fluid acceleration effects

## Control System Design

### SISO Control
- **Primary**: Control h2 with q_in
- **Secondary**: Control h1 with intermediate manipulator

### MIMO Control
- **Inputs**: [q_in, q_intermediate] (if available)
- **Outputs**: [h1, h2]
- **Coupling**: Moderate to strong depending on time constant ratio

### Controller Tuning Guidelines
For h2 control with q_in input:
- **Proportional gain**: Kc = 1/(K*(τ1 + τ2))
- **Integral time**: Ti = τ1 + τ2
- **Derivative time**: Td = τ1*τ2/(τ1 + τ2)

## Literature References

1. Seborg, D.E., Edgar, T.F., Mellichamp, D.A., & Doyle III, F.J. (2016). *Process Dynamics and Control* (4th ed.). Wiley.

2. Stephanopoulos, G. (1984). *Chemical Process Control: An Introduction to Theory and Practice*. Prentice Hall.

3. Astrom, K.J., & Hagglund, T. (2006). *Advanced PID Control*. ISA Press.

4. Luyben, W.L. (1990). *Process Modeling, Simulation, and Control for Chemical Engineers* (2nd ed.). McGraw-Hill.

5. Marlin, T.E. (2000). *Process Control: Designing Processes and Control Systems for Dynamic Performance* (2nd ed.). McGraw-Hill.

## Industrial Applications

### Water Treatment
- Multi-stage clarifiers
- Sequential treatment tanks
- pH neutralization systems

### Chemical Processing
- Reactor cascades
- Crystallization trains
- Separation sequences

### Wastewater Treatment
- Aeration basins
- Settling tank sequences
- Biological treatment stages

## Advanced Topics

### Optimal Design
- Tank sizing for desired dynamics
- Discharge coefficient selection
- Area ratio optimization

### Nonlinear Control
- Feedback linearization
- Model predictive control
- Adaptive control strategies
