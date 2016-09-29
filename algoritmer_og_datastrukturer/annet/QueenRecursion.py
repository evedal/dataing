maks = 25
plass = [0]*maks

def lovlig(r,k):
    for i in range(r):
        y = plass[i]
        if y == k:
            return False
        if i-y == r-k:
            return False
        if i+y == r+k:
            return False
    return True


def plassering(rad):
    if rad == maks:
        return True
    for kol in range(maks):
        if lovlig(rad,kol):
            plass[rad] = kol
            funnet = plassering(rad+1)
            if(funnet):
                return True

    return False

if plassering(0):
    for i in range(maks):
        print("(",i,",_",plass[i],")_")
else:
    print("Ikke funnet løsning.")