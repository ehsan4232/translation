"""
تبدیل MD به PDF با ظاهر GitHub
استفاده از Pandoc و CSS GitHub
"""

import os
import glob
from pathlib import Path
import subprocess
import sys

def install_requirements():
    """نصب کتابخانه‌های مورد نیاز"""
    try:
        import pdfkit
        import markdown
        return True
    except ImportError:
        print("📦 نصب کتابخانه‌های مورد نیاز...")
        os.system("pip install pdfkit markdown2 beautifulsoup4")
        print("✅ کتابخانه‌ها نصب شدند.")
        return True

def download_wkhtmltopdf():
    """راهنمای نصب wkhtmltopdf"""
    print("🔧 نصب wkhtmltopdf:")
    print("Windows: https://wkhtmltopdf.org/downloads.html")
    print("یا: winget install wkhtmltopdf")
    print("macOS: brew install wkhtmltopdf")
    print("Linux: sudo apt-get install wkhtmltopdf")

def create_github_css():
    """ایجاد CSS مشابه GitHub"""
    css_content = """
@import url('https://fonts.googleapis.com/css2?family=Vazir:wght@100;200;300;400;500;600;700;800;900&display=swap');

body {
    font-family: 'Vazir', 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    color: #24292f;
    background-color: #ffffff;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
    direction: rtl;
    text-align: right;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Vazir', sans-serif;
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
    color: #1f2328;
}

h1 {
    font-size: 2em;
    font-weight: 600;
    padding-bottom: .3em;
    border-bottom: 1px solid #d8dee4;
}

h2 {
    font-size: 1.5em;
    font-weight: 600;
    padding-bottom: .3em;
    border-bottom: 1px solid #d8dee4;
}

h3 {
    font-size: 1.25em;
    font-weight: 600;
}

h4 {
    font-size: 1em;
    font-weight: 600;
}

h5 {
    font-size: .875em;
    font-weight: 600;
}

h6 {
    font-size: .85em;
    font-weight: 600;
    color: #656d76;
}

p {
    margin-top: 0;
    margin-bottom: 16px;
}

blockquote {
    margin: 0;
    padding: 0 1em;
    color: #656d76;
    border-right: .25em solid #d8dee4;
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
}

blockquote > :first-child {
    margin-top: 0;
}

blockquote > :last-child {
    margin-bottom: 0;
}

code {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 12px;
    padding: .2em .4em;
    background-color: #f6f8fa;
    border-radius: 6px;
}

pre {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 12px;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    direction: ltr;
    text-align: left;
}

pre code {
    background-color: transparent;
    border: 0;
    padding: 0;
    font-size: 100%;
}

ul, ol {
    margin-top: 0;
    margin-bottom: 16px;
    padding-right: 2em;
}

li {
    word-wrap: break-all;
}

li > p {
    margin-top: 16px;
}

li + li {
    margin-top: .25em;
}

table {
    border-spacing: 0;
    border-collapse: collapse;
    display: block;
    width: max-content;
    max-width: 100%;
    overflow: auto;
    margin-bottom: 16px;
}

table th {
    font-weight: 600;
}

table th, table td {
    padding: 6px 13px;
    border: 1px solid #d8dee4;
}

table tr {
    background-color: #ffffff;
    border-top: 1px solid #d8dee4;
}

table tr:nth-child(2n) {
    background-color: #f6f8fa;
}

hr {
    height: .25em;
    padding: 0;
    margin: 24px 0;
    background-color: #d8dee4;
    border: 0;
}

strong {
    font-weight: 600;
}

.highlight {
    background-color: #fff8c5;
    padding: 2px 4px;
    border-radius: 3px;
}

/* Custom styles for Persian content */
.rtl-content {
    direction: rtl;
    text-align: right;
}

.ltr-content {
    direction: ltr;
    text-align: left;
}

/* Print styles */
@media print {
    body {
        padding: 20px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
    }
    
    pre, blockquote {
        page-break-inside: avoid;
    }
}
"""
    
    css_file = Path("github_style.css")
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    return css_file

def md_to_pdf_github_style():
    """تبدیل MD به PDF با استایل GitHub"""
    
    if not install_requirements():
        return
    
    import pdfkit
    import markdown
    from markdown.extensions import codehilite, tables, toc
    
    # ایجاد CSS
    css_file = create_github_css()
    
    # پیدا کردن فایل‌ها
    md_files = glob.glob("*.md")
    if not md_files:
        print("❌ فایل MD پیدا نشد!")
        return
    
    # ایجاد پوشه خروجی
    output_dir = Path("pdf_output")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📚 {len(md_files)} فایل پیدا شد...")
    
    # تنظیمات wkhtmltopdf
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'print-media-type': None,
        'disable-smart-shrinking': None,
    }
    
    successful = 0
    failed = 0
    
    for md_file in md_files:
        try:
            print(f"🔄 تبدیل: {md_file}")
            
            # خواندن فایل MD
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # پاک کردن HTML tags اضافی
            import re
            md_content = re.sub(r'<div[^>]*>', '', md_content)
            md_content = re.sub(r'</div>', '', md_content)
            
            # تبدیل MD به HTML
            md = markdown.Markdown(
                extensions=[
                    'codehilite',
                    'tables', 
                    'toc',
                    'fenced_code',
                    'nl2br'
                ],
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'use_pygments': True
                    }
                }
            )
            
            html_content = md.convert(md_content)
            
            # ایجاد HTML کامل
            full_html = f"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Path(md_file).stem}</title>
    <link rel="stylesheet" href="{css_file.absolute()}">
</head>
<body class="rtl-content">
    {html_content}
</body>
</html>
"""
            
            # ذخیره HTML موقت
            temp_html = output_dir / f"{Path(md_file).stem}_temp.html"
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            # تبدیل به PDF
            output_pdf = output_dir / f"{Path(md_file).stem}.pdf"
            
            try:
                pdfkit.from_file(str(temp_html), str(output_pdf), options=options, css=str(css_file))
                print(f"✅ تکمیل شد: {output_pdf}")
                successful += 1
            except Exception as pdf_error:
                print(f"❌ خطا در تولید PDF: {pdf_error}")
                print("💡 ممکن است wkhtmltopdf نصب نباشد.")
                download_wkhtmltopdf()
                failed += 1
            
            # حذف HTML موقت
            if temp_html.exists():
                temp_html.unlink()
                
        except Exception as e:
            print(f"❌ خطا در {md_file}: {e}")
            failed += 1
    
    print(f"\n🎉 تبدیل کامل!")
    print(f"✅ موفق: {successful} فایل")
    print(f"❌ ناموفق: {failed} فایل")
    print(f"📁 فایل‌ها در پوشه {output_dir} ذخیره شدند.")
    
    if failed > 0:
        print(f"\n💡 برای حل مشکل:")
        print(f"1. wkhtmltopdf را نصب کنید")
        print(f"2. یا از روش browser-based استفاده کنید")

if __name__ == "__main__":
    print("🚀 تبدیل MD به PDF (استایل GitHub)")
    print("=" * 50)
    md_to_pdf_github_style()
