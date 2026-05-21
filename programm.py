import customtkinter as ctk
import json
import os
import shutil
from PIL import Image
import tkinter.messagebox as mb
import tkinter.filedialog as fd

# Настройка внешнего вида
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Файлы данных
USERS_FILE = "users.json"
ITEMS_FILE = "items.json"
IMAGES_DIR = "images"

# Создание папки для изображений, если её нет
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# --- Работа с данными ---
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Создаём администратора по умолчанию
        default = {
            "admin": {
                "password": "123",
                "role": "admin",
                "balance": 1000,
                "is_blocked": False,
                "block_reason": ""
            }
        }
        save_users(default)
        return default

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def load_items():
    if os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        default = []
        save_items(default)
        return default

def save_items(items):
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=4, ensure_ascii=False)

# --- Главное окно авторизации ---
class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Авторизация")
        self.geometry("400x350")
        self.resizable(False, False)

        self.users = load_users()

        # Заголовок
        self.label = ctk.CTkLabel(self, text="Вход в магазин", font=("Arial", 20))
        self.label.pack(pady=20)

        # Поле логина
        self.entry_login = ctk.CTkEntry(self, placeholder_text="Логин", width=250)
        self.entry_login.pack(pady=5)

        # Поле пароля
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Пароль", show="*", width=250)
        self.entry_password.pack(pady=5)

        # Поле подтверждения пароля (для регистрации)
        self.entry_confirm = ctk.CTkEntry(self, placeholder_text="Подтвердите пароль", show="*", width=250)
        # self.entry_confirm.pack(pady=5)

        # Кнопка входа
        self.btn_login = ctk.CTkButton(self, text="Войти", command=self.login)
        self.btn_login.pack(pady=10)

        # Кнопка регистрации
        self.btn_register = ctk.CTkButton(self, text="Регистрация", command=self.register_demo)
        self.btn_register.pack(pady=5)

    def login(self):
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()
        if not login or not password:
            mb.showerror("Ошибка", "Заполните все поля")
            return

        user = self.users.get(login)
        if not user:
            mb.showerror("Ошибка", "Пользователь не найден")
            return

        if user.get("is_blocked", False):
            reason = user.get("block_reason", "Причина не указана")
            mb.showerror("Доступ заблокирован", f"Ваш аккаунт заблокирован.\nПричина: {reason}")
            return

        if user["password"] != password:
            mb.showerror("Ошибка", "Неверный пароль")
            return

        # Успешный вход
        self.destroy()
        shop = ShopWindow(login, self.users[login])
        shop.mainloop()

    def register_demo(self):
        self.label.configure(text="Регистрация")
        self.entry_confirm.pack(pady=5)
        self.btn_login.pack_forget()
        self.btn_register.pack_forget()
        self.btn_register.pack(pady=5)
        self.btn_register.configure(command=self.register)

    def register(self):
        login = self.entry_login.get().strip()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()

        errors = []

        # 1. Логин не должен быть пустым (базовая проверка)
        if not login:
            errors.append("Логин не может быть пустым")

        # 2. Логин должен быть не менее 3 символов
        if len(login) < 3:
            errors.append("Логин должен содержать не менее 3 символов")

        # 3. Логин должен начинаться с большой буквы
        if login and (not login[0].isalpha() or not login[0].isupper()):
            errors.append("Логин должен начинаться с заглавной буквы")

        # 4. Логин должен содержать только буквы и цифры
        if login and not login.isalnum():
            errors.append("Логин может содержать только буквы и цифры")

        # 5. Проверка уникальности логина
        if login in self.users:
            errors.append("Пользователь с таким логином уже существует")

        # 6. Пароль не должен быть пустым
        if not password:
            errors.append("Пароль не может быть пустым")

        # 7. Пароль и подтверждение должны совпадать
        if password != confirm:
            errors.append("Пароли не совпадают")

        # 8. Длина пароля не менее 8 символов
        if len(password) < 8:
            errors.append("Пароль должен содержать не менее 8 символов")

        # 9. Пароль должен начинаться с большой буквы
        if password and (not password[0].isalpha() or not password[0].isupper()):
            errors.append("Пароль должен начинаться с заглавной буквы")

        # 10. Пароль не должен содержать пробелы
        if ' ' in password:
            errors.append("Пароль не должен содержать пробелов")

        # 11. Пароль не должен совпадать с логином
        if password == login:
            errors.append("Пароль не должен совпадать с логином")

        # 12. В пароле должны быть буквы, цифры и хотя бы один спецсимвол из набора ! _ ? / < > = - +
        allowed_symbols = set("!_?/<>=-+")
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in allowed_symbols for c in password)

        if not (has_letter and has_digit and has_symbol):
            errors.append(
                "Пароль должен содержать буквы, цифры и хотя бы один специальный символ из набора: ! _ ? / < > = - +"
            )

        # Если есть ошибки — показываем их и прерываем регистрацию
        if errors:
            error_message = "При регистрации возникли ошибки:\n\n" + "\n".join(f"• {err}" for err in errors)
            mb.showerror("Ошибка регистрации", error_message)
            return

        # Все проверки пройдены — создаём пользователя
        self.users[login] = {
            "password": password,
            "role": "user",
            "balance": 0,
            "is_blocked": False,
            "block_reason": ""
        }
        save_users(self.users)
        mb.showinfo("Успех", "Регистрация прошла успешно! Теперь войдите.")
        self.entry_login.delete(0, "end")
        self.entry_password.delete(0, "end")
        self.entry_confirm.delete(0, "end")

        self.label.configure(text="Вход в магазин")
        self.entry_confirm.pack_forget()
        self.btn_register.pack_forget()
        self.btn_login.pack(pady=5)
        self.btn_register.pack(pady=5)
        self.btn_register.configure(command=self.register_demo)

