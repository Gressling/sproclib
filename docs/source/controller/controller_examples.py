#!/usr/bin/env python3
"""
Controller Package Examples for SPROCLIB

This script demonstrates the new modular controller package structure
including PID controllers and various tuning methods.

Author: Thorsten Gressling <gressling@paramus.ai>
License: MIT License
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List

def pid_controller_example():
    """Demonstrate basic PID controller usage."""
    print("PID Controller Example")
    print("=" * 40)
    
    # Import from new modular structure
    from controller.pid.PIDController import PIDController
    
    # Create PID controller with industrial features
    pid = PIDController(
        Kp=1.2,           # Proportional gain
        Ki=0.8,           # Integral gain  
        Kd=0.3,           # Derivative gain
        MV_bar=50.0,      # Bias term
        beta=0.5,         # Setpoint weighting
        MV_min=0.0,       # Minimum output
        MV_max=100.0,     # Maximum output
        direct_action=False  # Reverse action
    )
    
    # Simulation parameters
    setpoint = 60.0
    process_value = 50.0  # Initial PV
    time_points = np.arange(0, 60, 0.1)
    outputs = []
    pvs = []
    
    # Simple process simulation (first-order lag)
    tau = 10.0  # Time constant
    K = 2.0     # Process gain
    
    for t in time_points:
        # Update controller
        output = pid.update(t, setpoint, process_value)
        outputs.append(output)
        pvs.append(process_value)
        
        # Simple process response (first-order)
        if t > 0:
            dt = 0.1
            dpv_dt = (K * output - process_value) / tau
            process_value += dpv_dt * dt
    
    print(f"Final PV: {process_value:.2f}")
    print(f"Final Output: {outputs[-1]:.2f}")
    print(f"Controller Status: {pid.get_status()}")
    print()

def tuning_methods_example():
    """Demonstrate various tuning methods."""
    print("Tuning Methods Example")
    print("=" * 40)
    
    # Import tuning methods
    from controller.tuning.ZieglerNicholsTuning import ZieglerNicholsTuning
    from controller.tuning.AMIGOTuning import AMIGOTuning
    from controller.tuning.RelayTuning import RelayTuning
    
    # Process model parameters (FOPDT)
    model_params = {
        'K': 2.5,      # Process gain
        'tau': 15.0,   # Time constant
        'theta': 3.0   # Dead time
    }
    
    # Test different tuning methods
    methods = [
        ("Ziegler-Nichols PID", ZieglerNicholsTuning("PID")),
        ("Ziegler-Nichols PI", ZieglerNicholsTuning("PI")),
        ("AMIGO PID", AMIGOTuning("PID")),
        ("AMIGO PI", AMIGOTuning("PI"))
    ]
    
    print("Tuning Results for Process K=2.5, τ=15.0, θ=3.0:")
    print("-" * 50)
    
    for name, tuner in methods:
        try:
            params = tuner.calculate_parameters(model_params)
            print(f"{name:20s}: Kp={params['Kp']:.3f}, Ki={params['Ki']:.3f}, Kd={params['Kd']:.3f}")
            if 'beta' in params:
                print(f"{'':20s}  β={params['beta']:.3f}, γ={params['gamma']:.3f}")
        except Exception as e:
            print(f"{name:20s}: Error - {e}")
    
    print()
    
    # Relay tuning example
    print("Relay Tuning Example:")
    print("-" * 25)
    relay_tuner = RelayTuning(relay_amplitude=5.0)
    
    # Simulate relay test results
    relay_results = {
        'Pu': 25.0,  # Ultimate period from relay test
        'a': 3.2     # Process amplitude response
    }
    
    params = relay_tuner.calculate_parameters(relay_results)
    print(f"Relay tuning results: Kp={params['Kp']:.3f}, Ki={params['Ki']:.3f}, Kd={params['Kd']:.3f}")
    print()

def backward_compatibility_example():
    """Demonstrate backward compatibility with legacy imports."""
    print("Backward Compatibility Example")
    print("=" * 40)
    
    # Legacy imports still work
    from controllers import PIDController, ZieglerNicholsTuning
    
    # Create controller using legacy interface
    tuner = ZieglerNicholsTuning("PID")
    params = tuner.calculate_parameters({'K': 2.0, 'tau': 10.0, 'theta': 2.0})
    
    pid = PIDController(Kp=params['Kp'], Ki=params['Ki'], Kd=params['Kd'])
    
    # Test operation
    output = pid.update(t=1.0, SP=50.0, PV=45.0)
    print(f"Legacy interface works: output = {output:.3f}")
    print("Legacy imports are fully compatible with existing code.")
    print()

def integration_with_units_example():
    """Demonstrate controller integration with process units."""
    print("Controller + Process Unit Integration")
    print("=" * 40)
    
    try:
        # Import both controller and unit
        from controller.pid.PIDController import PIDController
        from controller.tuning.AMIGOTuning import AMIGOTuning
        from unit.tank.Tank import Tank
        
        # Create process unit
        tank = Tank(A=2.0, C=1.5, name="Level Control Tank")
        
        # Auto-tune controller for tank
        # Approximate tank as FOPDT: K = 1/C, tau = A/C, theta = 0.5
        model_params = {
            'K': 1.0 / tank.C,
            'tau': tank.A / tank.C, 
            'theta': 0.5
        }
        
        tuner = AMIGOTuning("PI")
        params = tuner.calculate_parameters(model_params)
        
        # Create tuned controller
        pid = PIDController(
            Kp=params['Kp'],
            Ki=params['Ki'],
            Kd=params['Kd'],
            beta=params.get('beta', 1.0)
        )
        
        print(f"Tank parameters: A={tank.A}, C={tank.C}")
        print(f"Model approximation: K={model_params['K']:.3f}, τ={model_params['tau']:.3f}")
        print(f"Tuned controller: Kp={params['Kp']:.3f}, Ki={params['Ki']:.3f}")
        print("✓ Controller successfully tuned for tank level control")
        
    except ImportError as e:
        print(f"Unit integration example requires unit package: {e}")
    
    print()

def main():
    """Run all controller examples."""
    print("SPROCLIB Controller Package Examples")
    print("=" * 50)
    print()
    
    pid_controller_example()
    tuning_methods_example()
    backward_compatibility_example()
    integration_with_units_example()
    
    print("Controller Package Summary:")
    print("=" * 30)
    print("✓ Modular structure with separate PID and tuning packages")
    print("✓ Multiple tuning methods (Ziegler-Nichols, AMIGO, Relay)")
    print("✓ Industrial PID features (anti-windup, setpoint weighting)")
    print("✓ Full backward compatibility with legacy interface")
    print("✓ Integration with modular process units")

if __name__ == "__main__":
    main()
