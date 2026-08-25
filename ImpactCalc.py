import tkinter as tk
from tkinter import ttk

advancedmode = False
minimp = 0
maximp = 0

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

# сброс данных
def on_click_reset():
    label3.config(text="")
    slider.set(0)
    combo.set("Оптимизация")
    global minimp
    global maximp
    minimp = 0
    maximp = 0

# вычислить потенциальную выгоду
def on_click_calc():
    global minimp
    global maximp

    significance = slider.get()
    task = combo.get()

    if not advancedmode:
        minimp += (significance * impact[task]['min'] * capability[task]['min']) * 100
        maximp += (significance * impact[task]['max'] * capability[task]['max']) * 100
    else:
        minimp += (significance * float(tbimpmin.get()) * float(tbcapmin.get())) * 100
        maximp += (significance * float(tbimpmax.get()) * float(tbcapmax.get())) * 100

    label3.config(text=f"Потенциальный рост ВДС от {minimp:.1f}% до {maximp:.1f}%")

def on_click_show():
    global advancedmode
    advancedmode = True
    root.geometry("1100x300")

    currenttask = combo.get()
    tbcapmin.insert(0, str(capability[currenttask]['min']))
    tbcapmax.insert(0, str(capability[currenttask]['max']))
    tbimpmin.insert(0, str(impact[currenttask]['min']))
    tbimpmax.insert(0, str(impact[currenttask]['max']))

def on_combo_change(event):
    tbcapmin.delete(0, "end")
    tbcapmax.delete(0, "end")
    tbimpmin.delete(0, "end")
    tbimpmax.delete(0, "end")

    currenttask = combo.get()

    tbcapmin.insert(0, str(capability[currenttask]['min']))
    tbcapmax.insert(0, str(capability[currenttask]['max']))
    tbimpmin.insert(0, str(impact[currenttask]['min']))
    tbimpmax.insert(0, str(impact[currenttask]['max']))

# Создаем главное окно
root = tk.Tk()
root.title("Potential AI impact v3.0")
root.geometry("600x300")
root.resizable(False, False)

# меню сверхну
mainmenu = tk.Menu(root)
toolmenu = tk.Menu(mainmenu, tearoff=0)
toolmenu.add_command(label="Расширенные настройки", command=on_click_show)
mainmenu.add_cascade(label="Дополнительно", menu=toolmenu)
root.config(menu=mainmenu)

# структура с основными элементами
mainframe = tk.Frame(root)
mainframe.pack(side="left", fill="both", expand=True, padx=40, pady=10)

# структура с дополнительными элементами
additionalframe = tk.Frame(root)
additionalframe.pack(side="left", fill="both", expand=True, padx=40, pady=10)

# ОСНОВНЫЕ ЭЛЕМЕНТЫ ===
label1 = tk.Label(mainframe, text="Категория задачи", font=("Arial", 10))
label1.pack()

combo = ttk.Combobox(mainframe, values=["Оптимизация", "Прогнозирование", "Распознование", "Логистика", "Комбинаторный поиск"])
combo.current(0)
combo.pack(pady=(0, 20))
combo.bind("<<ComboboxSelected>>", on_combo_change)

label2 = tk.Label(mainframe, text="Экономическая значимость задачи для ВДС: 0 - отсутствует, 1 - крайне высокая:", font=("Arial", 10))
label2.pack()

# Создаем ползунок
slider = tk.Scale(
    mainframe,
    from_=0,
    to=1,
    resolution=0.01,
    orient=tk.HORIZONTAL,
    length=300
)
slider.pack(pady=(0,20))

# сетка для кнопок
butframe = tk.Frame(mainframe)
butframe.pack(pady=10, padx=10)

calcbut = tk.Button(butframe, text="Вычислить потенциальный вклад", command=on_click_calc, font=("Arial", 10, "bold"))
calcbut.grid(row=0, column=0, padx=(0, 20))

resbut = tk.Button(butframe, text="Сброс", command=on_click_reset, font=("Arial", 10, "bold"), fg='red')
resbut.grid(row=0, column=1)

label3 = tk.Label(mainframe, text="", fg='green', font=("Arial", 12, "bold"))
label3.pack()

# ОСНОВНЫЕ ЭЛЕМЕНТЫ ===

# ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ (РАСШИРЕННЫЕ НАТСРОЙКИ) ===
label4 = tk.Label(additionalframe, text="Вероятность высококачественного внедрения ML/AI:", font=("Arial", 10))
label4.pack()

# сетка для элементов capability (вероятность качественного внедрения)
capsettings = tk.Frame(additionalframe)
capsettings.pack(pady=10, padx=10)

label5 = tk.Label(capsettings, text="От:", font=("Arial", 10))
label5.grid(row=0, column=0, padx=(0, 5), sticky="e")

tbcapmin = tk.Entry(capsettings, width=10)
tbcapmin.grid(row=0, column=1, padx=(0, 15), sticky="w")

label6 = tk.Label(capsettings, text="До:", font=("Arial", 10))
label6.grid(row=0, column=2, padx=(0, 5), sticky="e")

tbcapmax = tk.Entry(capsettings, width=10)
tbcapmax.grid(row=0, column=3, sticky="w")

label7 = tk.Label(additionalframe, text="Потенциальное улучшение заданной задачи алгоритмом ML/AI:", font=("Arial", 10))
label7.pack()

# сетка для элементов impact (потенциальное улучшение посредством МЛ/ИИ)
impsettings = tk.Frame(additionalframe)
impsettings.pack(pady=10, padx=10)

label8 = tk.Label(impsettings, text="От:", font=("Arial", 10))
label8.grid(row=0, column=0, padx=(0, 5), sticky="e")

tbimpmin = tk.Entry(impsettings, width=10)
tbimpmin.grid(row=0, column=1, padx=(0, 15), sticky="w")

label9 = tk.Label(impsettings, text="До:", font=("Arial", 10))
label9.grid(row=0, column=2, padx=(0, 5), sticky="e")

tbimpmax = tk.Entry(impsettings, width=10)
tbimpmax.grid(row=0, column=3, sticky="w")


root.mainloop()