# --- Окно магазина ---
class ShopWindow(ctk.CTk):
    def __init__(self, username, user_data):
        super().__init__()
        self.username = username
        self.user_data = user_data
        self.title(f"Магазин - {username}")
        self.geometry("900x600")

        # Корзина: {id товара: количество}
        self.cart = {}

        # Загружаем товары
        self.items = load_items()
        self.filtered_items = self.items.copy()

        # Интерфейс
        self.create_widgets()
        self.update_balance()
        self.refresh_items()

    def create_widgets(self):
        # Верхняя панель с балансом и кнопками
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.balance_label = ctk.CTkLabel(top_frame, text=f"Баланс: {self.user_data['balance']} руб.", font=("Arial", 14))
        self.balance_label.pack(side="left", padx=10)

        self.btn_add_balance = ctk.CTkButton(top_frame, text="Пополнить баланс", command=self.add_balance)
        self.btn_add_balance.pack(side="left", padx=5)

        self.btn_cart = ctk.CTkButton(top_frame, text="Корзина", command=self.open_cart)
        self.btn_cart.pack(side="left", padx=5)

        if self.user_data["role"] == "admin":
            self.btn_admin = ctk.CTkButton(top_frame, text="Админка", command=self.open_admin)
            self.btn_admin.pack(side="left", padx=5)

        # Фильтры
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(filter_frame, text="Фильтр 1:").grid(row=0, column=0, padx=5)
        self.filter1 = ctk.CTkComboBox(filter_frame, values=["Все", "Электроника", "Одежда", "Книги"], command=self.apply_filters)
        self.filter1.grid(row=0, column=1, padx=5)
        self.filter1.set("Все")

        ctk.CTkLabel(filter_frame, text="Фильтр 2:").grid(row=0, column=2, padx=5)
        self.filter2 = ctk.CTkComboBox(filter_frame, values=["Все", "Apple", "Samsung", "Xiaomi"], command=self.apply_filters)
        self.filter2.grid(row=0, column=3, padx=5)
        self.filter2.set("Все")

        ctk.CTkLabel(filter_frame, text="Фильтр 3:").grid(row=0, column=4, padx=5)
        self.filter3 = ctk.CTkComboBox(filter_frame, values=["Все", "Красный", "Синий", "Зелёный"], command=self.apply_filters)
        self.filter3.grid(row=0, column=5, padx=5)
        self.filter3.set("Все")

        # Область прокрутки для товаров
        self.items_frame = ctk.CTkScrollableFrame(self)
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def apply_filters(self, *args):
        f1 = self.filter1.get()
        f2 = self.filter2.get()
        f3 = self.filter3.get()

        self.filtered_items = []
        for item in self.items:
            tags = item.get("hashtags", [])
            match = True
            if f1 != "Все" and f1 not in tags:
                match = False
            if f2 != "Все" and f2 not in tags:
                match = False
            if f3 != "Все" and f3 not in tags:
                match = False
            if match:
                self.filtered_items.append(item)
        self.refresh_items()

    def refresh_items(self):
        # Очистить предыдущие виджеты
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        if not self.filtered_items:
            lbl = ctk.CTkLabel(self.items_frame, text="Нет товаров", font=("Arial", 16))
            lbl.pack(pady=20)
            return

        for item in self.filtered_items:
            self.create_item_card(item)

    def create_item_card(self, item):
        card = ctk.CTkFrame(self.items_frame)
        card.pack(fill="x", pady=5, padx=5)

        # Информация о товаре
        info_frame = ctk.CTkFrame(card)
        info_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(info_frame, text=item["name"], font=("Arial", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Цена: {item['price']} руб.").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"Теги: {', '.join(item.get('hashtags', []))}").pack(anchor="w")

        # Кнопки
        btn_frame = ctk.CTkFrame(card)
        btn_frame.pack(side="right", padx=5)

        ctk.CTkButton(btn_frame, text="Просмотр", command=lambda i=item: self.view_item(i)).pack(pady=2)

        item_id = item["id"]
        if item_id in self.cart:
            ctk.CTkButton(btn_frame, text="Убрать из корзины", command=lambda i=item: self.remove_from_cart(i)).pack(pady=2)
        else:
            ctk.CTkButton(btn_frame, text="В корзину", command=lambda i=item: self.add_to_cart(i)).pack(pady=2)

    def add_to_cart(self, item):
        item_id = item["id"]
        if item_id in self.cart:
            self.cart[item_id] += 1
        else:
            self.cart[item_id] = 1
        self.refresh_items()  # обновим кнопки
        mb.showinfo("Корзина", f"Товар '{item['name']}' добавлен в корзину")

    def remove_from_cart(self, item):
        item_id = item["id"]
        if item_id in self.cart:
            del self.cart[item_id]
            self.refresh_items()
            mb.showinfo("Корзина", f"Товар '{item['name']}' убран из корзины")

    def view_item(self, item):
        ViewItemWindow(self, item)

    def open_cart(self):
        CartWindow(self)

    def open_admin(self):
        AdminWindow(self)

    def add_balance(self):
        AddBalanceWindow(self)

    def update_balance(self):
        # Обновить баланс из файла (на случай изменений из другого окна)
        users = load_users()
        self.user_data = users[self.username]
        self.balance_label.configure(text=f"Баланс: {self.user_data['balance']} руб.")

    def save_user_data(self):
        users = load_users()
        users[self.username] = self.user_data
        save_users(users)

# --- Окно просмотра товара ---
class ViewItemWindow(ctk.CTkToplevel):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.parent = parent
        self.item = item
        self.title(item["name"])
        self.geometry("400x500")
        self.resizable(False, False)

        # Изображение
        img_path = item.get("image", "")
        if img_path and os.path.exists(img_path):
            img = ctk.CTkImage(light_image=Image.open(img_path), size=(200, 200))
            lbl_img = ctk.CTkLabel(self, image=img, text="")
            lbl_img.pack(pady=10)
        else:
            ctk.CTkLabel(self, text="Нет изображения").pack(pady=10)

        ctk.CTkLabel(self, text=item["name"], font=("Arial", 18, "bold")).pack(pady=5)
        ctk.CTkLabel(self, text=f"Цена: {item['price']} руб.").pack(pady=2)
        ctk.CTkLabel(self, text="Описание:").pack(pady=2)
        desc = ctk.CTkTextbox(self, height=100, width=350, wrap="word")
        desc.insert("1.0", item.get("description", ""))
        desc.configure(state="disabled")
        desc.pack(pady=5)

        tags = ", ".join(item.get("hashtags", []))
        ctk.CTkLabel(self, text=f"Теги: {tags}").pack(pady=5)

        # Кнопка добавления/удаления из корзины
        item_id = item["id"]
        if item_id in parent.cart:
            btn = ctk.CTkButton(self, text="Убрать из корзины", command=self.remove)
        else:
            btn = ctk.CTkButton(self, text="В корзину", command=self.add)
        btn.pack(pady=10)

    def add(self):
        self.parent.add_to_cart(self.item)
        self.destroy()

    def remove(self):
        self.parent.remove_from_cart(self.item)
        self.destroy()

# --- Окно корзины ---
class CartWindow(ctk.CTkToplevel):
    def __init__(self, shop_window):
        super().__init__(shop_window)
        self.shop = shop_window
        self.title("Корзина")
        self.geometry("600x500")

        self.items = {item["id"]: item for item in self.shop.items}
        self.cart_items = []
        self.total = 0

        self.create_widgets()
        self.update_cart_display()

    def create_widgets(self):
        # Заголовок
        ctk.CTkLabel(self, text="Ваша корзина", font=("Arial", 18)).pack(pady=10)

        # Список товаров в корзине
        self.cart_frame = ctk.CTkScrollableFrame(self)
        self.cart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Итоговая сумма и кнопки
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(fill="x", padx=10, pady=5)

        self.total_label = ctk.CTkLabel(bottom_frame, text="Итого: 0 руб.", font=("Arial", 14))
        self.total_label.pack(side="left", padx=10)

        self.btn_buy = ctk.CTkButton(bottom_frame, text="Купить", command=self.buy)
        self.btn_buy.pack(side="left", padx=5)

        self.btn_add_balance = ctk.CTkButton(bottom_frame, text="Пополнить баланс", command=self.add_balance)
        self.btn_add_balance.pack(side="left", padx=5)

        self.btn_close = ctk.CTkButton(bottom_frame, text="Закрыть", command=self.destroy)
        self.btn_close.pack(side="left", padx=5)

    def update_cart_display(self):
        # Очистить предыдущие элементы
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        self.cart_items = []
        self.total = 0

        if not self.shop.cart:
            ctk.CTkLabel(self.cart_frame, text="Корзина пуста").pack(pady=20)
            self.total_label.configure(text="Итого: 0 руб.")
            return

        for item_id, quantity in self.shop.cart.items():
            item = self.items.get(item_id)
            if not item:
                continue
            self.cart_items.append((item, quantity))
            self.total += item["price"] * quantity

            # Карточка товара
            card = ctk.CTkFrame(self.cart_frame)
            card.pack(fill="x", pady=2)

            info = f"{item['name']} - {item['price']} руб. x {quantity} = {item['price'] * quantity} руб."
            ctk.CTkLabel(card, text=info, anchor="w").pack(side="left", padx=5, fill="x", expand=True)

            # Кнопки управления количеством
            btn_frame = ctk.CTkFrame(card)
            btn_frame.pack(side="right", padx=5)

            ctk.CTkButton(btn_frame, text="+", width=30, command=lambda i=item_id: self.change_quantity(i, 1)).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="-", width=30, command=lambda i=item_id: self.change_quantity(i, -1)).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="Удалить", command=lambda i=item_id: self.remove_item(i)).pack(side="left", padx=2)

        self.total_label.configure(text=f"Итого: {self.total} руб.")

    def change_quantity(self, item_id, delta):
        if item_id in self.shop.cart:
            new_qty = self.shop.cart[item_id] + delta
            if new_qty <= 0:
                del self.shop.cart[item_id]
            else:
                self.shop.cart[item_id] = new_qty
            self.update_cart_display()
            self.shop.refresh_items()  # обновить кнопки в магазине

    def remove_item(self, item_id):
        if item_id in self.shop.cart:
            del self.shop.cart[item_id]
            self.update_cart_display()
            self.shop.refresh_items()

    def buy(self):
        if not self.shop.cart:
            mb.showwarning("Корзина пуста", "Добавьте товары в корзину")
            return

        if self.shop.user_data["balance"] < self.total:
            mb.showerror("Недостаточно средств", "Пополните баланс")
            return

        # Списание средств
        self.shop.user_data["balance"] -= self.total
        self.shop.save_user_data()
        self.shop.update_balance()

        # Очистка корзины
        self.shop.cart.clear()
        self.shop.refresh_items()

        mb.showinfo("Покупка совершена", f"Спасибо за покупку!\nСписано: {self.total} руб.")
        self.update_cart_display()

    def add_balance(self):
        AddBalanceWindow(self.shop, self)

