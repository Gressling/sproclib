"""
Capture All SPROCLIB Examples Output for Documentation
======================================================

This script runs all SPROCLIB examples and captures their outputs for use in Sphinx documentation.
It also captures any generated images/plots.

Requirements:
- All SPROCLIB examples must be functional
- Output captured to text files for documentation
"""

import subprocess
import sys
import os
import shutil
from datetime import datetime

def run_example_and_capture(example_name, output_dir):
    """
    Run a specific example and capture its output.
    
    Args:
        example_name (str): Name of the example script (without .py)
        output_dir (str): Directory to save output files
    """
    script_path = f"{example_name}.py"
    output_file = os.path.join(output_dir, f"{example_name}_output.txt")
    
    print(f"Running {example_name}...")
    
    try:
        # Run the example script and capture output
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'  # Handle encoding issues gracefully
        )
        
        # Write output to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"SPROCLIB Example Output: {example_name}\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            if result.stdout:
                f.write("STDOUT:\n")
                f.write("-" * 40 + "\n")
                f.write(result.stdout)
                f.write("\n\n")
            
            if result.stderr:
                f.write("STDERR:\n")
                f.write("-" * 40 + "\n")
                f.write(result.stderr)
                f.write("\n\n")
            
            f.write(f"Return code: {result.returncode}\n")
        
        # Check for generated images
        image_extensions = ['.png', '.jpg', '.jpeg', '.pdf', '.svg']
        for ext in image_extensions:
            for file in os.listdir('.'):
                if file.endswith(ext) and example_name in file:
                    # Copy image to output directory
                    dest_path = os.path.join(output_dir, file)
                    shutil.copy2(file, dest_path)
                    print(f"  Captured image: {file}")
        
        if result.returncode == 0:
            print(f"  SUCCESS: {example_name}")
            return True
        else:
            print(f"  ERROR: {example_name} (return code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"  EXCEPTION: {example_name} - {e}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"ERROR running {example_name}: {e}\n")
        return False

def main():
    """Main function to capture all example outputs."""
    
    # Create output directory
    output_dir = "captured_outputs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # List of all example scripts
    examples = [
        "pump_examples",
        "compressor_examples", 
        "valve_examples",
        "tank_examples",
        "reactor_examples",
        "heat_exchanger_examples",
        "distillation_examples",
        "utilities_examples",
        "complete_process_examples"
    ]
    
    print("SPROCLIB Examples Output Capture")
    print("=" * 50)
    print(f"Output directory: {output_dir}")
    print(f"Total examples: {len(examples)}")
    print()
    
    results = {}
    
    # Run each example
    for i, example in enumerate(examples, 1):
        print(f"[{i}/{len(examples)}] {example}")
        success = run_example_and_capture(example, output_dir)
        results[example] = success
    
    # Generate summary
    print("\n" + "=" * 50)
    print("CAPTURE SUMMARY")
    print("=" * 50)
    
    successful = sum(results.values())
    total = len(results)
    
    print(f"Successful: {successful}/{total}")
    print(f"Failed: {total - successful}/{total}")
    print()
    
    print("Individual Results:")
    for example, success in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"  {example:<25} {status}")
    
    # Create index file
    index_file = os.path.join(output_dir, "index.txt")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("SPROCLIB Examples Output Index\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total examples: {total}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {total - successful}\n\n")
        
        f.write("Available Output Files:\n")
        f.write("-" * 30 + "\n")
        
        for example in examples:
            output_file = f"{example}_output.txt"
            status = "SUCCESS" if results[example] else "FAILED"
            f.write(f"{output_file:<35} [{status}]\n")
        
        f.write("\nGenerated Images:\n")
        f.write("-" * 20 + "\n")
        
        image_files = [f for f in os.listdir(output_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.pdf', '.svg'))]
        if image_files:
            for img in sorted(image_files):
                f.write(f"{img}\n")
        else:
            f.write("No images generated.\n")
    
    print(f"\nOutput files saved to: {output_dir}/")
    print(f"Index file: {index_file}")
    
    if successful == total:
        print("\nAll examples captured successfully!")
    else:
        print(f"\n{total - successful} examples failed. Check individual output files for details.")

if __name__ == "__main__":
    main()
