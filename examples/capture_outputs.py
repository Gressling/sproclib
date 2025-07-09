"""
Documentation Output Capture Script
===================================

This script runs all SPROCLIB examples and captures their output
for inclusion in Sphinx documentation.
"""

import subprocess
import sys
import os
from pathlib import Path
import time

def run_example_and_capture(script_name, output_dir):
    """Run an example script and capture its output."""
    
    print(f"Running {script_name}...")
    
    try:
        # Run the script and capture output
        result = subprocess.run(
            [sys.executable, script_name],
            cwd="examples",
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout
        )
        
        # Create output filename
        base_name = script_name.replace('.py', '')
        output_file = output_dir / f"{base_name}_output.txt"
        
        # Write the output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Output from {script_name}\n")
            f.write(f"# Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Exit code: {result.returncode}\n\n")
            
            f.write("## STDOUT:\n")
            f.write(result.stdout)
            
            if result.stderr:
                f.write("\n## STDERR:\n")
                f.write(result.stderr)
        
        print(f"✅ {script_name} completed (exit code: {result.returncode})")
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print(f"❌ {script_name} timed out")
        return False
    except Exception as e:
        print(f"❌ {script_name} failed: {e}")
        return False

def main():
    """Main function to run all examples and capture outputs."""
    
    print("SPROCLIB Documentation Output Capture")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path("documentation_outputs")
    output_dir.mkdir(exist_ok=True)
    
    # List of example scripts
    example_scripts = [
        "pump_examples.py",
        "compressor_examples.py", 
        "valve_examples.py",
        "tank_examples.py",
        "reactor_examples.py",
        "heat_exchanger_examples.py",
        "distillation_examples.py",
        "utilities_examples.py",
        "complete_process_examples.py"
    ]
    
    # Run each example
    results = {}
    
    for script in example_scripts:
        success = run_example_and_capture(script, output_dir)
        results[script] = success
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    successful = sum(results.values())
    total = len(results)
    
    print(f"Successful: {successful}/{total}")
    
    for script, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {script}")
    
    # Copy any generated images
    examples_dir = Path("examples")
    images = list(examples_dir.glob("*.png")) + list(examples_dir.glob("*.jpg")) + list(examples_dir.glob("*.svg"))
    
    if images:
        print(f"\nFound {len(images)} image files:")
        for img in images:
            print(f"📊 {img.name}")
            # Copy to output directory
            import shutil
            shutil.copy2(img, output_dir / img.name)
    
    print(f"\nAll outputs saved to: {output_dir.absolute()}")
    
    # Create index file
    index_file = output_dir / "index.md"
    with open(index_file, 'w') as f:
        f.write("# SPROCLIB Examples Documentation Outputs\n\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Example Scripts Output Files\n\n")
        for script in example_scripts:
            base_name = script.replace('.py', '')
            status = "✅" if results[script] else "❌"
            f.write(f"- {status} [{base_name}_output.txt]({base_name}_output.txt) - Output from {script}\n")
        
        if images:
            f.write("\n## Generated Images\n\n")
            for img in images:
                f.write(f"- 📊 [{img.name}]({img.name})\n")
        
        f.write(f"\n## Summary\n")
        f.write(f"- Total examples: {total}\n")
        f.write(f"- Successful: {successful}\n")
        f.write(f"- Failed: {total - successful}\n")

if __name__ == "__main__":
    main()
