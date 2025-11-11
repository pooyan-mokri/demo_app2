import { Receipt } from "lucide-react";

const sales = [
  { id: "SO-140401", customer: "علی موحد", total: "۶,۶۰۰,۰۰۰ ریال", method: "کارت" },
  { id: "SO-140402", customer: "نرگس رحیمی", total: "۴,۲۰۰,۰۰۰ ریال", method: "نقد" },
  { id: "SO-140403", customer: "سارا حیدری", total: "۷,۸۰۰,۰۰۰ ریال", method: "انتقال" }
];

export default function RecentSales() {
  return (
    <div className="card p-6">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-700">آخرین فاکتورها</h2>
        <Receipt className="h-5 w-5 text-brand-primary" />
      </div>
      <div className="mt-4 space-y-3">
        {sales.map((sale) => (
          <div key={sale.id} className="flex items-center justify-between rounded-xl border border-slate-100 px-4 py-3">
            <div>
              <p className="text-sm font-semibold text-slate-700">{sale.customer}</p>
              <p className="text-xs text-slate-400">{sale.id}</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-bold text-brand-primary">{sale.total}</p>
              <p className="text-xs text-slate-400">روش پرداخت: {sale.method}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
