# LaTeX Build Scripts Collection

This repository contains multiple scripts for building the Persian LaTeX book with different approaches and platforms.

## 🚀 Quick Start

### Windows Users

**Option 1: PowerShell (Recommended)**
```powershell
.\Build-LaTeX.ps1
```

**Option 2: Batch File**
```cmd
build_windows.bat
```

**Option 3: Git Bash**
```bash
chmod +x build_gitbash.sh
./build_gitbash.sh
```

### Linux/macOS Users
```bash
chmod +x quick_build.sh
./quick_build.sh
```

## 📋 Available Scripts

### Main Scripts
- **`combine_latex_vazir.py`** - Main script with Vazir font support
- **`quick_build.sh`** - Original Unix build script
- **`combine_latex.py`** - Original combine script

### Windows-Specific
- **`build_windows.bat`** - Windows batch file
- **`Build-LaTeX.ps1`** - PowerShell script with error handling
- **`build_gitbash.sh`** - Git Bash compatible script

### Utilities
- **`install_vazir.py`** - Download and install Vazir font
- **`debug_combine.py`** - Debug version for troubleshooting
- **`create_minimal.py`** - Minimal version without Persian fonts

## 🔧 Prerequisites

### Required Software
1. **Python 3.x**
2. **LaTeX Distribution:**
   - Windows: [MiKTeX](https://miktex.org/download)
   - macOS: [MacTeX](https://www.tug.org/mactex/)
   - Linux: `sudo apt-get install texlive-xetex texlive-lang-other`

### Required Fonts
- **Vazir Font** (for Persian text)
  - Download: https://github.com/rastikerdar/vazir-font/releases
  - Or run: `python install_vazir.py`

## 🎯 Usage Instructions

### Step 1: Install Vazir Font
```bash
# Automatic installation
python install_vazir.py

# Or download manually from GitHub and install .ttf files
```

### Step 2: Build the Book

**Windows PowerShell:**
```powershell
.\Build-LaTeX.ps1
```

**Windows Command Prompt:**
```cmd
build_windows.bat
```

**Unix/Linux/macOS:**
```bash
./quick_build.sh
```

**Manual Steps:**
```bash
# 1. Combine files
python combine_latex_vazir.py

# 2. Test font
xelatex vazir_test.tex

# 3. Build main document
xelatex complete_book.tex
xelatex complete_book.tex  # Run twice for TOC
```

## 🐛 Troubleshooting

### Font Issues
If you get "nullfont" errors:
1. Install Vazir font properly
2. Try the font test: `xelatex vazir_test.tex`
3. Use fallback script: `python create_minimal.py`

### Python Script Hangs
```bash
# Run debug version
python debug_combine.py

# Check file encodings
file *.tex
```

### XeLaTeX Not Found
- **Windows:** Install MiKTeX, restart terminal
- **Git Bash:** Use `build_gitbash.sh` which finds MiKTeX automatically
- **Linux:** `sudo apt-get install texlive-xetex`

### Permission Issues
```bash
# Make scripts executable
chmod +x *.sh
```

## 📂 Output Files

After successful build:
- **`complete_book.pdf`** - Final PDF book
- **`complete_book.tex`** - Combined LaTeX source
- **`vazir_test.pdf`** - Font test document

## 🔄 Workflow

1. **Preparation:** Install Python, LaTeX, and Vazir font
2. **Combine:** Run combine script to merge all .tex files
3. **Test:** Verify font setup with test document
4. **Build:** Compile main document (run twice for references)
5. **View:** Open the final PDF

## 💡 Tips

- **First time:** Run `python install_vazir.py` to setup fonts
- **Quick test:** Use `xelatex vazir_test.tex` to verify setup
- **Debugging:** Use `debug_combine.py` if main script fails
- **Minimal version:** Use `create_minimal.py` for basic PDF without Persian fonts
- **Windows users:** PowerShell script has the best error handling

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run the debug script: `python debug_combine.py`
3. Verify font installation: `python install_vazir.py`
4. Try the minimal version: `python create_minimal.py`