import tkinter as tk
from tkinter import ttk
import webbrowser
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox

advancedmode = False    # переключение на расширенные настройки
minimp = 0  # нижняя граница потенциальной выгоды
maximp = 0  # верхняя граница потенциальной выгоды
adoption = 0    # счётчик внедрений

# усредненные выгоды от использования МЛ/ИИ в сравнении с классическими подходами
impact = {
    "Оптимизация": {'min': 0.1, 'max': 0.3},
    "Прогнозирование": {'min': 0.1, 'max': 0.3},
    "Распознавание": {'min': 0.5, 'max': 0.9},
    "Логистика": {'min': 0.05, 'max': 0.15},
    "Комбинаторный поиск": {'min': 0.05, 'max': 0.1}
}

# вероятность успешной реализации (уровень технологической готовности: сигмоида)
capability = {
    "УГТ-1": {0.057},
    "УГТ-2": {0.119},
    "УГТ-3": {0.231},
    "УГТ-4": {0.401},
    "УГТ-5": {0.599},
    "УГТ-6": {0.769},
    "УГТ-7": {0.881},
    "УГТ-8": {0.943},
    "УГТ-9": {0.973}
}

# сброс данных
def on_click_reset():
    label3.config(text="")
    slider.set(0)
    combo.set("Оптимизация")
    combocap.current(5)
    tbimpmin.delete(0, "end")
    tbimpmax.delete(0, "end")
    tbimpmin.insert(0, str(impact["Оптимизация"]['min']))
    tbimpmax.insert(0, str(impact["Оптимизация"]['max']))
    global minimp
    global maximp
    global adoption
    minimp = 0
    maximp = 0
    adoption = 0
    mainmenu.entryconfigure(2, label="Количество внедрений: 0")

# вычислить потенциальную выгоду
def on_click_calc():
    global minimp
    global maximp
    global adoption

    significance = slider.get()
    task = combo.get()
    TRL = combocap.get()

    if not advancedmode:
        if TRL == "УГТ-1" or TRL == "УГТ-2":
            minimp += (significance * impact[task]['min'] * float(*capability[TRL])) * 100
            maximp += (significance * impact[task]['max'] * float(*capability[TRL])) * 100
        else:
            minimp += (significance * impact[task]['min'] * (float(*capability[TRL]) - 0.1)) * 100
            maximp += (significance * impact[task]['max'] * float(*capability[TRL])) * 100
    else:
        if TRL == "УГТ-1" or TRL == "УГТ-2":
            minimp += (significance * float(tbimpmin.get()) * float(*capability[TRL])) * 100
            maximp += (significance * float(tbimpmax.get()) * float(*capability[TRL])) * 100
        else:
            minimp += (significance * float(tbimpmin.get()) * (float(*capability[TRL]) - 0.1)) * 100
            maximp += (significance * float(tbimpmax.get()) * float(*capability[TRL])) * 100

    label3.config(text=f"Потенциальный рост ВДС от {minimp:.1f}% до {maximp:.1f}%")
    adoption += 1
    mainmenu.entryconfigure(2, label="Количество внедрений: " + str(adoption))


# переключение на расширенные настройки
def on_click_show():
    global advancedmode
    if not advancedmode:
        advancedmode = True
        root.geometry("1100x350")

        currenttask = combo.get()
        tbimpmin.insert(0, str(impact[currenttask]['min']))
        tbimpmax.insert(0, str(impact[currenttask]['max']))

# изменение класса задачи в комбобоксе
def on_combo_change(event):
    if advancedmode:
        tbimpmin.delete(0, "end")
        tbimpmax.delete(0, "end")

    currenttask = combo.get()
    if advancedmode:
        tbimpmin.insert(0, str(impact[currenttask]['min']))
        tbimpmax.insert(0, str(impact[currenttask]['max']))

# График роста ВДС в зависимости от УГТ
def on_click_getgraph():
    global adoption

    if adoption == 0:
        messagebox.showerror("Ошибка", "Сначала вычислите потенциальный вклад.")
    elif adoption > 1:
        messagebox.showerror("Ошибка", "На данный момент динамика рассчитывается только для 1 внедрения.")
    elif adoption == 1:
        significance = slider.get()
        task = combo.get()

        maxlist = []
        minlist = []
        for i in range(combocap.current(), 9):
            maxlist.append((significance * impact[task]['max'] * float(*capability["УГТ-"+ str(i+1)])) * 100)
            minlist.append((significance * impact[task]['min'] * (float(*capability["УГТ-"+ str(i+1)]) - 0.1)) * 100)

        TRLnum = np.arange(combocap.current()+1, 10)
        plt.plot(TRLnum, maxlist, ls=':', marker='^', color='red', label='Верхняя граница')
        plt.plot(TRLnum, minlist, ls=':', marker='v', color='green', label='Нижняя граница')

        for i, txt in enumerate(maxlist):
            plt.text(TRLnum[i], maxlist[i] + 0.3, f"{txt:.1f}%", fontsize=10, ha='center')

        for i, txt in enumerate(minlist):
            plt.text(TRLnum[i], minlist[i] + 0.3, f"{txt:.1f}%", fontsize=10, ha='center')

        plt.title("Динамика роста ВДС в зависимости от УГТ")
        plt.xlabel('Уровень технологической готовности')
        plt.ylabel('Приблизительный рост ВДС %')
        plt.legend()
        plt.grid()
        plt.show()

