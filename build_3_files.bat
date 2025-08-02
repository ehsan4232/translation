@echo off
echo 📄 Building first 3 chapters...

python merge_first_3.py

if not exist "first_3_chapters.tex" (
    echo ❌ Merge failed
    pause
    exit /b 1
)

echo 🔨 Building PDF...
pdflatex -interaction=nonstopmode first_3_chapters.tex
pdflatex -interaction=nonstopmode first_3_chapters.tex

if exist "first_3_chapters.pdf" (
    echo ✅ SUCCESS! PDF created
    start first_3_chapters.pdf
) else (
    echo ❌ PDF build failed
)

echo 🧹 Cleaning up...
del /q *.aux *.log *.toc *.out 2>nul

pause