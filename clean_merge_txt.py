#!/usr/bin/env python3
"""
Merge .txt files and CLEAN the corrupted LaTeX commands
"""

import os
import glob
import re

def clean_latex_content(content):
    """Remove corrupted LaTeX commands"""
    
    # Remove the problematic commands
    content = re.sub(r'\\setmainlanguage\{latex\}', '', content)
    content = re.sub(r'\\setmainlanguage\{[^}]*\}', '', content)
    content = re.sub(r'\\setdefaultlanguage\{latex\}', '', content)
    content = re.sub(r'\\usepackage\{xepersian\}', '', content)
    content = re.sub(r'\\settextfont\{[^}]*\}', '', content)
    content = re.sub(r'\\setdigitfont\{[^}]*\}', '', content)
    
    return content

def merge_and_clean_txt():
    """Merge .txt files and clean corrupted LaTeX"""
    
    folder_path = "translated_files_deepseek_latex"
    
    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} not found!")
        return
    
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    def extract_number(filename):
        basename = os.path.basename(filename)
        try:
            return int(basename.split('.')[0])
        except:
            return 0
    
    txt_files.sort(key=extract_number)
    print(f"📄 Found {len(txt_files)} .txt files")
    
    # Simple, working LaTeX header
    latex_content = r"""\documentclass[12pt,a4paper]{book}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}

\title{System Design Interview Guide}
\author{Alex Xu}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""
    
    for txt_file in txt_files:
        file_number = extract_number(txt_file)
        print(f"📝 Processing: {os.path.basename(txt_file)}")
        
        try:
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
            
            # CLEAN the corrupted content
            cleaned_content = clean_latex_content(content)
            
            if cleaned_content:
                latex_content += f"\\chapter{{Chapter {file_number}}}\n\n"
                latex_content += cleaned_content + "\n\n"
                
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    latex_content += "\\end{document}\n"
    
    # Write CLEAN LaTeX file
    with open("clean_book.tex", 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print("✅ Created clean_book.tex")
    print("🚀 Build with: pdflatex clean_book.tex")

if __name__ == "__main__":
    merge_and_clean_txt()