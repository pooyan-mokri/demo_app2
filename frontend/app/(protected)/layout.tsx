"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "@/components/sidebar";
import Topbar from "@/components/topbar";
import { useAuthStore } from "@/store/auth";

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const tokens = useAuthStore((state) => state.tokens);

  useEffect(() => {
    if (!tokens) {
      router.replace("/login");
    }
  }, [tokens, router]);

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex flex-1 flex-col">
        <Topbar />
        <main className="flex-1 bg-brand-background p-6">
          <div className="card p-6">{children}</div>
        </main>
      </div>
    </div>
  );
}
