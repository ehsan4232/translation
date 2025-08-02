"""
تنظیمات سفارشی فونت و استایل برای تبدیل MD به DOCX
"""

# تنظیمات فونت
FONT_SETTINGS = {
    # فونت‌های اصلی (اولویت بر اساس دسترسی)
    'PERSIAN_FONTS': [
        'B Nazanin',      # اولویت اول
        'Vazir',          # فونت مدرن
        'Iran Sans',      # فونت استاندارد
        'Tahoma',         # پشتیبان
        'Arial Unicode MS'  # نهایی
    ],
    
    'CODE_FONTS': [
        'Fira Code',      # فونت کد مدرن
        'Consolas',       # ویندوز
        'Monaco',         # مک
        'Courier New'     # کلاسیک
    ],
    
    # اندازه فونت‌ها (بر اساس نقطه)
    'SIZES': {
        'H1': 20,         # عنوان اصلی
        'H2': 18,         # عنوان فرعی
        'H3': 16,         # عنوان سطح سوم
        'H4': 14,         # عنوان سطح چهارم
        'NORMAL': 12,     # متن عادی
        'QUOTE': 11,      # نقل قول
        'CODE': 10,       # کد
        'CAPTION': 9      # توضیحات
    },
    
    # رنگ‌ها (RGB)
    'COLORS': {
        'H1': (0, 51, 102),        # آبی تیره
        'H2': (51, 102, 153),      # آبی متوسط
        'H3': (102, 102, 102),     # خاکستری
        'H4': (136, 136, 136),     # خاکستری روشن
        'NORMAL': (0, 0, 0),       # مشکی
        'QUOTE': (85, 85, 85),     # خاکستری تیره
        'CODE': (139, 69, 19),     # قهوه‌ای (برای کد)
        'LINK': (0, 102, 204),     # آبی برای لینک
        'EMPHASIS': (204, 0, 0)    # قرمز برای تأکید
    },
    
    # فاصله‌گذاری (نقطه)
    'SPACING': {
        'H1_BEFORE': 18,
        'H1_AFTER': 12,
        'H2_BEFORE': 15,
        'H2_AFTER': 10,
        'H3_BEFORE': 12,
        'H3_AFTER': 8,
        'PARAGRAPH_AFTER': 6,
        'QUOTE_INDENT': 36,        # 0.5 اینچ
        'LIST_INDENT': 18,
        'LINE_SPACING': 1.15
    }
}

# تنظیمات صفحه
PAGE_SETTINGS = {
    'WIDTH': 8.5,              # اینچ
    'HEIGHT': 11,              # اینچ
    'MARGIN_TOP': 1,           # اینچ
    'MARGIN_BOTTOM': 1,        # اینچ
    'MARGIN_LEFT': 1.25,       # اینچ (بیشتر برای صحافی)
    'MARGIN_RIGHT': 1,         # اینچ
    'ORIENTATION': 'portrait'  # عمودی
}

# انواع استایل‌های قابل تنظیم
CUSTOM_STYLES = {
    'HEADING_NUMBERING': True,     # شماره‌گذاری عناوین
    'RTL_SUPPORT': True,           # پشتیبانی راست به چپ
    'JUSTIFY_TEXT': True,          # تراز کردن متن
    'INDENT_FIRST_LINE': False,    # تورفتگی خط اول
    'SPACE_BETWEEN_PARAGRAPHS': True,  # فاصله بین پاراگراف‌ها
    'HIGHLIGHT_CODE': True,        # برجسته کردن کد
    'WATERMARK': False,            # واترمارک
    'HEADER_FOOTER': False         # سرصفحه و پاصفحه
}

def get_available_font(font_list):
    """
    انتخاب اولین فونت موجود از لیست
    """
    # در محیط واقعی باید فونت‌های نصب شده را بررسی کنیم
    # فعلاً اولین فونت را برمی‌گردانیم
    return font_list[0]

# تنظیمات خاص کاربر (قابل تغییر)
USER_PREFERENCES = {
    'MAIN_FONT': 'B Nazanin',
    'CODE_FONT': 'Consolas', 
    'BASE_SIZE': 12,
    'COLOR_SCHEME': 'default',  # default, dark, colorful
    'SPACING_MODE': 'normal'    # tight, normal, loose
}

print("📝 فایل تنظیمات فونت آماده شد!")
print("💡 برای تغییر تنظیمات، متغیر USER_PREFERENCES را ویرایش کنید.")
