"use client";

import { useState } from "react";
import { useForm, useFieldArray } from "react-hook-form";
import { authenticatedFetch } from "@/store/auth";

interface SalesFormValues {
  order_number: string;
  customer_id?: number;
  warehouse_id: number;
  discount_total: number;
  shipping_cost: number;
  lines: Array<{ product_id: number; quantity: number; unit_price: number; discount_line: number }>;
  payments: Array<{ method: string; amount: number }>;
}

const defaultLine = { product_id: 0, quantity: 1, unit_price: 0, discount_line: 0 };
const defaultPayment = { method: "CARD", amount: 0 };

export default function SalesForm() {
  const [message, setMessage] = useState<string | null>(null);
  const { register, handleSubmit, control, reset } = useForm<SalesFormValues>({
    defaultValues: {
      order_number: "SO-" + new Date().getTime(),
      warehouse_id: 1,
      discount_total: 0,
      shipping_cost: 0,
      lines: [defaultLine],
      payments: [defaultPayment]
    }
  });

  const linesField = useFieldArray({ control, name: "lines" });
  const paymentField = useFieldArray({ control, name: "payments" });

  const onSubmit = handleSubmit(async (values) => {
    setMessage(null);
    try {
      await authenticatedFetch("/sales", {
        method: "POST",
        body: JSON.stringify({
          ...values,
          lines: values.lines.map((line) => ({ ...line, product_id: Number(line.product_id) })),
          payments: values.payments.map((payment) => ({ ...payment, amount: Number(payment.amount) }))
        })
      });
      setMessage("فاکتور با موفقیت ثبت شد");
      reset({
        order_number: "SO-" + new Date().getTime(),
        warehouse_id: 1,
        discount_total: 0,
        shipping_cost: 0,
        lines: [{ ...defaultLine }],
        payments: [{ ...defaultPayment }]
      });
    } catch (error) {
      setMessage("خطا در ثبت فاکتور");
    }
  });

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label className="text-sm text-slate-500">شماره فاکتور</label>
          <input className="input" {...register("order_number", { required: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">کد انبار</label>
          <input type="number" className="input" {...register("warehouse_id", { valueAsNumber: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">تخفیف کلی</label>
          <input type="number" className="input" {...register("discount_total", { valueAsNumber: true })} />
        </div>
        <div>
          <label className="text-sm text-slate-500">هزینه ارسال</label>
          <input type="number" className="input" {...register("shipping_cost", { valueAsNumber: true })} />
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-700">اقلام فاکتور</h3>
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
                placeholder="قیمت واحد"
                className="input"
                {...register(`lines.${index}.unit_price` as const, { valueAsNumber: true })}
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

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-700">پرداخت ها</h3>
          <button
            type="button"
            className="rounded-xl border border-brand-primary px-3 py-2 text-sm text-brand-primary"
            onClick={() => paymentField.append({ ...defaultPayment })}
          >
            افزودن پرداخت
          </button>
        </div>
        <div className="space-y-3">
          {paymentField.fields.map((field, index) => (
            <div key={field.id} className="grid gap-3 rounded-xl border border-slate-200 p-4 md:grid-cols-2">
              <input
                className="input"
                placeholder="روش پرداخت"
                {...register(`payments.${index}.method` as const)}
              />
              <input
                type="number"
                className="input"
                placeholder="مبلغ"
                {...register(`payments.${index}.amount` as const, { valueAsNumber: true })}
              />
            </div>
          ))}
        </div>
      </div>

      <button type="submit" className="rounded-xl bg-brand-primary px-6 py-3 text-white shadow">ذخیره فاکتور</button>
      {message && <p className="text-sm text-brand-primary">{message}</p>}
    </form>
  );
}
