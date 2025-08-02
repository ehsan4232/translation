#!/usr/bin/env python3
"""
Simple script to merge first 3 .tex files and make PDF
"""

import os
import glob

def merge_first_3():
    """Merge only the first 3 .tex files"""
    
    # Simple LaTeX document
    content = r"""\documentclass[12pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}

\title{System Design Interview - First 3 Chapters}
\author{Alex Xu}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    # Get first 3 .tex files
    tex_files = ['002.tex', '003.tex', '004.tex']
    
    for i, tex_file in enumerate(tex_files, 1):
        if os.path.exists(tex_file):
            print(f"Adding {tex_file}")
            
            try:
                with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read()
                
                # Extract content between \begin{document} and \end{document}
                start = file_content.find('\\begin{document}')
                end = file_content.find('\\end{document}')
                
                if start != -1 and end != -1:
                    doc_content = file_content[start + len('\\begin{document}'):end]
                else:
                    doc_content = file_content
                
                # Remove problematic commands
                doc_content = doc_content.replace('\\maketitle', '')
                doc_content = doc_content.replace('\\settextfont{XB Niloofar}', '')
                doc_content = doc_content.replace('\\setdigitfont{XB Niloofar}', '')
                
                # Add to main document
                content += f"\n\\chapter{{Chapter {i}}}\n"
                content += doc_content + "\n\n"
                
                # Add image if exists
                img_num = str(i + 1).zfill(3)  # 003, 004, 005
                img_file = f"{img_num}.png"
                if os.path.exists(img_file):
                    content += f"""
\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{img_file}}}
\\caption{{Figure {img_num}}}
\\end{{figure}}

"""
                    print(f"Added image {img_file}")
                    
            except Exception as e:
                print(f"Error with {tex_file}: {e}")
                continue
        else:
            print(f"File {tex_file} not found")
    
    content += "\n\\end{document}"
    
    # Write output
    with open('first_3_chapters.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created first_3_chapters.tex")
    return "first_3_chapters.tex"

if __name__ == "__main__":
    print("📄 Merging first 3 .tex files...")
    merge_first_3()
    print("🚀 Now run: pdflatex first_3_chapters.tex")