# PipeFlow Class Documentation

## Overview

The `PipeFlow` class is a comprehensive model for simulating liquid flow through pipes in process control systems. It implements both steady-state and dynamic flow calculations using fundamental fluid mechanics principles, including the Darcy-Weisbach equation for pressure loss calculations.

## Scientific Background

### Pipe Flow Fundamentals

Pipe flow is one of the most fundamental problems in fluid mechanics and engineering. The flow of liquids through pipes is governed by several key principles:

1. **Conservation of Mass (Continuity Equation)**: The mass flow rate remains constant for incompressible flow in a pipe of constant cross-section.

2. **Conservation of Momentum**: Applied through the Navier-Stokes equations, which for pipe flow reduce to simpler forms depending on flow regime.

3. **Energy Conservation**: Expressed through the mechanical energy balance equation, accounting for kinetic energy, potential energy, and friction losses.

### Darcy-Weisbach Equation

The primary equation used for pressure loss calculations is the Darcy-Weisbach equation:

```
ΔP = f × (L/D) × (ρ × v²)/2
```

Where:
- ΔP = Pressure loss [Pa]
- f = Darcy friction factor [-]
- L = Pipe length [m]
- D = Pipe diameter [m]
- ρ = Fluid density [kg/m³]
- v = Average fluid velocity [m/s]

### Friction Factor Calculation

The friction factor depends on the Reynolds number and pipe roughness:

**Reynolds Number:**
```
Re = (ρ × v × D) / μ
```

**Friction Factor Correlations:**
- **Laminar flow (Re < 2300)**: f = 64/Re
- **Turbulent flow (Re > 4000)**: Colebrook-White equation or approximations
- **Transition region (2300 < Re < 4000)**: Interpolation methods

### Dynamic Flow Modeling

The dynamic model accounts for fluid inertia and compressibility effects using:

```
dQ/dt = (A/ρL) × [ΔP - f × (L/D) × (ρ × v × |v|)/2]
```

This represents the momentum equation for unsteady flow in pipes.

## Use Cases

### Industrial Applications

1. **Chemical Process Plants**
   - Reactor feed lines
   - Product transfer lines
   - Cooling water systems
   - Chemical feed systems

2. **Water Treatment Facilities**
   - Raw water intake lines
   - Treated water distribution
   - Chemical dosing lines
   - Backwash systems

3. **Oil and Gas Industry**
   - Crude oil transport
   - Refined product pipelines
   - Process unit interconnections
   - Utility systems

4. **Pharmaceutical Manufacturing**
   - Clean-in-place (CIP) systems
   - Product transfer lines
   - Buffer and media distribution
   - Waste handling systems

### Process Control Applications

- **Flow Control Loops**: Modeling the process dynamics for controller tuning
- **Pressure Management**: Predicting pressure drops for pump sizing
- **System Design**: Optimizing pipe diameters and layouts
- **Operational Monitoring**: Real-time performance assessment
- **Safety Systems**: Emergency shutdown and relief system design

## Class Structure

### Main Class: `PipeFlow`

The primary class inheriting from `ProcessModel` that encapsulates all pipe flow functionality.

#### Key Parameters

| Parameter | Unit | Description | Typical Range |
|-----------|------|-------------|---------------|
| `pipe_length` | m | Total pipe length | 1-10000 |
| `pipe_diameter` | m | Internal pipe diameter | 0.01-2.0 |
| `roughness` | m | Pipe wall roughness | 1e-6 to 1e-3 |
| `fluid_density` | kg/m³ | Fluid density | 500-2000 |
| `fluid_viscosity` | Pa·s | Dynamic viscosity | 1e-6 to 1e-1 |
| `elevation_change` | m | Height difference (outlet-inlet) | -1000 to 1000 |
| `flow_nominal` | m³/s | Design flow rate | 1e-6 to 10 |

#### Key Methods

1. **`steady_state(flow_rate)`**
   - Calculates steady-state pressure drop and flow conditions
   - Returns pressure loss, Reynolds number, friction factor, and velocity
   - Uses iterative methods for turbulent flow calculations

2. **`dynamics(flow_rate, time_step)`**
   - Simulates dynamic flow response to changes
   - Includes fluid inertia effects
   - Returns time-dependent flow variables

3. **`describe()`**
   - Provides comprehensive metadata about the model
   - Returns algorithm information, parameters, and equations
   - Useful for documentation and introspection

### Static Methods

- **`describe_steady_state()`**: Metadata for steady-state calculations
- **`describe_dynamics()`**: Metadata for dynamic simulations

## Mathematical Models

### Steady-State Model

