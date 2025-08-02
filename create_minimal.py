#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create minimal LaTeX document without complex Persian setup
"""

import os
import glob
import re

def create_minimal_latex():
    """Create a minimal LaTeX document that should work on Windows"""
    
    # Ultra-simple LaTeX setup
    content = r"""\documentclass[12pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{hyperref}

% Simple setup - no complex fonts
\title{System Design Interview Guide}
\author{Alex Xu}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    # Process .tex files
    tex_files = sorted(glob.glob('*.tex'), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    
    for tex_file in tex_files:
        if tex_file == 'complete_book.tex':
            continue
            
        print(f"Processing: {tex_file}")
        file_num = re.findall(r'\d+', tex_file)[0] if re.findall(r'\d+', tex_file) else '000'
        
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                tex_content = f.read()
            
            # Extract content between \begin{document} and \end{document}
            start = tex_content.find('\\begin{document}')
            end = tex_content.find('\\end{document}')
            
            if start != -1 and end != -1:
                doc_content = tex_content[start + len('\\begin{document}'):end].strip()
                
                # Remove problematic commands
                doc_content = re.sub(r'\\maketitle', '', doc_content)
                doc_content = re.sub(r'\\settextfont\{[^}]*\}', '', doc_content)
                doc_content = re.sub(r'\\setdigitfont\{[^}]*\}', '', doc_content)
                
                # Add as chapter
                content += f"\n\\chapter{{Chapter {file_num}}}\n"
                content += doc_content + "\n\n"
                
                # Add image if exists
                img_file = f"{file_num.zfill(3)}.png"
                if os.path.exists(img_file):
                    content += f"""
\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.7\\textwidth]{{{img_file}}}
\\caption{{Figure {file_num}}}
\\end{{figure}}
\\newpage

"""
                    
        except Exception as e:
            print(f"Error with {tex_file}: {e}")
            continue
    
    content += "\n\\end{document}"
    
    # Write the file
    with open('minimal_book.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created minimal_book.tex")

if __name__ == "__main__":
    create_minimal_latex()