#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create PDFLaTeX-compatible version (fallback option)
"""

import os
import re
import glob

def create_pdflatex_version():
    """Create a version that works with PDFLaTeX"""
    
    content = r"""\documentclass[12pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{geometry}
\usepackage{fancyhdr}

% Page setup
\geometry{a4paper, margin=2.5cm}

% Headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
    pdftitle={System Design Interview Guide},
    pdfauthor={Alex Xu}
}

\title{System Design Interview: An Insider's Guide}
\author{Alex Xu}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    # Process .tex files
    tex_files = sorted(glob.glob('*.tex'), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    
    print(f"📄 Processing {len(tex_files)} files for PDFLaTeX...")
    
    for tex_file in tex_files:
        if any(skip in tex_file for skip in ['complete_book', 'test', 'pdflatex', 'font']):
            continue
            
        file_num = re.findall(r'\d+', tex_file)[0] if re.findall(r'\d+', tex_file) else '000'
        
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='replace') as f:
                tex_content = f.read()
            
            # Extract content
            start = tex_content.find('\\begin{document}')
            end = tex_content.find('\\end{document}')
            
            if start != -1 and end != -1:
                doc_content = tex_content[start + len('\\begin{document}'):end].strip()
                
                # Remove all font-related commands
                doc_content = re.sub(r'\\[a-zA-Z]*font\{[^}]*\}', '', doc_content)
                doc_content = re.sub(r'\\maketitle', '', doc_content)
                
                # Skip TOC files
                if '003' in tex_file:
                    continue
                
                # Extract title
                title = extract_pdflatex_title(doc_content, file_num)
                
                content += f"\n\\chapter{{{title}}}\n"
                content += doc_content + "\n\n"
                
                # Add image
                img_file = f"{file_num.zfill(3)}.png"
                if os.path.exists(img_file):
                    content += f"""
\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{img_file}}}
\\caption{{Figure {file_num}}}
\\label{{fig:{file_num}}}
\\end{{figure}}

"""
                    print(f"🖼️ Added image: {img_file}")
                    
        except Exception as e:
            print(f"❌ Error with {tex_file}: {e}")
            continue
    
    content += "\n\\end{document}"
    
    # Write PDFLaTeX version
    with open('pdflatex_book.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created pdflatex_book.tex")
    print("🚀 Build with:")
    print("   pdflatex pdflatex_book.tex")
    print("   pdflatex pdflatex_book.tex")

def extract_pdflatex_title(content, file_num):
    """Extract title for PDFLaTeX version"""
    
    # Look for titles in various formats
    title_patterns = [
        r'\\title\{([^}]+)\}',
        r'\\section\*?\{([^}]+)\}',
        r'\\textbf\{([^}]+)\}'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, content)
        if match:
            title = match.group(1).strip()
            # Clean up title
            title = re.sub(r'\\[a-zA-Z]+\{?', '', title)
            title = re.sub(r'[{}]', '', title).strip()
            if len(title) > 3:
                # Convert Persian/Arabic to transliteration for PDFLaTeX
                return f"Chapter {file_num}: {title[:40]}"
    
    return f"Chapter {file_num}"

if __name__ == "__main__":
    print("🔧 Creating PDFLaTeX version...")
    create_pdflatex_version()