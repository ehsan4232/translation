#!/bin/bash

# Git Bash compatible build script for Windows

echo "🚀 Building LaTeX book in Git Bash..."

# Common MiKTeX installation paths
MIKTEX_PATHS=(
    "/c/Program Files/MiKTeX/miktex/bin/x64"
    "/c/Users/$USER/AppData/Local/Programs/MiKTeX/miktex/bin/x64"
    "/c/Program Files (x86)/MiKTeX/miktex/bin/x64"
)

# Find XeLaTeX
XELATEX=""
for path in "${MIKTEX_PATHS[@]}"; do
    if [ -f "$path/xelatex.exe" ]; then
        XELATEX="$path/xelatex.exe"
        echo "✅ Found XeLaTeX at: $XELATEX"
        break
    fi
done

if [ -z "$XELATEX" ]; then
    echo "❌ XeLaTeX not found in common locations."
    echo "Please add MiKTeX to your PATH or update this script."
    echo "Common paths checked:"
    for path in "${MIKTEX_PATHS[@]}"; do
        echo "  - $path"
    done
    exit 1
fi

# Run Python script
echo "📋 Running Python script..."
python combine_latex_vazir.py

if [ ! -f "complete_book.tex" ]; then
    echo "❌ Error: complete_book.tex was not created"
    exit 1
fi

echo "✅ complete_book.tex created"

# Build PDF
echo "📄 Building PDF (first pass)..."
"$XELATEX" -interaction=nonstopmode complete_book.tex

if [ $? -ne 0 ]; then
    echo "❌ Error in first XeLaTeX run"
    exit 1
fi

echo "🔄 Building PDF (second pass)..."
"$XELATEX" -interaction=nonstopmode complete_book.tex

if [ $? -ne 0 ]; then
    echo "❌ Error in second XeLaTeX run"
    exit 1
fi

# Clean up
echo "🧹 Cleaning up temporary files..."
rm -f *.aux *.log *.toc *.out *.fdb_latexmk *.fls

if [ -f "complete_book.pdf" ]; then
    echo "✅ Success! PDF created: complete_book.pdf"
    echo "📖 Opening PDF..."
    start complete_book.pdf
else
    echo "❌ Error: PDF was not created"
    exit 1
fi

echo "🎉 Build completed successfully!"