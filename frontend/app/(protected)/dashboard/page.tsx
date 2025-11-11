import StatsCards from "@/components/stats-cards";
import RecentSales from "@/components/recent-sales";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-brand-primary">داشبورد فروش</h1>
      <StatsCards />
      <RecentSales />
    </div>
  );
}
