"""
Fix Unicode characters in reactor examples for Windows compatibility.
"""

import re

def fix_unicode_in_file(filename):
    """Fix Unicode characters in a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Unicode characters with ASCII equivalents
    replacements = {
        'h⁻¹': 'h^-1',
        '°C': 'degC',
        'k₁': 'k1',
        'k₂': 'k2',
        '→': ' -> ',
        'τ': 'tau'
    }
    
    for unicode_char, ascii_equiv in replacements.items():
        content = content.replace(unicode_char, ascii_equiv)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed Unicode characters in {filename}")

if __name__ == "__main__":
    fix_unicode_in_file("reactor_examples.py")
