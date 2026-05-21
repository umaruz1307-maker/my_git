import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Мой ежедневник")
        self.geometry("700x450")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.login_frame, text="Вход в систему", font=("Arial", 24)).pack(pady=40)
        self.entry_pass = ctk.CTkEntry(self.login_frame, placeholder_text="Введите пароль (123)", show="*")
        self.entry_pass.pack(pady=10)
        ctk.CTkButton(self.login_frame, text="Войти", command=self.login_event).pack(pady=20)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.menu_frame = ctk.CTkFrame(self.main_frame, width=150, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkButton(self.menu_frame, text="Задачи", command=self.show_tasks_page).pack(pady=10, padx=10)
        ctk.CTkButton(self.menu_frame, text="Добавить", command=self.show_add_page).pack(pady=10, padx=10)

        self.tasks_page = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.add_page = ctk.CTkFrame(self.main_frame, fg_color="transparent")

        ctk.CTkLabel(self.tasks_page, text="Список задач", font=("Arial", 20)).pack(pady=10)
        self.tasks_list_frame = ctk.CTkFrame(self.tasks_page, fg_color="transparent")
        self.tasks_list_frame.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(self.add_page, text="Добавить новую задачу", font=("Arial", 20)).pack(pady=10)
        self.task_entry = ctk.CTkEntry(self.add_page, placeholder_text="Текст задачи...", width=300)
        self.task_entry.pack(pady=10)
        ctk.CTkButton(self.add_page, text="Добавить", command=self.add_task).pack(pady=10)

        self.show_tasks_page()

    def show_tasks_page(self):
        self.add_page.grid_forget()
        self.tasks_page.grid(row=0, column=1, sticky="nsew")

    def show_add_page(self):
        self.tasks_page.grid_forget()
        self.add_page.grid(row=0, column=1, sticky="nsew")

    def add_task(self):
        text = self.task_entry.get()
        if text:
            new_task = ctk.CTkCheckBox(self.tasks_list_frame, text=text)
            new_task.pack(anchor="w", pady=5, padx=10)
            self.task_entry.delete(0, 'end')
            self.show_tasks_page()

    def login_event(self):
        if self.entry_pass.get() == "123":
            self.login_frame.grid_forget()
            self.main_frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()