from random import randrange
from datetime import datetime

def shellsort(n, t):
    s = n//2
    while s > 0:
        for i in range(s,n):
            j = i
            flytt = t[i]
            while j >= s and flytt < t[j-s]:
                t[j] = t[j-s]
                j -= s
            t[j] = flytt

        if s == 2:
            s = 1
        else:
            #s = int(s//2.8)
            #"""
            s = int(s//2)
            if s % 2 == 0 and s != 0:
                if s != 1:
                    s += 1

#"""

def countSort(n,t):
    index = 0
    ht = [0]*n
    for i in range(len(t)):
        ht[t[i]] += 1
    for i in range(len(ht)):
        for j in range(ht[i]):
            t[index] = i
            index += 1


def quickSort(t, v, h):
    m = median3sort(t,v,h)
    dv = t[m]
    bytt(t,m,h-1)
    while True:
        iv = v
        ih = h-1
        while t[++iv] < dv:
            pass
        while t[--ih] > dv:
            pass
        if(iv >= ih):
            break
        bytt(t,iv,h-1)
    bytt(t,iv,h-1)
    return iv


def bytt(t,t1,t2):
    tmp = t[t1]
    t[t1] = t[t2]
    t[t2] = tmp

def median3sort(t,v,h):
    m = (int)(v+h)//2
    if t[v] > t[m]:
        bytt(t,v,m)
    if t[m] > t[h]:
        bytt(t,m,h)
        if t[v] > t[m]:
            bytt(t,m,v)
    return m



runder = 0
start = datetime.now()
ekstratid = datetime.now() - datetime.now()
while True:
    startekstra = datetime.now()
    t = [0]*100000
    for i in range(100000):
        t[i] = randrange(0,999)
    ekstratid += datetime.now()-startekstra
    #countSort(1000,t)
    shellsort(len(t),t)
    #quickSort(t,0,len(t)-1)
    for i in range(len(t)-2):
        if t[i+1] < t[i]:
            print("Funker ikke!")
    runder += 1
    if(datetime.now()- ekstratid - start).total_seconds() >= 3:
        break
print("Tid per runde:",(datetime.now() - start - ekstratid)/runder,"Antall runder:",runder)

"""
s = 2.8
t1 = 0.119999 n1 = 10 000
t2 = 1.370945 n2 = 100 000
t3 = 15.704279 n3 = 1 000 000

-------

n3/n2 = 10
t3/t2 = 11.4551

O(n^x) --> 10^x = 11.4551 --> x = log(11.4551)/log(10)

x = 1.0590

------

n2/n1 = 10
t1/t1 = 11.4246

O(n^x) --> 10^x = 11.4246 --> x = log(11.4246)/log(10)

x = 1.05784

--------

s = 2 then +1 if even
t1 = 0.110791 n1 = 10 000
t2 = 1.759459 n2 = 100 000
t3 = 28.973018 n3 = 1 000 000

-------

n3/n2 = 10
t3/t2 = 16.8809

O(n^x) --> 10^x = 16.46700 --> x = log(16.46700)/log(10)

x = 1.2166

------

n2/n1 = 10
t1/t1 = 11.4246

O(n^x) --> 10^x = 11.4246 --> x = log(11.4246)/log(10)

x = 1.05784


Testdata:
s = 2.8, tid = 0.008863s ved n=1000
n^x når n = 1000
1000^x = 0.008863
x = -0.687996                                       23.59
---
s = 2.8, tid = 0.119999s ved n=10000
n^x når n = 10000
10000^x = 0.119999
x = -0.230206

s = 2.8, tid = 0.119999s ved n=100 000
n^x når n = 100 000
10000^x = 1.370945
x = 0.027404

s = 2.8, tid = 15.704279s ved n=1 000 000
n^x når n = 1 000 000
1000000^x = 15.704279
x = 0.199336

s = 2.2, tid = 17.888923s ved n=1 000 000
n^x når n = 1 000 000
10000^x = 17.888923
x = 0.208764

n = 100 000
100000^(3/2) =

n^x = t
0.2

n^x * n^y = n^x+y



n^7/6 - n^5/4

n^(7/6 - 5/4)

10 000 000^0.2 =


"""