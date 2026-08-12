import tkinter as tk
from tkinter import ttk

def on_click():
    val = slider.get()
    com = combo.get()

    minimp = (val * impact[com]['min'] * capability[com]['min']) * 100
    maximp = (val * impact[com]['max'] * capability[com]['max']) * 100

    label3.config(text=f"Потенциальный рост ВДС от {minimp:.1f}% до {maximp:.1f}%")

impact = {
    "Оптимизация": {'min': 0.1, 'max': 0.3},
    "Прогнозирование": {'min': 0.1, 'max': 0.3},
    "Распознование": {'min': 0.3, 'max': 0.9},
    "Логистика": {'min': 0.05, 'max': 0.25},
    "Комбинаторный поиск": {'min': 0.4, 'max': 1}
}

capability = {
    "Оптимизация": {'min': 0.4, 'max': 0.7},
    "Прогнозирование": {'min': 0.5, 'max': 0.8},
    "Распознование": {'min': 0.7, 'max': 0.9},
    "Логистика": {'min': 0.5, 'max': 0.7},
    "Комбинаторный поиск": {'min': 0.15, 'max': 0.3}
}

# Создаем главное окно
root = tk.Tk()
root.title("Potential AI impact")
root.geometry("600x250")

label1 = tk.Label(root, text="Категория задачи", font=("Arial", 10))
label1.pack()

combo = ttk.Combobox(root, values=["Оптимизация", "Прогнозирование", "Распознование", "Логистика", "Комбинаторный поиск"])
combo.current(0)  # Устанавливаем первый элемент по умолчанию
combo.pack(pady=(0, 20))

label2 = tk.Label(root, text="Экономическая значимость задачи для ВДС: 0 - отсутствует, 1 - крайне высокая:", font=("Arial", 10))
label2.pack()

# Создаем ползунок
slider = tk.Scale(
    root,
    from_=0,
    to=1,
    resolution=0.01,  # Шаг ползунка (сотые доли)
    orient=tk.HORIZONTAL,
    length=300
)
slider.pack(pady=(0,20))

button = tk.Button(root, text="Вычислить потенциальный вклад", command=on_click, font=("Arial", 10, "bold"))
button.pack(pady=(0,20))

label3 = tk.Label(root, text="", fg='green', font=("Arial", 12, "bold"))
label3.pack()

# Запускаем приложение
root.mainloop()