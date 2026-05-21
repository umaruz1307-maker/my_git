import tkinter as tk


def calculate():
    lbl_result.config(text="", fg="black")

    try:
        s_price = ent_price.get().strip()
        s_qty = ent_qty.get().strip()
        s_discount = ent_discount.get().strip()

        if not s_price or not s_qty or not s_discount:
            raise ValueError("Пустые поля ввода")

        try:
            price = float(s_price)
            quantity = int(s_qty)
            discount = float(s_discount)
        except ValueError:
            raise ValueError("Некорректный формат числа")

        if price <= 0 or quantity <= 0:
            raise ValueError("Цена и количество должны быть > 0")

        if not (0 <= discount <= 100):
            raise ValueError("Недопустимый процент скидки")

        total = price * quantity * (1 - discount / 100)
        lbl_result.config(text=f"Итого: {total:.2f} руб.", fg="green")

    except ValueError as e:
        lbl_result.config(text=str(e), fg="red")


def clear():
    ent_price.delete(0, tk.END)
    ent_qty.delete(0, tk.END)
    ent_discount.delete(0, tk.END)
    lbl_result.config(text="", fg="black")


root = tk.Tk()
root.title("Калькулятор стоимости")
root.geometry("300x250")

tk.Label(root, text="Цена:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
ent_price = tk.Entry(root)
ent_price.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Количество:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
ent_qty = tk.Entry(root)
ent_qty.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Скидка (%):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
ent_discount = tk.Entry(root)
ent_discount.grid(row=2, column=1, padx=10, pady=5)

btn_calc = tk.Button(root, text="Рассчитать", command=calculate)
btn_calc.grid(row=3, column=0, columnspan=2, sticky="we", padx=10, pady=5)

btn_clear = tk.Button(root, text="Очистить", command=clear)
btn_clear.grid(row=4, column=0, columnspan=2, sticky="we", padx=10, pady=5)

lbl_result = tk.Label(root, text="", font=("Arial", 10, "bold"), wraplength=250)
lbl_result.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()