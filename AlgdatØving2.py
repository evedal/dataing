from datetime import datetime
from math import pow
#Oppgave 2.1-1

def calc(x, n):
    if n == 0:
        return 1
    else:
        return x*calc(x, n-1)



def calc2(x,n):
    if n == 0:
        return 1
    elif n % 2 == 0:
        return calc2(x*x,n/2)
    else:
        return x*calc2(x*x,(n-1)/2)


runder = 0
start = datetime.now()  # Starter tidtakning
while True:
    calc(2,100)
    runder += 1
    if (datetime.now() - start).total_seconds() > 1:
        print("Enkel algoritme:",(datetime.now() - start)/runder)
        break

runder = 0
start = datetime.now()
while True:
    calc2(2,100)
    runder += 1
    if (datetime.now() - start).total_seconds() > 1:
        print("Avansert algoritme:",(datetime.now() - start)/runder)
        break

runder = 0
start = datetime.now()
while True:
    pow(2,100)
    runder += 1
    if (datetime.now() - start).total_seconds() > 1:
        print("Pythons algoritme:",(datetime.now() - start)/runder)
        break

print(calc2(2,100))





def palidrom(ord):
    if len(ord) == 0 or len(ord) == 1:
        print("Ordet er et palidrom")
    else:
        if ord[0] == ord[-1]:
            return palidrom(ord[1:-1])
        else:
            print("Ordet er ikke et palidrom")

#palidrom("redder")


