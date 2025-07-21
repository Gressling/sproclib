# Compressor Documentation

## Overview and Use Case

Gas compression model for industrial applications including natural gas pipelines, refrigeration cycles, and process gas handling. Implements isentropic compression theory with efficiency corrections for realistic performance prediction.

## Physical/Chemical Principles

The compressor model is based on isentropic compression relationships for ideal gases:

**Isentropic Temperature Rise:**
```
T₂ˢ = T₁ × (P₂/P₁)^((γ-1)/γ)
```

**Actual Temperature with Efficiency:**
```
T₂ = T₁ + (T₂ˢ - T₁)/η_isentropic
```

**Compression Power:**
```
W = ṅ × R × (T₂ - T₁) / M
```

Where:
- γ = heat capacity ratio (Cp/Cv)
- η_isentropic = isentropic efficiency
- ṅ = molar flow rate
- R = universal gas constant
- M = molar mass

## Process Parameters

| Parameter | Typical Range | Units | Description |
|-----------|---------------|-------|-------------|
| η_isentropic | 0.70-0.90 | - | Isentropic efficiency |
| Pressure Ratio | 1.5-10 | - | P_discharge/P_suction |
| Suction Temperature | 250-350 | K | Inlet gas temperature |
| Suction Pressure | 1-50 | bar | Inlet gas pressure |
| Flow Rate | 10-10000 | Nm³/h | Volumetric flow at standard conditions |

## Operating Conditions

**Typical Industrial Ranges:**
- **Natural Gas Compression:** P₁ = 20-80 bar, P₂ = 40-200 bar, T₁ = 280-320 K
- **Refrigeration:** P₁ = 1-5 bar, P₂ = 10-25 bar, T₁ = 250-290 K  
- **Process Air:** P₁ = 1-2 bar, P₂ = 3-8 bar, T₁ = 288-308 K

**Design Constraints:**
- Maximum compression ratio per stage: ~4:1 for centrifugal, ~2:1 for axial
- Surge margin: 10-15% above surge line
- Maximum outlet temperature: 150-200°C (depending on gas properties)

## Industrial Applications

- **Natural Gas Pipelines:** Transmission and distribution compression stations
- **Petrochemical Plants:** Process gas compression, hydrogen recycle
- **Refrigeration Systems:** Vapor compression cycles for cooling
- **Air Separation:** Compressed air for cryogenic separation processes
- **Power Generation:** Gas turbine fuel gas compression
- **Pneumatic Conveying:** Material transport systems

## Limitations and Assumptions

- Assumes ideal gas behavior (PV = nRT)
- Constant isentropic efficiency across operating range
- No consideration of compressor surge or choke phenomena
- Neglects mechanical losses (bearings, seals, gearbox)
- First-order dynamics approximation for temperature response
- No gas property variations with temperature/pressure

## Key References

1. **Perry's Chemical Engineers' Handbook, 8th Edition** - Chapter 10: Transport and Storage of Fluids
2. **Compressor Handbook** by Paul C. Hanlon - McGraw-Hill Professional
3. **Gas Turbine Engineering Handbook** by Meherwan P. Boyce - Gulf Professional Publishing
