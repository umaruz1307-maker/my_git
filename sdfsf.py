import customtkinter as ctk
from CTkTable import *
from faker import Faker

fake = Faker('ru_RU')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Задание 2 и 3")
        self.geometry("900x600")

        self.headers = ["ФИО", "Фамилия", "Телефон"]
        self.table_data = [self.headers]
        for _ in range(5):
            self.table_data.append([fake.name(), fake.last_name(), fake.phone_number()])

        self.table = CTkTable(master=self, values=self.table_data)
        self.table.pack(expand=True, fill="both", padx=20, pady=20)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        ctk.CTkButton(self.btn_frame, text="+ Строка", command=self.add_row).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(self.btn_frame, text="- Строка", command=self.delete_row, fg_color="#911a1a").grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(self.btn_frame, text="+ Столбец", command=self.add_column).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkButton(self.btn_frame, text="- Столбец", command=self.delete_column, fg_color="#911a1a").grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkButton(self, text="Заполнить пустые ячейки", command=self.fill_empty_cells, fg_color="#27ae60").pack(pady=10)

    def add_row(self):
        new_row = [fake.name(), fake.last_name(), fake.phone_number()]
        while len(new_row) < self.table.columns:
            new_row.append("")
        self.table.add_row(values=new_row)

    def delete_row(self):
        if self.table.rows > 1:
            self.table.delete_row(self.table.rows - 1)

    def add_column(self):
        col_name = "Работа" if self.table.columns % 2 != 0 else "Дата рег."
        column_values = [col_name] + [""] * (self.table.rows - 1)
        self.table.add_column(values=column_values)

    def delete_column(self):
        if self.table.columns > 1:
            self.table.delete_column(self.table.columns - 1)

    def fill_empty_cells(self):
        for r in range(1, self.table.rows):
            for c in range(self.table.columns):
                cell_value = self.table.get(r, c)
                if cell_value == "" or cell_value is None or cell_value == " ":
                    header_text = self.table.get(0, c)
                    if "Работа" in str(header_text):
                        self.table.insert(r, c, fake.job())
                    elif "Дата" in str(header_text):
                        self.table.insert(r, c, fake.date())

if __name__ == "__main__":
    app = App()
    app.mainloop()