The steady-state model solves the following system:

1. **Continuity**: Q = A × v
2. **Momentum**: ΔP = f × (L/D) × (ρ × v²)/2 + ρ × g × Δh
3. **Friction factor**: f = f(Re, ε/D)

### Dynamic Model

The dynamic model uses a simplified momentum equation:

```
L × dv/dt = (ΔP_applied - ΔP_friction - ΔP_gravity) / ρ
```

This is integrated numerically to predict transient behavior.

## Implementation Details

### Algorithm Features

- **Robust friction factor calculation** with automatic regime detection
- **Numerical stability** through adaptive time stepping
- **Physical constraints** enforcement (positive pressures, realistic velocities)
- **Error handling** for extreme conditions
- **Unit consistency** checking

### Computational Methods

- **Newton-Raphson iteration** for implicit friction factor calculation
- **Explicit Euler integration** for dynamic simulations
- **Adaptive convergence criteria** based on engineering accuracy requirements

## Validation and Testing

The model has been validated against:

1. **Analytical solutions** for laminar flow
2. **Experimental data** from pipe flow literature
3. **Commercial software** results (HYSYS, Aspen Plus)
4. **Industry benchmarks** for common configurations

Test coverage includes:
- Edge cases (very low/high Reynolds numbers)
- Physical consistency checks
- Numerical stability verification
- Parameter sensitivity analysis

## Scientific References

1. **Moody, L.F.** (1944). "Friction factors for pipe flow." *Transactions of the ASME*, 66(8), 671-684.
   - Classic reference for friction factor correlations and the famous Moody diagram

2. **Colebrook, C.F.** (1939). "Turbulent flow in pipes, with particular reference to the transition region between smooth and rough pipe laws." *Journal of the Institution of Civil Engineers*, 11(4), 133-156.
   - Fundamental work on friction factor calculation for turbulent flow

3. **White, F.M.** (2015). *Fluid Mechanics*, 8th Edition. McGraw-Hill Education.
   - Comprehensive textbook covering pipe flow theory and applications

4. **Streeter, V.L., Wylie, E.B., & Bedford, K.W.** (1997). *Fluid Mechanics*, 9th Edition. WCB/McGraw-Hill.
   - Detailed treatment of unsteady flow in pipes and water hammer phenomena

5. **Crane Company** (1988). *Flow of Fluids Through Valves, Fittings, and Pipe*. Technical Paper No. 410.
   - Industry standard reference for practical pipe flow calculations

6. **Blevins, R.D.** (1984). *Applied Fluid Dynamics Handbook*. Van Nostrand Reinhold.
   - Practical handbook with numerous pipe flow examples and correlations

## Related Wikipedia Articles

- [Pipe Flow](https://en.wikipedia.org/wiki/Pipe_flow)
- [Darcy-Weisbach Equation](https://en.wikipedia.org/wiki/Darcy%E2%80%93Weisbach_equation)
- [Reynolds Number](https://en.wikipedia.org/wiki/Reynolds_number)
- [Friction Factor](https://en.wikipedia.org/wiki/Friction_factor)
- [Fluid Dynamics](https://en.wikipedia.org/wiki/Fluid_dynamics)

## Example Usage

```python
# Create a pipe flow model
pipe = PipeFlow(
    pipe_length=100.0,      # 100 m pipe
    pipe_diameter=0.1,      # 10 cm diameter
    roughness=0.046e-3,     # Commercial steel
    fluid_density=1000.0,   # Water
    fluid_viscosity=1e-3,   # Water at 20°C
    elevation_change=10.0   # 10 m elevation gain
)

# Steady-state calculation
flow_rate = 0.01  # 10 L/s
results = pipe.steady_state(flow_rate)
print(f"Pressure drop: {results['pressure_loss']:.1f} Pa")

# Dynamic simulation
dt = 0.1  # 0.1 second time step
dynamic_results = pipe.dynamics(flow_rate, dt)

# Get model information
info = pipe.describe()
print(f"Model: {info['model_type']}")
```

## Limitations and Assumptions

1. **Incompressible flow**: Suitable for liquids, not gases at high velocities
2. **Fully developed flow**: Entrance effects are neglected
3. **Smooth pipe assumption**: For complex geometries, use equivalent roughness
4. **Newtonian fluids**: Non-Newtonian behavior requires specialized models
5. **Single-phase flow**: Gas-liquid mixtures need multiphase models

## Future Enhancements

- **Non-Newtonian fluid support**
- **Heat transfer coupling**
- **Multiphase flow capabilities**
- **Advanced turbulence models**
- **Real-time optimization features**
