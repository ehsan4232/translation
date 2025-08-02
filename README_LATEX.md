# 📚 راهنمای کامل ساخت کتاب لاتک

## 🎯 نحوه استفاده (سریع)

```bash
# 1. کلون کردن ریپو
git clone https://github.com/ehsan4232/translation.git
cd translation

# 2. ساخت سریع PDF
chmod +x quick_build.sh
./quick_build.sh
```

## 📋 نیازمندی‌ها

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install texlive-xetex texlive-lang-other texlive-fonts-extra python3
```

### macOS:
```bash
# نصب MacTeX
brew install --cask mactex

# یا استفاده از BasicTeX
brew install --cask basictex
sudo tlmgr update --self
sudo tlmgr install xetex babel-persian
```

### Windows:
1. [MiKTeX](https://miktex.org) را دانلود و نصب کنید
2. Python 3 را نصب کنید
3. Git Bash یا PowerShell استفاده کنید

## 🔧 نصب فونت فارسی

### Ubuntu/Debian:
```bash
sudo apt-get install fonts-hosny-amiri fonts-farsiweb
# یا دانلود XB Niloofar از ایران‌نویس
```

### macOS:
```bash
# فونت XB Niloofar را از سایت ایران‌نویس دانلود و نصب کنید
# یا از فونت‌های سیستم استفاده کنید
```

### Windows:
- فونت‌های فارسی را در پنل کنترل > فونت‌ها نصب کنید

## 📁 ساختار فایل‌ها

```
translation/
├── 002.tex, 003.tex, ...     # فایل‌های LaTeX ویراستاری شده
├── 001.png, 006.png, ...     # تصاویر کتاب
├── combine_latex.py           # اسکریپت ترکیب فایل‌ها
├── quick_build.sh            # ساخت سریع
└── README_LATEX.md           # این فایل
```

## ⚙️ نحوه کار اسکریپت‌ها

### combine_latex.py:
1. 🔍 تمام فایل‌های `.tex` را پیدا می‌کند
2. 📑 آنها را به ترتیب شماره مرتب می‌کند  
3. 🖼️ تصاویر مربوطه را شناسایی می‌کند
4. 📖 یک فایل `complete_book.tex` کامل ایجاد می‌کند
5. 🛠️ اسکریپت `build.sh` برای ساخت PDF می‌سازد

### quick_build.sh:
1. ▶️ اسکریپت پایتون را اجرا می‌کند
2. 📄 XeLaTeX را دو بار اجرا می‌کند (برای فهرست مطالب)
3. 🧹 فایل‌های موقت را پاک می‌کند
4. ✅ PDF نهایی را ایجاد می‌کند

## 🎨 تنظیمات پیشرفته

### تغییر فونت:
فایل `complete_book.tex` را ویرایش کنید:
```latex
% تغییر فونت اصلی
\settextfont{Vazir}           % بجای XB Niloofar

% تغییر فونت اعداد  
\setdigitfont{Yas}           % برای اعداد فارسی

% اضافه کردن فونت انگلیسی
\setlatintextfont{Times New Roman}
```

### تنظیم اندازه صفحه:
```latex
\geometry{a4paper, margin=2cm}     % حاشیه کمتر
\geometry{a5paper, margin=1.5cm}   # اندازه A5
```

## 🐛 عیب‌یابی

### مشکل فونت:
```bash
# بررسی فونت‌های نصب شده
fc-list | grep -i persian
fc-list | grep -i farsi

# اگر فونت پیدا نشد، از فونت سیستم استفاده کنید
```

### خطای LaTeX:
```bash
# مشاهده جزئیات خطا
xelatex complete_book.tex
# لاگ را بررسی کنید: complete_book.log
```

### مشکل اسکریپت پایتون:
```bash
# بررسی نسخه پایتون
python3 --version

# اجرای دستی
python3 combine_latex.py
```

### تصاویر نمایش داده نمی‌شوند:
1. بررسی وجود فایل‌های PNG
2. مسیر صحیح تصاویر در LaTeX  
3. اجازه دسترسی به فایل‌ها

## 📖 مشاهده PDF

### Linux:
```bash
xdg-open complete_book.pdf
evince complete_book.pdf      # یا هر PDF viewer دیگر
```

### macOS:
```bash
open complete_book.pdf
```

### Windows:
```bash
start complete_book.pdf
# یا دوبار کلیک روی فایل
```

## 🔄 به‌روزرسانی

برای به‌روزرسانی کتاب پس از تغییرات:
```bash
git pull                      # دریافت آخرین تغییرات
./quick_build.sh             # ساخت مجدد PDF
```

## 📞 پشتیبانی

اگر مشکلی داشتید:
1. 📋 ابتدا لاگ‌های خطا را بررسی کنید
2. 🔍 فونت‌ها و بسته‌های LaTeX نصب باشند  
3. 💬 در Issues ریپو سوال بپرسید

## 💡 نکات مفید

- ✨ برای کیفیت بهتر PDF از `pdflatex` بجای `xelatex` **استفاده نکنید** (فارسی پشتیبانی نمی‌کند)
- 🎯 اگر فقط قسمتی از کتاب را می‌خواهید، فایل‌های `.tex` غیرضروری را موقتاً حذف کنید
- 📱 برای مطالعه روی موبایل، PDF را به فرمت EPUB تبدیل کنید
- 🔖 فهرست مطالب و صفحه‌بندی خودکار تولید می‌شود

---

**موفق باشید! 🎉**
