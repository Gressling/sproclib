"""
SPROCLIB Documentation Builder

Technical documentation build system for SPROCLIB process control library.
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

class SPROCLIBDocumentationBuilder:
    """Documentation builder for SPROCLIB process control library."""
    
    def __init__(self):
        self.docs_dir = Path(__file__).parent
        self.source_dir = self.docs_dir / "source"
        self.build_dir = self.docs_dir / "build"
        self.examples_dir = self.docs_dir.parent / "examples"
        
    def clean_all(self):
        """Clean all build artifacts."""
        print("Cleaning all documentation artifacts...")
        
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        examples_dest = self.source_dir / "examples"
        if examples_dest.exists():
            shutil.rmtree(examples_dest)
        
        api_dir = self.source_dir / "api"
        if api_dir.exists():
            for file in api_dir.glob("*.rst"):
                if file.name not in ["index.rst"]:
                    file.unlink()
        
        print("Clean complete!")
    
    def prepare_content(self):
        """Prepare all content for the documentation build."""
        print("Preparing content...")
        
        # Copy examples
        if self.examples_dir.exists():
            examples_dest = self.source_dir / "examples"
            examples_dest.mkdir(exist_ok=True)
            
            for example_file in self.examples_dir.glob("*.py"):
                shutil.copy2(example_file, examples_dest / example_file.name)
        
        # Create examples index
        examples_index = self.source_dir / "examples" / "index.rst"
        examples_index.parent.mkdir(exist_ok=True)
        
        content = """Examples
========

Process control and plant design examples demonstrating SPROCLIB capabilities.

.. toctree::
   :maxdepth: 2
   
   semantic_plant_example

Quick Start Example
------------------

.. code-block:: python

    from unit.plant import ChemicalPlant
    from unit.reactor.cstr import CSTR
    from unit.pump import CentrifugalPump
    
    # Define plant
    plant = ChemicalPlant("Process Plant")
    plant.add(CentrifugalPump(H0=50.0), name="pump")
    plant.add(CSTR(V=150.0), name="reactor")
    plant.connect("pump", "reactor")
    plant.compile(optimizer="economic")
    plant.optimize(target_production=1000.0)
    plant.summary()
"""
        
        with open(examples_index, 'w') as f:
            f.write(content)
        
        # Create semantic example documentation
        semantic_example = self.source_dir / "examples" / "semantic_plant_example.rst"
        
        semantic_content = """Complete Plant Design Example
==============================

Demonstration of SPROCLIB's semantic plant design API.

.. literalinclude:: semantic_plant_example.py
   :language: python
   :caption: Complete Semantic Plant Example

This example shows how to build complete chemical plants using TensorFlow/Keras-style syntax.

Key Features Demonstrated
------------------------

* **Sequential unit addition** like neural network layers
* **Functional connections** between process units
* **Compilation and optimization** like ML model training
* **Plant-wide analysis** and performance metrics
* **Industrial-grade calculations** with simple syntax

