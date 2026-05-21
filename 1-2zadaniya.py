import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Первое приложение")
        self.geometry("400x300")

        self.count = 15

        self.label_title = ctk.CTkLabel(self, text="Первое приложение", font=("Arial", 24))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.btn_plus = ctk.CTkButton(self, text="+", command=self.increase)
        self.btn_plus.grid(row=1, column=0, padx=20, pady=10)

        self.label_count = ctk.CTkLabel(self, text=str(self.count), font=("Arial", 20))
        self.label_count.grid(row=1, column=1, rowspan=2, padx=20)

        self.btn_minus = ctk.CTkButton(self, text="-", command=self.decrease)
        self.btn_minus.grid(row=2, column=0, padx=20, pady=10)

        self.label_limit = ctk.CTkLabel(self, text="Это предел", font=("Arial", 18))

    def increase(self):
        if self.count < 20:
            self.count += 1
            self.label_count.configure(text=str(self.count))

        if self.count == 20:
            self.btn_plus.grid_forget()
            self.label_limit.grid(row=3, column=1, padx=20, pady=10)

    def decrease(self):
        if self.count > 0:
            self.count -= 1
            self.label_count.configure(text=str(self.count))

        if self.count < 20:
            self.btn_plus.grid(row=1, column=0, padx=20, pady=10)
            self.label_limit.grid_forget()


if __name__ == "__main__":
    app = App()
    app.mainloop()