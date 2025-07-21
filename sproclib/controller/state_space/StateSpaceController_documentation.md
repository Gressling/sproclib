# State-Space Controller Documentation

## Overview and Use Case
Multivariable controller using state-space representation for optimal control of MIMO (Multiple Input Multiple Output) systems. Employs full state feedback with observer-based state estimation for complex process control applications.

## Physical/Chemical Principles
**State Equations**: dx/dt = Ax + Bu + Ed
**Output Equations**: y = Cx + Du + Fd
**Control Law**: u = -Kx + Nr (state feedback with reference tracking)
**Observer**: dx̂/dt = Ax̂ + Bu + L(y - Cx̂)

Where:
- x = state vector (internal process variables)
- u = input vector (manipulated variables)  
- y = output vector (measured variables)
- A = state matrix, B = input matrix, C = output matrix
- K = controller gain matrix, L = observer gain matrix

**Design Methods**:
- LQR (Linear Quadratic Regulator): Minimizes J = ∫(x'Qx + u'Ru)dt
- Pole Placement: Places closed-loop poles at desired locations

## Process Parameters
| Parameter | Description | Units | Typical Range |
|-----------|-------------|-------|---------------|
| A matrix | State dynamics | 1/s | -0.001 to -10 |
| B matrix | Input coupling | process dependent | 0.1 to 10 |
| C matrix | Output coupling | dimensionless | 0 to 1 |
| K matrix | Controller gains | process dependent | 0.1 to 100 |
| L matrix | Observer gains | process dependent | 1 to 1000 |

## Operating Conditions
- **Multi-component distillation**: 10-50 trays, 2-5 products
- **Reactor networks**: 2-10 CSTRs, temperatures 50-300°C
- **Heat exchanger networks**: 3-20 exchangers, duties 1-100 MW
- **Batch crystallization**: 100-10000 L, residence times 1-10 hours

## Industrial Applications
- **Distillation column control**: Simultaneous control of multiple product compositions using reflux, reboiler duty, and side draws
- **Reactor network optimization**: Coordinated control of CSTR temperatures, concentrations, and flow rates
- **Heat integration systems**: Optimal heat exchanger network operation with utility minimization
- **Batch process control**: Recipe execution with quality constraints for crystallization and polymerization

## Limitations and Assumptions
- Linear process behavior around operating point
- All states measurable or observable through outputs
- Constant process parameters (A, B, C matrices)
- No significant model-plant mismatch
- Requires process model identification
- Higher computational requirements than single-loop controllers

## Key References
1. Maciejowski, J.M. (2002). *Predictive Control with Constraints*. Prentice Hall.
2. Ogunnaike, B.A. & Ray, W.H. (1994). *Process Dynamics, Modeling, and Control*. Oxford University Press.
3. Rawlings, J.B., Mayne, D.Q. & Diehl, M. (2017). *Model Predictive Control: Theory, Computation, and Design*. Nob Hill Publishing.
