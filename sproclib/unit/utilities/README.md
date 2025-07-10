# Utility Units

This directory contains utility classes and functions for process modeling.

## Contents

- `__init__.py`: Contains the `LinearApproximation` utility class

## LinearApproximation Class

A utility for creating linear approximations of nonlinear process models around operating points. This is useful for:

- Control system design
- Stability analysis  
- Model predictive control formulations
- Process identification

### Features
- Numerical Jacobian calculation
- State-space model generation
- Operating point linearization
- Input-output mapping

### Key Methods
- `linearize_at_point()`: Create linear model at specific operating point
- `get_state_space()`: Get A, B, C, D matrices
- `validate_linearization()`: Check linearization accuracy

## Usage Example

```python
from paramus.chemistry.process_control.unit.utilities import LinearApproximation
from paramus.chemistry.process_control.unit.reactor.cstr import CSTR

# Create a nonlinear model
cstr = CSTR(volume=1.0, k_reaction=0.1)

# Create linear approximation
lin_approx = LinearApproximation(cstr)

# Linearize around operating point
x_op = [300.0, 0.8]  # Temperature, concentration
u_op = [295.0, 1.0]  # Feed temp, flow rate

A, B, C, D = lin_approx.linearize_at_point(x_op, u_op)
```

## For Contributors

When adding utility functions:
- Focus on commonly needed modeling tasks
- Provide numerical methods for analysis
- Include validation and error checking
- Add parameter estimation utilities
- Create optimization helpers
- Include data preprocessing tools
