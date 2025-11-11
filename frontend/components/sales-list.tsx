"use client";

import { useQuery } from "@tanstack/react-query";
import { authenticatedFetch } from "@/store/auth";

interface SalesOrder {
  id: number;
  order_number: string;
  total_amount: number;
  currency_code: string;
  order_date: string;
}

async function fetchSales(): Promise<SalesOrder[]> {
  return authenticatedFetch<SalesOrder[]>("/sales");
}

export default function SalesList() {
  const { data, isLoading, error } = useQuery({ queryKey: ["sales"], queryFn: fetchSales });

  if (isLoading) {
    return <p>در حال دریافت فاکتورها...</p>;
  }

  if (error) {
    return <p className="text-rose-500">خطا در دریافت اطلاعات</p>;
  }

  return (
    <div className="space-y-3">
      {data?.map((order) => (
        <div key={order.id} className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3">
          <div>
            <p className="text-sm font-semibold text-slate-700">{order.order_number}</p>
            <p className="text-xs text-slate-400">{new Date(order.order_date).toLocaleDateString("fa-IR")}</p>
          </div>
          <p className="text-sm font-bold text-brand-primary">
            {order.total_amount.toLocaleString("fa-IR")} {order.currency_code}
          </p>
        </div>
      ))}
    </div>
  );
}
