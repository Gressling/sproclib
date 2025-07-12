"""
Setup configuration for SPROCLIB - Standard Process Control Library
"""

from setuptools import setup, find_packages
import os

# Read README file
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Standard Process Control Library for chemical process control"

setup(
    name="sproclib",
    version="2.0.0",
    author="Thorsten Gressling",
    author_email="gressling@paramus.ai",
    description="Standard Process Control Library for chemical process control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gressling/sproclib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
        "optimization": [
            "cvxpy>=1.1.0",
            "gekko>=1.0.0",
        ],
    },
    keywords="process control, chemical engineering, PID, control systems, process modeling, simulation",
    project_urls={
        "Documentation": "https://sproclib.readthedocs.io/",
        "Source": "https://github.com/gressling/sproclib",
        "Tracker": "https://github.com/gressling/sproclib/issues",
    },
)
