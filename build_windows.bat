@echo off
echo 🚀 Building LaTeX book on Windows...

echo 📋 Running Python script to combine files...
python combine_latex_vazir.py

if not exist "complete_book.tex" (
    echo ❌ Error: complete_book.tex was not created
    pause
    exit /b 1
)

echo 📄 Building PDF with XeLaTeX...
xelatex -interaction=nonstopmode complete_book.tex

if %errorlevel% neq 0 (
    echo ❌ Error in first XeLaTeX run
    pause
    exit /b 1
)

echo 🔄 Second XeLaTeX run for references...
xelatex -interaction=nonstopmode complete_book.tex

echo 🧹 Cleaning up temporary files...
del /q *.aux *.log *.toc *.out *.fdb_latexmk *.fls 2>nul

if exist "complete_book.pdf" (
    echo ✅ Success! PDF created: complete_book.pdf
    echo 📖 Opening PDF...
    start complete_book.pdf
) else (
    echo ❌ Error: PDF was not created
    pause
    exit /b 1
)

echo Press any key to exit...
pause >nul