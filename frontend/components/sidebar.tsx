"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Package, ShoppingCart, Receipt, Warehouse } from "lucide-react";

const links = [
  { href: "/dashboard", label: "داشبورد", icon: Home },
  { href: "/products", label: "محصولات", icon: Package },
  { href: "/sales", label: "فروش", icon: ShoppingCart },
  { href: "/purchases", label: "خرید", icon: Receipt },
  { href: "/warehouses", label: "انبار", icon: Warehouse }
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-72 flex-col border-l border-slate-200 bg-white p-6 shadow-sm lg:flex">
      <div className="mb-8">
        <p className="text-lg font-bold text-brand-primary">TheMoak ERP</p>
        <p className="text-sm text-slate-500">ابر مدیریت فروش تموک</p>
      </div>
      <nav className="flex flex-1 flex-col gap-2">
        {links.map((link) => {
          const Icon = link.icon;
          const active = pathname === link.href;
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                active
                  ? "bg-brand-primary/10 text-brand-primary"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <Icon className="h-5 w-5" />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
