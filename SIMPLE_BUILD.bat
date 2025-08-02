@echo off
echo === SIMPLE BUILD FOR FIRST 3 CHAPTERS ===
echo.
echo Running merge script...
python merge_first_3.py
echo.
echo Building PDF...
pdflatex first_3_chapters.tex
pdflatex first_3_chapters.tex
echo.
if exist "first_3_chapters.pdf" (
    echo SUCCESS! Opening PDF...
    start first_3_chapters.pdf
) else (
    echo FAILED! Check for errors above.
)
echo.
pause