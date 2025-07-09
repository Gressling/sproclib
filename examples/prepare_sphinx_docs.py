"""
Prepare SPROCLIB Examples for Sphinx Documentation
===================================================

This script organizes all captured example outputs and creates documentation-ready files
for inclusion in Sphinx documentation.

Features:
- Organizes outputs by example type
- Creates reStructuredText (.rst) files
- Includes code examples and outputs
- Handles images and plots
- Creates index files for navigation
"""

import os
import shutil
from datetime import datetime

def create_rst_file(example_name, output_content, output_dir):
    """
    Create a reStructuredText file for an example.
    
    Args:
        example_name (str): Name of the example
        output_content (str): Content of the example output
        output_dir (str): Directory to save the RST file
    """
    
    # Extract just the stdout content (remove headers and stderr)
    lines = output_content.split('\n')
    stdout_start = None
    stdout_end = None
    
    for i, line in enumerate(lines):
        if line.strip() == "STDOUT:":
            stdout_start = i + 2  # Skip the separator line
        elif line.strip() == "STDERR:" or line.strip().startswith("Return code:"):
            stdout_end = i
            break
    
    if stdout_start is not None:
        if stdout_end is not None:
            stdout_content = '\n'.join(lines[stdout_start:stdout_end])
        else:
            stdout_content = '\n'.join(lines[stdout_start:])
    else:
        stdout_content = output_content
    
    # Clean up the content
    stdout_content = stdout_content.strip()
    
    # Create RST content
    title = f"{example_name.replace('_', ' ').title()}"
    rst_content = f"""
{title}
{'=' * len(title)}

This example demonstrates the usage of {example_name.replace('_examples', '').replace('_', ' ')} units in SPROCLIB.

Example Output
--------------

.. code-block:: text

"""
    
    # Indent the output content for code block
    indented_output = '\n'.join(f"    {line}" for line in stdout_content.split('\n'))
    rst_content += indented_output
    
    # Add image if exists
    image_file = f"{example_name}.png"
    if os.path.exists(os.path.join("captured_outputs", image_file)):
        rst_content += f"""

Generated Plot
--------------

.. image:: ../captured_outputs/{image_file}
    :width: 600px
    :align: center
    :alt: {title} Plot

"""
    
    rst_content += f"""

Source Code
-----------

The complete source code for this example can be found in:
``examples/{example_name}.py``

Key Features Demonstrated
-------------------------

* Simple usage examples for quick learning
* Comprehensive analysis for advanced applications  
* Real engineering calculations and parameters
* Educational explanations and insights

This example is part of the refactored SPROCLIB where each unit class 
is now in its own file for better modularity and maintainability.
"""
    
    # Write RST file
    rst_file = os.path.join(output_dir, f"{example_name}.rst")
    with open(rst_file, 'w', encoding='utf-8') as f:
        f.write(rst_content)
    
    return rst_file

def create_master_index(examples, doc_dir):
    """Create a master index file for all examples."""
    
    index_content = """
SPROCLIB Examples Documentation
===============================

This section contains comprehensive examples demonstrating the usage of all SPROCLIB units.
Each example includes both simple introductory cases and comprehensive advanced analysis.

The examples are organized by unit type and demonstrate real engineering calculations
with educational explanations.

.. toctree::
    :maxdepth: 2
    :caption: Example Categories:

"""
    
    # Add each example to the toctree
    for example in examples:
        index_content += f"    {example}\n"
    
    index_content += """

Overview
--------

Each example demonstrates:

* **Simple Examples**: Basic operations for quick learning
* **Comprehensive Examples**: Advanced analysis and calculations  
* **Real Engineering Data**: Realistic parameters and calculations
* **Educational Content**: Clear explanations and engineering insights

Refactored Architecture
-----------------------

These examples showcase the refactored SPROCLIB architecture where:

* Each unit class is in its own dedicated file
* Better discoverability through class-named files
* Improved maintainability and modularity
* Clear import structure and dependencies
* Backward compatibility maintained

Example Categories
------------------

Pump Examples
    Demonstrates CentrifugalPump and PositiveDisplacementPump operations,
    performance analysis, and system curves.

Compressor Examples  
    Shows compressor performance, multi-stage compression analysis,
    and energy optimization.

Valve Examples
    Covers ControlValve and ThreeWayValve operations, flow characteristics,
    and sizing calculations.

Tank Examples
    Illustrates tank systems, level control, interacting tanks,
    and mixing analysis.

Reactor Examples
    Comprehensive reactor analysis including CSTR, PFR, batch reactors,
    and specialized reactor types with kinetics.

Heat Exchanger Examples
    Heat transfer calculations, different configurations,
    NTU-effectiveness method, and sizing.

Distillation Examples
    Binary distillation analysis, McCabe-Thiele method,
    and tray calculations.

Utilities Examples
    Mathematical utilities, regression analysis,
    and data fitting tools.

Complete Process Examples
    Integrated multi-unit process simulations demonstrating
    how all units work together.
"""
    
    index_file = os.path.join(doc_dir, "index.rst")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    return index_file

def main():
    """Main function to prepare documentation."""
    
    captured_dir = "captured_outputs"
    doc_dir = "sphinx_docs"
    
    # Create documentation directory
    if os.path.exists(doc_dir):
        shutil.rmtree(doc_dir)
    os.makedirs(doc_dir)
    
    print("Preparing SPROCLIB Examples for Sphinx Documentation")
    print("=" * 60)
    print(f"Source directory: {captured_dir}")
    print(f"Documentation directory: {doc_dir}")
    print()
    
    # Copy captured outputs directory
    dest_captured = os.path.join(doc_dir, "captured_outputs")
    shutil.copytree(captured_dir, dest_captured)
    print(f"Copied captured outputs to: {dest_captured}")
    
    # Process each example output file
    examples = []
    
    for filename in os.listdir(captured_dir):
        if filename.endswith("_output.txt"):
            example_name = filename.replace("_output.txt", "")
            examples.append(example_name)
            
            print(f"Processing: {example_name}")
            
            # Read output content
            with open(os.path.join(captured_dir, filename), 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create RST file
            rst_file = create_rst_file(example_name, content, doc_dir)
            print(f"  Created: {os.path.basename(rst_file)}")
    
    # Create master index
    index_file = create_master_index(sorted(examples), doc_dir)
    print(f"Created master index: {os.path.basename(index_file)}")
    
    # Create summary file
    summary_file = os.path.join(doc_dir, "summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("SPROCLIB Examples Documentation Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total examples: {len(examples)}\n")
        f.write(f"Documentation files: {len(examples) + 1} (including index)\n\n")
        
        f.write("Generated Files:\n")
        f.write("-" * 20 + "\n")
        f.write("index.rst (master index)\n")
        for example in sorted(examples):
            f.write(f"{example}.rst\n")
        
        f.write(f"\nCaptured Outputs Directory:\n")
        f.write("-" * 30 + "\n")
        f.write("captured_outputs/ (all original outputs and images)\n")
    
    print(f"Created summary: {os.path.basename(summary_file)}")
    print()
    print("Documentation Preparation Complete!")
    print("=" * 40)
    print(f"Files ready for Sphinx in: {doc_dir}/")
    print(f"Total RST files: {len(examples) + 1}")
    print(f"Images captured: 1 (pump_examples.png)")
    print()
    print("To integrate with Sphinx:")
    print("1. Copy the RST files to your Sphinx source directory")
    print("2. Add the examples to your main toctree")
    print("3. Copy the captured_outputs directory for images")
    print("4. Run 'sphinx-build' to generate documentation")

if __name__ == "__main__":
    main()
