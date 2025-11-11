"use client";

import { useMemo } from "react";
import { Menu, User } from "lucide-react";
import dayjs from "dayjs";
import jalaliday from "jalaliday";
import { useAuthStore } from "@/store/auth";

dayjs.extend(jalaliday);

dayjs.calendar("jalali");

export default function Topbar() {
  const user = useAuthStore((state) => state.user);
  const today = useMemo(() => dayjs().calendar("jalali").locale("fa").format("YYYY/MM/DD"), []);

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
      <button className="flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-slate-600 lg:hidden">
        <Menu className="h-5 w-5" />
        <span>منو</span>
      </button>
      <div className="hidden text-sm text-slate-500 lg:block">تاریخ امروز: {today}</div>
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-brand-primary/10 text-brand-primary">
          <User className="h-5 w-5" />
        </div>
        <div className="text-right">
          <p className="text-sm font-semibold text-slate-700">{user?.fullName ?? "کاربر مهمان"}</p>
          <p className="text-xs text-slate-400">مدیر سیستم</p>
        </div>
      </div>
    </header>
  );
}
