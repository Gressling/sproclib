"""
Example usage of the LinearApproximation utility for SPROCLIB.

This example demonstrates how to linearize a nonlinear CSTR model
around an operating point for control system design.
"""

import numpy as np
import matplotlib.pyplot as plt
from paramus.chemistry.process_control.unit.utilities import LinearApproximation
from paramus.chemistry.process_control.unit.reactor.cstr import CSTR


def main():
    """Demonstrate linearization of a CSTR model."""
    
    # Create a nonlinear CSTR model
    cstr = CSTR(
        volume=1.0,           # m³
        k_reaction=0.5,       # reaction rate constant (1/s)
        E_activation=8000.0,  # activation energy (J/mol)
        rho=1000.0,           # density (kg/m³)
        Cp=4184.0,            # heat capacity (J/kg·K)
        delta_H=-50000.0,     # heat of reaction (J/mol)
        UA=2000.0,            # overall heat transfer (W/K)
        name="NonlinearCSTR"
    )
    
    print(f"Nonlinear Model: {cstr.name}")
    print(f"Volume: {cstr.volume} m³")
    print(f"Reaction rate constant: {cstr.k_reaction} 1/s")
    print(f"Activation energy: {cstr.E_activation} J/mol")
    
    # Create linear approximation utility
    lin_approx = LinearApproximation(cstr)
    
    # Define operating point
    # States: [concentration (mol/m³), temperature (K)]
    x_op = np.array([800.0, 350.0])
    
    # Inputs: [feed concentration (mol/m³), feed temperature (K), flow rate (m³/s), jacket temperature (K)]
    u_op = np.array([1000.0, 300.0, 0.1, 320.0])
    
    print(f"\\nOperating Point:")
    print(f"Concentration: {x_op[0]:.1f} mol/m³")
    print(f"Temperature: {x_op[1]:.1f} K")
    print(f"Feed concentration: {u_op[0]:.1f} mol/m³")
    print(f"Feed temperature: {u_op[1]:.1f} K")
    print(f"Flow rate: {u_op[2]:.3f} m³/s")
    print(f"Jacket temperature: {u_op[3]:.1f} K")
    
    # Linearize around operating point
    print("\\nLinearizing around operating point...")
    A, B, C, D = lin_approx.linearize_at_point(x_op, u_op)
    
    print(f"\\nLinear State-Space Model:")
    print(f"A matrix (2x2):")
    print(f"  {A[0,0]:.4f}  {A[0,1]:.4f}")
    print(f"  {A[1,0]:.4f}  {A[1,1]:.4f}")
    
    print(f"\\nB matrix (2x4):")
    for i in range(2):
        print(f"  {B[i,0]:.4e}  {B[i,1]:.4e}  {B[i,2]:.4e}  {B[i,3]:.4e}")
    
    # Validate linearization by comparing responses
    print("\\nValidating linearization...")
    
    # Small perturbation in feed temperature
    delta_u = np.array([0.0, 5.0, 0.0, 0.0])  # +5K feed temperature
    
    # Nonlinear response
    t_span = (0, 100)
    t_eval = np.linspace(0, 100, 200)
    
    def perturbed_input(t):
        return u_op + (delta_u if t >= 10 else np.zeros_like(delta_u))
    
    result_nonlinear = cstr.simulate(
        t_span=t_span,
        x0=x_op,
        input_func=perturbed_input,
        t_eval=t_eval
    )
    
    # Linear response (approximate)
    # For simplicity, calculate step response analytically
    # This is a simplified approach - in practice, use control systems libraries
    
    # Calculate eigenvalues for stability analysis
    eigenvalues = np.linalg.eigvals(A)
    print(f"\\nSystem Eigenvalues:")
    for i, eig in enumerate(eigenvalues):
        print(f"  λ{i+1} = {eig:.4f}")
        if eig.real < 0:
            print(f"      Stable mode (time constant: {-1/eig.real:.2f} s)")
        else:
            print(f"      Unstable mode!")
    
    # Plot comparison
    plt.figure(figsize=(12, 8))
    
    # Concentration response
    plt.subplot(2, 1, 1)
    plt.plot(result_nonlinear.t, result_nonlinear.y[0], 'b-', linewidth=2, label='Nonlinear')
    plt.axvline(x=10, color='r', linestyle='--', alpha=0.5, label='Perturbation start')
    plt.ylabel('Concentration (mol/m³)')
    plt.title('CSTR Response to Feed Temperature Step (+5K)')
    plt.legend()
    plt.grid(True)
    
    # Temperature response
    plt.subplot(2, 1, 2)
    plt.plot(result_nonlinear.t, result_nonlinear.y[1], 'b-', linewidth=2, label='Nonlinear')
    plt.axvline(x=10, color='r', linestyle='--', alpha=0.5, label='Perturbation start')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (K)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # Controllability and observability analysis
    print(f"\\nSystem Analysis:")
    
    # Controllability matrix
    controllability_matrix = np.hstack([B, A @ B])
    cont_rank = np.linalg.matrix_rank(controllability_matrix)
    print(f"Controllability rank: {cont_rank} (full rank: {A.shape[0]})")
    
    if cont_rank == A.shape[0]:
        print("  System is controllable")
    else:
        print("  System is not fully controllable")
    
    # Observability matrix  
    observability_matrix = np.vstack([C, C @ A])
    obs_rank = np.linalg.matrix_rank(observability_matrix)
    print(f"Observability rank: {obs_rank} (full rank: {A.shape[0]})")
    
    if obs_rank == A.shape[0]:
        print("  System is observable")
    else:
        print("  System is not fully observable")
    
    print(f"\\nLinearization complete. The linear model can be used for:")
    print(f"  - PID controller tuning")
    print(f"  - Model predictive control (MPC)")
    print(f"  - Kalman filter design")
    print(f"  - Stability analysis")


if __name__ == "__main__":
    main()
