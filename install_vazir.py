#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to download and check Vazir font installation
"""

import os
import urllib.request
import zipfile
import shutil

def download_vazir_font():
    """Download Vazir font from GitHub"""
    
    print("📥 Downloading Vazir font...")
    
    # Vazir font download URL
    font_url = "https://github.com/rastikerdar/vazir-font/releases/download/v30.1.0/vazir-font-v30.1.0.zip"
    
    try:
        # Download the font
        urllib.request.urlretrieve(font_url, "vazir-font.zip")
        print("✅ Font downloaded successfully")
        
        # Extract the font
        with zipfile.ZipFile("vazir-font.zip", 'r') as zip_ref:
            zip_ref.extractall("vazir-font")
        
        print("✅ Font extracted")
        
        # List the font files
        font_dir = "vazir-font"
        font_files = []
        for root, dirs, files in os.walk(font_dir):
            for file in files:
                if file.endswith('.ttf'):
                    font_files.append(os.path.join(root, file))
        
        print(f"📄 Found font files: {font_files}")
        
        # Instructions for installation
        print("\n" + "="*50)
        print("📋 FONT INSTALLATION INSTRUCTIONS:")
        print("="*50)
        print("1. Navigate to the vazir-font folder")
        print("2. Double-click on each .ttf file")
        print("3. Click 'Install' button")
        print("4. After installing all fonts, run:")
        print("   python combine_latex_vazir.py")
        print("   xelatex vazir_test.tex")
        
        # Clean up
        os.remove("vazir-font.zip")
        
    except Exception as e:
        print(f"❌ Error downloading font: {e}")
        print("Please manually download from:")
        print("https://github.com/rastikerdar/vazir-font/releases")

def check_font_availability():
    """Check if Vazir font is available on the system"""
    
    print("🔍 Checking font availability...")
    
    # Create a test LaTeX file to check fonts
    test_content = r"""\documentclass{article}
\usepackage{fontspec}

\begin{document}
\fontspec{Vazir} Persian text test
\end{document}"""
    
    with open('font_check.tex', 'w') as f:
        f.write(test_content)
    
    # Try to compile with XeLaTeX
    result = os.system('xelatex -interaction=nonstopmode font_check.tex > nul 2>&1')
    
    if result == 0:
        print("✅ Vazir font is available!")
        # Clean up
        for ext in ['tex', 'pdf', 'log', 'aux']:
            try:
                os.remove(f'font_check.{ext}')
            except:
                pass
        return True
    else:
        print("❌ Vazir font not found")
        return False

if __name__ == "__main__":
    print("🔧 Vazir Font Setup Helper")
    print("=" * 30)
    
    # Check if font is already available
    if check_font_availability():
        print("✅ Vazir font is ready to use!")
        print("You can now run: python combine_latex_vazir.py")
    else:
        print("📥 Vazir font not found. Downloading...")
        download_vazir_font()