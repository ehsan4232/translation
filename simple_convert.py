"""
تبدیل ساده MD به DOCX بدون Pandoc
فقط با کتابخانه‌های پایتون
"""

import os
import glob
from pathlib import Path
import re

def install_required_packages():
    """نصب کتابخانه‌های مورد نیاز"""
    try:
        import docx
        from markdown import markdown
        from bs4 import BeautifulSoup
        return True
    except ImportError:
        print("📦 در حال نصب کتابخانه‌های مورد نیاز...")
        os.system("pip install python-docx markdown beautifulsoup4")
        print("✅ کتابخانه‌ها نصب شدند. لطفاً دوباره اجرا کنید.")
        return False

def md_to_docx_simple():
    """تبدیل MD به DOCX بدون pandoc"""
    
    if not install_required_packages():
        return
    
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from markdown import markdown
    from bs4 import BeautifulSoup
    import html
    
    # ایجاد پوشه خروجی
    output_dir = Path("docx_output")
    output_dir.mkdir(exist_ok=True)
    
    # پیدا کردن فایل‌های MD
    md_files = glob.glob("*.md")
    
    if not md_files:
        print("❌ هیچ فایل MD پیدا نشد!")
        return
    
    print(f"📚 {len(md_files)} فایل MD پیدا شد...")
    
    successful = 0
    failed = 0
    
    for md_file in md_files:
        try:
            print(f"🔄 در حال تبدیل: {md_file}")
            
            # خواندن فایل MD
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # تبدیل MD به HTML
            html_content = markdown(md_content)
            
            # پارس HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # ایجاد سند Word
            doc = Document()
            
            # تنظیمات RTL
            sections = doc.sections
            for section in sections:
                section.page_width = Inches(8.5)
                section.page_height = Inches(11)
            
            # پردازش عناصر HTML
            for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'blockquote']):
                
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    # عناوین
                    level = int(element.name[1])
                    heading = doc.add_heading(element.get_text().strip(), level=level)
                    heading.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    
                elif element.name == 'p':
                    # پاراگراف‌ها
                    text = element.get_text().strip()
                    if text:
                        p = doc.add_paragraph(text)
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        
                elif element.name in ['ul', 'ol']:
                    # لیست‌ها
                    for li in element.find_all('li'):
                        text = li.get_text().strip()
                        if text:
                            p = doc.add_paragraph(text, style='List Bullet' if element.name == 'ul' else 'List Number')
                            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                            
                elif element.name == 'blockquote':
                    # نقل قول‌ها
                    text = element.get_text().strip()
                    if text:
                        p = doc.add_paragraph(text)
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                        # اضافه کردن استایل نقل قول
                        p.style = 'Quote'
            
            # ذخیره سند
            output_file = output_dir / f"{Path(md_file).stem}.docx"
            doc.save(str(output_file))
            
            print(f"✅ تکمیل شد: {output_file}")
            successful += 1
            
        except Exception as e:
            print(f"❌ خطا در تبدیل {md_file}: {e}")
            failed += 1
    
    print(f"\n🎉 تبدیل کامل!")
    print(f"✅ موفق: {successful} فایل")
    print(f"❌ ناموفق: {failed} فایل")
    print(f"📁 فایل‌ها در پوشه {output_dir} ذخیره شدند.")

if __name__ == "__main__":
    print("🚀 تبدیل MD به DOCX (بدون Pandoc)")
    print("=" * 40)
    md_to_docx_simple()
