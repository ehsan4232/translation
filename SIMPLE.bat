@echo off
echo === ULTIMATE SIMPLE BUILD ===

python ultimate_simple.py

if not exist "simple.tex" (
    echo FAILED to create simple.tex
    pause
    exit /b 1
)

echo Building with PDFLaTeX...
pdflatex simple.tex
pdflatex simple.tex

if exist "simple.pdf" (
    echo SUCCESS!
    start simple.pdf
) else (
    echo PDF build failed
    echo Trying with different engine...
    latex simple.tex
    dvipdf simple.dvi
    if exist "simple.pdf" (
        echo SUCCESS with latex+dvipdf!
        start simple.pdf
    ) else (
        echo All methods failed
    )
)

pause