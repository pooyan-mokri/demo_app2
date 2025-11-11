import PurchaseForm from "@/components/purchase-form";

export default function PurchasesPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-brand-primary">ثبت خرید</h1>
      <PurchaseForm />
    </div>
  );
}