# --- Окно пополнения баланса ---
class AddBalanceWindow(ctk.CTkToplevel):
    def __init__(self, shop_window, parent=None):
        super().__init__(parent if parent else shop_window)
        self.shop = shop_window
        self.title("Пополнение баланса")
        self.geometry("300x150")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Введите сумму:").pack(pady=10)
        self.entry_sum = ctk.CTkEntry(self, placeholder_text="Сумма")
        self.entry_sum.pack(pady=5)

        ctk.CTkButton(self, text="Пополнить", command=self.add).pack(pady=10)

    def add(self):
        try:
            amount = float(self.entry_sum.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            mb.showerror("Ошибка", "Введите положительное число")
            return

        self.shop.user_data["balance"] += amount
        self.shop.save_user_data()
        self.shop.update_balance()
        mb.showinfo("Успех", f"Баланс пополнен на {amount} руб.")
        self.destroy()

# --- Окно администратора ---
class AdminWindow(ctk.CTkToplevel):
    def __init__(self, shop_window):
        super().__init__(shop_window)
        self.shop = shop_window
        self.title("Панель администратора")
        self.geometry("800x500")

        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True)

        self.tab_items = self.tab_view.add("Товары")
        self.tab_users = self.tab_view.add("Пользователи")

        self.setup_items_tab()
        self.setup_users_tab()

    def setup_items_tab(self):
        # Кнопка добавления товара
        btn_add = ctk.CTkButton(self.tab_items, text="Добавить товар", command=self.add_item)
        btn_add.pack(pady=5)

        # Список товаров
        self.items_frame = ctk.CTkScrollableFrame(self.tab_items)
        self.items_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.refresh_items_list()

    def refresh_items_list(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        items = load_items()
        for item in items:
            frame = ctk.CTkFrame(self.items_frame)
            frame.pack(fill="x", pady=2)

            info = f"{item['name']} - {item['price']} руб. | Теги: {', '.join(item.get('hashtags', []))}"
            ctk.CTkLabel(frame, text=info, anchor="w").pack(side="left", padx=5, fill="x", expand=True)

            btn_edit = ctk.CTkButton(frame, text="Редактировать", width=100,
                                      command=lambda i=item: self.edit_item(i))
            btn_edit.pack(side="right", padx=2)

            btn_del = ctk.CTkButton(frame, text="Удалить", width=80,
                                     command=lambda i=item: self.delete_item(i))
            btn_del.pack(side="right", padx=2)

    def add_item(self):
        AddItemWindow(self, None)

    def edit_item(self, item):
        AddItemWindow(self, item)

    def delete_item(self, item):
        if mb.askyesno("Подтверждение", f"Удалить товар '{item['name']}'?"):
            items = load_items()
            items = [i for i in items if i["id"] != item["id"]]
            save_items(items)
            self.shop.items = load_items()  # обновить в магазине
            self.shop.apply_filters()       # переприменить фильтры
            self.refresh_items_list()

    def setup_users_tab(self):
        self.users_frame = ctk.CTkScrollableFrame(self.tab_users)
        self.users_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.refresh_users_list()

    def refresh_users_list(self):
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        users = load_users()
        for login, data in users.items():
            frame = ctk.CTkFrame(self.users_frame)
            frame.pack(fill="x", pady=2)

            status = "Заблокирован" if data.get("is_blocked") else "Активен"
            info = f"{login} ({data['role']}) | Баланс: {data['balance']} | Статус: {status}"
            if data.get("is_blocked") and data.get("block_reason"):
                info += f" | Причина: {data['block_reason']}"

            ctk.CTkLabel(frame, text=info, anchor="w").pack(side="left", padx=5, fill="x", expand=True)

            if login != "admin":  # админа нельзя блокировать
                if data.get("is_blocked"):
                    btn = ctk.CTkButton(frame, text="Разблокировать", width=120,
                                         command=lambda u=login: self.unblock_user(u))
                else:
                    btn = ctk.CTkButton(frame, text="Блокировать", width=100,
                                         command=lambda u=login: self.block_user(u))
                btn.pack(side="right", padx=2)

    def block_user(self, login):
        dialog = ctk.CTkInputDialog(text=f"Укажите причину блокировки для {login}:", title="Блокировка")
        reason = dialog.get_input()
        if reason is not None:  # пользователь не нажал "Отмена"
            users = load_users()
            if login in users:
                users[login]["is_blocked"] = True
                users[login]["block_reason"] = reason if reason else ""  # пустая строка допустима
                save_users(users)
                self.refresh_users_list()

    def unblock_user(self, login):
        users = load_users()
        if login in users:
            users[login]["is_blocked"] = False
            users[login]["block_reason"] = ""
            save_users(users)
            self.refresh_users_list()

# --- Окно добавления/редактирования товара ---
class AddItemWindow(ctk.CTkToplevel):
    def __init__(self, admin_window, item):
        super().__init__(admin_window)
        self.admin = admin_window
        self.item = item  # None если новый товар
        self.title("Редактирование товара" if item else "Новый товар")
        self.geometry("400x500")
        self.resizable(False, False)

        # Поля ввода
        ctk.CTkLabel(self, text="Название:").pack(pady=2)
        self.entry_name = ctk.CTkEntry(self, width=300)
        self.entry_name.pack(pady=2)
        if item:
            self.entry_name.insert(0, item["name"])

        ctk.CTkLabel(self, text="Описание:").pack(pady=2)
        self.text_desc = ctk.CTkTextbox(self, height=100, width=300)
        self.text_desc.pack(pady=2)
        if item:
            self.text_desc.insert("1.0", item.get("description", ""))

        ctk.CTkLabel(self, text="Цена:").pack(pady=2)
        self.entry_price = ctk.CTkEntry(self, width=300)
        self.entry_price.pack(pady=2)
        if item:
            self.entry_price.insert(0, str(item["price"]))

        ctk.CTkLabel(self, text="Изображение:").pack(pady=2)
        self.image_path = ctk.StringVar()
        self.entry_image = ctk.CTkEntry(self, textvariable=self.image_path, width=250)
        self.entry_image.pack(side="left", padx=(20,5), pady=2)
        self.btn_browse = ctk.CTkButton(self, text="Обзор", width=50, command=self.browse_image)
        self.btn_browse.pack(side="left", pady=2)

        ctk.CTkLabel(self, text="Хештеги (через запятую):").pack(pady=2)
        self.entry_tags = ctk.CTkEntry(self, width=300)
        self.entry_tags.pack(pady=2)
        if item:
            self.entry_tags.insert(0, ", ".join(item.get("hashtags", [])))

        self.btn_save = ctk.CTkButton(self, text="Сохранить", command=self.save)
        self.btn_save.pack(pady=20)

    def browse_image(self):
        filename = fd.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if filename:
            # Копируем изображение в папку images
            basename = os.path.basename(filename)
            dest = os.path.join(IMAGES_DIR, basename)
            shutil.copy(filename, dest)
            self.image_path.set(dest)

    def save(self):
        name = self.entry_name.get().strip()
        desc = self.text_desc.get("1.0", "end-1c").strip()
        price_str = self.entry_price.get().strip()
        image = self.image_path.get().strip()
        tags_str = self.entry_tags.get().strip()

        if not name or not price_str:
            mb.showerror("Ошибка", "Название и цена обязательны")
            return

        try:
            price = float(price_str)
        except ValueError:
            mb.showerror("Ошибка", "Цена должна быть числом")
            return

        hashtags = [t.strip() for t in tags_str.split(",") if t.strip()]

        items = load_items()
        if self.item:  # редактирование
            # Обновляем существующий товар
            for i in items:
                if i["id"] == self.item["id"]:
                    i["name"] = name
                    i["description"] = desc
                    i["price"] = price
                    i["image"] = image
                    i["hashtags"] = hashtags
                    break
        else:  # новый товар
            new_id = max([item["id"] for item in items], default=0) + 1
            new_item = {
                "id": new_id,
                "name": name,
                "description": desc,
                "price": price,
                "image": image,
                "hashtags": hashtags
            }
            items.append(new_item)

        save_items(items)
        self.admin.shop.items = load_items()  # обновить в магазине
        self.admin.shop.apply_filters()       # переприменить фильтры
        self.admin.refresh_items_list()
        self.destroy()

# --- Запуск приложения ---
if __name__ == "__main__":
    app = AuthWindow()
    app.mainloop()