The semantic plant design API makes chemical engineering as intuitive as machine learning!
"""
        
        with open(semantic_example, 'w') as f:
            f.write(semantic_content)
        
        print("✅ Content preparation complete!")
    
    def build_documentation(self):
        """Build the complete documentation."""
        print("🔨 Building complete SPROCLIB documentation...")
        
        self.build_dir.mkdir(exist_ok=True)
        html_dir = self.build_dir / "html"
        
        cmd = [
            sys.executable, "-m", "sphinx",
            "-b", "html",
            "-E",  # Rebuild all files
            str(self.source_dir),
            str(html_dir)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=self.docs_dir)
            print("✅ Documentation built successfully!")
            print(f"📖 Documentation available at: {html_dir / 'index.html'}")
            return True
        except subprocess.CalledProcessError as e:
            print("❌ Documentation build failed:")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return False
    
    def build_complete(self):
        """Complete build process."""
        print("🚀 SPROCLIB Documentation - The TensorFlow/Keras for Chemical Engineering")
        print("=" * 75)
        
        # Clean everything
        self.clean_all()
        
        # Prepare content
        self.prepare_content()
        
        # Build documentation
        success = self.build_documentation()
        
        print("\n" + "=" * 75)
        if success:
            print("🎉 SPROCLIB Documentation Build Complete!")
            print(f"\n📖 View documentation:")
            print(f"   {self.build_dir / 'html' / 'index.html'}")
            print("\n🌟 Semantic Plant Design API - The core of SPROCLIB!")
        else:
            print("❌ Documentation build failed")
        
        return success

def main():
    """Main build function."""
    try:
        builder = SPROCLIBDocumentationBuilder()
        return builder.build_complete()
    except Exception as e:
        print(f"❌ Build script error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
.. code-block:: python

    # TensorFlow/Keras
    model = keras.Sequential()
    model.add(layers.Dense(64, activation='relu'))
    model.compile(optimizer='adam', loss='mse')
    model.fit(x_train, y_train)
    
    # SPROCLIB (same pattern!)
    plant = ChemicalPlant()
    plant.add(CentrifugalPump(H0=50.0, eta=0.75))
    plant.compile(optimizer='economic', loss='total_cost')
    plant.optimize(target_production=1000.0)

**2. Industrial-Grade Results**

Despite the simple syntax, you get production-ready calculations:

* Real chemical reaction kinetics
* Accurate pump performance curves
* Rigorous distillation calculations
* Economic optimization with constraints
* Dynamic simulation with mass/energy balances

Running the Example
------------------

.. code-block:: bash

    cd examples
    python semantic_plant_example.py

The semantic plant design API represents the future of chemical engineering software!
'''
        
        with open(semantic_example, 'w') as f:
            f.write(semantic_content)
        
        print("✅ Semantic content created!")
    
    def build_html(self, strict=True):
        """Build HTML documentation."""
        print("🔨 Building HTML documentation...")
        
        self.build_dir.mkdir(exist_ok=True)
        html_dir = self.build_dir / "html"
        
        cmd = [
            sys.executable, "-m", "sphinx",
            "-b", "html",
        ]
        
        if strict:
            cmd.append("-W")  # Treat warnings as errors
        
        cmd.extend([
            str(self.source_dir),
            str(html_dir)
        ])
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=self.docs_dir)
            print("✅ HTML documentation built successfully!")
            print(f"📖 Documentation available at: {html_dir / 'index.html'}")
            return True
        except subprocess.CalledProcessError as e:
            print("❌ HTML documentation build failed:")
            print(f"Command: {' '.join(cmd)}")
            print(f"STDOUT: {e.stdout}")
            print(f"STDERR: {e.stderr}")
            return False
    
    def build_all(self, clean=True, strict=False):
        """Complete build process."""
        print("🚀 SPROCLIB Documentation Build - Semantic Plant Design Focus")
        print("=" * 70)
        
        if clean:
            self.clean_all()
        
        success = True
        
        # Copy examples
        self.copy_examples()
        
        # Create semantic content
        self.create_semantic_content()
        
        # Build HTML
        if not self.build_html(strict=strict):
            success = False
        
        print("\n" + "=" * 70)
        if success:
            print("🎉 Documentation build completed successfully!")
            print("\n📖 View documentation:")
            print(f"   HTML: {self.build_dir / 'html' / 'index.html'}")
            print("\n🌟 Semantic Plant Design API is now the main feature!")
        else:
            print("❌ Documentation build completed with errors")
            print("Check the output above for details")
        
        return success

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description="SPROCLIB Documentation Builder")
    parser.add_argument("--no-clean", action="store_true", help="Skip cleaning step")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--clean-only", action="store_true", help="Only clean, don't build")
    
    args = parser.parse_args()
    
    builder = DocumentationBuilder()
    
    if args.clean_only:
        builder.clean_all()
        return True
    
    return builder.build_all(
        clean=not args.no_clean,
        strict=args.strict
    )

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
