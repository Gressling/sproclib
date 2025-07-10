# PneumaticConveying Model Documentation

## Overview

The PneumaticConveying class models the transport of solid particles through pipes using pressurized air flow. This system is widely used in industries for moving powders, granules, and other bulk materials over long distances with minimal contamination.

## Use Case

Pneumatic conveying systems are used for:
- Powder transport in pharmaceutical manufacturing
- Grain handling in food processing
- Chemical powder conveying
- Plastic pellet transport
- Cement and fly ash handling
- Waste material transport
- Clean room material handling

## Algorithm Description

The PneumaticConveying model implements:

1. **Particle Terminal Velocity**: Based on drag force calculations
2. **Slip Velocity**: Difference between air and particle velocities
3. **Pressure Drop Calculation**: Air-only plus particle loading effects
4. **Two-Phase Flow**: Air-particle mixture transport dynamics

### Particle Motion Analysis

Particle terminal velocity calculation:
```
F_drag = (1/2) × ρ_air × C_d × A_particle × (v_air - v_particle)²
F_gravity = m_particle × g
v_terminal = sqrt(4 × g × d_particle × (ρ_particle - ρ_air) / (3 × C_d × ρ_air))
```

### Pressure Drop Model

Total pressure drop consists of:
1. **Air-only pressure drop** (Darcy-Weisbach equation)
2. **Particle acceleration pressure drop**
3. **Additional friction due to particles**

```
ΔP_total = ΔP_air + ΔP_acceleration + ΔP_friction
ΔP_air = f × (L/D) × (ρ_air × v_air²) / 2
ΔP_acceleration = μ_s × ρ_air × v_air²
ΔP_friction = empirical_factor × μ_s × ΔP_air
```

### Dynamic Model

The model considers:
- Pressure response: `τ_pressure = 3.0 s`
- Particle velocity response: based on particle relaxation time

## Parameters

| Parameter | Unit | Description | Typical Range |
|-----------|------|-------------|---------------|
| pipe_length | m | Conveying line length | 10-500 |
| pipe_diameter | m | Pipe diameter | 0.025-0.5 |
| particle_density | kg/m³ | Particle density | 500-5000 |
| particle_diameter | m | Average particle diameter | 10e-6-5e-3 |
| air_density | kg/m³ | Air density | 1.0-1.5 |
| air_viscosity | Pa·s | Air viscosity | 15e-6-25e-6 |
| conveying_velocity | m/s | Air velocity | 10-40 |
| solid_loading_ratio | - | Solid/air mass ratio | 1-50 |

## Inputs and Outputs

### Inputs
- **P_inlet** (Pa): Inlet pressure
- **air_flow_rate** (kg/s): Air mass flow rate
- **solid_mass_flow** (kg/s): Solid mass flow rate

### Outputs
- **P_outlet** (Pa): Outlet pressure
- **particle_velocity** (m/s): Average particle velocity

## Working Ranges

- **Conveying Velocity**: 10-40 m/s (dilute phase), 3-10 m/s (dense phase)
- **Solid Loading Ratio**: 1-50 (higher ratios for dense phase)
- **Particle Size**: 10 μm - 5 mm
- **Pipe Diameter**: 25-500 mm

## Transport Modes

### Dilute Phase (Suspension Flow)
- High air velocity (15-40 m/s)
- Low solid loading ratio (1-15)
- Particles fully suspended
- Lower pressure requirements

### Dense Phase (Plug Flow)
- Lower air velocity (3-10 m/s)
- High solid loading ratio (15-50)
- Particle plugs move through pipe
- Higher pressure requirements

## Equations

### Reynolds Number
```
Re = ρ_air × v_air × d_particle / μ_air
```

### Drag Coefficient
```
C_d = 24/Re + 6/(1+√Re) + 0.4  (general correlation)
```

### Friction Factor (smooth pipes)
```
f = 0.316 / Re^0.25  (turbulent flow)
```

### Particle Relaxation Time
```
τ_p = ρ_particle × d_particle² / (18 × μ_air)
```

### Minimum Transport Velocity
```
v_min = sqrt(gD × (ρ_particle - ρ_air) / ρ_air) × factor
```

## Literature References

1. Mills, D. "Pneumatic Conveying Design Guide." 3rd Edition, Butterworth-Heinemann, 2016.
2. Klinzing, G.E., Marcus, R.D., Rizk, F., and Leung, L.S. "Pneumatic Conveying of Solids." 3rd Edition, Springer, 2010.
3. Wypych, P.W. "Pneumatic Conveying of Bulk Solids." Blackwell Publishing, 2009.
4. Reed, A.R. "An Investigation of Numerical Methods for Predicting Pneumatic Conveying Characteristics." PhD Thesis, Thames Polytechnic, 1993.
5. Konrad, K. "Dense-Phase Pneumatic Conveying: A Review." Powder Technology, 49(1):1-35, 1986.

## Usage Guidelines

### System Design
- Select conveying velocity based on material properties
- Ensure adequate pipe diameter for flow regime
- Consider particle degradation during transport
- Design for easy maintenance and cleaning
- Include pressure monitoring and control

### Material Considerations
- **Free-flowing powders**: Suitable for both dilute and dense phase
- **Cohesive materials**: May require special handling
- **Abrasive particles**: Consider pipe wear
- **Fragile materials**: Use lower velocities

### Operational Guidelines
- Start with dilute phase for new materials
- Monitor pressure drop for system optimization
- Regular pipe inspection for wear
- Maintain proper air drying for hygroscopic materials
- Consider static electricity effects

### Applications by Industry
- **Pharmaceutical**: API powder transfer
- **Food**: Flour, sugar, grain transport
- **Chemical**: Catalyst and additive handling
- **Plastics**: Pellet and powder conveying
- **Power**: Fly ash and coal dust handling

### Limitations
- Model assumes spherical particles
- Dilute phase transport only
- No particle agglomeration effects
- Steady-state flow assumption
- No electrostatic considerations
