# SPROCLIB Documentation Makefile - Semantic Plant Design Core

SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = source
BUILDDIR     = build
PYTHON       = python

# Default target - complete build
.DEFAULT_GOAL := all

# Complete documentation build with semantic plant design focus
all:
	@echo "🚀 Building SPROCLIB - The TensorFlow/Keras for Chemical Engineering"
	@echo "=================================================================="
	@echo ""
	@echo "🧹 Cleaning previous build..."
	@rm -rf $(BUILDDIR)/*
	@rm -rf $(SOURCEDIR)/examples
	@echo "🔨 Building complete documentation..."
	@if [ -f clean_and_build.py ]; then \
		$(PYTHON) clean_and_build.py; \
	else \
		$(SPHINXBUILD) -b html -E "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS); \
	fi
	@echo ""
	@echo "🎉 SPROCLIB Documentation Build Complete!"
	@echo "📖 Documentation ready at: $(BUILDDIR)/html/index.html"
	@echo "🌟 Semantic Plant Design API is the core feature!"

# Standard Sphinx targets for advanced users
html:
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)

pdf:
	$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)/latex" $(SPHINXOPTS)
	@if [ -d "$(BUILDDIR)/latex" ]; then \
		cd "$(BUILDDIR)/latex" && make; \
	fi

linkcheck:
	$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS)

help:
	@echo "SPROCLIB Documentation Builder"
	@echo "=============================="
	@echo ""
	@echo "Default: make (or make all)"
	@echo "  Complete documentation build with semantic plant design focus"
	@echo ""
	@echo "Advanced targets:"
	@echo "  html       - Build HTML documentation only"
	@echo "  pdf        - Build PDF documentation"
	@echo "  linkcheck  - Check for broken links"
	@echo ""
	@echo "The semantic plant design API is SPROCLIB's core feature."

.PHONY: all html pdf linkcheck help
# API documentation only
api:
	@echo "📚 Generating API documentation..."
	$(PYTHON) clean_and_build.py --api-only
	@echo "📚 API documentation generated!"

# Quick build for development
quick:
	@echo "⚡ Quick HTML build..."
	$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
	@echo "⚡ Quick build complete: $(BUILDDIR)/html/index.html"

# Clean only
clean-only:
	@echo "🧹 Cleaning only..."
	$(PYTHON) clean_and_build.py --clean-only

# Build without strict warnings
no-strict:
	@echo "🔨 Building without strict warnings..."
	$(PYTHON) clean_and_build.py --no-strict

# Check documentation for issues
check:
	@echo "🔍 Checking documentation..."
	$(SPHINXBUILD) -b linkcheck "$(SOURCEDIR)" "$(BUILDDIR)/linkcheck" $(SPHINXOPTS)
	@echo "🔍 Link check complete!"

# Open documentation in browser (platform specific)
open: html
	@echo "🌐 Opening documentation..."
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(BUILDDIR)/html/index.html; \
	elif command -v open > /dev/null; then \
		open $(BUILDDIR)/html/index.html; \
	elif command -v start > /dev/null; then \
		start $(BUILDDIR)/html/index.html; \
	else \
		echo "📖 Documentation ready at: $(BUILDDIR)/html/index.html"; \
	fi

# Development server (if sphinx-autobuild is available)
serve:
	@echo "🖥️ Starting development server..."
	@if command -v sphinx-autobuild > /dev/null; then \
		sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" --host 0.0.0.0 --port 8000; \
	else \
		echo "❌ sphinx-autobuild not available. Install with: pip install sphinx-autobuild"; \
	fi

# Show build info
info:
	@echo "SPROCLIB Documentation Build Information"
	@echo "======================================="
	@echo "Source directory: $(SOURCEDIR)"
	@echo "Build directory:  $(BUILDDIR)"
	@echo "Python:          $(PYTHON)"
	@echo "Sphinx build:    $(SPHINXBUILD)"
	@echo "Sphinx options:  $(SPHINXOPTS)"
	@echo ""
	@echo "Key Features:"
	@echo "• Semantic Plant Design API (main focus)"
	@echo "• TensorFlow/Keras-style syntax"
	@echo "• Complete process unit library"
	@echo "• Industrial-grade examples"

# Phony targets
.PHONY: help semantic clean html pdf api quick clean-only no-strict check open serve info
