from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

class generator:
    imagePaths = ['static/template2.jpg', 'static/template3.jpg']
    def create_fact_image(fact):
        # Открываем фон изображения

        img = Image.open('static/template.jpg')  # Замените на путь к вашему фону

        # Подготовка для добавления текста
        draw = ImageDraw.Draw(img)
        font_path = 'static/CaskaydiaCoveNerdFont-Regular.ttf'  # Укажите путь к своему шрифту TTF
        font = ImageFont.truetype(font_path, 13)  # Установите нужный размер шрифта
        text = fact

        # Задаем размеры коробки для текста
        box_width = img.width // 2 - 40  # Уменьшаем ширину коробки (делаем рамки уже)
        box_height = 100  # Высота коробки, можно настроить по желанию
        text_x = 65  # Уменьшаем отступ от левого края
        text_y = 20  # Отступ от верхнего края

        # Разбиваем текст на строки, чтобы он не выходил за пределы коробки
        lines = []
        words = text.split()
        line = ''
        for word in words:
            # Проверяем, помещается ли слово в текущую строку
            test_line = line + ' ' + word if line else word
            bbox = draw.textbbox((text_x, text_y), test_line, font=font)  # Получаем ограничивающий прямоугольник
            test_width = bbox[2] - bbox[0]  # Ширина текста
            if test_width <= box_width:
                line = test_line  # Добавляем слово в текущую строку
            else:
                lines.append(line)  # Сохраняем текущую строку
                line = word  # Начинаем новую строку с текущего слова
        lines.append(line)  # Добавляем последнюю строку

        # Рисуем текст внутри коробки
        current_y = text_y + 5  # Отступ сверху внутри коробки
        for line in lines:
            bbox = draw.textbbox((text_x + 5, current_y), line, font=font)  # Получаем bbox для каждой строки
            text_height = bbox[3] - bbox[1]  # Высота текста
            draw.text((text_x + 5, current_y), line, font=font, fill="black")  # Отступ слева внутри коробки
            current_y += text_height  # Увеличиваем вертикальную позицию для следующей строки

        # Сохраняем изображение в памяти
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr

    def create_fact_image_static(fact):
        # Загружаем случайное изображение
        #img_path = random.choice(generator.imagePaths)
        img_path = 'static/template3.jpg'
        img = Image.open(img_path)

        img_width, img_height = img.size  # Определяем реальные размеры изображения

        # Подготовка для добавления текста
        draw = ImageDraw.Draw(img)
        font_path = 'static/CaskaydiaCoveNerdFont-Regular.ttf'  # Укажите путь к вашему шрифту TTF
        font = ImageFont.truetype(font_path, 20)  # Настройка шрифта
        text = fact

        # Задаем размеры коробки для текста
        box_width = img_width // 2
        box_height = 100
        box_x = (img_width - box_width) // 2  # Центрируем коробку по горизонтали
        box_y = (img_height - box_height) // 2  # Центрируем коробку по вертикали

        # Разбиваем текст на строки, чтобы он не выходил за пределы коробки
        lines = []
        words = text.split()
        line = ''
        for word in words:
            # Проверяем, помещается ли слово в текущую строку
            test_line = line + ' ' + word if line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)  # Получаем ограничивающий прямоугольник
            test_width = bbox[2] - bbox[0]  # Ширина текста
            if test_width <= box_width:
                line = test_line  # Добавляем слово в текущую строку
            else:
                lines.append(line)  # Сохраняем текущую строку
                line = word  # Начинаем новую строку с текущего слова
        lines.append(line)  # Добавляем последнюю строку

        # Вычисляем общую высоту текста
        line_height = font.getbbox("Test")[3] - font.getbbox("Test")[1]
        total_text_height = len(lines) * line_height

        # Рассчитываем начальную вертикальную позицию текста для центрирования
        current_y = box_y + (box_height - total_text_height) // 2

        # Рисуем текст внутри коробки с горизонтальным центрированием
        for line in lines:
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            current_x = box_x + (box_width - text_width) // 2

            if img_path.endswith('template3.jpg'):
                current_x += 70
                color = 'white'
            else:
                color = 'black'

            draw.text((current_x, current_y), line, font=font, fill=color)
            current_y += line_height

        # Сохраняем изображение в памяти
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr
