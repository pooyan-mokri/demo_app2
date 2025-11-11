"use client";

import { useEffect } from "react";
import { useProducts } from "@/hooks/use-products";

export default function ProductsTable() {
  const { data, isLoading, error, refetch } = useProducts();

  useEffect(() => {
    refetch();
  }, [refetch]);

  if (isLoading) {
    return <p>در حال بارگذاری...</p>;
  }

  if (error) {
    return <p className="text-rose-500">مشکل در دریافت محصولات</p>;
  }

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr className="text-right text-sm text-slate-500">
            <th className="px-4 py-3">کد</th>
            <th className="px-4 py-3">نام کالا</th>
            <th className="px-4 py-3">برند</th>
            <th className="px-4 py-3">دسته بندی</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 bg-white text-sm">
          {data?.map((product) => (
            <tr key={product.id}>
              <td className="px-4 py-3 font-semibold text-slate-600">{product.sku}</td>
              <td className="px-4 py-3">{product.name}</td>
              <td className="px-4 py-3">{product.brand ?? "-"}</td>
              <td className="px-4 py-3">{product.categoryName ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
