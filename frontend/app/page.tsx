import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 text-center">
      <h1 className="text-4xl font-bold text-brand-primary">سامانه ابری TheMoak ERP</h1>
      <p className="max-w-xl text-lg text-slate-600">
        فروش، خرید، انبار و حسابداری تموک را در یک داشبورد یکپارچه مدیریت کنید.
      </p>
      <Link
        href="/(auth)/login"
        className="rounded-xl bg-brand-primary px-6 py-3 text-white shadow-lg transition hover:bg-indigo-700"
      >
        ورود به سامانه
      </Link>
    </main>
  );
}
