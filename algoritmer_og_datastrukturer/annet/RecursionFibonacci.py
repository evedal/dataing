def findNumber(numb):
    for i in range(0,10):
        if fib(i,numb) < 0:
            return i

def fib(n,numb):
    if n == numb:
        return -1
    if n == numb:
        return numb
    elif n == 0:
        return 0
    else:
        return fib(n-1,numb) + fib(n-2,numb)

def findFibSequence(valueOfOne):
    for i in range(1,10):
        
print("Startnumber:",findNumber(9))