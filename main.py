import tkinter as tk  # Импортируем tkinter для создания графического интерфейса
from PIL import ImageGrab  # Импортируем ImageGrab из PIL для захвата изображения экрана
import pyautogui  # Импортируем pyautogui для управления мышью и клавиатурой
import time  # Импортируем time для работы с задержками
import threading  # Импортируем threading для выполнения кода в отдельных потоках
import keyboard  # Импортируем keyboard для обработки горячих клавиш
import cv2  # Импортируем OpenCV для обработки изображений
import numpy as np  # Импортируем numpy для работы с массивами
import os
import glob
import cv2

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
def compare_images(img1, img2, threshold_distance=50, threshold_percent=0.05):
    img1_cv = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    img2_cv = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2BGR)
    
    orb = cv2.ORB_create()
    
    kp1, des1 = orb.detectAndCompute(img1_cv, None)
    kp2, des2 = orb.detectAndCompute(img2_cv, None)
    
    if len(kp1) == 0 or len(kp2) == 0:
        print("Одно из изображений не содержит ключевых точек, пропуск сравнения.")
        return False
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    good_matches = [m for m in matches if m.distance < threshold_distance]
    
    match_percent = len(good_matches) / min(len(kp1), len(kp2))
    
    return match_percent > threshold_percent


# Функция для вычисления процента темного цвета в изображении
def calculate_dark_percentage(img, threshold=50):
    gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    dark_pixels = np.sum(gray_img < threshold)
    total_pixels = gray_img.size
    dark_percent = dark_pixels / total_pixels
    return dark_percent

# Основная функция для обработки карточек
def process_cards(card_positions, card_size):
    global stop_program
    memory = {}

    for i in range(len(card_positions)):
        if stop_program:
            print("Программа остановлена.")
            break
        
        x, y = card_positions[i]
        
        print(f"Обрабатываем карточку в координатах ({x}, {y})")
        
        open_card(x, y)
        time.sleep(0.2)
        
        open_card(x, y)
        time.sleep(0.1)
        
        pyautogui.moveTo(100, 100)
        time.sleep(0.2)
        card_image = capture_card_image(x, y, card_size[0], card_size[1])
        
        save_image(card_image, f"card_{x}_{y}.png")
        
        # Проверяем процент темного цвета в изображении
        dark_percent = calculate_dark_percentage(card_image)
        
        if dark_percent < 0.05:
            print(f"Карточка в координатах ({x}, {y}) содержит слишком мало темного цвета ({dark_percent:.2%}), пропуск.")
            # Удаляем предыдущую карточку из памяти, если она есть
            if memory:
                last_key = list(memory.keys())[-1]
                del memory[last_key]
                print(f"Карточка в координатах {last_key} также удалена из памяти.")
            continue
        
        match_found = False
        
        for key, saved_image in memory.items():
            if compare_images(card_image, saved_image):
                print(f"Совпадение найдено для карточек в координатах {key} и ({x}, {y}).")
                open_card(key[0], key[1])
                time.sleep(0.2)
                
                pyautogui.moveTo(100, 100)
                time.sleep(0.2)
                del memory[key]
                match_found = True
                break
        
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

    # Добавляем небольшую задержку перед удалением
    time.sleep(0.5)  # Задержка в 100 миллисекунд

    # Удаление всех файлов .png в текущей папке
    current_folder = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к текущей папке
    png_files = glob.glob(os.path.join(current_folder, '*.png'))  # Получаем список всех .png файлов в папке
    
    for file in png_files:
        try:
            os.remove(file)  # Удаляем каждый .png файл
        except Exception as e:
            print(f"Не удалось удалить {file}: {e}")

    print("Все файлы формата .png удалены.")

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