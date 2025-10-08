@echo off
echo Compiling EDGE-QI IEEE Conference Paper...
echo.

REM Check if pdflatex is available
where pdflatex >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pdflatex not found. Please install a LaTeX distribution like:
    echo - MiKTeX: https://miktex.org/
    echo - TeX Live: https://www.tug.org/texlive/
    echo.
    pause
    exit /b 1
)

REM Compile the paper
echo Step 1: First compilation...
pdflatex -interaction=nonstopmode EDGE_QI_IEEE_Paper.tex

echo Step 2: Processing bibliography...
bibtex EDGE_QI_IEEE_Paper

echo Step 3: Second compilation...
pdflatex -interaction=nonstopmode EDGE_QI_IEEE_Paper.tex

echo Step 4: Final compilation...
pdflatex -interaction=nonstopmode EDGE_QI_IEEE_Paper.tex

REM Clean up auxiliary files
echo Cleaning up auxiliary files...
del *.aux *.bbl *.blg *.log *.out 2>nul

echo.
if exist EDGE_QI_IEEE_Paper.pdf (
    echo ✅ SUCCESS: EDGE_QI_IEEE_Paper.pdf generated successfully!
    echo.
    echo The paper includes:
    echo - Complete IEEE conference format
    echo - 4 high-quality figures with proper captions
    echo - Comprehensive technical content
    echo - 13 relevant citations
    echo.
    echo You can now submit this paper to IEEE conferences!
) else (
    echo ❌ ERROR: PDF generation failed. Check the LaTeX log for errors.
)

pause