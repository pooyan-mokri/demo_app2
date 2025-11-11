import type { Metadata } from "next";
import "./globals.css";
import { Vazirmatn } from "next/font/google";
import { AppProviders } from "./providers";

const vazir = Vazirmatn({ subsets: ["arabic"], variable: "--font-vazirmatn" });

export const metadata: Metadata = {
  title: "TheMoak ERP",
  description: "سامانه مدیریت فروش و انبار عینک تموک"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fa" dir="rtl" className={vazir.variable}>
      <body className="min-h-screen bg-brand-background">
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
