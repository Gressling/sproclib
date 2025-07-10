# Distillation Units

This directory contains distillation process unit models for separation operations.

## Contents

- `tray/`: Single distillation tray models
- `column/`: Complete distillation column models

## Available Models

### DistillationTray (`tray/`)
Models a single theoretical tray with:
- Component mass balances
- Energy balance
- Vapor-liquid equilibrium
- Tray hydraulics

### BinaryDistillationColumn (`column/`)
Models a complete binary distillation column with:
- Multiple theoretical trays
- Reboiler and condenser dynamics
- Reflux control
- Product composition control

## Usage Examples

```python
# Single tray
from paramus.chemistry.process_control.unit.distillation.tray import DistillationTray

tray = DistillationTray(
    holdup=100.0,      # kmol
    alpha=2.5,         # relative volatility
    efficiency=0.8     # tray efficiency
)

# Complete column
from paramus.chemistry.process_control.unit.distillation.column import BinaryDistillationColumn

column = BinaryDistillationColumn(
    n_trays=20,        # number of trays
    feed_tray=10,      # feed tray location
    alpha=2.5,         # relative volatility
    holdup=50.0        # tray holdup (kmol)
)
```

## For Contributors

When adding distillation models:
- Consider multicomponent systems
- Add rigorous thermodynamic property calculations
- Include tray hydraulic limitations
- Model non-ideal vapor-liquid equilibrium
- Add column startup and shutdown dynamics
