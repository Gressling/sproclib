# ScrewFeeder Model Documentation

## Overview

The ScrewFeeder class models volumetric feeding systems using rotating screws for precise powder and granular material dosing. This model is essential for applications requiring accurate flow rate control and consistent material delivery.

## Use Case

Screw feeders are widely used in:
- Pharmaceutical powder dosing
- Food ingredient feeding systems
- Chemical process control
- Plastic extrusion feeding
- Coal and biomass feeding
- Additive manufacturing material handling
- Batch weighing systems
- Continuous blending operations

## Algorithm Description

The ScrewFeeder model implements:

1. **Volumetric Flow Calculation**: Based on screw geometry and rotational speed
2. **Fill Factor Correction**: Accounting for material properties and operating conditions
3. **Torque Calculation**: Motor load based on material resistance
4. **Dynamic Response**: Flow rate and torque response characteristics

### Volumetric Flow Model

The theoretical volumetric flow rate is:
```
V_theoretical = (N/60) × V_revolution
V_revolution = π × (D/2)² × P
```
where:
- N = screw speed (rpm)
- D = screw diameter (m)
- P = screw pitch (m)

### Effective Fill Factor

The actual flow is reduced by several factors:
```
F_effective = F_nominal × F_level × F_moisture × F_flowability
```

Fill factor corrections:
- Level factor: `F_level = min(1.0, hopper_level/critical_level)`
- Moisture factor: `F_moisture = max(0.7, 1.0 - 2.0 × moisture)`
- Flowability factor: based on material flow properties

### Mass Flow Rate

```
Q_mass = V_actual × ρ_bulk × F_effective
```

### Torque Calculation

Total motor torque includes:
```
T_total = T_base + T_load
T_base = constant friction torque
T_load = function(fill_factor, moisture, material_properties)
```

### Dynamic Model

Response characteristics:
- Flow response: `τ_flow = residence_time + settling_time`
- Torque response: `τ_torque = 1.0 s` (motor dynamics)

## Parameters

| Parameter | Unit | Description | Typical Range |
|-----------|------|-------------|---------------|
| screw_diameter | m | Screw diameter | 0.01-0.5 |
| screw_length | m | Screw length | 0.1-2.0 |
| screw_pitch | m | Screw pitch | 0.005-0.2 |
| screw_speed | rpm | Screw rotational speed | 10-500 |
| fill_factor | - | Nominal fill factor | 0.1-0.8 |
| powder_density | kg/m³ | Bulk powder density | 200-2000 |
| powder_flowability | - | Flowability index | 0.3-1.0 |
| motor_torque_max | N⋅m | Maximum motor torque | 1-100 |

## Inputs and Outputs

### Inputs
- **screw_speed_setpoint** (rpm): Desired screw speed
- **hopper_level** (m): Material level in hopper
- **powder_moisture** (-): Moisture content (fraction)

### Outputs
- **mass_flow_rate** (kg/s): Actual mass flow rate
- **motor_torque** (N⋅m): Motor torque requirement

## Working Ranges

- **Screw Speed**: 10-500 rpm (optimal: 50-200 rpm for most powders)
- **Fill Factor**: 0.1-0.8 (0.3-0.6 typical for good accuracy)
- **Powder Density**: 200-2000 kg/m³
- **Flowability Index**: 0.3-1.0 (1.0 = perfect flow, 0.3 = poor flow)

## Design Considerations

### Screw Geometry
- **Pitch-to-Diameter Ratio**: 0.5-1.5 (1.0 typical)
- **Length-to-Diameter Ratio**: 5-20 (longer for better mixing)
- **Flight Thickness**: 0.1-0.2 × pitch
- **Clearance**: 0.5-2.0 mm between screw and housing

### Material Properties
- **Flowability**: Affects fill factor and torque requirements
- **Particle Size**: Influences segregation and flow consistency
- **Moisture Content**: Significantly affects flow behavior
- **Bulk Density**: Determines mass flow rate

## Equations

### Theoretical Volume Flow
```
Q_vol = (π × D² × P × N) / (4 × 60)
```

### Actual Mass Flow
```
Q_mass = Q_vol × ρ_bulk × F_fill × F_corrections
```

### Residence Time
```
t_res = (60 × L_screw) / (P × N)
```

### Power Requirement
```
P_motor = T_motor × ω = T_motor × (2π × N) / 60
```

### Flow Accuracy
```
CV = σ/μ × 100%  (coefficient of variation)
```

## Literature References

1. Marinelli, J. and Carson, J.W. "Solve Solids Flow Problems in Bins, Hoppers, and Feeders." Chemical Engineering Progress, 88(5):29-35, 1992.
2. Roberts, A.W. "The Science of Screw Feeders and Screw Conveyors." Bulk Solids Handling, 19(3):285-297, 1999.
3. Schulze, D. "Powders and Bulk Solids: Behavior, Characterization, Storage and Flow." Springer, 2008.
4. Shamlou, P.A. "Handling of Bulk Solids: Theory and Practice." Butterworths, 1988.
5. Wypych, P.W. "Pneumatic Conveying of Bulk Solids." Blackwell Publishing, 2009.

## Usage Guidelines

### System Design
- Select screw diameter based on required flow rate
- Ensure adequate hopper capacity for continuous operation
- Consider material characteristics in screw selection
- Design for easy cleaning and maintenance
- Include flow rate monitoring and control

### Operational Guidelines
- Maintain consistent hopper level for accurate feeding
- Monitor motor torque for overload detection
- Regular calibration for flow rate accuracy
- Control environmental conditions (humidity, temperature)
- Prevent material segregation in hopper

### Flow Rate Control
- **Volumetric Control**: Speed-based flow rate control
- **Gravimetric Control**: Weight-based feedback control
- **Loss-in-Weight**: Continuous weight monitoring
- **Gain-in-Weight**: Batch weight accumulation

### Applications by Material Type
- **Free-flowing powders**: Standard screw design
- **Cohesive materials**: Ribbon or paddle screws
- **Fragile materials**: Low-speed, gentle handling
- **Abrasive materials**: Hardened screw surfaces
- **Hygroscopic materials**: Enclosed system design

### Accuracy Considerations
- **Flow rate range**: 10:1 typical turndown ratio
- **Accuracy**: ±1-5% for well-designed systems
- **Repeatability**: ±0.5-2% short-term variation
- **Linearity**: Flow rate vs. speed relationship

### Limitations
- Assumes uniform powder properties
- No consideration of segregation effects
- Steady-state operation assumption
- Limited to free-flowing to moderately cohesive materials
- No temperature effects on material properties
