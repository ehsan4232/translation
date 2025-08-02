#!/usr/bin/env python3
"""
اسکریپت تبدیل فایل‌های Markdown به Word با نصب خودکار Pandoc
"""

import os
import glob
import sys
from pathlib import Path

def install_pandoc():
    """نصب خودکار pandoc"""
    try:
        import pypandoc
        print("📥 در حال دانلود و نصب Pandoc...")
        pypandoc.download_pandoc()
        print("✅ Pandoc با موفقیت نصب شد!")
        return True
    except Exception as e:
        print(f"❌ خطا در نصب Pandoc: {e}")
        return False

def convert_md_to_docx():
    """تبدیل همه فایل‌های MD به DOCX"""
    
    try:
        import pypandoc
    except ImportError:
        print("❌ pypandoc نصب نیست!")
        print("لطفاً اجرا کنید: pip install pypandoc")
        return
    
    # تلاش برای تست pandoc
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        print("⚠️ Pandoc پیدا نشد. در حال نصب خودکار...")
        if not install_pandoc():
            print("❌ نصب Pandoc ناموفق بود.")
            print("لطفاً دستی نصب کنید:")
            print("Windows: winget install --id JohnMacFarlane.Pandoc")
            print("macOS: brew install pandoc")
            print("Linux: sudo apt-get install pandoc")
            return
    
    # ایجاد پوشه خروجی
    output_dir = Path("docx_output")
    output_dir.mkdir(exist_ok=True)
    
    # پیدا کردن همه فایل‌های MD
    md_files = glob.glob("*.md")
    
    if not md_files:
        print("هیچ فایل MD پیدا نشد!")
        return
    
    print(f"📚 تعداد {len(md_files)} فایل MD پیدا شد...")
    successful = 0
    failed = 0
    
    for md_file in md_files:
        try:
            # نام فایل خروجی
            filename = Path(md_file).stem
            output_file = output_dir / f"{filename}.docx"
            
            print(f"🔄 در حال تبدیل: {md_file}")
            
            # خواندن محتوای فایل
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تبدیل با pandoc
            pypandoc.convert_text(
                content,
                'docx',
                format='md',
                outputfile=str(output_file),
                extra_args=[
                    '--metadata', 'dir=rtl',
                    '--metadata', 'lang=fa'
                ]
            )
            
            print(f"✅ تکمیل شد: {output_file}")
            successful += 1
            
        except Exception as e:
            print(f"❌ خطا در تبدیل {md_file}: {e}")
            failed += 1
    
    print(f"\n🎉 تبدیل کامل!")
    print(f"✅ موفق: {successful} فایل")
    print(f"❌ ناموفق: {failed} فایل")
    print(f"📁 فایل‌ها در پوشه {output_dir} ذخیره شدند.")

def main():
    """تابع اصلی"""
    print("🚀 شروع تبدیل فایل‌های Markdown به Word...")
    print("=" * 50)
    
    # بررسی وجود pip
    try:
        import pypandoc
    except ImportError:
        print("❌ کتابخانه pypandoc نصب نیست!")
        response = input("آیا می‌خواهید نصب کنم؟ (y/n): ")
        if response.lower() in ['y', 'yes', 'بله']:
            os.system(f"{sys.executable} -m pip install pypandoc")
            print("✅ pypandoc نصب شد. لطفاً دوباره اجرا کنید.")
        return
    
    convert_md_to_docx()

if __name__ == "__main__":
    main()
