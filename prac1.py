import math
from string import ascii_lowercase,digits

m = 36
alf = digits + ascii_lowercase
print(alf)
def valid(c_type,key):
    if c_type == 0 and len(key) != m:raise(ValueError(f"Ключ для простой замены должен содержать {m} значений"))
    if c_type != 0: 
        if len(key) != 2 and len(key)!= 4:raise(ValueError("Ключ для афиныых шифров должен быть длинной 2"))
        if not (str.isdigit(key[0]) and str.isdigit(key[1])): raise(ValueError("Ключи должны быть числами"))
        if int(key[2]) == 0:raise(ValueError("a = 0"))
        if math.gcd(int(key[2]),m) != 1:raise(ValueError(f"a1 должно быть взаимно простым с {m}"))
    if c_type == 2:
        if len(key) != 4:raise(ValueError("должно быть 4 символа через пробел в ключе"))
        if key[2] == "0":raise(ValueError(f"a2 = 0"))
        if math.gcd(int(key[2]),m) != 1:raise(ValueError(f"a2 должно быть взаимно простым с {m}"))


def stupid(mode,key,msg):
    if mode == 0:return "".join([key[alf.index(x)] if x != " " else " " for x in msg])
    if mode == 1:return "".join([alf[key.index(x)] if x != " " else " " for x in msg])

def afinn(mode,key,msg):
    a,b = map(int,key)
    if mode == 0:return "".join([alf[(a * alf.index(x) + b)%m] if x != " " else " " for x in msg])
    if mode == 1:return "".join([alf[(pow(a,-1,m) * (alf.index(x) - b)%m)] if x != " " else " " for x in msg])

def recafinn(mode,key,msg):

    a1,b1,a2,b2 = map(int,key)
    keys = [(a1,b1),(a2,b2)]
    res = ""

    for i in range(len(msg)):

        if msg[i] == " ":
            res += " "
            continue
        
        a,b = (keys[-1][0]*keys[-2][0])%m,(keys[-1][1] + keys[-2][1])
        
        if i > 1:
            keys.pop(0)
            keys.append((a,b))

        if mode == 0:res += alf[(a * alf.index(msg[i]) + b)%m]
        else: res += alf[(pow(a,-1,m) * (alf.index(msg[i]) - b))%m]
    return res

c_type = int(input("Вид шифра (0 - простая замена, 1 - афинный шифр, 2 - рекурентный афинный шифр): "))
mode = int(input("Режим (0-Encode, 1-Decode): "))
key = (input(f"Ключ ({m} значений через пробел[0-9A-Z] | 2 значения через пробел | 4 значения через пробел): ")).lower().strip().split()
msg = input("Текст: ").lower()
valid(c_type,key)
match c_type:
    case 0:
        print(stupid(mode,key,msg))
    case 1:
        print(afinn(mode,key,msg))
    case 2:
        print(recafinn(mode,key,msg))
    case _:
        raise(ValueError("вид шифра должен принадлежать[0,2]"))





