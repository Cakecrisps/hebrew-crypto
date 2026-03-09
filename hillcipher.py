import numpy as np
import math

MOD = 26

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_invertible(matrix, m):
    det = int(np.round(np.linalg.det(matrix))) % m
    return det != 0 and math.gcd(det, m) == 1

def matrix_mod_inverse(matrix, m):
    n = matrix.shape[0]
    det = int(np.round(np.linalg.det(matrix))) % m
    det_inv = mod_inverse(det, m)
    if det_inv is None:
        raise ValueError("Матрица не обратима по модулю 26.")
    
    adjugate = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
            minor_det = int(np.round(np.linalg.det(minor)))
            adjugate[j, i] = ((-1)**(i+j) * minor_det) % m
    return (det_inv * adjugate) % m

def preprocess_text(text, n):
    clean = "".join([c.upper() for c in text if 'a' <= c.lower() <= 'z'])
    while len(clean) % n != 0:
        clean += 'X'
    return clean

def text_to_vectors(text, n):
    return [np.array([ord(c) - ord('A') for c in text[i:i+n]]) for i in range(0, len(text), n)]

def vectors_to_text(vectors):
    return "".join(chr(int(round(val)) % MOD + ord('A')) for v in vectors for val in v)

def input_matrix(n, label=""):
    print(f"Введите элементы матрицы {label} ({n}x{n}) через пробел:")
    elements = list(map(int, input().split()))
    return np.array(elements).reshape(n, n)


def hill_process(text, key, mode):
    n = key.shape[0]
    clean_text = preprocess_text(text, n)
    vectors = text_to_vectors(clean_text, n)
    
    matrix = matrix_mod_inverse(key, MOD) if mode == '1' else key
    
    res = []
    for v in vectors:
        column = v.reshape(n, 1)
        res_v = np.dot(matrix, column) % MOD
        res.append(res_v.flatten())
    return vectors_to_text(res)

def recurrent_hill_process(text, k1, k2, mode):
    n = k1.shape[0]
    clean_text = preprocess_text(text, n)
    vectors = text_to_vectors(clean_text, n)
    
    keys = [k1, k2]
    res = []
    for i, v in enumerate(vectors):
        if i < 2:
            cur_key = keys[i]
        else:
            # Рекурсия: Ki = Ki-1 * Ki-2 (матричное умножение)
            cur_key = np.dot(keys[i-1], keys[i-2]) % MOD
            keys.append(cur_key)
        
        op_matrix = matrix_mod_inverse(cur_key, MOD) if mode == '1' else cur_key
        
        column = v.reshape(n, 1)
        res_v = np.dot(op_matrix, column) % MOD
        res.append(res_v.flatten())
    return vectors_to_text(res)

def main():
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Шифр Хилла")
        print("2. Рекуррентный шифр Хилла")
        print("0. Выход")
        choice = input("Выбор: ")
        if choice == '0': break
        if choice not in ['1', '2']: continue

        mode = input("Режим (0-Зашифр, 1-Расшифр): ")
        text = input("Текст: ")
        n = int(input("Размерность n: "))

        try:
            if choice == '1':
                k = input_matrix(n, "K")
                if is_invertible(k, MOD):
                    print("Результат:", hill_process(text, k, mode))
                else: print("Матрица не подходит!")
            elif choice == '2':
                k1 = input_matrix(n, "K1")
                k2 = input_matrix(n, "K2")
                if is_invertible(k1, MOD) and is_invertible(k2, MOD):
                    print("Результат:", recurrent_hill_process(text, k1, k2, mode))
                else: print("Матрицы не подходят!")
        except Exception as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    main()