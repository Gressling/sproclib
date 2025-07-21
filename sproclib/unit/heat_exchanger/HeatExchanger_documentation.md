# HeatExchanger Documentation

## Overview and Use Case

The HeatExchanger class models counter-current shell-and-tube heat exchangers using the effectiveness-NTU method. This model is used for process heating, cooling, heat recovery, and thermal management in chemical plants.

## Physical/Chemical Principles

**Effectiveness-NTU Method:**
- Effectiveness: ε = (1-exp(-NTU(1-Cr)))/(1-Cr*exp(-NTU(1-Cr))) for counter-current flow
- Number of Transfer Units: NTU = UA/Cmin
- Heat capacity rate ratio: Cr = Cmin/Cmax
- Heat transfer rate: Q = ε × Cmin × (Th,in - Tc,in)

**Thermal Dynamics:**
- First-order dynamics: τ × dT/dt = Tss - T
- Thermal time constant: τ = ρVcp/C
- Log Mean Temperature Difference: LMTD = (ΔT1 - ΔT2)/ln(ΔT1/ΔT2)

## Process Parameters

| Parameter | Typical Range | Units | Description |
|-----------|---------------|-------|-------------|
| U | 100-2000 | W/m²·K | Overall heat transfer coefficient |
| A | 1-500 | m² | Heat transfer area |
| m_hot | 0.1-50 | kg/s | Hot fluid mass flow rate |
| m_cold | 0.1-50 | kg/s | Cold fluid mass flow rate |
| cp | 1000-5000 | J/kg·K | Specific heat capacity |
| ρ | 500-1500 | kg/m³ | Fluid density |
| Effectiveness | 0.1-0.95 | - | Thermal effectiveness |
| NTU | 0.5-10 | - | Number of Transfer Units |

## Operating Conditions

**Typical Industrial Conditions:**
- Hot fluid inlet: 60-200°C (333-473 K)
- Cold fluid inlet: 10-80°C (283-353 K)
- Pressure: 1-20 bar (1×10⁵-2×10⁶ Pa)
- Flow rates: 0.5-100 kg/s depending on application
- Residence time: 10-300 seconds

**Design Considerations:**
- Temperature approach: 5-20 K minimum
- Velocity: 0.5-3 m/s (shell side), 1-5 m/s (tube side)
- Pressure drop: <10% of operating pressure

## Industrial Applications

**Process Industries:**
- Oil refinery heat integration (crude preheat, product cooling)
- Chemical reactor feed/product heat exchange
- Distillation column condensers and reboilers
- Gas processing (cooling, heating, heat recovery)

**Power Generation:**
- Steam condensers
- Feedwater heating
- Cooling water systems

**HVAC Systems:**
- Building heating/cooling
- Heat recovery ventilation

## Limitations and Assumptions

**Physical Constraints:**
- Constant fluid properties (cp, ρ, μ)
- No phase change during heat transfer
- Counter-current flow configuration only
- Negligible heat losses to environment
- Uniform temperature distribution across flow cross-section

**Modeling Limitations:**
- Lumped thermal capacitance (no spatial temperature gradients)
- Linear heat transfer coefficient (no temperature dependence)
- No fouling resistance modeling
- Pressure drop effects neglected

## Key References

1. Incropera, F.P. & DeWitt, D.P. "Fundamentals of Heat and Mass Transfer", 7th Ed., Wiley (2011)
2. Shah, R.K. & Sekulic, D.P. "Fundamentals of Heat Exchanger Design", Wiley (2003)
3. Perry's Chemical Engineers' Handbook, 8th Ed., McGraw-Hill (2008) - Heat Transfer Section
