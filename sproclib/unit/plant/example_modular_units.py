"""
Example: Using the Modular SPROCLIB Process Units

This example demonstrates how to use the new modular structure
to import and use different process units.
"""

import numpy as np
import matplotlib.pyplot as plt

# Import from the new modular structure
from unit import ProcessModel, CSTR, InteractingTanks, HeatExchanger
from unit.reactor.batch import BatchReactor
from unit.utilities import LinearApproximation

def main():
    print("SPROCLIB Modular Structure Example")
    print("=" * 40)
    
    # 1. Interacting Tanks Example
    print("\n1. Interacting Tanks Simulation")
    tanks = InteractingTanks(
        A1=1.0, A2=1.5, 
        C1=0.5, C2=0.3,
        name="TwoTanksSystem"
    )
    
    # Simulate step response
    t_span = (0, 20)
    x0 = np.array([2.0, 1.0])  # Initial heights
    u_func = lambda t: np.array([1.5])  # Step input
    
    result = tanks.simulate(t_span, x0, u_func)
    
    print(f"Initial heights: {x0}")
    print(f"Final heights: {result['x'][:, -1]}")
    print(f"Steady-state: {tanks.steady_state(np.array([1.5]))}")
    
    # 2. CSTR Example
    print("\n2. CSTR Simulation")
    cstr = CSTR(
        V=100.0, k0=7.2e10, Ea=72750.0,
        name="CSTR_Reactor"
    )
    
    # Operating conditions
    u_steady = np.array([100.0, 1.0, 350.0, 300.0])  # [q, CAi, Ti, Tc]
    x_steady = cstr.steady_state(u_steady)
    
    print(f"Operating conditions: q={u_steady[0]}, CAi={u_steady[1]}, Ti={u_steady[2]}, Tc={u_steady[3]}")
    print(f"Steady-state: CA={x_steady[0]:.3f}, T={x_steady[1]:.1f}")
    
    # 3. Linearization Example
    print("\n3. Linear Approximation")
    linearizer = LinearApproximation(cstr)
    A, B = linearizer.linearize(u_steady, x_steady)
    
    print(f"A matrix shape: {A.shape}")
    print(f"B matrix shape: {B.shape}")
    print(f"Eigenvalues: {np.linalg.eigvals(A)}")
    
    # 4. Batch Reactor Example
    print("\n4. Batch Reactor")
    batch = BatchReactor(
        V=50.0, k0=1e8, Ea=50000.0,
        name="BatchReactor"
    )
    
    # Calculate time to 90% conversion
    time_90 = batch.batch_time_to_conversion(0.9, CA0=2.0, T_avg=370.0)
    print(f"Time to 90% conversion: {time_90:.1f} minutes")
    
    print("\n" + "=" * 40)
    print("Modular structure working successfully!")
    print("Each unit is now independent and easily extendable.")

if __name__ == "__main__":
    main()
