"""
Utilities Examples - SPROCLIB
=============================

This module contains examples demonstrating the usage of utility units in SPROCLIB.
Each example includes both simple and comprehensive use cases.

Requirements:
- NumPy
- SciPy
- Matplotlib (for plotting)
"""

import numpy as np
import sys
import os

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unit.utilities.LinearApproximation import LinearApproximation


def simple_utilities_examples():
    """
    Simple examples of using utility units.
    
    This example demonstrates basic utility operations.
    """
    print("=== Simple Utilities Examples ===")
    
    # Linear Approximation
    print("\n--- Linear Approximation ---")
    
    # Create a simple model for the LinearApproximation
    from unit.base.ProcessModel import ProcessModel
    import numpy as np
    
    class SimpleModel(ProcessModel):
        def dynamics(self, t, x, u):
            return np.array([0.0])
        def steady_state(self, u):
            return np.array([0.0])
    
    simple_model = SimpleModel(name="Test Model")
    linear_approx = LinearApproximation(model=simple_model)
    
    print(f"Linear approximation created for model: {simple_model.name}")
    print(f"Type: {type(linear_approx).__name__}")
    
    # Set data points
    x_data = [10, 20, 30, 40, 50]
    y_data = [25, 45, 70, 90, 115]
    
    print(f"\nData points:")
    print(f"X values: {x_data}")
    print(f"Y values: {y_data}")
    
    # Calculate linear regression
    n = len(x_data)
    sum_x = sum(x_data)
    sum_y = sum(y_data)
    sum_xy = sum(x * y for x, y in zip(x_data, y_data))
    sum_x2 = sum(x * x for x in x_data)
    
    # Linear regression coefficients
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    
    print(f"\nLinear approximation:")
    print(f"Slope: {slope:.3f}")
    print(f"Intercept: {intercept:.3f}")
    print(f"Equation: y = {slope:.3f}x + {intercept:.3f}")
    
    # Calculate R-squared
    y_mean = sum_y / n
    ss_tot = sum((y - y_mean)**2 for y in y_data)
    ss_res = sum((y - (slope * x + intercept))**2 for x, y in zip(x_data, y_data))
    r_squared = 1 - (ss_res / ss_tot)
    
    print(f"R-squared: {r_squared:.4f}")
    
    # Interpolation and extrapolation
    test_x_values = [15, 25, 35, 55]
    print(f"\nInterpolation/Extrapolation:")
    print(f"{'X':<8} {'Y (predicted)':<15} {'Type':<15}")
    print("-" * 40)
    
    for x in test_x_values:
        y_pred = slope * x + intercept
        interp_type = "Interpolation" if min(x_data) <= x <= max(x_data) else "Extrapolation"
        print(f"{x:<8} {y_pred:<15.2f} {interp_type:<15}")
    
    print("\nSimple utilities examples completed successfully!")


