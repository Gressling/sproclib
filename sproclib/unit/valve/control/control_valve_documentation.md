# ControlValve Documentation

## Overview and Use Case

Industrial control valve model with flow coefficient characteristics for automated flow control in chemical processes. Provides dead-time compensation and multiple valve characteristic curves for precise flow regulation.

## Physical/Chemical Principles

The control valve operates based on the fundamental valve flow equation:

**Q = Cv × √(ΔP/ρ)**

Where:
- Q = Volumetric flow rate (m³/s)
- Cv = Flow coefficient (gpm/psi^0.5) 
- ΔP = Pressure drop across valve (Pa)
- ρ = Fluid density (kg/m³)

**Valve Characteristics:**
- **Linear**: Cv = Cv_min + x(Cv_max - Cv_min), uniform flow change
- **Equal Percentage**: Cv = Cv_min × R^x, constant percentage flow change
- **Quick Opening**: Cv = Cv_min + (Cv_max - Cv_min)√x, rapid initial response

**Actuator Dynamics**: First-order lag with dead-time: τ(dpos/dt) + pos = pos_cmd(t-td)

## Process Parameters

| Parameter | Typical Range | Units | Description |
|-----------|---------------|-------|-------------|
| Cv_max | 10-500 | gpm/psi^0.5 | Maximum flow coefficient |
| Rangeability | 20-50 | - | Cv_max/Cv_min ratio |
| Dead Time | 0.5-5.0 | s | Actuator response delay |
| Time Constant | 1-10 | s | Actuator time constant |
| Position | 0-1 | fraction | Valve opening (0=closed, 1=open) |

## Operating Conditions

- **Pressure Drop**: 0.5-20 bar (50-2000 kPa)
- **Temperature**: -40°C to 400°C (process dependent)
- **Flow Rate**: 1-1000 m³/h (typical industrial range)
- **Fluid Density**: 500-2000 kg/m³ (liquids)
- **Viscosity**: 0.1-100 cP (affects Cv slightly)

## Industrial Applications

- **Flow Control Loops**: Primary/secondary flow control in chemical reactors
- **Level Control**: Tank level regulation via outlet flow manipulation
- **Pressure Control**: Downstream pressure regulation
- **Temperature Control**: Cooling/heating fluid flow control
- **Safety Systems**: Emergency shutdown valves (ESV)
- **Blending Operations**: Ratio control in product mixing

## Limitations and Assumptions

- **Single-phase flow**: No vapor-liquid mixtures or flashing
- **Incompressible fluid**: Liquid density assumed constant
- **No cavitation**: Pressure drop below vapor pressure not modeled
- **Linear actuator**: Simplified first-order + dead-time dynamics
- **Constant properties**: Fluid density and viscosity assumed constant
- **No flow reversal**: Unidirectional flow assumption

## Key References

1. **Instrument Society of America (ISA)**: "Control Valve Sizing Equations" (ISA-75.01.01)
2. **Perry's Chemical Engineers' Handbook**: Chapter 6 - Fluid and Particle Dynamics
3. **Fisher Controls**: "Control Valve Handbook" - Valve sizing and characteristics
