# راهنمای تبدیل فایل‌های Markdown به Word

این مخزن شامل فایل‌های ترجمه شده به فرمت Markdown است که می‌توانید آن‌ها را به Word تبدیل کنید.

## روش‌های تبدیل

### 1️⃣ استفاده از Pandoc (توصیه شده)

#### نصب Pandoc:
```bash
# Windows
winget install --id JohnMacFarlane.Pandoc

# macOS  
brew install pandoc

# Linux
sudo apt-get install pandoc
```

#### تبدیل فایل‌ها:
```bash
# تبدیل یک فایل
pandoc 021.md -o 021.docx --metadata dir=rtl

# تبدیل همه فایل‌ها
for file in *.md; do pandoc "$file" -o "${file%.md}.docx" --metadata dir=rtl; done
```

### 2️⃣ استفاده از GitHub Actions

GitHub Action خودکار را فعال کرده‌ام که با هر push فایل‌های DOCX تولید می‌کند:

1. به تب **Actions** در GitHub برو
2. روی **Convert MD to DOCX** کلیک کن  
3. روی **Run workflow** کلیک کن
4. فایل‌های DOCX در بخش **Artifacts** دانلود کن

### 3️⃣ استفاده از اسکریپت Python

```bash
# نصب کتابخانه‌ها
pip install pypandoc python-docx

# اجرای اسکریپت
python convert_to_docx.py
```

### 4️⃣ تبدیل آنلاین

می‌توانید از سایت‌های آنلاین مثل:
- [Pandoc Try](https://pandoc.org/try/)
- [CloudConvert](https://cloudconvert.com/md-to-docx)
- [Convertio](https://convertio.co/md-docx/)

## نکات مهم

- **RTL Support**: همه روش‌ها از راست‌چین بودن متن پشتیبانی می‌کنند
- **فونت فارسی**: ممکن است نیاز باشد فونت فارسی در Word تنظیم کنید
- **فرمت‌بندی**: عناوین، لیست‌ها و جدول‌ها به درستی تبدیل می‌شوند

## فایل‌های آماده

فایل‌های MD موجود:
- 021.md - جریان کار سیستم
- 024.md - کش
- 026.md - چالش‌های کش  
- 029.md - شبکه تحویل محتوا (CDN)
- 030.md - ادامه گردش کار CDN
- 032.md - بهبودهای حاصل شده
- 034.md - لایه وب بدون حالت
- 036.md - مزایای معماری بدون حالت
- 038.md - طراحی نهایی لایه وب
- 040.md - مراکز داده

## مشکل داری؟

اگر مشکلی داری، یه Issue بساز یا مستقیم با من در ارتباط باش.
