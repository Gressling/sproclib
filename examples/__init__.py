"""
SPROCLIB Examples Index
======================

This module provides an index and runner for all SPROCLIB examples.
Each example demonstrates the usage of refactored SPROCLIB units with both
simple and comprehensive use cases.

Available Examples:
- Pump Examples: CentrifugalPump, PositiveDisplacementPump
- Compressor Examples: Compressor operations and performance
- Valve Examples: ControlValve, ThreeWayValve operations
- Tank Examples: Tank, InteractingTanks systems
- Reactor Examples: CSTR, PFR, Batch, SemiBatch, Fixed/Fluidized Bed
- Heat Exchanger Examples: Various configurations and calculations
- Distillation Examples: BinaryDistillationColumn, DistillationTray
- Utilities Examples: LinearApproximation and analysis tools
- Complete Process Examples: Integrated multi-unit processes

Requirements:
- NumPy
- SciPy
- All refactored SPROCLIB units
"""

import sys
import os

# Add the process_control directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_example(example_name):
    """
    Run a specific example by name.
    
    Args:
        example_name (str): Name of the example to run
    """
    examples = {
        "pump": "pump_examples",
        "compressor": "compressor_examples", 
        "valve": "valve_examples",
        "tank": "tank_examples",
        "reactor": "reactor_examples",
        "heat_exchanger": "heat_exchanger_examples",
        "distillation": "distillation_examples",
        "utilities": "utilities_examples",
        "complete_process": "complete_process_examples"
    }
    
    if example_name not in examples:
        print(f"Error: Example '{example_name}' not found.")
        print(f"Available examples: {', '.join(examples.keys())}")
        return
    
    try:
        module_name = examples[example_name]
        module = __import__(module_name)
        module.main()
    except ImportError as e:
        print(f"Error importing {module_name}: {e}")
    except Exception as e:
        print(f"Error running {example_name} example: {e}")


def list_examples():
    """List all available examples with descriptions."""
    
    examples_info = [
        ("pump", "Pump Examples", "CentrifugalPump and PositiveDisplacementPump operations"),
        ("compressor", "Compressor Examples", "Compressor performance and multi-stage analysis"),
        ("valve", "Valve Examples", "ControlValve and ThreeWayValve operations"),
        ("tank", "Tank Examples", "Tank systems, level control, and interacting tanks"),
        ("reactor", "Reactor Examples", "CSTR, PFR, Batch, and specialized reactors"),
        ("heat_exchanger", "Heat Exchanger Examples", "Heat transfer calculations and configurations"),
        ("distillation", "Distillation Examples", "Binary distillation and tray analysis"),
        ("utilities", "Utilities Examples", "LinearApproximation and analysis tools"),
        ("complete_process", "Complete Process Examples", "Integrated multi-unit process simulations")
    ]
    
    print("SPROCLIB Examples Available:")
    print("=" * 60)
    
    for i, (key, title, description) in enumerate(examples_info, 1):
        print(f"{i:2d}. {title}")
        print(f"    Key: '{key}'")
        print(f"    Description: {description}")
        print()


def run_all_examples():
    """Run all examples in sequence."""
    
    examples = [
        "pump", "compressor", "valve", "tank", "reactor", 
        "heat_exchanger", "distillation", "utilities", "complete_process"
    ]
    
    print("Running All SPROCLIB Examples")
    print("=" * 50)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'='*20} Example {i}/{len(examples)}: {example.replace('_', ' ').title()} {'='*20}")
        try:
            run_example(example)
        except Exception as e:
            print(f"Error in {example} example: {e}")
            continue
        
        if i < len(examples):
            print(f"\n{'-'*50}")
            input("Press Enter to continue to next example...")
    
    print(f"\n{'='*50}")
    print("All examples completed!")


def run_simple_examples_only():
    """Run only the simple portions of all examples."""
    
    print("Running Simple Examples Only")
    print("=" * 40)
    
    simple_functions = [
        ("pump_examples", "simple_pump_example"),
        ("compressor_examples", "simple_compressor_example"),
        ("valve_examples", "simple_valve_examples"),
        ("tank_examples", "simple_tank_examples"),
        ("reactor_examples", "simple_reactor_examples"),
        ("heat_exchanger_examples", "simple_heat_exchanger_examples"),
        ("distillation_examples", "simple_distillation_examples"),
        ("utilities_examples", "simple_utilities_examples"),
        ("complete_process_examples", "simple_integrated_process")
    ]
    
    for module_name, function_name in simple_functions:
        try:
            print(f"\n--- {module_name.replace('_', ' ').title()} ---")
            module = __import__(module_name)
            getattr(module, function_name)()
        except (ImportError, AttributeError) as e:
            print(f"Error running {function_name}: {e}")


def run_comprehensive_examples_only():
    """Run only the comprehensive portions of all examples."""
    
    print("Running Comprehensive Examples Only")
    print("=" * 40)
    
    comprehensive_functions = [
        ("pump_examples", "comprehensive_pump_example"),
        ("compressor_examples", "comprehensive_compressor_example"),
        ("valve_examples", "comprehensive_valve_examples"),
        ("tank_examples", "comprehensive_tank_examples"),
        ("reactor_examples", "comprehensive_reactor_examples"),
        ("heat_exchanger_examples", "comprehensive_heat_exchanger_examples"),
        ("distillation_examples", "comprehensive_distillation_examples"),
        ("utilities_examples", "comprehensive_utilities_examples"),
        ("complete_process_examples", "comprehensive_chemical_plant")
    ]
    
    for module_name, function_name in comprehensive_functions:
        try:
            print(f"\n--- {module_name.replace('_', ' ').title()} ---")
            module = __import__(module_name)
            getattr(module, function_name)()
        except (ImportError, AttributeError) as e:
            print(f"Error running {function_name}: {e}")


def main():
    """
    Main function to provide an interactive menu for running examples.
    """
    
    while True:
        print("\n" + "=" * 60)
        print("SPROCLIB Examples - Interactive Menu")
        print("=" * 60)
        print("1. List all available examples")
        print("2. Run a specific example")
        print("3. Run all examples")
        print("4. Run simple examples only")
        print("5. Run comprehensive examples only")
        print("6. Exit")
        print("-" * 60)
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                list_examples()
                
            elif choice == "2":
                list_examples()
                example_name = input("Enter example key: ").strip().lower()
                run_example(example_name)
                
            elif choice == "3":
                run_all_examples()
                
            elif choice == "4":
                run_simple_examples_only()
                
            elif choice == "5":
                run_comprehensive_examples_only()
                
            elif choice == "6":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("SPROCLIB Examples Collection")
    print("=" * 30)
    print("This collection demonstrates the usage of refactored SPROCLIB units.")
    print("Each unit class is now in its own file for better modularity.")
    print()
    
    # Check if run directly with argument
    if len(sys.argv) > 1:
        example_name = sys.argv[1].lower()
        
        if example_name == "--list":
            list_examples()
        elif example_name == "--all":
            run_all_examples()
        elif example_name == "--simple":
            run_simple_examples_only()
        elif example_name == "--comprehensive":
            run_comprehensive_examples_only()
        else:
            run_example(example_name)
    else:
        main()
