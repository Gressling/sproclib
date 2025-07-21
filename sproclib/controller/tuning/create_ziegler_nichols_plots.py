import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import sys
import os

# Add parent directory to path to import the example
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ZieglerNicholsTuning_simple_example import main

def create_ziegler_nichols_plots():
    """
    Create comprehensive visualizations for Ziegler-Nichols tuning methodology.
    """
    
    # Get simulation results
    results = main()
    
    # Create figure with professional styling
    plt.style.use('default')
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    # Color scheme for professional plots
    colors = {
        'temperature': '#2E8B57',  # Sea green
        'setpoint': '#DC143C',     # Crimson
        'cooling': '#4169E1',      # Royal blue
        'error': '#FF6347',        # Tomato
        'grid': '#E0E0E0',         # Light gray
        'text': '#2F4F4F'          # Dark slate gray
    }
    
    # ==============================================
    # PLOT 1: STEP TEST RESPONSE AND IDENTIFICATION
    # ==============================================
    ax1 = fig.add_subplot(gs[0, :2])
    
    # Plot step test data
    ax1.plot(results['step_test_time'], results['step_test_response'], 
             'o-', color=colors['temperature'], markersize=3, linewidth=2,
             label='Process Response', alpha=0.8)
    
    # Add step input indication
    step_time = 5.0
    ax1.axvline(x=step_time, color='gray', linestyle='--', alpha=0.7, 
                label='Step Input (+2 L/min)')
    
    # Identification visualization
    time_vector = results['step_test_time']
    temp_response = results['step_test_response']
    
    # Identify parameters for tangent line
    final_value = np.mean(temp_response[-20:])
    initial_value = temp_response[0]
    
    # Find inflection point and draw tangent
    response_after_step = temp_response[50:]
    time_after_step = time_vector[50:]
    slopes = np.gradient(response_after_step, time_after_step[1] - time_after_step[0])
    max_slope_idx = np.argmax(np.abs(slopes))
    
    inflection_time = time_after_step[max_slope_idx]
    inflection_temp = response_after_step[max_slope_idx]
    max_slope = slopes[max_slope_idx]
    
    # Draw tangent line
    tangent_time = np.linspace(0, 60, 100)
    tangent_temp = max_slope * (tangent_time - inflection_time) + inflection_temp
    
    # Only show tangent in relevant range
    valid_range = (tangent_temp >= initial_value - 2) & (tangent_temp <= final_value + 1)
    ax1.plot(tangent_time[valid_range], tangent_temp[valid_range], 
             'r--', linewidth=2, alpha=0.8, label='Tangent Line')
    
    # Mark key points
    x_intercept = (initial_value - inflection_temp) / max_slope + inflection_time
    dead_time = x_intercept - step_time
    x_final = (final_value - inflection_temp) / max_slope + inflection_time
    time_constant = x_final - x_intercept
    
    ax1.plot(inflection_time, inflection_temp, 'ro', markersize=8, 
             label='Inflection Point')
    ax1.plot(x_intercept, initial_value, 'bs', markersize=8, 
             label=f'Dead Time = {dead_time:.1f} min')
    
    # Add parameter annotations
    ax1.annotate(f'θ = {dead_time:.1f} min', xy=(x_intercept, initial_value), 
                xytext=(x_intercept + 5, initial_value + 1),
                arrowprops=dict(arrowstyle='->', color='blue'),
                fontsize=10, color='blue', weight='bold')
    
    ax1.annotate(f'T = {time_constant:.1f} min', 
                xy=(x_final, final_value), xytext=(x_final + 5, final_value - 1),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=10, color='red', weight='bold')
    
    kp_identified = (final_value - initial_value) / 2.0
    ax1.annotate(f'Kp = {kp_identified:.2f} K/(L/min)', 
                xy=(40, (initial_value + final_value)/2), xytext=(42, (initial_value + final_value)/2),
                fontsize=10, color=colors['text'], weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    ax1.set_xlabel('Time (min)', fontsize=12, weight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=12, weight='bold')
    ax1.set_title('Step Test Response and Parameter Identification\n(CSTR Temperature Control)', 
                  fontsize=14, weight='bold', color=colors['text'])
    ax1.grid(True, alpha=0.3, color=colors['grid'])
    ax1.legend(loc='lower right', fontsize=10)
    ax1.set_xlim(0, 60)
    
    # ==============================================
    # PLOT 2: TUNING PARAMETER COMPARISON
    # ==============================================
    ax2 = fig.add_subplot(gs[0, 2])
    
    # Create comparison bar chart
    tuning_methods = ['ZN-PID', 'ZN-PI', 'Conservative\nPI']
    kc_values = [results['tuning_parameters']['Kc_pid'],
                 results['tuning_parameters']['Kc_pi'],
                 results['tuning_parameters']['Kc_pi'] * 0.8]
    ti_values = [results['tuning_parameters']['tau_I_pid'],
                 results['tuning_parameters']['tau_I_pi'],
                 results['tuning_parameters']['tau_I_pi'] * 1.2]
    
    x_pos = np.arange(len(tuning_methods))
    width = 0.35
    
    bars1 = ax2.bar(x_pos - width/2, kc_values, width, 
                    label='Kc (L/min)/K', color=colors['cooling'], alpha=0.8)
    
    # Create secondary y-axis for integral time
    ax2_twin = ax2.twinx()
    bars2 = ax2_twin.bar(x_pos + width/2, ti_values, width, 
                         label='τI (min)', color=colors['error'], alpha=0.8)
    
    ax2.set_xlabel('Tuning Method', fontsize=11, weight='bold')
    ax2.set_ylabel('Controller Gain Kc', fontsize=11, weight='bold', color=colors['cooling'])
    ax2_twin.set_ylabel('Integral Time τI', fontsize=11, weight='bold', color=colors['error'])
    ax2.set_title('ZN Tuning Parameters\nComparison', fontsize=12, weight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(tuning_methods, fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax2.text(bar1.get_x() + bar1.get_width()/2., height1 + 0.01,
                f'{height1:.2f}', ha='center', va='bottom', fontsize=9, weight='bold')
        ax2_twin.text(bar2.get_x() + bar2.get_width()/2., height2 + 0.2,
                     f'{height2:.1f}', ha='center', va='bottom', fontsize=9, weight='bold')
    
    ax2.tick_params(axis='y', labelcolor=colors['cooling'])
    ax2_twin.tick_params(axis='y', labelcolor=colors['error'])
    
    # ==============================================
    # PLOT 3: CLOSED-LOOP RESPONSE
    # ==============================================
    ax3 = fig.add_subplot(gs[1, :])
    
    # Plot temperature response
    ax3.plot(results['time'], results['temperature'], 
             color=colors['temperature'], linewidth=2.5, label='Process Temperature')
    ax3.plot(results['time'], results['setpoint'], 
             color=colors['setpoint'], linewidth=2, linestyle='--', label='Setpoint')
    
    # Fill between for better visualization
    ax3.fill_between(results['time'], results['temperature'], results['setpoint'],
                     alpha=0.2, color=colors['temperature'])
    
    # Add cooling flow on secondary axis
    ax3_twin = ax3.twinx()
    ax3_twin.plot(results['time'], results['cooling_flow'], 
                  color=colors['cooling'], linewidth=2, alpha=0.8, label='Cooling Flow')
    
    # Mark performance characteristics
    step_time = 50.0
    ax3.axvline(x=step_time, color='gray', linestyle=':', alpha=0.7)
    ax3.text(step_time + 1, 352, 'Setpoint\nStep', fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Performance metrics annotation
    metrics = results['performance_metrics']
    perf_text = f"Rise Time: {metrics['rise_time']:.1f} min\n"
    perf_text += f"Settling Time: {metrics['settling_time']:.1f} min\n"
    perf_text += f"Overshoot: {metrics['overshoot']:.1f}%"
    
    ax3.text(0.02, 0.98, perf_text, transform=ax3.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", 
             facecolor='lightblue', alpha=0.8))
    
    ax3.set_xlabel('Time (min)', fontsize=12, weight='bold')
    ax3.set_ylabel('Temperature (K)', fontsize=12, weight='bold', color=colors['temperature'])
    ax3_twin.set_ylabel('Cooling Flow (L/min)', fontsize=12, weight='bold', color=colors['cooling'])
    ax3.set_title('Closed-Loop Response with ZN-PI Tuning\n(5K Setpoint Step at t=50 min)', 
                  fontsize=14, weight='bold', color=colors['text'])
    ax3.grid(True, alpha=0.3, color=colors['grid'])
    ax3.legend(loc='upper left', fontsize=10)
    ax3_twin.legend(loc='upper right', fontsize=10)
    ax3.tick_params(axis='y', labelcolor=colors['temperature'])
    ax3_twin.tick_params(axis='y', labelcolor=colors['cooling'])
    
    # ==============================================
    # PLOT 4: CONTROL ERROR ANALYSIS
    # ==============================================
    ax4 = fig.add_subplot(gs[2, 0])
    
    # Error magnitude plot
    error_magnitude = np.abs(results['control_error'])
    ax4.plot(results['time'], error_magnitude, 
             color=colors['error'], linewidth=2, label='|Control Error|')
    ax4.fill_between(results['time'], 0, error_magnitude, 
                     alpha=0.3, color=colors['error'])
    
    # Add tolerance bands
    ax4.axhline(y=1.0, color='orange', linestyle='--', alpha=0.7, label='±1K Tolerance')
    ax4.axhline(y=0.5, color='green', linestyle='--', alpha=0.7, label='±0.5K Tolerance')
    
    ax4.set_xlabel('Time (min)', fontsize=11, weight='bold')
    ax4.set_ylabel('|Error| (K)', fontsize=11, weight='bold')
    ax4.set_title('Control Error Analysis', fontsize=12, weight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend(fontsize=9)
    ax4.set_xlim(0, 100)
    
    # Add IAE annotation
    iae = results['performance_metrics']['iae']
    ax4.text(0.7, 0.9, f'IAE = {iae:.1f} K·min', transform=ax4.transAxes, 
             fontsize=10, weight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # ==============================================
    # PLOT 5: STABILITY ANALYSIS
    # ==============================================
    ax5 = fig.add_subplot(gs[2, 1])
    
    # Create Bode-like plot for stability margin assessment
    # Simplified analysis based on tuning parameters
    frequency = np.logspace(-3, 1, 100)  # rad/min
    
    # Process transfer function: Kp * exp(-θs) / (Ts + 1)
    Kp = results['tuning_parameters']['Kc_pi'] * (-2.5)  # Include process gain
    T = 12.0  # Process time constant
    theta = 0.8  # Dead time
    
    # Magnitude and phase (simplified)
    magnitude = np.abs(Kp) / np.sqrt((T * frequency)**2 + 1)
    phase = -np.arctan(T * frequency) - theta * frequency
    
    # Convert to dB and degrees
    magnitude_db = 20 * np.log10(magnitude)
    phase_deg = np.degrees(phase)
    
    ax5.semilogx(frequency, magnitude_db, color=colors['cooling'], linewidth=2, 
                 label='Open-Loop Magnitude')
    ax5.axhline(y=0, color='red', linestyle='--', alpha=0.7, label='0 dB')
    ax5.set_xlabel('Frequency (rad/min)', fontsize=11, weight='bold')
    ax5.set_ylabel('Magnitude (dB)', fontsize=11, weight='bold')
    ax5.set_title('Stability Analysis\n(Open-Loop)', fontsize=12, weight='bold')
    ax5.grid(True, alpha=0.3)
    ax5.legend(fontsize=9)
    
    # Find gain and phase margins (simplified)
    try:
        # Gain margin at phase crossover
        phase_crossover_idx = np.where(np.diff(np.signbit(phase_deg + 180)))[0]
        if len(phase_crossover_idx) > 0:
            gain_margin = -magnitude_db[phase_crossover_idx[0]]
            ax5.text(0.05, 0.95, f'GM ≈ {gain_margin:.1f} dB', transform=ax5.transAxes,
                     fontsize=10, weight='bold', color='red',
                     bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    except:
        pass
    
    # ==============================================
    # PLOT 6: TUNING GUIDELINES
    # ==============================================
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')  # Remove axes for text plot
    
    # Create tuning guidelines table
    guidelines_text = """ZIEGLER-NICHOLS TUNING GUIDELINES
    
Process Characteristics:
• L/T Ratio: 0.067 (Low dead time)
• Control Quality: Good
• Recommended: PI Control
    
Tuning Recommendations:
✓ Use ZN-PI for temperature loops
✓ Consider conservative tuning
⚠ Avoid derivative action
⚠ Implement anti-windup
    
Performance Assessment:
• Overshoot: Acceptable
• Settling: Fast
• Stability: Good margins
• Economy: Cost effective
    
Process Industries Applications:
• Chemical reactors
• Heat exchangers  
• Distillation columns
• Crystallizers"""
    
    ax6.text(0.05, 0.95, guidelines_text, transform=ax6.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.3))
    
    # ==============================================
    # OVERALL FIGURE FORMATTING
    # ==============================================
    
    # Main title
    fig.suptitle('Ziegler-Nichols Tuning Methodology: CSTR Temperature Control Analysis',
                 fontsize=16, weight='bold', y=0.95, color=colors['text'])
    
    # Add watermark/attribution
    fig.text(0.99, 0.01, 'sproclib.controller.tuning', ha='right', va='bottom',
             fontsize=8, alpha=0.7, style='italic')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = '/Users/macmini/Desktop/github/sproclib/sproclib/controller/tuning/ZieglerNicholsTuning_analysis_plots.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"✓ Comprehensive Ziegler-Nichols analysis plots saved to: {output_path}")
    
    return fig

if __name__ == "__main__":
    # Create the comprehensive plots
    fig = create_ziegler_nichols_plots()
    plt.show()
    
    print("✓ Ziegler-Nichols visualization complete!")
    print("✓ Analysis includes: step test, parameter identification, tuning comparison,")
    print("  closed-loop response, error analysis, stability assessment, and guidelines.")
