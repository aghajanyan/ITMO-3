import tkinter as tk
from tkinter import ttk

significance = []   #коэффициенты экономической значимости
task = []    #выбор класса задач

# сохранение набора задач
def on_click_save():
    significance.append(slider.get())
    slider.set(0)
    task.append(combo.get())
    combo.set("Оптимизация")

# вычислить потенциальную выгоду
def on_click_calc():
    if slider.get() != 0:
        significance.append(slider.get())
        task.append(combo.get())

    minimp = 0
    maximp = 0
    for i in range(len(task)):
        minimp += (significance[i] * impact[task[i]]['min'] * capability[task[i]]['min']) * 100
        maximp += (significance[i] * impact[task[i]]['max'] * capability[task[i]]['max']) * 100

    label3.config(text=f"Потенциальный рост ВДС от {minimp:.1f}% до {maximp:.1f}%")

# усредненные выгоды от использования МЛ/ИИ в сравнении с классическими подходами
impact = {
    "Оптимизация": {'min': 0.1, 'max': 0.3},
    "Прогнозирование": {'min': 0.1, 'max': 0.3},
    "Распознование": {'min': 0.5, 'max': 0.9},
    "Логистика": {'min': 0.05, 'max': 0.15},
    "Комбинаторный поиск": {'min': 0.05, 'max': 0.1}
}

# сложность/вероятность успешной реализации (пока вилка из 0.3 и 0.7)
capability = {
    "Оптимизация": {'min': 0.3, 'max': 0.7},
    "Прогнозирование": {'min': 0.3, 'max': 0.7},
    "Распознование": {'min': 0.3, 'max': 0.7},
    "Логистика": {'min': 0.3, 'max': 0.7},
    "Комбинаторный поиск": {'min': 0.3, 'max': 0.7}
}

# Создаем главное окно
root = tk.Tk()
root.title("Potential AI impact v2.0")
root.geometry("600x300")

label1 = tk.Label(root, text="Категория задачи", font=("Arial", 10))
label1.pack()

combo = ttk.Combobox(root, values=["Оптимизация", "Прогнозирование", "Распознование", "Логистика", "Комбинаторный поиск"])
combo.current(0)
combo.pack(pady=(0, 20))

label2 = tk.Label(root, text="Экономическая значимость задачи для ВДС: 0 - отсутствует, 1 - крайне высокая:", font=("Arial", 10))
label2.pack()

# Создаем ползунок
slider = tk.Scale(
    root,
    from_=0,
    to=1,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=300
)
slider.pack(pady=(0,20))

button1 = tk.Button(root, text="Добавить еще одну задачу?", command=on_click_save, font=("Arial", 10, "bold"))
button1.pack(pady=(0,20))

button2 = tk.Button(root, text="Вычислить потенциальный вклад", command=on_click_calc, font=("Arial", 10, "bold"))
button2.pack(pady=(0,20))

label3 = tk.Label(root, text="", fg='green', font=("Arial", 12, "bold"))
label3.pack()

root.mainloop()