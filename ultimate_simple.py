#!/usr/bin/env python3
"""
Ultimate simple - just extract text and make basic PDF
"""

import os

def create_ultimate_simple():
    """Create the most basic possible LaTeX file"""
    
    # Ultra-basic LaTeX - no fonts, no packages that cause issues
    content = r"""\documentclass{article}
\usepackage{graphicx}

\title{System Design Interview}
\author{Alex Xu}

\begin{document}

\maketitle

"""

    # Just read 002.tex and extract the text manually
    if os.path.exists('002.tex'):
        print("Reading 002.tex...")
        
        try:
            with open('002.tex', 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            # Find the actual content (everything after \begin{document})
            start = text.find('\\begin{document}')
            if start != -1:
                # Get everything after \begin{document}
                content_part = text[start + len('\\begin{document}'):]
                
                # Remove \end{document}
                end = content_part.find('\\end{document}')
                if end != -1:
                    content_part = content_part[:end]
                
                # Remove problematic commands
                content_part = content_part.replace('\\maketitle', '')
                content_part = content_part.replace('\\settextfont{XB Niloofar}', '')
                content_part = content_part.replace('\\setdigitfont{XB Niloofar}', '')
                
                # Add the cleaned content
                content += "\n\\section{Chapter 1}\n"
                content += content_part
                
        except Exception as e:
            print(f"Error reading 002.tex: {e}")
            content += "\nError reading file, but this document should still compile.\n"
    
    # Add image if it exists
    if os.path.exists('001.png'):
        content += """

\\begin{figure}[h]
\\centering
\\includegraphics[width=0.8\\textwidth]{001.png}
\\caption{Figure 1}
\\end{figure}

"""
        print("Added 001.png")

    content += "\n\\end{document}"
    
    # Write the simplest possible file
    with open('simple.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Created simple.tex")
    
    # Also create a pure text version for debugging
    with open('debug_content.txt', 'w', encoding='utf-8') as f:
        if os.path.exists('002.tex'):
            with open('002.tex', 'r', encoding='utf-8', errors='ignore') as source:
                f.write("=== RAW CONTENT OF 002.tex ===\n")
                f.write(source.read())
    
    print("✅ Created debug_content.txt")

if __name__ == "__main__":
    print("🔧 Creating ultimate simple version...")
    create_ultimate_simple()
    print("\n🚀 Now run:")
    print("   pdflatex simple.tex")
    print("   pdflatex simple.tex")