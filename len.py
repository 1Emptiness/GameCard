import tkinter as tk
from tkinter import messagebox
import json
import os
import pyautogui
from pynput import mouse, keyboard
import keyboard as kb  # Библиотека для работы с горячими клавишами

# Файлы для хранения данных
COORDINATES_FILE = 'coordinates.json'
DISTANCES_FILE = 'distances.json'

# Загрузка данных из файлов
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    return []

coordinates = load_data(COORDINATES_FILE)
distances = load_data(DISTANCES_FILE)
stop_program = False

# Сохранение данных в файлы
def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Функция для закрытия программы
def close_program():
    save_data(coordinates, COORDINATES_FILE)
    save_data(distances, DISTANCES_FILE)
    root.quit()

# Функция для выбора режима работы
def select_mode(mode):
    if mode == "coordinates":
        root.withdraw()  # Сворачиваем окно
        start_coordinate_mode()
    elif mode == "distance":
        root.withdraw()  # Сворачиваем окно
        start_distance_mode()

# Функция для получения координат
def start_coordinate_mode():
    global stop_program

    def on_click(x, y, button, pressed):
        if pressed:
            coordinates.append((x, y))
            print(f"Координаты: ({x}, {y})")
        if stop_program:
            return False

    def on_press(key):
        global stop_program
        stop_program = True
        return False

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    mouse_listener.stop()
    stop_program = False
    root.deiconify()  # Возвращаем окно программы после завершения

# Функция для измерения расстояния
def start_distance_mode():
    global stop_program

    points = []

    def on_click(x, y, button, pressed):
        if pressed:
            points.append((x, y))
            if len(points) == 2:
                x1, y1 = points[0]
                x2, y2 = points[1]
                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                distances.append(distance)
                print(f"Расстояние: {distance:.2f} пикселей")
                points.clear()
        if stop_program:
            return False

    def on_press(key):
        global stop_program
        stop_program = True
        return False

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    mouse_listener.stop()
    stop_program = False
    root.deiconify()  # Возвращаем окно программы после завершения

# Функция для отображения координат
def show_coordinates():
    def copy_selected():
        selected_indices = listbox.curselection()
        if not selected_indices:
            return
        selected_texts = [listbox.get(i) for i in selected_indices]
        clipboard_text = '\n'.join(selected_texts)
        root.clipboard_clear()
        root.clipboard_append(clipboard_text)
        root.update()  # Обновление буфера обмена

    coord_window = tk.Toplevel(root)
    coord_window.title("Координаты")
    coord_window.geometry("400x400")

    listbox = tk.Listbox(coord_window, selectmode=tk.EXTENDED)  # Изменяем режим выбора
    listbox.pack(fill=tk.BOTH, expand=True)

    for idx, coord in enumerate(coordinates):
        listbox.insert(tk.END, f"{idx+1}. {coord}")

    def delete_selected():
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices):
            del coordinates[index]
            listbox.delete(index)

    def select_all():
        listbox.select_set(0, tk.END)

    tk.Button(coord_window, text="Удалить выбранное", command=delete_selected).pack()
    tk.Button(coord_window, text="Выбрать все", command=select_all).pack()  # Кнопка для выбора всех
    tk.Button(coord_window, text="Копировать", command=copy_selected).pack()  # Кнопка для копирования
    tk.Button(coord_window, text="Назад", command=coord_window.destroy).pack()
    coord_window.protocol("WM_DELETE_WINDOW", coord_window.destroy)

# Функция для отображения сохраненных длин
def show_distances():
    def copy_selected():
        selected_indices = listbox.curselection()
        if not selected_indices:
            return
        selected_texts = [listbox.get(i) for i in selected_indices]
        clipboard_text = '\n'.join(selected_texts)
        root.clipboard_clear()
        root.clipboard_append(clipboard_text)
        root.update()  # Обновление буфера обмена

    dist_window = tk.Toplevel(root)
    dist_window.title("Сохраненные длины")
    dist_window.geometry("400x400")

    listbox = tk.Listbox(dist_window, selectmode=tk.EXTENDED)  # Изменяем режим выбора
    listbox.pack(fill=tk.BOTH, expand=True)

    for idx, dist in enumerate(distances):
        listbox.insert(tk.END, f"{idx+1}. {dist:.2f} пикселей")

    def delete_selected():
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices):
            del distances[index]
            listbox.delete(index)

    def select_all():
        listbox.select_set(0, tk.END)

    tk.Button(dist_window, text="Удалить выбранное", command=delete_selected).pack()
    tk.Button(dist_window, text="Выбрать все", command=select_all).pack()  # Кнопка для выбора всех
    tk.Button(dist_window, text="Копировать", command=copy_selected).pack()  # Кнопка для копирования
    tk.Button(dist_window, text="Назад", command=dist_window.destroy).pack()
    dist_window.protocol("WM_DELETE_WINDOW", dist_window.destroy)

# Создание главного окна
root = tk.Tk()
root.title("Программа для координат и расстояний")
root.geometry("300x200")

# Кнопки для выбора режима
tk.Button(root, text="Узнать координаты", command=lambda: select_mode("coordinates")).pack(pady=10)
tk.Button(root, text="Измерить расстояние", command=lambda: select_mode("distance")).pack(pady=10)
tk.Button(root, text="Просмотр координат", command=show_coordinates).pack(pady=10)
tk.Button(root, text="Сохраненные длины", command=show_distances).pack(pady=10)

# Закрытие программы по нажатию на крестик
root.protocol("WM_DELETE_WINDOW", close_program)

# Установка горячих клавиш
kb.add_hotkey('ctrl+a', lambda: select_mode("coordinates"))
kb.add_hotkey('ctrl+s', lambda: select_mode("distance"))

root.mainloop()
