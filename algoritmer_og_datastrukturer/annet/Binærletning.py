import random
import time

n = [int(100*random.random()) for i in range(10)]
sortedN = [0]*len(n)

for i in range(len(n)-1,0,-1):
    for j in range(i):
        if n[j] > n[j+1]:
            tmp1 = n[j]
            tmp2 = n[j+1]
            n[j] = tmp2
            n[j+1] = tmp1
printn)


def findNumber(n, element, min=0, max=len(n)):
    tmp = max-(int)((max-min)/2)
    print(min,max)
    if min >= max:
        print("Fant ikke tallet")
    elif n[tmp] == element:
        print("Fant objectet på index:", tmp)
    elif n[tmp] > element:
        findNumber(n,element,min,tmp)
    else:
        findNumber(n,element,tmp,max)

findNumber(n,39)