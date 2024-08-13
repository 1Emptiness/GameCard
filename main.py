from PIL import ImageGrab
import pyautogui
import time

def capture_screen(region=None):
    screen = ImageGrab.grab(bbox=region)
    return screen

def open_card(x, y):
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()

def capture_card_image(x, y, width, height):
    region = (x, y, x + width, y + height)
    card_image = capture_screen(region=region)
    return card_image

def compare_images(img1, img2):
    return list(img1.getdata()) == list(img2.getdata())

def process_cards(card_positions, card_size):
    memory = {}  # Словарь для хранения изображений карточек
    
    for i, pos in enumerate(card_positions):
        x, y = pos
        open_card(x, y)
        time.sleep(0.5)  # Ждем, пока карточка откроется
        
        card_image = capture_card_image(x, y, card_size[0], card_size[1])
        
        match_found = False
        for key, saved_image in memory.items():
            if compare_images(card_image, saved_image):
                print(f"Совпадение найдено для карточек в координатах {key} и {pos}. Удаляем их из памяти.")
                del memory[key]  # Удаляем совпавшую карточку из памяти
                match_found = True
                break
        
        if not match_found:
            memory[pos] = card_image
            print(f"Карточка в координатах {pos} добавлена в память.")
    
    print("Все карточки обработаны.")

if __name__ == "__main__":
    # Пример списка координат карточек и их размера
    card_positions = [
        (100, 100), (200, 100), (300, 100), (400, 100), (500, 100),
        (100, 200), (200, 200), (300, 200), (400, 200), (500, 200),
        # Добавьте остальные координаты карточек...
    ]
    card_size = (50, 70)  # Размеры карточек (ширина, высота)
    
    process_cards(card_positions, card_size)
