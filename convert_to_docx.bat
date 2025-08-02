@echo off
chcp 65001 >nul
echo 🚀 شروع تبدیل فایل‌های Markdown به Word...
echo.

REM بررسی وجود pandoc
pandoc --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pandoc پیدا نشد!
    echo.
    echo نصب Pandoc:
    echo 1. با winget: winget install --id JohnMacFarlane.Pandoc
    echo 2. یا از https://pandoc.org/installing.html دانلود کنید
    echo.
    pause
    exit /b 1
)

echo ✅ Pandoc یافت شد
echo.

REM ایجاد پوشه خروجی
if not exist "docx_output" mkdir docx_output

echo 📚 در حال تبدیل فایل‌های MD...
echo.

set count=0
set success=0
set failed=0

REM تبدیل هر فایل MD
for %%f in (*.md) do (
    set /a count+=1
    echo 🔄 در حال تبدیل: %%f
    
    pandoc "%%f" -o "docx_output\%%~nf.docx" --metadata dir=rtl --metadata lang=fa
    
    if errorlevel 1 (
        echo ❌ خطا در تبدیل %%f
        set /a failed+=1
    ) else (
        echo ✅ تکمیل شد: docx_output\%%~nf.docx
        set /a success+=1
    )
    echo.
)

echo ================================
echo 🎉 تبدیل کامل!
echo ✅ موفق: %success% فایل
echo ❌ ناموفق: %failed% فایل
echo 📁 فایل‌ها در پوشه docx_output ذخیره شدند
echo ================================
echo.
pause
