import sys
from PIL import Image

def resize_image(input_path, output_path, width, height):
    try:
        with Image.open(input_path) as img:
            # Поддержка прозрачности PNG
            img = img.convert("RGBA")
            
            new_size = (width, height)
            # Ресайз с максимальным качеством
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            resized_img.save(output_path, "PNG")
            print(f"✅ Готово: {output_path} [{width}x{height}]")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    # Проверяем наличие всех 4 аргументов
    if len(sys.argv) != 5:
        print("Использование: python res.py input.png output.png ширина высота")
        print("Пример: python res.py logo.png small.png 800 600")
    else:
        # sys.argv[0] - имя скрипта
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        w = int(sys.argv[3])
        h = int(sys.argv[4])
        
        resize_image(file_in, file_out, w, h)
