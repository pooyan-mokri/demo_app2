# TheMoak ERP

پروژه کامل ERP ابری برای برند عینک TheMoak با Next.js 14 و FastAPI.

## ساختار
- `backend/` سرویس FastAPI با SQLModel و JWT
- `frontend/` اپلیکیشن Next.js با Tailwind RTL، React Query و Zustand

## اجرای محلی
1. محیط پایتون ایجاد و نصب وابستگی‌ها:
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
