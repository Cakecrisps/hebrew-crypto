from prac1 import afinn,recafinn
from hillcipher import hill_process, text_to_vectors, matrix_mod_inverse, is_invertible
import collections
import heapq
import json
import math
with open('freq_3l.json', 'r') as f:
    ENGLISH_MODEL = json.load(f)
FLOOR = -10.0 

def get_score(text):
    text = "".join(filter(str.isalpha, text.lower()))
    if not text: return -100.0
    
    current_score = 0
    for i in range(len(text) - 2):
        tri = text[i:i+3]
        current_score += ENGLISH_MODEL.get(tri, FLOOR)
        
    return current_score / len(text) 

def brute_afin(text: str,m: int,out_n: int) -> None:
    ans = []
    for a in range(1,m):
        print(f"{(a/35)*100}/100%")
        for b in range(1,m):
            try:
                s,key = afinn(1,[a,b],text),(a,b)
                score = get_score(s)
                ans.append((score,s,key))
                if len(ans) > out_n:
                    ans = sorted(ans,key=lambda x:-x[0])[:out_n]
                print(s,key)
            except:
                pass
    return ans,f"closest key is {ans[0][2]}\ndecoded:{ans[0][1]}"
def brute_recafin(text: str,m: int,out_n: int) -> None:
    ans = []
    for a1 in range(1,m):
        print(f"{(a1/35)*100}/100%")
        for b1 in range(1,m):
            for a2 in range(1,m):
                for b2 in range(1,m):
                    try:
                        s,key = recafinn(1,[a1,b1,a2,b2],text),(a1,b1,a2,b2)
                        score = get_score(s)
                        ans.append((score,s,key))
                        if len(ans) > out_n:
                            ans = sorted(ans,key=lambda x:-x[0])[:out_n]
                    except:
                        pass
    return ans,f"closest key is {ans[0][2]}\ndecoded:{ans[0][1]}"

def freq_anal(s: str):
    return sorted(dict(collections.Counter(s.replace(" ",""))).items(),key = lambda x: -x[1])


sss = "7sdue mzkye mk kmez7q nyeeq rujr s1 rfu zdmlrml8 2ln rqzukurrml8 mlnykrdq. 7sdue mzkye f2k 9uul rfu mlnykrdq'k kr2ln2dn nyeeq rujr u5ud kmlgu rfu b344k, cful 2l yl0lscl zdmlrud rss0 2 8277uq s1 rqzu 2ln kgd2e97un mr rs e20u 2 rqzu kzugmeul 9ss0. mr f2k kyd5m5un lsr sl7q 1m5u gulrydmuk, 9yr 27ks rfu 7u2z mlrs u7ugrdslmg rqzukurrml8, due2mlml8 ukkulrm277q ylgf2l8un. mr c2k zszy72dmkun ml rfu bva4k cmrf rfu du7u2ku s1 7urd2kur kfuurk gslr2mlml8 7sdue mzkye z2kk28uk, 2ln esdu dugulr7q cmrf nuk0rsz zy97mkfml8 ks1rc2du 7m0u 27nyk z28ue20ud mlg7ynml8 5udkmslk s1 7sdue mzkye."



import numpy as np

def brute_hill_2x2(ciphertext, out_n):
    """Брутфорс шифра Хилла 2x2"""
    ans = []
    m = 26
    
    # Перебор всех элементов матрицы K = [[a, b], [c, d]]
    for a in range(m):
        for b in range(m):
            for c in range(m):
                for d in range(m):
                    key = np.array([[a, b], [c, d]])
                    
                    # Проверка на обратимость матрицы
                    det = (a * d - b * c) % m
                    if det != 0 and math.gcd(det, m) == 1:
                        try:
                            # Пробное расшифрование
                            decrypted = hill_process(ciphertext, key, mode='1')
                            score = get_score(decrypted)
                            ans.append((score, decrypted, key.flatten()))
                            
                            # Ограничение списка лучших результатов
                            if len(ans) > out_n:
                                ans = sorted(ans, key=lambda x: -x[0])[:out_n]
                        except:
                            continue
    
    return ans

# Пример вызова:
results = brute_hill_2x2("XOLCIMVQSWACAYDVBMRCUGZNDTVEUBHISLLDDAFENNOXNTOURZDAFELDRCHBTYXOLCIMVQSWVOFPYCSRHILDRCHBTYEWFMWPZHSVSWEORGWLXJLPAYTKRZHIQQHINAVWRYDSBFSLLDRGEZGUEUSMOZGYFBZCFYNNLSFLKIKFVXDHVEKYQOFRNTOUFYESWSQFGUCIAVCMKGKJJRVXDSVEUDJVJRSSZVNIXWOULYFMJIVTHITQTXLDVETLSSETDPEAZCFYOEKDLDRTWQYOLOFEOUOESRYQOZCSTKVOFEVXDHOSVHJZPRZHACVXLDAVOUMGAVAVLPTLMIOEFBTQETCMRZXTYCHYWWSRYOLOFEXOLCIMVQSWTEEWSEOUNNTOPJLPSSZVMPICDHEDOUJLJZBAKFACTCFESCUBOSLCFKQOHDRCVHSEWQEYLPLDNHRDLDDNLPAYDPSCWNPJWQRNKGBJ", 5)
print(f"Closest key: {results[0][2]}, Decoded: {results[0][1]}")
