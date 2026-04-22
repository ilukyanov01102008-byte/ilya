import json
import os
import requests
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Конфигурация ----------
API_KEY = "ваш_api_ключ"  # Получить на https://app.exchangerate-api.com/sign-up
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"
HISTORY_FILE = "conversion_history.json"


# ---------- Работа с историей ----------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def add_to_history(from_curr, to_curr, amount, result, rate):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "from": from_curr,
        "to": to_curr,
        "amount": amount,
        "result": result,
        "rate": rate
    })
    save_history(history)


# ---------- Работа с API ----------
def get_exchange_rate(from_currency, to_currency):
    try:
        response = requests.get(BASE_URL + from_currency, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data["result"] == "success":
            rate = data["conversion_rates"].get(to_currency)
            if rate:
                return rate
            else:
                messagebox.showerror("Ошибка", f"Валюта {to_currency} не найдена")
                return None
        else:
            messagebox.showerror("Ошибка", "Не удалось получить курс. Проверьте API-ключ.")
            return None
    except Exception as e:
        messagebox.showerror("Ошибка", f"Сетевая ошибка: {e}")
        return None


# ---------- GUI приложение ----------
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Доступные валюты (можно расширить)
        self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT", "UAH", "TRY"]

        # Создание интерфейса
        self.create_widgets()
        self.update_history_table()

    def create_widgets(self):
        # Рамка конвертации
        conv_frame = ttk.LabelFrame(self.root, text="Конвертация", padding=10)
        conv_frame.pack(fill="x", padx=10, pady=5)

        # Выбор "из"
        ttk.Label(conv_frame, text="Из валюты:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.from_currency = ttk.Combobox(conv_frame, values=self.currencies, state="readonly")
        self.from_currency.set("USD")
        self.from_currency.grid(row=0, column=1, padx=5, pady=5)

        # Выбор "в"
        ttk.Label(conv_frame, text="В валюту:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.to_currency = ttk.Combobox(conv_frame, values=self.currencies, state="readonly")
        self.to_currency.set("EUR")
        self.to_currency.grid(row=1, column=1, padx=5, pady=5)

        # Сумма
        ttk.Label(conv_frame, text="Сумма:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = ttk.Entry(conv_frame, width=20)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка конвертации
        self.convert_btn = ttk.Button(conv_frame, text="Конвертировать", command=self.convert)
        self.convert_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Результат
        self.result_label = ttk.Label(conv_frame, text="Результат: ---", font=("Arial", 10, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=5)

        # Рамка истории
        hist_frame = ttk.LabelFrame(self.root, text="История конвертаций", padding=10)
        hist_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Таблица истории (Treeview)
        columns = ("timestamp", "from", "to", "amount", "result", "rate")
        self.history_tree = ttk.Treeview(hist_frame, columns=columns, show="headings")
        self.history_tree.heading("timestamp", text="Дата/время")
        self.history_tree.heading("from", text="Из")
        self.history_tree.heading("to", text="В")
        self.history_tree.heading("amount", text="Сумма")
        self.history_tree.heading("result", text="Результат")
        self.history_tree.heading("rate", text="Курс")

        self.history_tree.column("timestamp", width=140)
        self.history_tree.column("amount", width=80)
        self.history_tree.column("result", width=100)
        self.history_tree.column("rate", width=80)

        scrollbar = ttk.Scrollbar(hist_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопка очистки истории
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Обновить таблицу", command=self.update_history_table).pack(side="left", padx=5)

    def validate_amount(self, amount_str):
        """Проверяет, что сумма — положительное число."""
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Сумма должна быть положительным числом!")
            return None

    def convert(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        amount_str = self.amount_entry.get()

        amount = self.validate_amount(amount_str)
        if amount is None:
            return

        rate = get_exchange_rate(from_curr, to_curr)
        if rate is None:
            return

        result = amount * rate
        result_text = f"{result:.2f} {to_curr}"
        self.result_label.config(text=f"Результат: {result_text}")

        # Сохраняем в историю
        add_to_history(from_curr, to_curr, amount, result, rate)
        self.update_history_table()

    def update_history_table(self):
        # Очищаем таблицу
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        history = load_history()
        for entry in reversed(history):  # последние сверху
            self.history_tree.insert("", "end", values=(
                entry["timestamp"],
                entry["from"],
                entry["to"],
                entry["amount"],
                f"{entry['result']:.2f}",
                f"{entry['rate']:.4f}"
            ))

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Удалить всю историю?"):
            save_history([])
            self.update_history_table()
            self.result_label.config(text="Результат: ---")


# ---------- Запуск приложения ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
