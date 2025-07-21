# ThreeWayValve Documentation

## Overview and Use Case

Three-way control valve for flow mixing (two inlets, one outlet) or diverting (one inlet, two outlets) applications in chemical processes. Enables proportional flow splitting and stream mixing control.

## Physical/Chemical Principles

**Flow Coefficient Splitting:**
- Cv_A = Cv_max × (1 - position)
- Cv_B = Cv_max × position

**Flow Calculations:**
- Each path: Q = Cv × √(ΔP/ρ)
- **Mixing**: Q_out = Q_inlet1 + Q_inlet2 (mass balance)
- **Diverting**: Q_inlet = Q_outlet1 + Q_outlet2 (mass balance)

**Position Control**: 
- position = 0: Full flow to Path A
- position = 1: Full flow to Path B
- Linear flow coefficient distribution

**Actuator Dynamics**: τ(dpos/dt) + pos = pos_cmd(t-td)

## Process Parameters

| Parameter | Typical Range | Units | Description |
|-----------|---------------|-------|-------------|
| Cv_max | 10-500 | gpm/psi^0.5 | Maximum single-path flow coefficient |
| Position | 0-1 | fraction | Flow split ratio |
| Dead Time | 0.5-5.0 | s | Actuator response delay |
| Time Constant | 1-10 | s | Actuator time constant |
| Flow Split | 0-100% | % | Percentage to each outlet |

## Operating Conditions

- **Pressure Drop**: 0.5-10 bar (50-1000 kPa) per path
- **Temperature**: -20°C to 200°C (depends on valve materials)
- **Flow Rate**: 5-500 m³/h per path
- **Fluid Density**: 800-1200 kg/m³ (typical process liquids)
- **Mixing Ratio**: 0-100% between streams

## Industrial Applications

- **Reactor Feed Mixing**: Hot/cold reactant stream blending
- **Temperature Control**: Cold bypass mixing for temperature regulation
- **Product Blending**: Ratio control for product specifications
- **Heat Exchanger Bypass**: Flow diversion for temperature control
- **Distillation Column**: Reflux distribution control
- **Waste Heat Recovery**: Stream routing for energy optimization

## Limitations and Assumptions

- **Linear flow splitting**: Equal pressure drop assumption for both paths
- **No interaction**: Flow paths assumed independent
- **Single-phase flow**: No vapor-liquid separation effects
- **Instantaneous mixing**: Perfect mixing at junction points
- **Constant properties**: Fluid properties assumed uniform
- **No cross-contamination**: Clean switching between flow paths

## Key References

1. **ANSI/ISA-75.25.01**: "Test Procedure for Control Valve Response Measurement"
2. **Engineering Equipment Users Association**: "Three-Way Control Valves - Selection and Sizing"
3. **Crane Technical Paper 410**: "Flow of Fluids Through Valves, Fittings, and Pipe"
