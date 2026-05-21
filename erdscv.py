import customtkinter as ctk
import sqlite3


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Регистрация и БД")
        self.geometry("900x700")
        self.vidjets()
        self.polojenie()

    def vidjets(self):
        self.Frame1 = ctk.CTkFrame(self)
        self.Frame2 = ctk.CTkFrame(self)

        self.Frame2_1 = ctk.CTkFrame(self.Frame2, fg_color="transparent")
        self.Frame2_2 = ctk.CTkFrame(self.Frame2, fg_color="transparent")
        self.Frame2_3 = ctk.CTkFrame(self.Frame2, fg_color="transparent")

        self.Frame2_2_1 = ctk.CTkFrame(self.Frame2_2, fg_color="transparent")
        self.Frame2_2_2 = ctk.CTkFrame(self.Frame2_2, fg_color="transparent")

        self.Button = ctk.CTkButton(self.Frame1, text="Заполнить", command=self.button_frame1)
        self.Button2 = ctk.CTkButton(self.Frame1, text="Посмотреть", command=self.button_frame2)
        self.Button3 = ctk.CTkButton(self.Frame1, text="Удалить", command=self.button_frame3)

        self.Label1 = ctk.CTkLabel(self.Frame2_1, text="Впишите данные", font=("Arial", 24))
        self.Label_Name = ctk.CTkLabel(self.Frame2_1, text="Имя", font=("Arial", 18))
        self.Label_Fam = ctk.CTkLabel(self.Frame2_1, text="Фамилия", font=("Arial", 18))
        self.Label_Age = ctk.CTkLabel(self.Frame2_1, text="Возраст (14-35)", font=("Arial", 18))
        self.Label_City = ctk.CTkLabel(self.Frame2_1, text="Город", font=("Arial", 18))
        self.Label_Zan = ctk.CTkLabel(self.Frame2_1, text="Текущая занятость", font=("Arial", 18))

        self.Entry1 = ctk.CTkEntry(self.Frame2_1, width=200)
        self.Entry2 = ctk.CTkEntry(self.Frame2_1, width=200)
        self.Entry_Age = ctk.CTkEntry(self.Frame2_1, width=200)
        self.Entry_City = ctk.CTkEntry(self.Frame2_1, width=200)

        self.var_1 = ctk.IntVar(value=0)
        self.var_2 = ctk.IntVar(value=0)
        self.var_3 = ctk.IntVar(value=0)

        self.Variant1 = ctk.CTkCheckBox(self.Frame2_1, text="Работник", variable=self.var_1, onvalue=1, offvalue=0)
        self.Variant2 = ctk.CTkCheckBox(self.Frame2_1, text="Студент", variable=self.var_2, onvalue=1, offvalue=0)
        self.Variant3 = ctk.CTkCheckBox(self.Frame2_1, text="Школьник", variable=self.var_3, onvalue=1, offvalue=0)

        self.Button_Save = ctk.CTkButton(self.Frame2_1, text="Зарегистрировать", command=self.save_to_db)

        self.Label2 = ctk.CTkLabel(self.Frame2_2_1, text="Посмотрите данные", font=("Arial", 24))
        self.L_H1 = ctk.CTkLabel(self.Frame2_2_2, text="Номер", font=("Arial", 18))
        self.L_H2 = ctk.CTkLabel(self.Frame2_2_2, text="Имя", font=("Arial", 18))
        self.L_H3 = ctk.CTkLabel(self.Frame2_2_2, text="Фамилия", font=("Arial", 18))
        self.L_H4 = ctk.CTkLabel(self.Frame2_2_2, text="Занятость", font=("Arial", 18))

        self.Label3 = ctk.CTkLabel(self.Frame2_3, text="Удаление по ID", font=("Arial", 24))
        self.Entry_Delete = ctk.CTkEntry(self.Frame2_3, placeholder_text="Введите ID")
        self.Button_Del = ctk.CTkButton(self.Frame2_3, text="Удалить запись", fg_color="red",
                                        command=self.delete_from_db)

        self.Frame2_1.tkraise()

    def polojenie(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        self.Frame1.grid(row=0, column=0, sticky="ewns", padx=10, pady=10)
        self.Frame2.grid(row=0, column=1, sticky="ewns", padx=(0, 10), pady=10)

        self.Frame1.grid_rowconfigure(0, weight=1)
        self.Button.grid(row=1, column=1, pady=10, padx=20)
        self.Button2.grid(row=2, column=1, pady=10, padx=20)
        self.Button3.grid(row=3, column=1, pady=10, padx=20)
        self.Frame1.grid_rowconfigure(4, weight=1)

        self.Frame2_1.grid(row=0, column=0, sticky="ewns")
        self.Frame2_2.grid(row=0, column=0, sticky="ewns")
        self.Frame2_3.grid(row=0, column=0, sticky="ewns")

        self.Label1.grid(row=0, column=0, pady=30, padx=10, columnspan=3, sticky="w")
        self.Label_Name.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.Entry1.grid(row=1, column=1, pady=5)
        self.Label_Fam.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.Entry2.grid(row=2, column=1, pady=5)
        self.Label_Age.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.Entry_Age.grid(row=3, column=1, pady=5)
        self.Label_City.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.Entry_City.grid(row=4, column=1, pady=5)

        self.Label_Zan.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.Variant1.grid(row=5, column=1, sticky="w")
        self.Variant2.grid(row=5, column=2, sticky="w")
        self.Variant3.grid(row=6, column=1, sticky="w")

        self.Button_Save.grid(row=7, column=1, pady=30)

        self.Frame2_2_1.pack(side="top", pady=30, padx=10, anchor="w")
        self.Frame2_2_2.pack(side="top", anchor="w")
        self.Label2.grid(row=0, column=0, columnspan=4, sticky="w")
        self.L_H1.grid(row=1, column=0, pady=(20, 0), padx=20)
        self.L_H2.grid(row=1, column=1, pady=(20, 0), padx=20)
        self.L_H3.grid(row=1, column=2, pady=(20, 0), padx=20)
        self.L_H4.grid(row=1, column=3, pady=(20, 0), padx=20)

        self.Label3.pack(pady=20)
        self.Entry_Delete.pack(pady=10)
        self.Button_Del.pack(pady=10)

    def button_frame1(self):
        self.Frame2_1.tkraise()

    def button_frame2(self):
        self.Frame2_2.tkraise()
        self.show_db_data()

    def button_frame3(self):
        self.Frame2_3.tkraise()

    def save_to_db(self):
        name = self.Entry1.get()
        lastname = self.Entry2.get()
        age = self.Entry_Age.get()
        city = self.Entry_City.get()

        if not name or not lastname or not age or not city:
            return

        try:
            age_int = int(age)
            if not (14 <= age_int <= 35):
                return
        except ValueError:
            return

        zanatost = ""
        if self.var_1.get() == 1: zanatost += "Работник "
        if self.var_2.get() == 1: zanatost += "Студент "
        if self.var_3.get() == 1: zanatost += "Школьник "

        con = sqlite3.connect('test.db')
        cur = con.cursor()
        cur.execute('''create table if not exists users (
                    id integer primary key autoincrement,
                    Name text, LastName text, Zanatost text, Age integer, City text)''')

        with con:
            con.execute('insert into users (Name, LastName, Zanatost, Age, City) values (?, ?, ?, ?, ?)',
                        (name, lastname, zanatost, age_int, city))

        self.Entry1.delete(0, 'end')
        self.Entry2.delete(0, 'end')
        self.Entry_Age.delete(0, 'end')
        self.Entry_City.delete(0, 'end')

    def show_db_data(self):
        for widget in self.Frame2_2_2.winfo_children():
            if widget not in [self.L_H1, self.L_H2, self.L_H3, self.L_H4]:
                widget.destroy()

        con = sqlite3.connect('test.db')
        cur = con.cursor()
        try:
            result = cur.execute("select id, Name, LastName, Zanatost from users").fetchall()

            mass = [(ctk.CTkLabel(self.Frame2_2_2, text=str(row[0]), font=("Arial", 16)),
                     ctk.CTkLabel(self.Frame2_2_2, text=str(row[1]), font=("Arial", 16)),
                     ctk.CTkLabel(self.Frame2_2_2, text=str(row[2]), font=("Arial", 16)),
                     ctk.CTkLabel(self.Frame2_2_2, text=str(row[3]), font=("Arial", 16))) for row in result]

            row_idx = 2
            for i in mass:
                i[0].grid(row=row_idx, column=0, padx=20, pady=5)
                i[1].grid(row=row_idx, column=1, padx=20, pady=5)
                i[2].grid(row=row_idx, column=2, padx=20, pady=5)
                i[3].grid(row=row_idx, column=3, padx=20, pady=5)
                row_idx += 1
        except sqlite3.OperationalError:
            pass

    def delete_from_db(self):
        user_id = self.Entry_Delete.get()
        if not user_id: return

        con = sqlite3.connect('test.db')
        cur = con.cursor()
        with con:
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.Entry_Delete.delete(0, 'end')


app = App()
app.mainloop()