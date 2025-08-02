#!/bin/bash

# اسکریپت ساخت سریع PDF

echo "🚀 ساخت سریع کتاب..."

# اجرای اسکریپت ترکیب
echo "📋 ترکیب فایل‌های LaTeX..."
python3 combine_latex.py

# بررسی وجود فایل ترکیبی
if [ ! -f "complete_book.tex" ]; then
    echo "❌ خطا: فایل complete_book.tex ایجاد نشد"
    exit 1
fi

# ساخت PDF
echo "📄 تولید PDF..."
xelatex -interaction=nonstopmode complete_book.tex

# اجرای دوباره برای فهرست مطالب
echo "🔄 بهینه‌سازی فهرست مطالب..."
xelatex -interaction=nonstopmode complete_book.tex

# پاک‌سازی
echo "🧹 پاک‌سازی فایل‌های موقت..."
rm -f *.aux *.log *.toc *.out *.fdb_latexmk *.fls

# نتیجه
if [ -f "complete_book.pdf" ]; then
    echo "✅ کتاب آماده است: complete_book.pdf"
    echo "📖 برای مشاهده:"
    echo "   - Linux: xdg-open complete_book.pdf"
    echo "   - macOS: open complete_book.pdf"
    echo "   - Windows: start complete_book.pdf"
else
    echo "❌ خطا در ایجاد PDF"
    exit 1
fi
