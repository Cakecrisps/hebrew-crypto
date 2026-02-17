from prac1 import afinn,recafinn




def brute_afin(text: str,m: int) -> None:
    for a in range(1,m):
        for b in range(1,m):
            try:
                print(afinn(1,[a,b],text),(a,b))
            except:
                pass

def brute_recafin(text: str,m: int) -> None:
    for a1 in range(1,m):
        for b1 in range(1,m):
            for a2 in range(1,m):
                for b2 in range(1,m):
                    try:
                        print(recafinn(1,[a1,b1,a2,b2],text),(a1,b1,a2,b2))
                    except:
                        pass
