import customtkinter as ctk


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Первое приложение")
        self.geometry("400x350")

        self.label_title = ctk.CTkLabel(self, text="Первое приложение", font=("Arial", 24))
        self.label_title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        self.label_login = ctk.CTkLabel(self, text="Введите логин", font=("Arial", 16))
        self.label_login.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.entry_login = ctk.CTkEntry(self)
        self.entry_login.grid(row=1, column=1, padx=20, pady=10)

        self.label_pass = ctk.CTkLabel(self, text="Введите пароль", font=("Arial", 16))
        self.label_pass.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.entry_pass = ctk.CTkEntry(self, show="*")
        self.entry_pass.grid(row=2, column=1, padx=20, pady=10)

        self.label_result = ctk.CTkLabel(self, text="", font=("Arial", 16))
        self.label_result.grid(row=3, column=0, columnspan=2, pady=10)

        self.btn_check = ctk.CTkButton(self, text="Войти", command=self.check_auth)
        self.btn_check.grid(row=4, column=0, columnspan=2, pady=20)

    def check_auth(self):
        if self.entry_login.get() == "admin" and self.entry_pass.get() == "123":
            self.label_result.configure(text="Успешный вход", text_color="green")
        else:
            self.label_result.configure(text="Неверные данные", text_color="red")


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()