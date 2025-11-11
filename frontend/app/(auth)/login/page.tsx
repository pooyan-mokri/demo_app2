"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";

export default function LoginPage() {
  const router = useRouter();
  const login = useAuthStore((state) => state.login);
  const [email, setEmail] = useState("admin@themoak.ir");
  const [password, setPassword] = useState("password");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login({ email, password });
      router.push("/dashboard");
    } catch (err) {
      setError("ورود ناموفق بود");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-brand-background px-6">
      <div className="card w-full max-w-md space-y-6 p-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-brand-primary">ورود به TheMoak ERP</h1>
          <p className="mt-2 text-sm text-slate-500">مدیریت فروشگاه عینک تموک</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-600">ایمیل</label>
            <input
              type="email"
              className="mt-1 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-right focus:border-brand-primary focus:outline-none"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-600">رمز عبور</label>
            <input
              type="password"
              className="mt-1 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-right focus:border-brand-primary focus:outline-none"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </div>
          {error && <p className="text-sm text-rose-500">{error}</p>}
          <button
            type="submit"
            className="w-full rounded-xl bg-brand-primary py-3 text-white shadow-lg transition hover:bg-indigo-700 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "در حال ورود..." : "ورود"}
          </button>
        </form>
      </div>
    </main>
  );
}
