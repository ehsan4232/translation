#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Robust LaTeX combiner that handles corrupted content
"""

import os
import re
import glob

def create_clean_latex():
    """Create a clean LaTeX document with robust content filtering"""
    
    # Ultra-clean LaTeX setup
    main_content = r"""\documentclass[12pt,a4paper]{book}
\usepackage{fontspec}
\usepackage{polyglossia}
\usepackage{graphicx}
\usepackage{geometry}
\usepackage{fancyhdr}

% Set up languages properly
\setdefaultlanguage{arabic}
\setotherlanguage{english}

% Page geometry
\geometry{a4paper, margin=2.5cm}

% Font setup with fallbacks
\IfFontExistsTF{Vazir}{
    \newfontfamily\arabicfont[Script=Arabic]{Vazir}
}{
    \IfFontExistsTF{Arial Unicode MS}{
        \newfontfamily\arabicfont[Script=Arabic]{Arial Unicode MS}
    }{
        \newfontfamily\arabicfont[Script=Arabic]{Arial}
    }
}
\newfontfamily\englishfont{Times New Roman}
\setmainfont{Times New Roman}

% Headers and footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[RO,LE]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% Hyperref at the end
\usepackage{hyperref}
\hypersetup{
    unicode=true,
    colorlinks=true,
    linkcolor=blue,
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

    # Process .tex files with robust error handling
    tex_files = sorted(glob.glob('*.tex'), key=lambda x: extract_number(x))
    
    print(f"📄 Found {len(tex_files)} .tex files")
    
    for tex_file in tex_files:
        # Skip generated files
        if any(skip in tex_file for skip in ['complete_book', 'test', 'pdflatex', 'font', 'clean']):
            continue
            
        print(f"📝 Processing: {tex_file}")
        file_num = extract_number(tex_file)
        
        try:
            # Read file with multiple encoding attempts
            content = read_file_robust(tex_file)
            
            if content is None:
                print(f"⚠️ Could not read {tex_file}, skipping...")
                continue
            
            # Extract and clean document content
            doc_content = extract_document_content(content)
            
            if not doc_content:
                print(f"⚠️ No valid content found in {tex_file}")
                continue
            
            # Skip table of contents files
            if '003' in tex_file:
                print(f"⏭️ Skipping TOC file: {tex_file}")
                continue
            
            # Clean and validate content
            cleaned_content = clean_latex_content(doc_content)
            
            if not cleaned_content.strip():
                print(f"⚠️ Content became empty after cleaning {tex_file}")
                continue
            
            # Extract title
            title = extract_safe_title(cleaned_content, file_num)
            
            # Add to main document
            main_content += f"\n% === Chapter from {tex_file} ===\n"
            main_content += f"\\chapter{{{title}}}\n\n"
            
            # Wrap Persian content properly
            main_content += "\\begin{arabic}\n"
            main_content += cleaned_content + "\n"
            main_content += "\\end{arabic}\n\n"
            
            # Add image if exists
            img_file = f"{file_num:03d}.png"
            if os.path.exists(img_file):
                main_content += f"""
\\begin{{figure}}[h]
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
    
    # Write clean output
    output_file = 'complete_book_clean.tex'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    print(f"✅ Created {output_file}")
    return output_file

def extract_number(filename):
    """Extract number from filename safely"""
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0

def read_file_robust(filename):
    """Read file with multiple encoding attempts"""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {filename} with {encoding}: {e}")
            continue
    
    return None

def extract_document_content(content):
    """Safely extract content between \\begin{document} and \\end{document}"""
    try:
        # Find document boundaries
        start_pattern = r'\\\\begin\s*\{\s*document\s*\}'
        end_pattern = r'\\\\end\s*\{\s*document\s*\}'
        
        start_match = re.search(start_pattern, content, re.IGNORECASE)
        end_match = re.search(end_pattern, content, re.IGNORECASE)
        
        if start_match and end_match:
            return content[start_match.end():end_match.start()].strip()
        else:
            # If no document environment, return the whole content
            return content.strip()
            
    except Exception as e:
        print(f"Error extracting document content: {e}")
        return ""

def clean_latex_content(content):
    """Clean and sanitize LaTeX content"""
    if not content:
        return ""
    
    # Remove problematic commands
    problematic_patterns = [
        r'\\\\maketitle\s*',
        r'\\\\settextfont\{[^}]*\}',
        r'\\\\setdigitfont\{[^}]*\}',
        r'\\\\setlatintextfont\{[^}]*\}',
        r'\\\\setmainlanguage\{[^}]*\}',  # Remove problematic language commands
        r'\\\\setdefaultlanguage\{[^}]*\}',
        r'\\\\usepackage\{[^}]*\}',  # Remove package declarations from content
        r'\\\\documentclass\{[^}]*\}',
    ]
    
    cleaned = content
    for pattern in problematic_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove empty lines and excessive whitespace
    lines = cleaned.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('%'):  # Skip empty lines and comments
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def extract_safe_title(content, file_num):
    """Extract title safely with fallbacks"""
    try:
        # Look for titles in various formats
        title_patterns = [
            r'\\\\title\{([^}]+)\}',
            r'\\\\section\*?\{([^}]+)\}',
            r'\\\\textbf\{([^}]+)\}',
            r'\\\\subsection\*?\{([^}]+)\}'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean up title
                title = re.sub(r'\\\\[a-zA-Z]+\*?\{?', '', title)
                title = re.sub(r'[{}*\\\\]', '', title).strip()
                if len(title) > 3:
                    return title[:50]  # Limit length
        
        # Extract first meaningful text
        lines = content.strip().split('\n')
        for line in lines[:10]:  # Check first 10 lines
            clean_line = re.sub(r'\\\\[a-zA-Z]+\*?\{?', '', line).strip()
            clean_line = re.sub(r'[{}*\\\\]', '', clean_line).strip()
            if clean_line and len(clean_line) > 5 and not clean_line.startswith('%'):
                return clean_line[:50]
                
    except Exception as e:
        print(f"Error extracting title: {e}")
    
    # Fallback title
    return f"فصل {file_num}"

def create_simple_test():
    """Create a simple test file"""
    
    test_content = r"""\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{polyglossia}

% Set up languages
\setdefaultlanguage{arabic}
\setotherlanguage{english}

% Font setup
\IfFontExistsTF{Vazir}{
    \newfontfamily\arabicfont[Script=Arabic]{Vazir}
}{
    \newfontfamily\arabicfont[Script=Arabic]{Arial}
}
\newfontfamily\englishfont{Times New Roman}
\setmainfont{Times New Roman}

\title{Clean Font Test}
\author{Test}

\begin{document}

\maketitle

\section{English Test}
This is English text with Times New Roman.

\begin{arabic}
\section{تست فارسی}
این یک متن فارسی برای تست فونت است.

\textbf{متن پررنگ:} این متن با فونت نوشته شده است.
\end{arabic}

\end{document}
"""
    
    with open('clean_test.tex', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Created clean_test.tex")

if __name__ == "__main__":
    print("🔧 Creating clean, robust LaTeX document...")
    
    # Create test file
    create_simple_test()
    
    # Create main document
    create_clean_latex()
    
    print("\n📋 Files created:")
    print("   🧪 clean_test.tex - Clean font test")
    print("   📄 complete_book_clean.tex - Clean main document")
    print("\n🚀 Build commands:")
    print("   xelatex clean_test.tex")
    print("   xelatex complete_book_clean.tex")
    print("   xelatex complete_book_clean.tex")