# ссылка на руководство пользователя
def on_click_getmanual(event=None):
    webbrowser.open("https://github.com/aghajanyan/ITMO-3/blob/main/ImpactCalc/%D0%A0%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%D0%B4%D1%81%D1%82%D0%B2%D0%BE%20%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F.docx")


# главное окно
root = tk.Tk()
root.title("Potential AI impact v6.0")
root.geometry("600x350")
root.resizable(False, False)

# меню сверхну
mainmenu = tk.Menu(root)
toolmenu = tk.Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Дополнительно", menu=toolmenu)
toolmenu.add_command(label="Расширенные настройки", command=on_click_show)
toolmenu.add_command(label="Динамика роста ВДС", command=on_click_getgraph)
toolmenu.add_command(label="Руководство пользователя", command=on_click_getmanual)
mainmenu.add_command(label="Количество внедрений: 0")
root.config(menu=mainmenu)

# структура с основными элементами
mainframe = tk.Frame(root)
mainframe.pack(side="left", fill="both", expand=True, padx=40, pady=10)

# структура с дополнительными элементами
additionalframe = tk.Frame(root)
additionalframe.pack(side="left", fill="both", expand=True, padx=40, pady=10)

# ОСНОВНЫЕ ЭЛЕМЕНТЫ (начало) ===
label1 = tk.Label(mainframe, text="Категория задачи", font=("Arial", 10))
label1.pack()

combo = ttk.Combobox(mainframe, values=["Оптимизация", "Прогнозирование", "Распознование", "Логистика", "Комбинаторный поиск"], width=22)
combo.current(0)
combo.pack(pady=(0, 20))
combo.bind("<<ComboboxSelected>>", on_combo_change)

label4 = tk.Label(mainframe, text="Вероятность качественного внедрения AI/ML (уровень технологической готовности):", font=("Arial", 10))
label4.pack()

combocap = ttk.Combobox(mainframe, values=["УГТ-1", "УГТ-2", "УГТ-3", "УГТ-4", "УГТ-5", "УГТ-6", "УГТ-7", "УГТ-8", "УГТ-9"], width=10)
combocap.current(5)
combocap.pack(pady=(0, 20))

label2 = tk.Label(mainframe, text="Экономическая значимость задачи для ВДС: 0 - отсутствует, 1 - крайне высокая:", font=("Arial", 10))
label2.pack()

# ползунок
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
label3.pack(pady=25)

# ОСНОВНЫЕ ЭЛЕМЕНТЫ (конец) ===

# ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ (начало) ===
"""
label4 = tk.Label(additionalframe, text="Вероятность качественного внедрения AI/ML (уровень технологической готовности):", font=("Arial", 10))
label4.pack()

# сетка для элементов capability (вероятность качественного внедрения)
capsettings = tk.Frame(additionalframe)
capsettings.pack(pady=10, padx=10)

label5 = tk.Label(capsettings, text="От:", font=("Arial", 10))
label5.grid(row=0, column=0, padx=(0, 5), sticky="e")

combocapmin = ttk.Combobox(capsettings, values=["УГТ-1 (10%)", "УГТ-2 (20%)", "УГТ-3 (30%)", "УГТ-4 (40%)", "УГТ-5 (50%)",
                                             "УГТ-6 (60%)", "УГТ-7 (70%)", "УГТ-8 (80%)", "УГТ-9 (90%)"], width=11)
combocapmin.current(2)
combocapmin.grid(row=0, column=1, padx=(0, 5), sticky="w")

#tbcapmin = tk.Entry(capsettings, width=10)
#tbcapmin.grid(row=0, column=1, padx=(0, 15), sticky="w")

label6 = tk.Label(capsettings, text="До:", font=("Arial", 10))
label6.grid(row=0, column=2, padx=(0, 5), sticky="e")

combocapmax = ttk.Combobox(capsettings, values=["УГТ-1 (10%)", "УГТ-2 (20%)", "УГТ-3 (30%)", "УГТ-4 (40%)", "УГТ-5 (50%)",
                                             "УГТ-6 (60%)", "УГТ-7 (70%)", "УГТ-8 (80%)", "УГТ-9 (90%)"], width=11)
combocapmax.current(6)
combocapmax.grid(row=0, column=3, sticky="w")
"""

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

# ДОПОЛНИТЕЛЬНЫЕ ЭЛЕМЕНТЫ (конец) ===


root.mainloop()