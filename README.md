# Persian-Word-Database

About 700,000 Persian(Farsi) Words

<div dir="rtl">
  <h1>دیتابیس لغات و اصطلاحات فارسی</h1>
مجموعه نزدیک به 700 هزار کلمه فارسی متشکل از فرهنگ لغت معین، کلمات فارسی ویکی پدیا، اشعار فارسی و سایر منابع برای کاربردهای پردازش داده و زبان.
هر کلمه در یک خط قرار گرفته است
</div>

## پروژه ها

پروژه های زیر از این مخزن استفاده کرده اند:  
https://github.com/shahind/tj2fa_php  
https://github.com/shahind/Persian-Spell-Corrector-PHP

# persianwords

a collection of common Persian names, words, stop words, films, books, cars ...

# اصلاح غلط املایی و نگارشی فارسی

این کد بر اساس کد فلیپ ریبرو توسعه داده شده است تا به کمک الگوریتم پیشنهادی پیتر نورویگ اشکالات نگارشی و غلط املایی متون و کلمات
فارسی را اصلاح کند.

برای استفاده از این کد به دیتابیسی از کلمات فارسی احتیاج دارید که باید در فایل متنی داخل پوشه پروژه قرار بگیرد، ما از دیتابیس زیر
استفاده کرده ایم اما شما می توانید هر متن فارسی را با هر شکلی در فایل مذکور قرار دهید

(https://github.com/shahind/Persian-Words-Database)

دیتابیس فوق از کلمات فرهنگ معین، ویکی پدیای فارسی، اشعار شاعران فارسی و سایر کلمات تشکیل شده است و مجموعا شامل نزدیک به 750 هزار کلمه می شود

# Persian-Spell-Corrector-PHP

This is a PHP Script which is developed based on Felipe Ribeiro's Work(http://www.feliperibeiro.com) who developed a Spell Checker for English based on Peter Norvig's algorithm for PHP.

I just changed it in order to use it for Persian words.
a database of Persian words is used from Persian-Words-Database (https://github.com/shahind/Persian-Words-Database)

Put your words into big.txt file, include the class in your project and use it: SpellCorrector::correct($string)
