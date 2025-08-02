#!/usr/bin/env python3
"""
اسکریپت تبدیل فایل‌های Markdown به Word
نیاز به نصب: pip install pypandoc python-docx
"""

import os
import glob
import pypandoc
from pathlib import Path

def convert_md_to_docx():
    """تبدیل همه فایل‌های MD به DOCX"""
    
    # ایجاد پوشه خروجی
    output_dir = Path("docx_output")
    output_dir.mkdir(exist_ok=True)
    
    # پیدا کردن همه فایل‌های MD
    md_files = glob.glob("*.md")
    
    if not md_files:
        print("هیچ فایل MD پیدا نشد!")
        return
    
    print(f"تعداد {len(md_files)} فایل MD پیدا شد...")
    
    for md_file in md_files:
        try:
            # نام فایل خروجی
            filename = Path(md_file).stem
            output_file = output_dir / f"{filename}.docx"
            
            print(f"در حال تبدیل: {md_file} -> {output_file}")
            
            # تبدیل با pandoc
            pypandoc.convert_file(
                md_file, 
                'docx', 
                outputfile=str(output_file),
                extra_args=['--metadata', 'dir=rtl']
            )
            
            print(f"✅ تکمیل شد: {output_file}")
            
        except Exception as e:
            print(f"❌ خطا در تبدیل {md_file}: {e}")
    
    print(f"\n🎉 تبدیل کامل! فایل‌ها در پوشه {output_dir} ذخیره شدند.")

if __name__ == "__main__":
    convert_md_to_docx()
