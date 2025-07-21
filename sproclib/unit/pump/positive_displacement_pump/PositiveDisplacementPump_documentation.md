# PositiveDisplacementPump Documentation

## Overview and Use Case
The PositiveDisplacementPump class models positive displacement pumps that deliver constant volumetric flow regardless of discharge pressure. These pumps are essential for precise metering, high-pressure applications, and handling viscous fluids in chemical processes.

## Physical/Chemical Principles
Positive displacement pumps operate by trapping fixed volumes of fluid and forcing them through the discharge:

**Volumetric Flow Equation:**
Q = η_vol × V_d × N (m³/s)

**Theoretical Displacement:**
V_d = swept volume per revolution (m³/rev)

**Slip Flow:**
Q_slip = (ΔP × clearance³) / (12μL) (for gear pumps)

**Power Relationship:**
P = Q × ΔP / η_overall

**Torque Requirement:**
T = (ΔP × V_d) / (2π × η_mech)

## Process Parameters
| Parameter | Symbol | Typical Range | Units | Description |
|-----------|--------|---------------|-------|-------------|
| Displacement | V_d | 1-1000 | cm³/rev | Volume per revolution |
| Volumetric Efficiency | η_vol | 0.85-0.98 | dimensionless | Accounts for slip |
| Mechanical Efficiency | η_mech | 0.80-0.95 | dimensionless | Friction losses |
| Overall Efficiency | η | 0.70-0.90 | dimensionless | Combined efficiency |
| Maximum Pressure | P_max | 10-700 | bar | Design pressure limit |
| Speed Range | N | 100-3600 | rpm | Operating speed range |

## Operating Conditions
- **Pressure Range:** 10 bar to 700 bar (typical industrial range)
- **Viscosity Range:** 1 cP to 100,000 cP (excellent for high viscosity)
- **Temperature Range:** -40°C to 200°C (material dependent)
- **Flow Turndown:** Up to 100:1 with speed control
- **Suction Conditions:** Self-priming capability up to 5-8 meters
- **Pulsation:** Minimal with multiple chambers or dampeners

## Industrial Applications
- **Chemical Injection:** Corrosion inhibitors, biocides, scale inhibitors
- **Hydraulic Systems:** High-pressure power units, actuator drives
- **Food Processing:** Sanitary pumping, chocolate transfer, viscous products
- **Pharmaceutical:** Precise dosing, sterile applications, API transfer
- **Oil & Gas:** Chemical injection, crude oil transfer, drilling mud circulation
- **Paint & Coatings:** High-viscosity transfer, metering applications
- **Petrochemical:** Catalyst circulation, polymer transfer, solvent handling

## Limitations and Assumptions
- Constant volumetric flow assumption (no slip modeling)
- Single-phase operation only
- No pulsation dampening effects
- Uniform fluid properties throughout cycle
- Steady-state efficiency assumptions
- No wear effects on clearances
- Incompressible fluid assumption
- No temperature effects on viscosity

## Key References
1. **Wright, W.A.** "Pumping Manual, 9th Edition" Elsevier, 1999 - Comprehensive pump selection guide
2. **Volk, M.** "Pump Characteristics and Applications, 2nd Edition" CRC Press, 2005 - Practical pump engineering
3. **ANSI/HI Standards** "Positive Displacement Pumps for Nomenclature, Definitions, Application, and Operation" HI, 2017
