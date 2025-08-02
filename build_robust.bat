@echo off
echo 🔧 Robust LaTeX Build Script

echo 🧹 Step 1: Creating clean LaTeX files...
python combine_clean_robust.py

if not exist "clean_test.tex" (
    echo ❌ Clean script failed
    pause
    exit /b 1
)

echo 🧪 Step 2: Testing clean setup...
xelatex -interaction=nonstopmode clean_test.tex

if %errorlevel% neq 0 (
    echo ❌ Clean test failed, trying PDFLaTeX fallback...
    python create_pdflatex.py
    echo 📄 Building with PDFLaTeX...
    pdflatex -interaction=nonstopmode pdflatex_book.tex
    pdflatex -interaction=nonstopmode pdflatex_book.tex
    if exist "pdflatex_book.pdf" (
        echo ✅ PDFLaTeX version created!
        start pdflatex_book.pdf
    ) else (
        echo ❌ All methods failed
        pause
        exit /b 1
    )
) else (
    echo ✅ Clean test passed! Building main document...
    xelatex -interaction=nonstopmode complete_book_clean.tex
    xelatex -interaction=nonstopmode complete_book_clean.tex
    
    if exist "complete_book_clean.pdf" (
        echo ✅ Clean XeLaTeX version created!
        start complete_book_clean.pdf
    ) else (
        echo ❌ Main document failed, trying PDFLaTeX...
        python create_pdflatex.py
        pdflatex -interaction=nonstopmode pdflatex_book.tex
        pdflatex -interaction=nonstopmode pdflatex_book.tex
        if exist "pdflatex_book.pdf" (
            echo ✅ PDFLaTeX fallback successful!
            start pdflatex_book.pdf
        ) else (
            echo ❌ All build methods failed
            pause
            exit /b 1
        )
    )
)

echo 🧹 Cleaning up temporary files...
del /q *.aux *.log *.toc *.out *.fdb_latexmk *.fls 2>nul

echo 🎉 Build process completed!
pause