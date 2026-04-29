import re

class VigenereCipher:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.n = len(self.alphabet)

    def _clean_text(self, text):
        """Оставляет только латиницу и переводит в верхний регистр."""
        return re.sub(r'[^A-Z]', '', text.upper())

    def _process(self, text, key, mode, encrypt=True):
        text = self._clean_text(text)
        key = self._clean_text(key)
        if not text or not key:
            return "Ошибка: текст и ключ должны содержать латинские буквы."

        result = []
        text_idxs = [ord(c) - 65 for c in text]
        gamma = [ord(c) - 65 for c in key]
        
        step = 1 if encrypt else -1

        for i in range(len(text_idxs)):
            if mode == 'repeat':
                g_idx = gamma[i % len(gamma)]
            else:
                g_idx = gamma[i]

            # Основная формула: C = (P + G) mod 26 или P = (C - G) mod 26
            res_idx = (text_idxs[i] + step * g_idx) % self.n
            result.append(chr(res_idx + 65))

            if mode == 'autokey_plain':
                p_idx = text_idxs[i] if encrypt else res_idx
                gamma.append(p_idx)
            elif mode == 'autokey_cipher':
                c_idx = res_idx if encrypt else text_idxs[i]
                gamma.append(c_idx)

        return "".join(result)

    def run(self):
        modes = {
            '1': ('repeat', 'Повторение лозунга'),
            '2': ('autokey_plain', 'Самоключ по открытому тексту'),
            '3': ('autokey_cipher', 'Самоключ по шифртексту')
        }

        while True:
            print("\n--- Виженер (A-Z) ---")
            for k, v in modes.items(): print(f"{k}. {v[1]}")
            print("0. Выход")
            
            m_choice = input("Выбор метода: ")
            if m_choice == '0': break
            if m_choice not in modes: continue

            action = input("1. Зашифровать, 2. Расшифровать: ")
            is_enc = action == '1'
            
            txt = input("Введите текст: ")
            k = input("Введите ключ: ")

            res = self._process(txt, k, modes[m_choice][0], encrypt=is_enc)
            with open("text.txt","w") as f:
                f.write(res)
            print(f"\nРЕЗУЛЬТАТ: {res}")

if __name__ == "__main__":
    VigenereCipher().run()