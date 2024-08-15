import tkinter as tk  # Импортируем tkinter для создания графического интерфейса
from PIL import ImageGrab  # Импортируем ImageGrab из PIL для захвата изображения экрана
import pyautogui  # Импортируем pyautogui для управления мышью и клавиатурой
import time  # Импортируем time для работы с задержками
import threading  # Импортируем threading для выполнения кода в отдельных потоках
import keyboard  # Импортируем keyboard для обработки горячих клавиш
import cv2  # Импортируем OpenCV для обработки изображений
import numpy as np  # Импортируем numpy для работы с массивами

# Флаг для остановки программы
stop_program = False

# Функция для захвата изображения экрана в указанной области
def capture_screen(region=None):
    screen = ImageGrab.grab(bbox=region)
    return screen

# Функция для перемещения курсора и клика по карточке
def open_card(x, y):
    pyautogui.moveTo(x, y, duration=0.5)  # Перемещаем курсор к заданным координатам
    pyautogui.click()  # Выполняем клик

# Функция для захвата изображения карточки в определенной области экрана
def capture_card_image(x, y, width, height):
    region = (x, y, x + width, y + height)  # Определяем область для захвата изображения
    card_image = capture_screen(region=region)  # Захватываем изображение экрана
    return card_image

# Функция для сохранения изображения на диск для проверки
def save_image(image, filename):
    image.save(filename)

# Функция для сравнения двух изображений (возвращает True, если изображения идентичны)
def compare_images(img1, img2, threshold_distance=50, threshold_percent = 0.05):
    # Конвертируем изображения в формат OpenCV
    img1_cv = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2_cv = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    
    # Инициализируем ORB детектор
    orb = cv2.ORB_create()
    
    # Найти ключевые точки и дескрипторы
    kp1, des1 = orb.detectAndCompute(img1_cv, None)
    kp2, des2 = orb.detectAndCompute(img2_cv, None)
    
    # Проверяем, если на одном из изображений отсутствуют ключевые точки
    if len(kp1) == 0 or len(kp2) == 0:
        print("Одно из изображений не содержит ключевых точек, пропуск сравнения.")
        return False
    
    # Сопоставление дескрипторов с помощью BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # Фильтруем хорошие совпадения
    good_matches = [m for m in matches if m.distance < threshold_distance]
    
    # Считаем процент хороших совпадений
    match_percent = len(good_matches) / min(len(kp1), len(kp2))
    
    # Возвращаем True, если процент хороших совпадений превышает порог
    return match_percent > threshold_percent

# Основная функция для обработки карточек
def process_cards(card_positions, card_size):
    global stop_program  # Используем глобальную переменную для остановки программы
    memory = {}  # Словарь для хранения изображений карточек и их координат

    # Цикл по всем позициям карточек
    for i in range(len(card_positions)):
        if stop_program:  # Проверяем, нужно ли остановить программу
            print("Программа остановлена.")
            break
        
        x, y = card_positions[i]  # Получаем координаты текущей карточки
        
        print(f"Обрабатываем карточку в координатах ({x}, {y})")
        
        # Нажатие на карточку
        open_card(x, y)
        time.sleep(0.3)
        
        # Повторное нажатие через 0.1 секунд
        open_card(x, y)
        time.sleep(0.1)
        
        # Перемещаем курсор
        pyautogui.moveTo(100, 100)
        
        time.sleep(0.2)
        card_image = capture_card_image(x, y, card_size[0], card_size[1])
        
        # Сохранение изображения для проверки
        save_image(card_image, f"card_{x}_{y}.png")
        
        match_found = False
        
        # Проверяем, есть ли совпадение с ранее открытыми карточками
        for key, saved_image in memory.items():
            if compare_images(card_image, saved_image):  # Сравниваем текущее изображение с сохраненными
                print(f"Совпадение найдено для карточек в координатах {key} и ({x}, {y}).")
                open_card(key[0], key[1])  # Открываем сохраненную карточку
                time.sleep(0.3)
                
                
                # Перемещаем курсор
                pyautogui.moveTo(100, 100)
                
                time.sleep(0.2)
                del memory[key]  # Удаляем совпавшую карточку из памяти
                match_found = True  # Устанавливаем флаг, что совпадение найдено
                break
        
        # Если совпадение не найдено, добавляем текущее изображение в память
        if not match_found:
            memory[(x, y)] = card_image
            print(f"Карточка в координатах ({x}, {y}) добавлена в память.")
    
    print("Все карточки обработаны.")

# Функция для запуска обработки карточек в отдельном потоке
def start_processing():
    global stop_program
    stop_program = False
    card_positions = [
    (164, 174), (319, 174), (474, 174), (629, 174), (784, 174), 
    (939, 174), (1094, 174), (1249, 174), (1404, 174),
    (164, 387), (319, 387), (474, 387), (629, 387), (784, 387), 
    (939, 387), (1094, 387), (1249, 387), (1404, 387),
    (164, 600), (319, 600), (474, 600), (629, 600), (784, 600), 
    (939, 600), (1094, 600), (1249, 600), (1404, 600),
    (164, 815), (319, 815), (474, 815), (629, 815), (784, 815), 
    (939, 815), (1094, 815), (1249, 815), (1404, 815)
]

    card_size = (94, 176)  # Размер карточки (ширина, высота)
    process_cards(card_positions, card_size)  # Запускаем процесс обработки карточек

# Функция для остановки обработки карточек
def stop_processing():
    global stop_program
    stop_program = True

# Функция, вызываемая при нажатии CTRL+A, чтобы остановить программу
def on_ctrl_a():
    stop_processing()

# Функция, вызываемая при нажатии CTRL+S, чтобы запустить программу
def on_ctrl_s():
    threading.Thread(target=start_processing).start()

# Функция для создания графического интерфейса
def create_gui():
    root = tk.Tk()  # Создаем главное окно приложения
    root.title("Card Matching Automation")  # Устанавливаем заголовок окна
    root.geometry("300x150")  # Задаем размеры окна

    # Создаем кнопку для запуска процесса обработки карточек
    start_button = tk.Button(root, text="Start Processing", command=lambda: threading.Thread(target=start_processing).start())
    start_button.pack(pady=20)  # Размещаем кнопку в окне с отступом

    root.mainloop()  # Запускаем главный цикл окна

# Главная точка входа в программу
if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+a', on_ctrl_a)  # Привязываем горячую клавишу CTRL+A к функции остановки программы
    keyboard.add_hotkey('ctrl+s', on_ctrl_s)  # Привязываем горячую клавишу CTRL+S к функции запуска программы
    create_gui()  # Создаем графический интерфейс