def comprehensive_utilities_examples():
    """
    Comprehensive examples demonstrating advanced utility operations.
    
    This example includes:
    - Multiple regression techniques
    - Non-linear curve fitting
    - Statistical analysis
    - Error analysis and confidence intervals
    - Interpolation methods comparison
    """
    print("\n=== Comprehensive Utilities Examples ===")
    
    # Multiple Linear Regression
    print("\n--- Multiple Linear Regression ---")
    
    # Process control example: Reactor temperature vs. conversion
    # y = conversion, x1 = temperature, x2 = pressure, x3 = residence time
    
    # Sample data
    np.random.seed(42)  # For reproducible results
    n_points = 20
    
    # Independent variables
    temperature = np.random.uniform(300, 400, n_points)  # K
    pressure = np.random.uniform(1, 5, n_points)  # bar
    residence_time = np.random.uniform(0.5, 2.0, n_points)  # hours
    
    # Dependent variable (with some noise)
    conversion = (0.002 * temperature + 0.05 * pressure + 0.3 * residence_time - 0.4 + 
                 np.random.normal(0, 0.05, n_points))
    conversion = np.clip(conversion, 0, 1)  # Keep between 0 and 1
    
    print("Multiple Linear Regression Analysis:")
    print("Conversion = f(Temperature, Pressure, Residence Time)")
    
    # Create design matrix
    X = np.column_stack([np.ones(n_points), temperature, pressure, residence_time])
    y = conversion
    
    # Calculate coefficients using normal equation
    coefficients = np.linalg.lstsq(X, y, rcond=None)[0]
    
    print(f"\nRegression equation:")
    print(f"Conversion = {coefficients[0]:.4f} + {coefficients[1]:.6f}*T + {coefficients[2]:.4f}*P + {coefficients[3]:.4f}*tau")
    
    # Calculate predictions and statistics
    y_pred = X @ coefficients
    residuals = y - y_pred
    
    # R-squared
    ss_tot = np.sum((y - np.mean(y))**2)
    ss_res = np.sum(residuals**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Adjusted R-squared
    n = len(y)
    p = len(coefficients) - 1  # Number of predictors
    adj_r_squared = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
    
    print(f"\nStatistics:")
    print(f"R-squared: {r_squared:.4f}")
    print(f"Adjusted R-squared: {adj_r_squared:.4f}")
    print(f"RMSE: {np.sqrt(np.mean(residuals**2)):.4f}")
    
    # Show first 10 predictions vs actual
    print(f"\n{'Actual':<10} {'Predicted':<10} {'Residual':<10}")
    print("-" * 35)
    for i in range(min(10, n_points)):
        print(f"{y[i]:<10.4f} {y_pred[i]:<10.4f} {residuals[i]:<10.4f}")
    
    # Non-linear Curve Fitting
    print("\n--- Non-linear Curve Fitting ---")
    
    # Note: Using the same model instance for demonstration
    
    # Example: Reaction rate vs temperature (Arrhenius equation)
    temp_data = np.linspace(300, 450, 15)  # K
    
    # True parameters
    A_true = 1e6  # Pre-exponential factor
    Ea_true = 8000  # Activation energy (J/mol)
    R = 8.314  # Gas constant
    
    # Generate "experimental" data with noise
    k_true = A_true * np.exp(-Ea_true / (R * temp_data))
    k_data = k_true * (1 + np.random.normal(0, 0.1, len(temp_data)))
    
    print("Arrhenius Equation Fitting:")
    print("k = A * exp(-Ea / (R*T))")
    print(f"True values: A = {A_true:.0e}, Ea = {Ea_true} J/mol")
    
    # Linearize: ln(k) = ln(A) - Ea/(R*T)
    ln_k = np.log(k_data)
    inv_T = 1 / temp_data
    
    # Linear regression on transformed data
    slope_ln = np.polyfit(inv_T, ln_k, 1)[0]
    intercept_ln = np.polyfit(inv_T, ln_k, 1)[1]
    
    # Back-transform to get A and Ea
    Ea_fitted = -slope_ln * R
    A_fitted = np.exp(intercept_ln)
    
    print(f"\nFitted values:")
    print(f"A = {A_fitted:.2e}")
    print(f"Ea = {Ea_fitted:.0f} J/mol")
    print(f"Error in A: {abs(A_fitted - A_true)/A_true*100:.1f}%")
    print(f"Error in Ea: {abs(Ea_fitted - Ea_true)/Ea_true*100:.1f}%")
    
    # Show fit quality
    k_fitted = A_fitted * np.exp(-Ea_fitted / (R * temp_data))
    relative_error = abs(k_fitted - k_data) / k_data * 100
    
    print(f"\n{'T (K)':<8} {'k_exp':<12} {'k_fit':<12} {'Error (%)':<10}")
    print("-" * 50)
    for i in range(0, len(temp_data), 3):  # Show every 3rd point
        print(f"{temp_data[i]:<8.0f} {k_data[i]:<12.2e} {k_fitted[i]:<12.2e} {relative_error[i]:<10.1f}")
    
    # Polynomial Approximation
    print("\n--- Polynomial Approximation ---")
    
    # Compare different polynomial orders
    x_poly = np.linspace(0, 10, 21)
    y_true = 2 + 3*x_poly - 0.5*x_poly**2 + 0.1*x_poly**3
    y_noisy = y_true + np.random.normal(0, 1, len(x_poly))
    
    print("Polynomial Fitting Comparison:")
    print("True function: y = 2 + 3x - 0.5x^2 + 0.1x^3")
    
    orders = [1, 2, 3, 4, 5]
    print(f"\n{'Order':<8} {'RMSE':<12} {'R^2':<8} {'AIC':<12} {'Overfitting Risk':<15}")
    print("-" * 65)
    
    for order in orders:
        # Fit polynomial
        coeffs = np.polyfit(x_poly, y_noisy, order)
        y_fit = np.polyval(coeffs, x_poly)
        
        # Calculate metrics
        rmse = np.sqrt(np.mean((y_noisy - y_fit)**2))
        ss_res = np.sum((y_noisy - y_fit)**2)
        ss_tot = np.sum((y_noisy - np.mean(y_noisy))**2)
        r2 = 1 - ss_res/ss_tot
        
        # AIC (Akaike Information Criterion)
        n = len(y_noisy)
        aic = n * np.log(ss_res/n) + 2 * (order + 1)
        
        # Overfitting risk assessment
        if order == 1:
            risk = "Low"
        elif order <= 3:
            risk = "Medium"
        else:
            risk = "High"
        
        print(f"{order:<8} {rmse:<12.3f} {r2:<8.3f} {aic:<12.1f} {risk:<15}")
    
    # Interpolation Methods Comparison
    print("\n--- Interpolation Methods Comparison ---")
    
    # Create sparse data
    x_sparse = np.array([0, 2, 5, 7, 10])
    y_sparse = np.array([1, 8, 15, 12, 20])
    
    # Dense grid for interpolation
    x_dense = np.linspace(0, 10, 50)
    
    print("Comparing interpolation methods:")
    print(f"Sparse data points: {len(x_sparse)}")
    print(f"Interpolation points: {len(x_dense)}")
    
    # Linear interpolation (simple)
    y_linear = np.interp(x_dense, x_sparse, y_sparse)
    
    # Polynomial interpolation
    poly_coeffs = np.polyfit(x_sparse, y_sparse, len(x_sparse)-1)
    y_poly = np.polyval(poly_coeffs, x_dense)
    
    # Calculate metrics at known points
    methods = ["Linear", "Polynomial"]
    interpolated_values = [y_linear, y_poly]
    
    print(f"\n{'Method':<12} {'Smoothness':<12} {'Overshoot Risk':<15} {'Computational Cost':<18}")
    print("-" * 65)
    
    for i, method in enumerate(methods):
        if method == "Linear":
            smoothness = "Low"
            overshoot = "None"
            cost = "Very Low"
        elif method == "Polynomial":
            smoothness = "High"
            overshoot = "High"
            cost = "Medium"
        
        print(f"{method:<12} {smoothness:<12} {overshoot:<15} {cost:<18}")
    
    # Error Analysis and Confidence Intervals
    print("\n--- Error Analysis and Confidence Intervals ---")
    
    # Bootstrap analysis for uncertainty estimation
    n_bootstrap = 1000
    
    # Original data
    x_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y_data = np.array([2.1, 3.9, 6.2, 7.8, 10.1, 12.2, 13.8, 16.1, 18.0, 19.9])
    
    print("Bootstrap Analysis for Linear Regression:")
    print(f"Number of bootstrap samples: {n_bootstrap}")
    
    slopes = []
    intercepts = []
    
    for i in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(len(x_data), size=len(x_data), replace=True)
        x_boot = x_data[indices]
        y_boot = y_data[indices]
        
        # Fit line
        slope_boot, intercept_boot = np.polyfit(x_boot, y_boot, 1)
        slopes.append(slope_boot)
        intercepts.append(intercept_boot)
    
    # Calculate confidence intervals
    slope_mean = np.mean(slopes)
    slope_std = np.std(slopes)
    slope_ci_lower = np.percentile(slopes, 2.5)
    slope_ci_upper = np.percentile(slopes, 97.5)
    
    intercept_mean = np.mean(intercepts)
    intercept_std = np.std(intercepts)
    intercept_ci_lower = np.percentile(intercepts, 2.5)
    intercept_ci_upper = np.percentile(intercepts, 97.5)
    
    print(f"\nBootstrap Results (95% confidence intervals):")
    print(f"Slope: {slope_mean:.4f} +/- {slope_std:.4f} [{slope_ci_lower:.4f}, {slope_ci_upper:.4f}]")
    print(f"Intercept: {intercept_mean:.4f} +/- {intercept_std:.4f} [{intercept_ci_lower:.4f}, {intercept_ci_upper:.4f}]")
    
    # Prediction intervals
    x_pred = np.array([2.5, 5.5, 8.5])
    
    print(f"\nPrediction intervals at selected points:")
    print(f"{'X':<8} {'Y_pred':<10} {'CI_lower':<10} {'CI_upper':<10}")
    print("-" * 45)
    
    for x in x_pred:
        # Calculate prediction for each bootstrap sample
        y_predictions = [slope * x + intercept for slope, intercept in zip(slopes, intercepts)]
        
        y_mean = np.mean(y_predictions)
        y_ci_lower = np.percentile(y_predictions, 2.5)
        y_ci_upper = np.percentile(y_predictions, 97.5)
        
        print(f"{x:<8.1f} {y_mean:<10.2f} {y_ci_lower:<10.2f} {y_ci_upper:<10.2f}")
    
    print("\nComprehensive utilities examples completed successfully!")


def main():
    """
    Main function to run all utilities examples.
    """
    print("SPROCLIB Utilities Examples")
    print("=" * 50)
    
    try:
        # Run simple examples
        simple_utilities_examples()
        
        # Run comprehensive examples
        comprehensive_utilities_examples()
        
        print("\n" + "=" * 50)
        print("All utilities examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
