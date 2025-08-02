@echo off
echo 🔧 Building with Fixed LaTeX Scripts...

echo 📋 Step 1: Creating fixed LaTeX files...
python combine_latex_fixed_vazir.py

echo 🧪 Step 2: Testing font setup...
xelatex -interaction=nonstopmode simple_test.tex

if %errorlevel% neq 0 (
    echo ❌ Font test failed, trying PDFLaTeX version...
    python create_pdflatex.py
    echo 📄 Building with PDFLaTeX...
    pdflatex -interaction=nonstopmode pdflatex_book.tex
    pdflatex -interaction=nonstopmode pdflatex_book.tex
    if exist "pdflatex_book.pdf" (
        echo ✅ PDFLaTeX version created successfully!
        start pdflatex_book.pdf
    ) else (
        echo ❌ Both XeLaTeX and PDFLaTeX failed
        pause
        exit /b 1
    )
) else (
    echo ✅ Font test passed, building main document...
    xelatex -interaction=nonstopmode complete_book_fixed.tex
    xelatex -interaction=nonstopmode complete_book_fixed.tex
    if exist "complete_book_fixed.pdf" (
        echo ✅ XeLaTeX version created successfully!
        start complete_book_fixed.pdf
    ) else (
        echo ❌ XeLaTeX main document failed
        pause
        exit /b 1
    )
)

echo 🧹 Cleaning up temporary files...
del /q *.aux *.log *.toc *.out *.fdb_latexmk *.fls 2>nul

echo ✅ Build completed!
pause