"""
Setup configuration for SPROCLIB - Standard Process Control Library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sproclib",
    version="1.0.0",
    author="Thorsten Gressling",
    author_email="gressling@paramus.ai",
    description="SPROCLIB - Standard Process Control Library for chemical processes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gressling/sproclib",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "control>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "sphinx>=4.0",
            "sphinx-rtd-theme",
            "black",
            "flake8",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme",
            "myst-parser",
        ],
    },
    keywords="process control, chemical engineering, PID, control systems, process modeling, simulation",
    project_urls={
        "Documentation": "https://sproclib.readthedocs.io/",
        "Source": "https://github.com/gressling/sproclib",
        "Tracker": "https://github.com/gressling/sproclib/issues",
    },
)
