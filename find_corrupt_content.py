#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Find and fix corrupted content in .tex files
"""

import os
import re
import glob

def scan_for_problems():
    """Scan all .tex files for problematic content"""
    
    print("🔍 Scanning for problematic content...")
    
    problematic_patterns = [
        r'\\setmainlanguage\{latex\}',
        r'\\setmainlanguage\{[^}]*\}',
        r'\\setdefaultlanguage\{latex\}',
        r'\\usepackage.*xepersian',
        r'\\settextfont.*',
        r'\\setdigitfont.*'
    ]
    
    tex_files = glob.glob('*.tex')
    problems_found = []
    
    for tex_file in tex_files:
        if any(skip in tex_file for skip in ['complete_book', 'test', 'clean', 'pdflatex', 'font']):
            continue
            
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_problems = []
            for i, pattern in enumerate(problematic_patterns):
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    file_problems.extend([(pattern, match) for match in matches])
            
            if file_problems:
                problems_found.append((tex_file, file_problems, content))
                print(f"⚠️ Problems in {tex_file}:")
                for pattern, match in file_problems:
                    print(f"   - Found: {match}")
                    
        except Exception as e:
            print(f"❌ Error reading {tex_file}: {e}")
    
    return problems_found

def create_nuclear_clean():
    """Create completely clean version by removing ALL LaTeX commands"""
    
    print("☢️ Creating nuclear-clean version...")
    
    # Ultra-minimal LaTeX setup
    main_content = r"""\documentclass[12pt,a4paper]{book}
\usepackage{fontspec}
\setmainfont{Times New Roman}
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

    tex_files = sorted(glob.glob('*.tex'), key=lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else 0)
    
    for tex_file in tex_files:
        if any(skip in tex_file for skip in ['complete_book', 'test', 'clean', 'pdflatex', 'font', 'nuclear']):
            continue
            
        file_num = re.findall(r'\d+', tex_file)[0] if re.findall(r'\d+', tex_file) else '000'
        
        if '003' in tex_file:  # Skip TOC
            continue
            
        print(f"💣 Nuclear cleaning: {tex_file}")
        
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Extract only the text content, remove ALL LaTeX commands
            cleaned = extract_pure_text(content)
            
            if cleaned.strip():
                main_content += f"\n\\chapter{{Chapter {file_num}}}\n"
                main_content += cleaned + "\n\n"
                
                # Add image
                img_file = f"{file_num.zfill(3)}.png"
                if os.path.exists(img_file):
                    main_content += f"""
\\begin{{figure}}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{{{img_file}}}
\\caption{{Figure {file_num}}}
\\end{{figure}}

"""
                    
        except Exception as e:
            print(f"❌ Error with {tex_file}: {e}")
            continue
    
    main_content += "\n\\end{document}"
    
    # Write nuclear-clean version
    with open('nuclear_clean.tex', 'w', encoding='utf-8', errors='replace') as f:
        f.write(main_content)
    
    print("✅ Created nuclear_clean.tex")

def extract_pure_text(content):
    """Extract only pure text, removing ALL LaTeX commands"""
    
    # First, extract content between \begin{document} and \end{document}
    start = content.find('\\begin{document}')
    end = content.find('\\end{document}')
    
    if start != -1 and end != -1:
        content = content[start + len('\\begin{document}'):end]
    
    # Remove ALL LaTeX commands (anything starting with backslash)
    content = re.sub(r'\\[a-zA-Z*]+\*?(\[[^\]]*\])?\{[^}]*\}', '', content)
    content = re.sub(r'\\[a-zA-Z*]+\*?', '', content)
    
    # Remove LaTeX special characters and environments
    content = re.sub(r'\{[^}]*\}', '', content)  # Remove remaining braces
    content = re.sub(r'%.*$', '', content, flags=re.MULTILINE)  # Remove comments
    content = re.sub(r'\$[^$]*\$', '', content)  # Remove math mode
    
    # Clean up whitespace
    lines = content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and len(line) > 2:  # Keep only meaningful lines
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def show_problematic_lines():
    """Show the actual problematic lines around line 1902"""
    
    print("🎯 Looking for line 1902 content...")
    
    tex_files = glob.glob('*.tex')
    
    for tex_file in tex_files:
        if any(skip in tex_file for skip in ['complete_book', 'test', 'clean', 'pdflatex', 'font']):
            continue
            
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            print(f"\n📄 Checking {tex_file} ({len(lines)} lines)")
            
            # Look for setmainlanguage
            for i, line in enumerate(lines, 1):
                if 'setmainlanguage' in line or 'latex' in line:
                    print(f"   Line {i}: {line.strip()}")
                    
        except Exception as e:
            print(f"❌ Error reading {tex_file}: {e}")

if __name__ == "__main__":
    print("🔍 Scanning for corruption...")
    
    # Scan for problems
    problems = scan_for_problems()
    
    # Show problematic lines
    show_problematic_lines()
    
    # Create nuclear clean version
    create_nuclear_clean()
    
    print("\n🚀 Try building:")
    print("   pdflatex nuclear_clean.tex")
    print("   pdflatex nuclear_clean.tex")
    
    if problems:
        print(f"\n⚠️ Found {len(problems)} files with issues")
        print("The nuclear_clean.tex should work with PDFLaTeX")
    else:
        print("\n🤔 No obvious problems found, but nuclear version should still work")