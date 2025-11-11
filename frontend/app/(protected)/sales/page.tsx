import SalesForm from "@/components/sales-form";
import SalesList from "@/components/sales-list";

export default function SalesPage() {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="space-y-4">
        <h1 className="text-2xl font-bold text-brand-primary">ثبت فاکتور فروش</h1>
        <SalesForm />
      </div>
      <div className="space-y-4">
        <h2 className="text-xl font-semibold text-slate-700">آخرین فاکتورها</h2>
        <SalesList />
      </div>
    </div>
  );
}
