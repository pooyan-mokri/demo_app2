"use client";

import { useQuery } from "@tanstack/react-query";
import { authenticatedFetch } from "@/store/auth";

interface Product {
  id: number;
  sku: string;
  name: string;
  brand?: string | null;
  category?: { name?: string | null };
}

export interface ProductRow extends Product {
  categoryName?: string | null;
}

export function useProducts() {
  return useQuery<ProductRow[]>({
    queryKey: ["products"],
    queryFn: async () => {
      const data = await authenticatedFetch<Product[]>("/products");
      return data.map((item) => ({
        ...item,
        categoryName: item.category?.name ?? null
      }));
    }
  });
}
