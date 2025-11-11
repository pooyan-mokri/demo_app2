"use client";

import { useState } from "react";
import { useForm, useFieldArray } from "react-hook-form";
import { authenticatedFetch } from "@/store/auth";

interface PurchaseFormValues {
  reference: string;
  supplier_id: number;
  warehouse_id: number;
  freight_cost: number;
  customs_cost: number;
  insurance_cost: number;
  other_cost: number;
  lines: Array<{ product_id: number; quantity: number; unit_cost: number; discount_line: number }>;
}

const defaultLine = { product_id: 0, quantity: 1, unit_cost: 0, discount_line: 0 };

export default function PurchaseForm() {
  const [message, setMessage] = useState<string | null>(null);
  const { register, handleSubmit, control, reset } = useForm<PurchaseFormValues>({
    defaultValues: {
      reference: "PO-" + new Date().getTime(),
      supplier_id: 1,
      warehouse_id: 1,
      freight_cost: 0,
      customs_cost: 0,
      insurance_cost: 0,
      other_cost: 0,
      lines: [defaultLine]
    }
  });
  const linesField = useFieldArray({ control, name: "lines" });

  const onSubmit = handleSubmit(async (values) => {
    setMessage(null);
    try {
      await authenticatedFetch("/purchases", {
        method: "POST",
        body: JSON.stringify({
          ...values,
          lines: values.lines.map((line) => ({
            ...line,
            product_id: Number(line.product_id)
          }))
        })
      });
      setMessage("خرید ثبت شد");
      reset({
        reference: "PO-" + new Date().getTime(),
        supplier_id: 1,
        warehouse_id: 1,
        freight_cost: 0,
        customs_cost: 0,
        insurance_cost: 0,
        other_cost: 0,
        lines: [{ ...defaultLine }]
      });
    } catch (error) {
      setMessage("خطا در ثبت خرید");
    }
  });

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="grid gap-4 md:grid-cols-3">
        <div>
          <label className="text-sm text-slate-500">شماره خرید</label>
          <input className="input" {...register("reference", { required: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">تأمین کننده</label>
          <input type="number" className="input" {...register("supplier_id", { valueAsNumber: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">انبار</label>
          <input type="number" className="input" {...register("warehouse_id", { valueAsNumber: true })} />
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <div>
          <label className="text-sm text-slate-500">حمل</label>
          <input type="number" className="input" {...register("freight_cost", { valueAsNumber: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">گمرک</label>
          <input type="number" className="input" {...register("customs_cost", { valueAsNumber: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">بیمه</label>
          <input type="number" className="input" {...register("insurance_cost", { valueAsNumber: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">سایر</label>
          <input type="number" className="input" {...register("other_cost", { valueAsNumber: true })} />
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-700">اقلام خرید</h3>
          <button
            type="button"
            className="rounded-xl border border-brand-primary px-3 py-2 text-sm text-brand-primary"
            onClick={() => linesField.append({ ...defaultLine })}
          >
            افزودن کالا
          </button>
        </div>
        <div className="space-y-3">
          {linesField.fields.map((field, index) => (
            <div key={field.id} className="grid gap-3 rounded-xl border border-slate-200 p-4 md:grid-cols-4">
              <input
                type="number"
                placeholder="کد کالا"
                className="input"
                {...register(`lines.${index}.product_id` as const, { valueAsNumber: true })}
              />
              <input
                type="number"
                placeholder="تعداد"
                className="input"
                {...register(`lines.${index}.quantity` as const, { valueAsNumber: true })}
              />
              <input
                type="number"
                placeholder="قیمت"
                className="input"
                {...register(`lines.${index}.unit_cost` as const, { valueAsNumber: true })}
              />
              <input
                type="number"
                placeholder="تخفیف"
                className="input"
                {...register(`lines.${index}.discount_line` as const, { valueAsNumber: true })}
              />
            </div>
          ))}
        </div>
      </div>

      <button type="submit" className="rounded-xl bg-brand-primary px-6 py-3 text-white shadow">ذخیره خرید</button>
      {message && <p className="text-sm text-brand-primary">{message}</p>}
    </form>
  );
}
