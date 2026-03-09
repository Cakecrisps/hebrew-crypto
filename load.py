import math
import json

def create_trigram_json(input_txt, output_json):
    trigrams = {}
    
    # Читаем файл (формат: ТРИГРАММА КОЛИЧЕСТВО)
    with open(input_txt, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                key, count = parts[0].lower(), int(parts[1])
                trigrams[key] = count
    
    total = sum(trigrams.values())
    # Считаем логарифм вероятности для каждой триграммы
    log_model = {k: math.log10(v/total) for k, v in trigrams.items()}
    
    # Сохраняем в JSON
    with open(output_json, 'w') as f:
        json.dump(log_model, f)
    
    print(f"Готово! Модель сохранена в {output_json}")

# Запуск (сначала скачай english_trigrams.txt)
create_trigram_json('count_3l.txt', 'freq_3l.json')
