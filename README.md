# TheMoak ERP

پروژه کامل ERP ابری برای برند عینک TheMoak با Next.js 14 و FastAPI.

## ساختار
- `backend/` سرویس FastAPI با SQLModel و JWT
- `frontend/` اپلیکیشن Next.js با Tailwind RTL، React Query و Zustand

## اجرای محلی
1. محیط پایتون (نسخه‌ی 3.11) ایجاد و نصب وابستگی‌ها:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. اجرای فرانت‌اند:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. تنظیم متغیر `NEXT_PUBLIC_API_URL` برای اتصال به API.

## استقرار روی Netlify
1. این ریپو را به Netlify متصل کنید (Deployment base = `frontend`).
2. دستور ساخت به صورت `npm run build` و مسیر خروجی `.next` (با کمک فایل `netlify.toml`) تنظیم شده است.
3. متغیر محیطی `NEXT_PUBLIC_API_URL` و سایر مقادیر لازم برای اتصال به بک‌اند را در محیط Netlify تعریف کنید.
4. افزونه `@netlify/plugin-nextjs` به عنوان devDependency اضافه شده است و در Netlify به صورت خودکار اجرا می‌شود.
