# SPROCLIB - Standard Process Control Library

A comprehensive Python library for chemical process control, providing essential classes and functions for PID control, process modeling, simulation, optimization, and advanced control techniques.

**SPROCLIB provides a semantic API for chemical plant design that uses familiar patterns from machine learning frameworks like TensorFlow and Keras.**

## Installation

```bash
pip install sproclib
```

## Features

- **Semantic Plant Design**: Intuitive API similar to ML frameworks for building complex chemical processes
- **Process Units**: CSTR, pumps, heat exchangers, distillation columns, reactors, and tanks
- **Economic Optimization**: Built-in optimization algorithms for cost minimization and profit maximization
- **PID Controllers**: Classical and advanced PID control implementations with auto-tuning
- **Analysis Tools**: Transfer functions, simulation, and system identification
- **Advanced Control**: Model predictive control, state-space controllers, and IMC
- **Transport Models**: Continuous and batch transport for liquids and solids

## Quick Start

Create and optimize a chemical plant in just a few lines:

```python
from sproclib.unit.plant import ChemicalPlant
from sproclib.unit.pump import CentrifugalPump
from sproclib.unit.reactor import CSTR

# Define plant
plant = ChemicalPlant(name="Process Plant")

# Add units
plant.add(CentrifugalPump(H0=50.0, eta=0.75), name="feed_pump")
plant.add(CSTR(V=150.0, k0=7.2e10), name="reactor")

# Connect units
plant.connect("feed_pump", "reactor", "feed_stream")

# Configure optimization
plant.compile(
   optimizer="economic",
   loss="total_cost",
   metrics=["profit", "conversion"]
)

# Optimize operations
plant.optimize(target_production=1000.0)
```

## Advanced Example

```python
# Traditional PID control example
import sproclib as spc

# Create a PID controller
controller = spc.PIDController(kp=1.0, ki=0.1, kd=0.05)

# Create a tank model
tank = spc.Tank(volume=100, area=10)

# Simulate step response
response = spc.step_response(tank, time_span=100)
```

## Requirements

- Python 3.8+
- NumPy >= 1.20.0
- SciPy >= 1.7.0
- Matplotlib >= 3.3.0

## License

MIT License

## Author

Thorsten Gressling <gressling@paramus.ai>
