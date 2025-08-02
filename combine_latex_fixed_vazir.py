#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fixed LaTeX combiner that avoids package conflicts
"""

import os
import re
import glob

def create_fixed_vazir_latex():
    """Create LaTeX file with Vazir font that avoids package conflicts"""
    
    # Use fontspec + polyglossia instead of xepersian to avoid conflicts
    main_content = r"""\documentclass[12pt,a4paper]{book}
\usepackage{fontspec}
\usepackage{polyglossia}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{enumitem}

% Set up languages - polyglossia instead of xepersian
\setdefaultlanguage[numerals=mashriq]{arabic}
\setotherlanguage{english}

% Page geometry
\geometry{a4paper, margin=2.5cm}

% Font setup - using fontspec directly
\newfontfamily\arabicfont[Script=Arabic,Scale=1.1]{Vazir}
\newfontfamily\englishfont{Times New Roman}
\setmainfont{Times New Roman}

% Headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% Hyperref - load AFTER other packages to avoid conflicts
\usepackage{hyperref}
\hypersetup{
    unicode=true,
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
    pdftitle={System Design Interview Guide},
    pdfauthor={Alex Xu}
}

\title{مصاحبهٔ طراحی سیستم: راهنمای یک فرد داخل‌کاری}
\author{الکس شو}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    # Process .tex files
    tex_files = sorted(glob.glob('*.tex'), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    
    print(f"📄 Found {len(tex_files)} .tex files")
    
    for tex_file in tex_files:
        if tex_file in ['complete_book.tex', 'complete_book_fixed.tex', 'vazir_test.tex', 'font_test.tex', 'test_output.tex', 'font_check.tex']:
            continue
            
        print(f"📝 Processing: {tex_file}")
        file_num = re.findall(r'\d+', tex_file)[0] if re.findall(r'\d+', tex_file) else '000'
        
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract document content
            start_pos = content.find('\\begin{document}')
            end_pos = content.find('\\end{document}')
            
            if start_pos != -1 and end_pos != -1:
                doc_content = content[start_pos + len('\\begin{document}'):end_pos].strip()
                
                # Clean up problematic commands
                doc_content = re.sub(r'\\maketitle\s*', '', doc_content)
                doc_content = re.sub(r'\\settextfont\{[^}]*\}', '', doc_content)
                doc_content = re.sub(r'\\setdigitfont\{[^}]*\}', '', doc_content)
                doc_content = re.sub(r'\\setlatintextfont\{[^}]*\}', '', doc_content)
                
                # Skip table of contents files
                if '003' in tex_file:
                    continue
                
                # Extract title
                title = extract_title(doc_content, file_num)
                
                # Add content with proper Arabic text environment
                main_content += f"\n\\chapter{{{title}}}\n"
                main_content += "\\begin{Arabic}\n"
                main_content += doc_content + "\n"
                main_content += "\\end{Arabic}\n\n"
                
                # Add image
                img_file = f"{file_num.zfill(3)}.png"
                if os.path.exists(img_file):
                    main_content += f"""
\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.8\\textwidth,keepaspectratio]{{{img_file}}}
\\caption{{شکل {file_num}}}
\\label{{fig:{file_num}}}
\\end{{figure}}

"""
                    print(f"🖼️ Added image: {img_file}")
                
        except Exception as e:
            print(f"❌ Error processing {tex_file}: {e}")
            continue
    
    # End document
    main_content += "\n\\end{document}"
    
    # Write output file
    with open('complete_book_fixed.tex', 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    print("✅ Created complete_book_fixed.tex")
    return "complete_book_fixed.tex"

def extract_title(content, file_num):
    """Extract title from LaTeX content"""
    
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
                return title[:60]
    
    # Extract first meaningful line
    lines = content.strip().split('\n')
    for line in lines:
        clean_line = re.sub(r'\\[a-zA-Z]+\*?\{?', '', line).strip()
        clean_line = re.sub(r'[{}*\\]', '', clean_line).strip()
        if clean_line and len(clean_line) > 3 and not clean_line.startswith('%'):
            return clean_line[:60]
    
    return f"فصل {file_num}"

def create_simple_test():
    """Create a simple test file"""
    
    test_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{polyglossia}

% Set up languages
\setdefaultlanguage[numerals=mashriq]{arabic}
\setotherlanguage{english}

% Font setup
\newfontfamily\arabicfont[Script=Arabic]{Vazir}
\newfontfamily\englishfont{Times New Roman}
\setmainfont{Times New Roman}

\title{Font Test}
\author{Test}

\begin{document}

\maketitle

\section{English Test}
This is English text with Times New Roman.

\begin{Arabic}
\section{تست فارسی}
این یک متن فارسی برای تست فونت Vazir است.

\textbf{متن پررنگ:} این متن با فونت Vazir نوشته شده است.
\end{Arabic}

\end{document}
"""
    
    with open('simple_test.tex', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Created simple_test.tex")

if __name__ == "__main__":
    print("🔧 Creating fixed LaTeX files...")
    
    # Create test file and main document
    create_simple_test()
    create_fixed_vazir_latex()
    
    print("\n📋 Files created:")
    print("   🧪 simple_test.tex - Simple font test")
    print("   📄 complete_book_fixed.tex - Fixed main document") 
    print("\n🚀 Try in this order:")
    print("   1. xelatex simple_test.tex")
    print("   2. xelatex complete_book_fixed.tex")
    print("   3. xelatex complete_book_fixed.tex")