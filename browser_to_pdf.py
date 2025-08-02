"""
تبدیل MD به PDF با مرورگر
روش آسان بدون نیاز به نصب اضافی
"""

import os
import glob
from pathlib import Path
import webbrowser
import markdown
import time

def md_to_pdf_browser():
    """تبدیل MD به PDF با استفاده از مرورگر"""
    
    try:
        import markdown
    except ImportError:
        print("📦 نصب markdown...")
        os.system("pip install markdown")
        import markdown
    
    # پیدا کردن فایل‌ها
    md_files = glob.glob("*.md")
    if not md_files:
        print("❌ فایل MD پیدا نشد!")
        return
    
    # ایجاد پوشه خروجی
    output_dir = Path("pdf_preview")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📚 {len(md_files)} فایل پیدا شد...")
    
    # CSS GitHub style
    github_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazir:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Vazir', 'Segoe UI', system-ui, sans-serif;
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
            padding-bottom: .3em;
            border-bottom: 1px solid #d8dee4;
        }
        
        h2 {
            font-size: 1.5em;
            padding-bottom: .3em;
            border-bottom: 1px solid #d8dee4;
        }
        
        h3 {
            font-size: 1.25em;
        }
        
        h4 {
            font-size: 1em;
        }
        
        p {
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
            margin-bottom: 16px;
        }
        
        code {
            font-family: 'SFMono-Regular', Consolas, monospace;
            font-size: 85%;
            padding: .2em .4em;
            background-color: #f6f8fa;
            border-radius: 6px;
        }
        
        pre {
            font-family: 'SFMono-Regular', Consolas, monospace;
            font-size: 85%;
            line-height: 1.45;
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
            direction: ltr;
            text-align: left;
            margin-bottom: 16px;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        ul, ol {
            margin-bottom: 16px;
            padding-right: 2em;
        }
        
        li + li {
            margin-top: .25em;
        }
        
        table {
            border-spacing: 0;
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }
        
        table th, table td {
            padding: 6px 13px;
            border: 1px solid #d8dee4;
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
        
        /* Print styles */
        @media print {
            body {
                padding: 20px;
                max-width: none;
            }
            
            h1, h2, h3, h4, h5, h6 {
                page-break-after: avoid;
            }
            
            pre, blockquote {
                page-break-inside: avoid;
            }
        }
    </style>
    """
    
    for md_file in md_files:
        try:
            print(f"🔄 آماده‌سازی: {md_file}")
            
            # خواندن فایل MD
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # پاک کردن HTML tags
            import re
            md_content = re.sub(r'<div[^>]*>', '', md_content)
            md_content = re.sub(r'</div>', '', md_content)
            
            # تبدیل MD به HTML
            md = markdown.Markdown(
                extensions=['codehilite', 'tables', 'fenced_code', 'nl2br']
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
    {github_css}
</head>
<body>
    <div style="text-align: left; margin-bottom: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px;">
        <strong>📄 فایل: {md_file}</strong><br>
        <small>برای ذخیره PDF: Ctrl+P → Save as PDF</small>
    </div>
    {html_content}
</body>
</html>
"""
            
            # ذخیره HTML
            html_file = output_dir / f"{Path(md_file).stem}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            print(f"✅ آماده شد: {html_file}")
            
        except Exception as e:
            print(f"❌ خطا در {md_file}: {e}")
    
    # باز کردن اولین فایل در مرورگر
    if md_files:
        first_html = output_dir / f"{Path(md_files[0]).stem}.html"
        if first_html.exists():
            print(f"\n🌐 باز کردن در مرورگر: {first_html}")
            webbrowser.open(f"file://{first_html.absolute()}")
    
    print(f"\n🎉 آماده‌سازی کامل!")
    print(f"📁 فایل‌های HTML در پوشه {output_dir} ذخیره شدند.")
    print(f"\n📋 مراحل تبدیل به PDF:")
    print(f"1. فایل HTML را در مرورگر باز کنید")
    print(f"2. Ctrl+P یا Cmd+P فشار دهید")
    print(f"3. Destination: Save as PDF انتخاب کنید")
    print(f"4. More settings → Paper size: A4")
    print(f"5. Save کلیک کنید")

if __name__ == "__main__":
    print("🚀 تبدیل MD به PDF (روش مرورگر)")
    print("=" * 50)
    md_to_pdf_browser()
