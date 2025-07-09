# Tank Units

This directory contains tank and storage vessel process unit models.

## Contents

- `single/`: Single tank models for storage and mixing
- `interacting/`: Multiple interacting tank systems

## Available Tank Models

### Tank (`single/`)
Single tank model with:
- Mass balance for liquid level
- Outlet flow calculation
- Temperature dynamics (if needed)
- Variable cross-sectional area support

### InteractingTanks (`interacting/`)
Multiple tank system with:
- Tank-to-tank flow interactions
- Level-dependent flow rates
- Gravity-driven or pump-assisted flows
- Complex hydraulic networks

## Usage Examples

```python
# Single tank
from paramus.chemistry.process_control.unit.tank.single import Tank

tank = Tank(
    area=10.0,           # m² cross-sectional area
    Cv=1.0,              # valve coefficient
    max_level=5.0        # maximum level (m)
)

# Interacting tanks
from paramus.chemistry.process_control.unit.tank.interacting import InteractingTanks

tanks = InteractingTanks(
    areas=[10.0, 8.0],        # tank areas
    Cvs=[1.0, 0.8],          # valve coefficients
    height_diff=2.0          # height difference
)
```

## For Contributors

When adding tank models:
- Consider non-cylindrical geometries
- Add mixing dynamics for composition
- Include heating/cooling capabilities  
- Model foam and settling effects
- Add level measurement dynamics
- Consider vapor space effects for volatile liquids
