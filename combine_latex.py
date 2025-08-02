#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اسکریپت ترکیب فایل‌های LaTeX و تصاویر
"""

import os
import re
import glob

def create_combined_latex():
    """ایجاد فایل LaTeX ترکیبی از تمام فایل‌های .tex موجود"""
    
    # شروع فایل اصلی
    main_content = r"""\documentclass[12pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage{xepersian}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{fancyhdr}
\usepackage{geometry}

% تنظیمات صفحه
\geometry{a4paper, margin=2.5cm}

% تنظیمات فونت
\settextfont{XB Niloofar}
\setdigitfont{XB Niloofar}

% تنظیمات سربرگ
\pagestyle{fancy}
\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\fancyhead[LO]{\rightmark}
\fancyhead[RE]{\leftmark}

% تنظیمات کد
\lstset{
    basicstyle=\footnotesize\ttfamily,
    breaklines=true,
    frame=single,
    numbers=left,
    numberstyle=\tiny
}

\title{مصاحبهٔ طراحی سیستم: راهنمای یک فرد داخل‌کاری}
\author{الکس شو}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    # پیدا کردن تمام فایل‌های .tex به ترتیب شماره
    tex_files = sorted(glob.glob('*.tex'), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    
    print(f"فایل‌های پیدا شده: {tex_files}")
    
    for tex_file in tex_files:
        print(f"در حال پردازش: {tex_file}")
        
        # استخراج شماره فایل
        file_num = re.findall(r'\d+', tex_file)[0] if re.findall(r'\d+', tex_file) else '000'
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # استخراج محتوای بین \begin{document} و \end{document}
            start_pattern = r'\\begin\{document\}'
            end_pattern = r'\\end\{document\}'
            
            start_match = re.search(start_pattern, content)
            end_match = re.search(end_pattern, content)
            
            if start_match and end_match:
                # استخراج محتوای داخل document
                doc_content = content[start_match.end():end_match.start()].strip()
                
                # حذف \maketitle اگر وجود دارد
                doc_content = re.sub(r'\\maketitle\s*', '', doc_content)
                
                # اضافه کردن chapter یا section بر اساس محتوا
                if any(keyword in tex_file for keyword in ['002', '004']):  # صفحات اصلی
                    main_content += f"\n% === فایل {tex_file} ===\n"
                    main_content += doc_content + "\n\n"
                elif '003' in tex_file:  # فهرست مطالب - خودکار ایجاد می‌شود
                    continue
                else:  # فصل‌ها
                    main_content += f"\n\\chapter{{{extract_title_from_content(doc_content)}}}\n"
                    main_content += doc_content + "\n\n"
                
                # اضافه کردن تصویر مربوطه اگر وجود دارد
                image_file = f"{file_num.zfill(3)}.png"
                if os.path.exists(image_file):
                    main_content += f"""
\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{image_file}}}
\\caption{{تصویر {file_num}}}
\\label{{fig:{file_num}}}
\\end{{figure}}

"""
        except Exception as e:
            print(f"خطا در پردازش {tex_file}: {e}")
            continue
    
    # پایان فایل
    main_content += "\n\\end{document}"
    
    # نوشتن فایل نهایی
    with open('complete_book.tex', 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    print("✅ فایل complete_book.tex ایجاد شد!")
    return "complete_book.tex"

def extract_title_from_content(content):
    """استخراج عنوان از محتوای LaTeX"""
    
    # جستجو برای title در محتوا
    title_match = re.search(r'\\title\{([^}]+)\}', content)
    if title_match:
        return title_match.group(1)
    
    # جستجو برای section
    section_match = re.search(r'\\section\*?\{([^}]+)\}', content)
    if section_match:
        return section_match.group(1)
    
    # جستجو برای textbf در ابتدا
    textbf_match = re.search(r'\\textbf\{([^}]+)\}', content)
    if textbf_match:
        return textbf_match.group(1)
    
    # استخراج اولین خط غیر خالی
    lines = content.strip().split('\n')
    for line in lines:
        clean_line = re.sub(r'\\[a-zA-Z]+\{?', '', line).strip()
        clean_line = re.sub(r'[{}*]', '', clean_line).strip()
        if clean_line and len(clean_line) > 3:
            return clean_line[:50]  # محدود کردن طول
    
    return "فصل بدون عنوان"

def create_build_script():
    """ایجاد اسکریپت ساخت PDF"""
    
    build_script = """#!/bin/bash

# اسکریپت ساخت PDF از فایل LaTeX فارسی

echo "🔨 شروع ساخت PDF..."

# بررسی وجود xelatex
if ! command -v xelatex &> /dev/null; then
    echo "❌ خطا: xelatex پیدا نشد. لطفاً TeXLive یا MiKTeX نصب کنید."
    echo "برای Ubuntu/Debian: sudo apt-get install texlive-xetex texlive-lang-other"
    echo "برای macOS: brew install --cask mactex"
    exit 1
fi

# ساخت PDF
echo "📄 در حال تولید PDF..."
xelatex -interaction=nonstopmode complete_book.tex

# اجرای دوباره برای فهرست مطالب و مراجع
echo "🔄 اجرای دوباره برای بهینه‌سازی..."
xelatex -interaction=nonstopmode complete_book.tex

# پاک‌سازی فایل‌های موقت
echo "🧹 پاک‌سازی فایل‌های موقت..."
rm -f *.aux *.log *.toc *.out *.fdb_latexmk *.fls

if [ -f "complete_book.pdf" ]; then
    echo "✅ PDF با موفقیت ایجاد شد: complete_book.pdf"
    echo "📖 برای مشاهده: open complete_book.pdf (macOS) یا xdg-open complete_book.pdf (Linux)"
else
    echo "❌ خطا در ایجاد PDF. لطفاً لاگ‌ها را بررسی کنید."
fi
"""
    
    with open('build.sh', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    # قابل اجرا کردن
    os.chmod('build.sh', 0o755)
    print("✅ اسکریپت build.sh ایجاد شد!")

def create_readme():
    """ایجاد فایل راهنما"""
    
    readme_content = """# راهنمای ساخت کتاب

## نیازمندی‌ها

### روی Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-lang-other texlive-fonts-extra
```

### روی macOS:
```bash
brew install --cask mactex
```

### روی Windows:
- MiKTeX را از [miktex.org](https://miktex.org) دانلود و نصب کنید

## نحوه استفاده

### 1. ترکیب فایل‌ها:
```bash
python3 combine_latex.py
```

### 2. ساخت PDF:
```bash
./build.sh
```

یا به صورت دستی:
```bash
xelatex complete_book.tex
xelatex complete_book.tex  # دوباره برای فهرست مطالب
```

## فایل‌های خروجی

- `complete_book.tex`: فایل LaTeX ترکیبی
- `complete_book.pdf`: فایل PDF نهایی
- `build.sh`: اسکریپت ساخت خودکار

## نکات مهم

- فونت XB Niloofar باید روی سیستم نصب باشد
- برای تغییر فونت، فایل complete_book.tex را ویرایش کنید
- اگر تصاویر نمایش داده نمی‌شوند، مسیر آنها را بررسی کنید

## عیب‌یابی

### اگر PDF ایجاد نشد:
1. لاگ خطاها را بررسی کنید
2. فونت‌های فارسی نصب باشند
3. تمام بسته‌های LaTeX موجود باشند

### اگر فونت مشکل دارد:
```latex
% در فایل complete_book.tex تغییر دهید:
\\settextfont{Vazir}  % یا هر فونت دیگری
```
"""
    
    with open('README_BUILD.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ فایل README_BUILD.md ایجاد شد!")

if __name__ == "__main__":
    print("🚀 شروع ترکیب فایل‌های LaTeX...")
    
    # ایجاد فایل ترکیبی
    output_file = create_combined_latex()
    
    # ایجاد اسکریپت ساخت
    create_build_script()
    
    # ایجاد راهنما
    create_readme()
    
    print("\n" + "="*50)
    print("✅ کار تمام شد!")
    print("\n📋 فایل‌های ایجاد شده:")
    print("   📄 complete_book.tex - فایل LaTeX ترکیبی")
    print("   🔨 build.sh - اسکریپت ساخت PDF")
    print("   📖 README_BUILD.md - راهنمای استفاده")
    print("\n🚀 برای ساخت PDF:")
    print("   python3 combine_latex.py && ./build.sh")
    print("\n📱 برای مشاهده PDF:")
    print("   - Linux: xdg-open complete_book.pdf")
    print("   - macOS: open complete_book.pdf") 
    print("   - Windows: start complete_book.pdf")
