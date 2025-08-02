#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LaTeX combiner with proper Vazir font setup
"""

import os
import re
import glob

def create_vazir_latex():
    """Create LaTeX file with Vazir font properly configured"""
    
    # Proper XeTeX setup with Vazir font
    main_content = r"""\documentclass[12pt,a4paper]{book}
\usepackage{fontspec}
\usepackage{xepersian}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{geometry}

% Page geometry
\geometry{a4paper, margin=2.5cm}

% Font setup - Vazir for Persian, Times New Roman for Latin
\settextfont[Scale=1.0]{Vazir}
\setlatintextfont[Scale=1.0]{Times New Roman}
\setdigitfont{Vazir}

% Headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\fancyhead[LO]{\rightmark}
\fancyhead[RE]{\leftmark}
\renewcommand{\headrulewidth}{0.4pt}

% Hyperref setup
\hypersetup{
    unicode=true,
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
    pdftitle={مصاحبهٔ طراحی سیستم},
    pdfauthor={الکس شو}
}

% List settings for Persian
\setlist[itemize]{rightmargin=2em}
\setlist[enumerate]{rightmargin=2em}

\title{مصاحبهٔ طراحی سیستم: راهنمای یک فرد داخل‌کاری}
\author{الکس شو}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    # Find .tex files and sort them
    tex_files = sorted(glob.glob('*.tex'), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    
    print(f"📄 پیدا شدن فایل‌های .tex: {tex_files}")
    
    for tex_file in tex_files:
        if tex_file == 'complete_book.tex':
            continue
            
        print(f"📝 در حال پردازش: {tex_file}")
        
        # Extract file number
        file_num = re.findall(r'\d+', tex_file)[0] if re.findall(r'\d+', tex_file) else '000'
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract content between \begin{document} and \end{document}
            start_pattern = r'\\begin\{document\}'
            end_pattern = r'\\end\{document\}'
            
            start_match = re.search(start_pattern, content)
            end_match = re.search(end_pattern, content)
            
            if start_match and end_match:
                # Extract document content
                doc_content = content[start_match.end():end_match.start()].strip()
                
                # Clean up problematic commands
                doc_content = re.sub(r'\\maketitle\s*', '', doc_content)
                doc_content = re.sub(r'\\settextfont\{[^}]*\}', '', doc_content)
                doc_content = re.sub(r'\\setdigitfont\{[^}]*\}', '', doc_content)
                
                # Extract title for chapter
                chapter_title = extract_title_from_content(doc_content, file_num)
                
                # Skip table of contents files (they'll be auto-generated)
                if '003' in tex_file or 'toc' in tex_file.lower():
                    print(f"⏭️  پرش از فایل فهرست: {tex_file}")
                    continue
                
                # Add chapter
                main_content += f"\n% === فایل {tex_file} ===\n"
                main_content += f"\\chapter{{{chapter_title}}}\n"
                main_content += doc_content + "\n\n"
                
                # Add corresponding image if exists
                image_file = f"{file_num.zfill(3)}.png"
                if os.path.exists(image_file):
                    main_content += f"""
\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth,keepaspectratio]{{{image_file}}}
\\caption{{شکل {file_num}}}
\\label{{fig:{file_num}}}
\\end{{figure}}

"""
                    print(f"🖼️  اضافه شد تصویر: {image_file}")
                
        except Exception as e:
            print(f"❌ خطا در پردازش {tex_file}: {e}")
            continue
    
    # End document
    main_content += "\n\\end{document}"
    
    # Write output file
    with open('complete_book.tex', 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    print("✅ فایل complete_book.tex با فونت Vazir ایجاد شد!")
    return "complete_book.tex"

def extract_title_from_content(content, file_num):
    """استخراج عنوان از محتوای LaTeX"""
    
    # Look for existing titles
    title_patterns = [
        r'\\title\{([^}]+)\}',
        r'\\section\*?\{([^}]+)\}',
        r'\\textbf\{([^}]+)\}',
        r'\\subsection\*?\{([^}]+)\}'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, content)
        if match:
            title = match.group(1).strip()
            # Clean up title
            title = re.sub(r'\\[a-zA-Z]+\{?', '', title)
            title = re.sub(r'[{}]', '', title).strip()
            if len(title) > 3:
                return title[:60]  # Limit length
    
    # Extract first meaningful line
    lines = content.strip().split('\n')
    for line in lines:
        clean_line = re.sub(r'\\[a-zA-Z]+\*?\{?', '', line).strip()
        clean_line = re.sub(r'[{}*\\]', '', clean_line).strip()
        if clean_line and len(clean_line) > 3 and not clean_line.startswith('%'):
            return clean_line[:60]
    
    # Fallback title
    return f"فصل {file_num}"

def create_font_test():
    """ایجاد فایل تست فونت"""
    
    test_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xepersian}

% Test Vazir font
\settextfont{Vazir}
\setlatintextfont{Times New Roman}
\setdigitfont{Vazir}

\title{تست فونت Vazir}
\author{تست}

\begin{document}

\maketitle

\section{تست متن فارسی}
این یک متن فارسی برای تست فونت Vazir است.

\textbf{متن پررنگ:} این متن با فونت Vazir نوشته شده است.

\section{English Text Test}
This is English text with Times New Roman font.

\section{تست اعداد و ارقام}
اعداد فارسی: ۱۲۳۴۵۶۷۸۹۰
اعداد انگلیسی: 1234567890

\end{document}
"""
    
    with open('vazir_test.tex', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ فایل تست vazir_test.tex ایجاد شد")

if __name__ == "__main__":
    print("🚀 شروع ترکیب فایل‌ها با فونت Vazir...")
    
    # Create font test file
    create_font_test()
    
    # Create main document
    create_vazir_latex()
    
    print("\n" + "="*50)
    print("✅ کار تمام شد!")
    print("\n📋 فایل‌های ایجاد شده:")
    print("   🧪 vazir_test.tex - فایل تست فونت")
    print("   📄 complete_book.tex - کتاب کامل با فونت Vazir")
    print("\n🚀 برای ساخت PDF:")
    print("   1. ابتدا تست فونت: xelatex vazir_test.tex")
    print("   2. سپس کتاب اصلی: xelatex complete_book.tex")
    print("                     xelatex complete_book.tex")