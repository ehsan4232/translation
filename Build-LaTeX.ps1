# PowerShell script to build LaTeX book
# Usage: .\Build-LaTeX.ps1

Write-Host "🚀 Building LaTeX book..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python." -ForegroundColor Red
    exit 1
}

# Run Python script
Write-Host "📋 Running combine script..." -ForegroundColor Yellow
try {
    python combine_latex_vazir.py
    if ($LASTEXITCODE -ne 0) {
        throw "Python script failed"
    }
} catch {
    Write-Host "❌ Python script failed: $_" -ForegroundColor Red
    exit 1
}

# Check if output file was created
if (-not (Test-Path "complete_book.tex")) {
    Write-Host "❌ complete_book.tex was not created" -ForegroundColor Red
    exit 1
}

Write-Host "✅ complete_book.tex created successfully" -ForegroundColor Green

# Check if XeLaTeX is available
try {
    $xelatexVersion = xelatex --version 2>&1
    Write-Host "✅ XeLaTeX found" -ForegroundColor Green
} catch {
    Write-Host "❌ XeLaTeX not found. Please install MiKTeX or TeX Live." -ForegroundColor Red
    Write-Host "Download from: https://miktex.org/download" -ForegroundColor Yellow
    exit 1
}

# Build PDF
Write-Host "📄 Building PDF (first pass)..." -ForegroundColor Yellow
try {
    xelatex -interaction=nonstopmode complete_book.tex
    if ($LASTEXITCODE -ne 0) {
        throw "XeLaTeX first pass failed"
    }
} catch {
    Write-Host "❌ XeLaTeX first pass failed" -ForegroundColor Red
    Write-Host "Check the .log file for errors" -ForegroundColor Yellow
    exit 1
}

Write-Host "📄 Building PDF (second pass)..." -ForegroundColor Yellow
try {
    xelatex -interaction=nonstopmode complete_book.tex
    if ($LASTEXITCODE -ne 0) {
        throw "XeLaTeX second pass failed"
    }
} catch {
    Write-Host "❌ XeLaTeX second pass failed" -ForegroundColor Red
    exit 1
}

# Clean up
Write-Host "🧹 Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item -Path "*.aux", "*.log", "*.toc", "*.out", "*.fdb_latexmk", "*.fls" -ErrorAction SilentlyContinue

# Check result
if (Test-Path "complete_book.pdf") {
    $pdfSize = (Get-Item "complete_book.pdf").Length
    Write-Host "✅ PDF created successfully!" -ForegroundColor Green
    Write-Host "📊 File size: $([math]::Round($pdfSize/1MB, 2)) MB" -ForegroundColor Cyan
    Write-Host "📖 Opening PDF..." -ForegroundColor Yellow
    Start-Process "complete_book.pdf"
} else {
    Write-Host "❌ PDF was not created" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 Build completed successfully!" -ForegroundColor Green