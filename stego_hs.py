import numpy as np
from PIL import Image
import argparse
import sys
from skimage.metrics import peak_signal_noise_ratio as psnr_metric
from skimage.metrics import structural_similarity as ssim_metric
import matplotlib.pyplot as plt

def calculate_ber(original_bits, extracted_bits):
    if len(original_bits) != len(extracted_bits):
        min_len = min(len(original_bits), len(extracted_bits))
        original_bits = original_bits[:min_len]
        extracted_bits = extracted_bits[:min_len]
    
    errors = sum(1 for a, b in zip(original_bits, extracted_bits) if a != b)
    
    ber = errors / len(original_bits)
    return ber

def plot_histograms(original_channel, stego_channel):
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.hist(original_channel.flatten(), bins=256, color='blue', alpha=0.7)
    plt.title("Гистограмма ДО")
    
    plt.subplot(1, 2, 2)
    plt.hist(stego_channel.flatten(), bins=256, color='red', alpha=0.7)
    plt.title("Гистограмма ПОСЛЕ")
    
    plt.show()

def str_to_bits(s):
    bits = []
    for char in s.encode('utf-8'):
        bin_val = bin(char)[2:].zfill(8)
        bits.extend([int(b) for b in bin_val])
    return bits

def bits_to_str(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8: break
        chars.append(int(''.join(map(str, byte)), 2))
    return bytes(chars).decode('utf-8', errors='ignore')

def get_histogram_params(channel):
    # Находим гистограмму
    hist = np.bincount(channel.flatten(), minlength=256)
    p = np.argmax(hist)
    z = np.argmin(hist)
    max_bits = hist[p] # Максимальная емкость - это высота пика P
    return int(p), int(z), int(max_bits)


def embed(img_path, message, output_path):
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)
    
    # Работаем с зеленым каналом (G)
    channel = img_array[:, :, 1].copy()
    p, z, mc = get_histogram_params(channel)
    
    message_bits = str_to_bits(message)
    
    if p < z:
        channel[(channel > p) & (channel < z)] += 1
        shift = 1
    else:
        channel[(channel > z) & (channel < p)] -= 1
        shift = -1
        
    bits_embedded = 0
    h, w = channel.shape
    for i in range(h):
        for j in range(w):
            if bits_embedded < len(message_bits):
                if channel[i, j] == p:
                    if message_bits[bits_embedded] == 1:
                        channel[i, j] += shift
                    bits_embedded += 1
            else: break
        if bits_embedded >= len(message_bits): break
        
    stego_array = img_array.copy()
    stego_array[:, :, 1] = channel
    
    metrics = calculate_metrics(img_array, stego_array, len(message_bits))
    
    # Сохранение
    Image.fromarray(stego_array).save(output_path)
    with open(f"{output_path}_stat.txt","w") as f:
        f.write(f'{" ".join(map(str, message_bits))}\n{p}\n{z}')
    print(f"--- Результаты встраивания ---")
    print(f"Параметры (нужны для извлечения): P={p}, Z={z}, Bits={len(message_bits)}")
    print(f"MSE: {metrics['MSE']:.4f}")
    print(f"PSNR: {metrics['PSNR']:.2f} dB")
    print(f"SSIM: {metrics['SSIM']:.4f}")
    print(f"Capacity (EC): {metrics['EC']:.4f} bpp")
    print(f"Максимальное место: {mc} bits\nМаксимально кол-во символов: {mc//8} chars")
    print(f"Стегоизображение сохранено в: {output_path}")
    plot_histograms(img_array[:,:,1],stego_array[:,:,1])

def extract(img_path, p, z, bit_len, is_compare):
    stego = Image.open(img_path).convert('RGB')
    stego_array = np.array(stego)
    channel = stego_array[:, :, 1]
    
    extracted_bits = []
    shift = 1 if p < z else -1
    
    idx = 0
    h, w = channel.shape
    for i in range(h):
        for j in range(w):
            if idx < bit_len:
                if channel[i, j] == p:
                    extracted_bits.append(0)
                    idx += 1
                elif channel[i, j] == p + shift:
                    extracted_bits.append(1)
                    idx += 1
            else: break
        if idx >= bit_len: break
            
    print(f"Извлеченное сообщение: {bits_to_str(extracted_bits)}")
    if(is_compare):
        if "___" in img_path:
            stat_path = img_path[:img_path.index("___")] +".png_stat.txt"
        else:
            stat_path = f"{img_path}_stat.txt"
        with open(stat_path,"r") as f:
            et_bits = [int(b) for b in f.readline().split()]
        print("---Сравнение с эталоном--")
        print(f"Кол-во битов эталона: {len(et_bits)}")
        print(f"Кол-ва битов вывода: {len(extracted_bits)}")
        print(f"Error per bit: {calculate_ber(et_bits,extracted_bits)}")

def calculate_metrics(orig, stego, b):
    mse = np.mean((orig.astype(float) - stego.astype(float)) ** 2)
    # PSNR по формуле из задания 
    psnr = 10 * np.log10((255**2) / mse) if mse > 0 else 100
    ssim = ssim_metric(orig, stego, channel_axis=2)
    # EC: биты / общее кол-во пикселей 
    ec = b / (orig.shape[0] * orig.shape[1])
    return {"MSE": mse, "PSNR": psnr, "SSIM": ssim, "EC": ec}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HS Steganography CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Команда встраивания
    embed_parser = subparsers.add_parser('embed')
    embed_parser.add_argument("input", help="Путь к исходному изображению")
    embed_parser.add_argument("message", help="Текст сообщения")
    embed_parser.add_argument("--out", default="stego.png", help="Путь к выходному файлу")

    # Команда извлечения
    extract_parser = subparsers.add_parser('extract')
    extract_parser.add_argument("input", help="Путь к стегоизображению")
    extract_parser.add_argument("p", type=int, help="Параметр P")
    extract_parser.add_argument("z", type=int, help="Параметр Z")
    extract_parser.add_argument("len", type=int, help="Длина сообщения в битах")
    extract_parser.add_argument("-c", "--compare", action="store_true", help="Сравнить результат с эталоном")
    args = parser.parse_args()

    if args.command == 'embed':
        embed(args.input, args.message, args.out)
    elif args.command == 'extract':
        extract(args.input, args.p, args.z, args.len,args.compare)
    else:
        parser.print_help()