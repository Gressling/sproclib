# SPROCLIB - Standard Process Control Library

A comprehensive Python library for chemical process control, providing essential classes and functions for PID control, process modeling, simulation, optimization, and advanced control techniques.

## Installation

```bash
pip install sproclib
```

## Features

- **PID Controllers**: Classical and advanced PID control implementations
- **Process Models**: CSTR, tanks, heat exchangers, distillation columns, and reactors
- **Analysis Tools**: Transfer functions, simulation, and optimization capabilities
- **Advanced Control**: Model predictive control and state task networks
- **Tuning Methods**: Ziegler-Nichols and other proven tuning rules

## Quick Start

```python
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
