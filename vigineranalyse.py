import re
from collections import Counter
from vijiner import VigenereCipher
class VigenereAttacker:
    def __init__(self, scoring_function=None):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.get_score = scoring_function
        # Эталонный индекс совпадения для английского языка (~0.0667)
        self.english_ic = 0.0667

    def _clean(self, text):
        return re.sub(r'[^A-Z]', '', text.upper())

    # --- 1. Метод Казиски (Поиск длины ключа) ---
    def kasiski_examination(self, text, seq_len=3):
        text = self._clean(text)
        repeats = {}
        for i in range(len(text) - seq_len):
            seq = text[i:i + seq_len]
            if seq in repeats:
                repeats[seq].append(i)
            else:
                repeats[seq] = [i]

        distances = []
        for seq, positions in repeats.items():
            if len(positions) > 1:
                for i in range(len(positions) - 1):
                    distances.append(positions[i+1] - positions[i])

        if not distances:
            return "Повторов не найдено. Текст слишком короткий."

        def get_factors(n):
            return [i for i in range(2, 21) if n % i == 0]

        factor_counts = Counter()
        for d in distances:
            factor_counts.update(get_factors(d))
        
        return [f[0] for f in factor_counts.most_common(3)]

    # --- 2. Тест Фридмана (Индекс совпадения) ---
    def calculate_ic(self, text):
        n = len(text)
        if n <= 1: return 0
        counts = Counter(text)
        num = sum(f * (f - 1) for f in counts.values())
        return num / (n * (n - 1))

    def friedman_test(self, text, max_len=20):
        text = self._clean(text)
        results = []
        threshold = 0.060 

        for l in range(1, max_len + 1):
            groups = [text[i::l] for i in range(l)]
            avg_ic = sum(self.calculate_ic(g) for g in groups) / l
            results.append((l, avg_ic))

        for l, ic in results:
            if ic > threshold:
                return l, results 
                
        return max(results, key=lambda x: x[1])[0], results

    # --- 3. Частотный анализ по группам ---
    def break_with_scoring(self, ciphertext, key_length):
        ciphertext = self._clean(ciphertext)
        best_key = ""
        
        for i in range(key_length):
            column = ciphertext[i::key_length]
            column_best_char = ''
            max_col_score = -float('inf')

            for char_code in range(26):
                shift_char = chr(char_code + 65)
                decrypted_col = "".join([chr((ord(c) - 65 - char_code) % 26 + 65) for c in column])
                
                score = self.calculate_column_score(decrypted_col)
                
                if score > max_col_score:
                    max_col_score = score
                    column_best_char = shift_char
            
            best_key += column_best_char

        return best_key

    def calculate_column_score(self, column_text):
        # Эталонные частоты (A=0.0817, B=0.0149...)
        english_freqs = [0.0817, 0.0149, 0.0278, 0.0425, 0.1270, 0.0223, 0.0202, 0.0609, 0.0697, 0.0015, 0.0077, 0.0402, 0.0241, 0.0675, 0.0751, 0.0193, 0.0009, 0.0599, 0.0633, 0.0906, 0.0276, 0.0098, 0.0236, 0.0015, 0.0197, 0.0007]
        
        score = 0
        counts = Counter(column_text)
        total = len(column_text)
        for i, freq in enumerate(english_freqs):
            char = chr(i + 65)
            observed = counts.get(char, 0) / total
            score += (observed * freq)
        return score
    

# --- Демонстрация работы ---

attacker = VigenereAttacker()

# Пример длинного шифртекста
sample_cipher = open("text.txt","r").read()
# 1. Определяем длину ключа Казиски
possible_lengths = attacker.kasiski_examination(sample_cipher)
print(f"Метод Казиски предполагает длину ключа: {possible_lengths}")

# 2. Проверяем тестом Фридмана
f_len, f_results = attacker.friedman_test(sample_cipher)
print(f"Тест Фридмана указывает на длину: {f_len}")
if f_len in possible_lengths:
    key_len = f_len
else:
    print("Текс слишком короткий,либо не является английским текстом")
    exit()
# 3. Зная длину , восстанавливаем ключ
final_key = attacker.break_with_scoring(sample_cipher, key_length=key_len)
print(f"Восстановленный ключ: {final_key}")
print(f"Восстановленное сообщение: {VigenereCipher()._process(sample_cipher,final_key,"repeat",False)}")