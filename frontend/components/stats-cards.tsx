import { CreditCard, Package, TrendingUp } from "lucide-react";

const cards = [
  {
    title: "فروش امروز",
    value: "۶۵,۰۰۰,۰۰۰ ریال",
    icon: TrendingUp,
    description: "۱۵٪ رشد نسبت به دیروز"
  },
  {
    title: "سفارشات معوق",
    value: "۱۲",
    icon: Package,
    description: "نیاز به پیگیری"
  },
  {
    title: "دریافتی ها",
    value: "۳۲,۰۰۰,۰۰۰ ریال",
    icon: CreditCard,
    description: "پرداخت کارت"
  }
];

export default function StatsCards() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <div key={card.title} className="card flex items-center justify-between p-6">
            <div>
              <p className="text-sm text-slate-500">{card.title}</p>
              <p className="mt-2 text-2xl font-bold text-slate-800">{card.value}</p>
              <p className="text-xs text-brand-primary/80">{card.description}</p>
            </div>
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-brand-primary/10 text-brand-primary">
              <Icon className="h-6 w-6" />
            </div>
          </div>
        );
      })}
    </div>
  );
}
