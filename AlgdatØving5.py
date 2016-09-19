import random
from timeit import default_timer as timer

#Creates an integer-value using ascii value of chars
def ascii_value(text):
    total_value = 0
    for char_numb in range(0,len(text)):
        total_value += ord(text[char_numb]) * (pow(2,char_numb))
        """adds ascii value times an incrementing value to differenciate words with
            identical chars but different arrangement"""
    return total_value

def read_file(filename):
    output = []
    try:
        f = open(filename,'r')  #reads file
        for line in f:
            output.append(line) #add names to list
    except FileNotFoundError:
        print("Filen ble ikke funnet")
    except IOError:
        print("Feil med lesing av filen")
    except Exception:
        print("En feil har oppstått")
    return output

#finds key using mod
def find_key1(total_value,size):
    return total_value % size

def find_key2(total_value,size):
    return (total_value % (size-1))+1

#Adds string object to hashtable
def add1(text, ht):
    total_value = ascii_value(text)
    size = len(ht)
    h1 = find_key1(total_value,size)
    if(ht[h1] == ""):
        ht[h1] = text
        return [h1,0]
    print("Kollisjon!", text,ht[h1])
    h2 = find_key2(total_value,size)
    for i in range(1,size):
        j = (h1+i*h2) % size
        if(ht[j] == ""):
            ht[j] = text
            return [j,1]

    return [-1,1]

#Searches for matching name in hashtable
def find_name(name,ht):
    m = len(ht)
    total_value = ascii_value(name)
    h1 = find_key1(total_value,m)
    if(name == ht[h1]):
        return "Fant",name,"på plass nr",h1
    h2 = find_key2(total_value,m)
    for i in range(1,m):
        j = (h1+i*h2) % m
        if(ht[j] == name):
            return "Fant",name,"på plass nr",j
    return "Person ikke funnet"

#Adds integer to hashtable
def add2(numb, ht):
    m = len(ht)
    h1 = find_key1(numb,m)
    if(ht[h1] == 0):
        ht[h1] = numb
        return h1
    h2 = find_key2(numb,m)
    for i in range(1,m):
        j = (h1+i*h2) % m
        if(ht[j] == 0):
            ht[j] = numb
            return j

    return -1

#Runs second task
def main2():
    ht = [0]*11000027
    numbs = [random.randint(1,100000000) for r in range(120000)]
    start = timer()
    for numb in numbs:
        add2(numb,ht)
    print("Tid for 12 millioner nummer:",timer() - start,"s")

    ht = [0] * 11000027

    py_ht = {}
    start = timer()
    for i in range(len(numbs)):
        py_ht.update({numbs[i]:i})
    print("Tid for 12 millioner nummer:",timer() - start,"s")



#runs first task
def main1():
    collitions = 0
    ht = [""]*107
    size = len(ht)
    names = read_file('navn.txt')
    keys = [0]*len(names)
    for i in range(len(names)):
        names[i] = names[i].replace("\n","")
        result = add1(names[i],ht)
        collitions += result[1]
        if result[0] == -1:
            print("Klarte ikke legge til i hashtable",names[i])

    print("Antall kollisjoner =",collitions,"Lastfaktor =",len(names)/size)

    while True:
        name = input("Skriv inn navn på personen: ")
        print(find_name(name,ht))

if __name__ == '__main__':
    main1()
    main2()




