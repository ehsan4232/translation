#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug version of the combine script
"""

import os
import re
import glob
import sys

def debug_step(message):
    print(f"🔍 {message}")
    sys.stdout.flush()

def main():
    debug_step("Starting debug script...")
    
    # Check current directory
    debug_step(f"Current directory: {os.getcwd()}")
    
    # List all files
    all_files = os.listdir('.')
    debug_step(f"All files in directory: {len(all_files)} files")
    
    # Find .tex files
    tex_files = glob.glob('*.tex')
    debug_step(f"Found .tex files: {tex_files}")
    
    if not tex_files:
        debug_step("❌ No .tex files found!")
        return
    
    # Sort them
    try:
        tex_files_sorted = sorted(tex_files, key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
        debug_step(f"Sorted .tex files: {tex_files_sorted}")
    except Exception as e:
        debug_step(f"❌ Error sorting files: {e}")
        return
    
    # Try to read each file
    for i, tex_file in enumerate(tex_files_sorted[:3]):  # Only test first 3 files
        debug_step(f"Processing file {i+1}/{len(tex_files_sorted)}: {tex_file}")
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
                debug_step(f"✓ Read {tex_file}: {len(content)} characters")
                
            # Check for document markers
            if '\\begin{document}' in content:
                debug_step(f"✓ Found \\begin{{document}} in {tex_file}")
            else:
                debug_step(f"⚠️ No \\begin{{document}} in {tex_file}")
                
        except Exception as e:
            debug_step(f"❌ Error reading {tex_file}: {e}")
            return
    
    # Try to create a simple output file
    debug_step("Creating test output file...")
    try:
        with open('test_output.tex', 'w', encoding='utf-8') as f:
            f.write("\\documentclass{article}\n\\begin{document}\nTest file created successfully!\n\\end{document}")
        debug_step("✅ Test output file created successfully!")
    except Exception as e:
        debug_step(f"❌ Error creating output file: {e}")
        return
    
    debug_step("✅ Debug completed successfully!")

if __name__ == "__main__":
    main()