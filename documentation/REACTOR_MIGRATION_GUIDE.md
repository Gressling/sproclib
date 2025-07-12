# SPROCLIB Reactor Package Migration Guide

## Overview

The SPROCLIB reactor package has been restructured to provide better organization, maintainability, and user experience. This guide explains the changes and how to migrate existing code.

## New Package Structure

### Before (Old Structure)
```
sproclib/unit/reactor/
├── __init__.py
├── BatchReactor.py                 # Class definition
├── batch_reactor_test.py          # Tests
├── batch_reactor_example.py       # Examples
├── batch_reactor_documentation.md # Documentation
├── batch_reactor_example_plots.png # Plots
├── cstr.py                        # Class definition
├── cstr_test.py                   # Tests
└── ... (all files mixed together)
```

### After (New Structure)
```
sproclib/unit/reactor/
├── __init__.py                    # Main package with all exports
├── cstr/                          # CSTR reactor package
│   ├── __init__.py               # CSTR class definition
│   ├── documentation.md          # Theory and usage
│   ├── test_cstr.py             # Comprehensive tests
│   ├── example.py               # Usage examples
│   ├── example.out              # Example output
│   ├── plots/                   # Visualization plots
│   │   ├── example_plots.png
│   │   └── detailed_analysis.png
│   └── cstr.rst                 # Sphinx documentation
├── batch/                        # Batch reactor package
│   └── ... (similar structure)
├── plug_flow/                    # PFR package
│   └── ... (similar structure)
├── fixed_bed/                    # Fixed bed package
│   └── ... (similar structure)
├── semi_batch/                   # Semi-batch package
│   └── ... (similar structure)
└── fluidized_bed/                # Fluidized bed package
    └── ... (similar structure)
```

## Import Changes

### Recommended Imports (Work with both old and new structure)

```python
# Method 1: Import from main reactor package (RECOMMENDED)
from sproclib.unit.reactor import CSTR, BatchReactor, PlugFlowReactor

# Method 2: Import from main sproclib package (ALSO RECOMMENDED)
from sproclib import CSTR, BatchReactor, PlugFlowReactor

# Method 3: Import from specific subpackage (NEW)
from sproclib.unit.reactor.cstr import CSTR
from sproclib.unit.reactor.batch import BatchReactor
```

### Legacy Imports (Still work during transition)

```python
# These still work but are deprecated
from sproclib.unit.reactor.BatchReactor import BatchReactor
from sproclib.unit.reactor.cstr import CSTR  # This was always a package
```

## Benefits of New Structure

### 1. **Better Organization**
- Each reactor type is self-contained
- Related files (docs, tests, examples) are grouped together
- Easier to find and maintain reactor-specific code

### 2. **Scalability**
- Easy to add new reactor types
- Each reactor can evolve independently
- Clear separation of concerns

### 3. **Improved Documentation**
- Reactor-specific documentation in dedicated files
- Plots and examples organized by reactor type
- Better Sphinx documentation structure

### 4. **Easier Testing**
- Tests are co-located with the reactor code
- Can run tests for specific reactor types
- Clear test organization

### 5. **Cleaner Imports**
- More intuitive import paths
- Consistent import patterns
- Better IDE support and autocomplete

## Migration Steps

### For Users (Code Updates)

1. **Update your imports** to use the recommended patterns:
   ```python
   # OLD
   from sproclib.unit.reactor.BatchReactor import BatchReactor
   
   # NEW (recommended)
   from sproclib.unit.reactor import BatchReactor
   # or
   from sproclib import BatchReactor
   ```

2. **No changes needed** to reactor usage - the API remains the same:
   ```python
   # This works exactly the same
   reactor = BatchReactor(V=100.0, k0=1e10)
   results = reactor.simulate(t_final=120.0)
   ```

### For Developers (Package Maintenance)

1. **File Organization**: Use the provided `organize_reactor_files.py` script:
   ```bash
   # Preview changes
   python organize_reactor_files.py --dry-run
   
   # Apply changes
   python organize_reactor_files.py
   ```

2. **Update Documentation**: Reactor-specific docs are now in `documentation.md` files
3. **Update Tests**: Tests are now named `test_{reactor_type}.py`
4. **Update Examples**: Examples are now named `example.py` per reactor

## Compatibility

### Backward Compatibility
- **All existing imports continue to work** during the transition period
- **No breaking changes** to reactor APIs
- **Gradual migration** - can migrate one reactor at a time

### Forward Compatibility
- New structure supports future enhancements
- Better plugin architecture for custom reactors
- Improved documentation generation

## Package Discovery and Introspection

The new structure includes utility functions for package discovery:

```python
from sproclib.unit.reactor import list_reactors, get_reactor_info, REACTOR_CATEGORIES

# List all available reactors
print(list_reactors())
# Output: ['CSTR', 'BatchReactor', 'PlugFlowReactor', ...]

# Get reactor categories
print(REACTOR_CATEGORIES['continuous'])
# Output: ['CSTR', 'PlugFlowReactor']

# Get detailed reactor information
info = get_reactor_info('CSTR')
print(info['description'])
```

## Testing the Migration

### Verify Imports Work
```python
# Test that all reactors can be imported
try:
    from sproclib.unit.reactor import (
        CSTR, BatchReactor, PlugFlowReactor, 
        FixedBedReactor, SemiBatchReactor, FluidizedBedReactor
    )
    print("✓ All reactor imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")

# Test instantiation
reactors = {
    'CSTR': CSTR(),
    'BatchReactor': BatchReactor(),
    'PlugFlowReactor': PlugFlowReactor()
}

for name, reactor in reactors.items():
    print(f"✓ {name} instantiated successfully")
```

### Run Tests
```bash
# Test all reactors
python -m pytest sproclib/unit/reactor/ -v

# Test specific reactor
python -m pytest sproclib/unit/reactor/cstr/ -v
```

## Timeline

- **Phase 1**: New structure implementation (✓ Complete)
- **Phase 2**: File organization and migration tools (✓ Complete)
- **Phase 3**: Documentation updates (In Progress)
- **Phase 4**: Deprecation warnings for old patterns (Future)
- **Phase 5**: Remove old files (Future)

## Questions and Support

For questions about the migration:
1. Check this migration guide
2. Review the new package structure
3. Test imports and functionality
4. Contact the development team if issues persist

The migration is designed to be **seamless and backward-compatible**, so existing code should continue to work without changes while new code can take advantage of the improved structure.
