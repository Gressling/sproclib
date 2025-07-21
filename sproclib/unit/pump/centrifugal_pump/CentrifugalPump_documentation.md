# CentrifugalPump Documentation

## Overview and Use Case
The CentrifugalPump class models centrifugal pumps with realistic quadratic head-flow characteristics. It accounts for the fundamental behavior where pump head decreases with increasing flow rate, making it suitable for variable flow applications in chemical processes.

## Physical/Chemical Principles
Centrifugal pumps operate on the principle of centrifugal force and momentum transfer:

**Pump Curve Equation:**
H = H₀ - K × Q² (m)

**Euler's Pump Equation:**
H = (u₂²/g) - (u₁²/g) + (C₂u₂ - C₁u₁)/g

**Pressure-Head Relationship:**
ΔP = ρ × g × H (Pa)

**Affinity Laws for Speed Changes:**
- Q₂/Q₁ = N₂/N₁
- H₂/H₁ = (N₂/N₁)²
- P₂/P₁ = (N₂/N₁)³

**Specific Speed:**
Ns = N × √Q / H^(3/4)

## Process Parameters
| Parameter | Symbol | Typical Range | Units | Description |
|-----------|--------|---------------|-------|-------------|
| Shutoff Head | H₀ | 10 - 200 | m | Head at zero flow |
| Head Coefficient | K | 1 - 500 | s²/m⁵ | Quadratic curve steepness |
| Efficiency | η | 0.3 - 0.85 | dimensionless | Peak efficiency point |
| Specific Speed | Ns | 10 - 200 | dimensionless | Impeller design parameter |
| Flow Rate | Q | 0.001 - 5 | m³/s | Operating flow range |

## Operating Conditions
- **Best Efficiency Point (BEP):** 70-90% of shutoff flow
- **Operating Range:** 50-120% of BEP flow for stable operation
- **Minimum Flow:** 10-20% of BEP to prevent overheating
- **Maximum Head:** Limited by shutoff head (H₀)
- **NPSH Available > NPSH Required** to prevent cavitation
- **Temperature:** -20°C to 150°C depending on materials
- **Pressure:** Suction pressure limited by NPSH requirements

## Industrial Applications
- **Water Treatment Plants:** Raw water intake, high service pumps, backwash pumps
- **Chemical Processing:** Process circulation, cooling water, reactor feed pumps
- **Power Generation:** Boiler feedwater pumps, circulating water pumps, condensate pumps
- **Oil & Gas:** Pipeline pumps, crude oil transfer, refinery process pumps
- **Municipal Systems:** Water distribution, wastewater treatment, irrigation systems
- **HVAC Systems:** Chilled water pumps, hot water circulation, cooling tower pumps

## Limitations and Assumptions
- Quadratic approximation of actual pump curve
- Constant speed operation (no VFD modeling)
- Single impeller design assumptions
- Newtonian fluid behavior only
- No cavitation effects included
- Constant efficiency across operating range
- No pump surge or instability modeling
- Single-phase liquid operation only

## Key References
1. **Gülich, J.F.** "Centrifugal Pumps, 3rd Edition" Springer, 2014 - Comprehensive pump theory
2. **Karassik, I.J.** "Pump Handbook, 4th Edition" McGraw-Hill, 2008 - Industry standard reference
3. **Stepanoff, A.J.** "Centrifugal and Axial Flow Pumps, 2nd Edition" Wiley, 1957 - Classical pump design
