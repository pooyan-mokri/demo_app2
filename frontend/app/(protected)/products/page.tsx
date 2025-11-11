import ProductsTable from "@/components/products-table";

export default function ProductsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-brand-primary">محصولات</h1>
      </div>
      <ProductsTable />
    </div>
  );
}
