#!/usr/bin/env python3
"""
اسکریپت تجمیع ترجمه‌ها
این اسکریپت فایل‌های ترجمه شده را در یک سند LaTeX واحد ترکیب می‌کند
"""

import os
import re
from pathlib import Path

def get_txt_files(directory):
    """دریافت تمام فایل‌های txt به ترتیب شماره"""
    txt_files = []
    if Path(directory).exists():
        for file in Path(directory).glob("*.txt"):
            match = re.match(r'(\d+)\.txt', file.name)
            if match:
                num = int(match.group(1))
                txt_files.append((num, str(file)))
    return sorted(txt_files, key=lambda x: x[0])

def read_file(filepath):
    """خواندن فایل با رمزگذاری مناسب"""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    # اگر همه رمزگذاری‌ها شکست خوردند
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def clean_content(content):
    """پاکسازی و استانداردسازی محتوای LaTeX"""
    # حذف کاراکترهای نامرئی
    content = content.encode('utf-8', 'ignore').decode('utf-8')
    
    # اطمینان از فاصله‌گذاری صحیح
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'  +', ' ', content)
    
    return content.strip()

def consolidate_translations(source_dir='translated_revised', output_file='consolidated_translation.tex'):
    """تجمیع تمام فایل‌های ترجمه شده در یک سند LaTeX"""
    
    # ایجاد سربرگ LaTeX
    latex_header = r"""\documentclass[12pt,a4paper]{article}
\usepackage{xepersian}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{listings}
\usepackage{verbatim}

\settextfont{XB Niloofar}
\setdigitfont{XB Niloofar}

\title{مصاحبه طراحی سیستم: راهنمای جامع}
\author{الکس شو \\ ترجمه: احسان سمیعی}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\newpage

"""

    latex_footer = r"""
\end{document}"""

    # دریافت فایل‌های txt
    txt_files = get_txt_files(source_dir)
    
    if not txt_files:
        print(f"هیچ فایل txt در {source_dir} یافت نشد")
        return
    
    # ترکیب محتوا
    full_content = latex_header
    
    for num, filepath in txt_files:
        print(f"پردازش فایل {num:03d}.txt...")
        content = read_file(filepath)
        content = clean_content(content)
        
        if content:
            # اضافه کردن شماره فایل به عنوان کامنت
            full_content += f"\n% --- فایل {num:03d}.txt ---\n"
            full_content += content
            full_content += "\n\n"
    
    full_content += latex_footer
    
    # ذخیره فایل خروجی
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"فایل تجمیع شده در {output_file} ذخیره شد")
    print(f"تعداد فایل‌های پردازش شده: {len(txt_files)}")

if __name__ == "__main__":
    consolidate_translations()
