"""
Example usage of the Base ProcessModel class for SPROCLIB.

This example demonstrates how to create a custom process unit by inheriting
from the ProcessModel base class.
"""

import numpy as np
import matplotlib.pyplot as plt
from paramus.chemistry.process_control.unit.base import ProcessModel


class SimpleFirstOrderSystem(ProcessModel):
    """Example first-order system inheriting from ProcessModel."""
    
    def __init__(self, time_constant: float = 1.0, gain: float = 1.0):
        """
        Initialize simple first-order system.
        
        Args:
            time_constant: Process time constant (s)
            gain: Process gain
        """
        super().__init__("SimpleFirstOrderSystem")
        self.time_constant = time_constant
        self.gain = gain
        
        # Set up parameters
        self.parameters = {
            'time_constant': time_constant,
            'gain': gain
        }
        
    def dynamics(self, t: float, x: np.ndarray, u: np.ndarray) -> np.ndarray:
        """
        First-order system dynamics: tau * dy/dt + y = K * u
        
        Args:
            t: Time
            x: State [output]
            u: Input [input]
            
        Returns:
            State derivative [dy/dt]
        """
        y = x[0]
        input_signal = u[0] if len(u) > 0 else 0.0
        
        dydt = (-y + self.gain * input_signal) / self.time_constant
        
        return np.array([dydt])


def main():
    """Demonstrate the custom ProcessModel implementation."""
    
    # Create the system
    system = SimpleFirstOrderSystem(time_constant=2.0, gain=1.5)
    
    # Set up simulation
    t_span = (0, 20)
    t_eval = np.linspace(0, 20, 200)
    x0 = np.array([0.0])  # Initial condition
    
    # Step input
    def step_input(t):
        return np.array([1.0 if t >= 1.0 else 0.0])
    
    # Simulate
    result = system.simulate(
        t_span=t_span,
        x0=x0,
        input_func=step_input,
        t_eval=t_eval
    )
    
    # Plot results
    plt.figure(figsize=(10, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(result.t, [step_input(t)[0] for t in result.t], 'r--', label='Input')
    plt.ylabel('Input')
    plt.title('Simple First-Order System Response')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(result.t, result.y[0], 'b-', label='Output')
    plt.xlabel('Time (s)')
    plt.ylabel('Output')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    print(f"System parameters:")
    print(f"  Time constant: {system.time_constant} s")
    print(f"  Gain: {system.gain}")
    print(f"  Final value: {result.y[0][-1]:.3f}")
    print(f"  Expected final value: {system.gain:.3f}")


if __name__ == "__main__":
    main()
