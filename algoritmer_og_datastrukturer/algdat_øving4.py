#4.3-5

#http://stackoverflow.com/questions/280243/python-linked-list
import time
from datetime import datetime

class node:
    def __init__(self):
        self.data = None
        self.next = None


class linked_list:
    def __init__(self):
        self.cur_node = None
        self.first_node = None

    def add_node(self, data):
        new_node = node() #lager ny node
        new_node.data = data #legger inn data til noden
        if self.first_node is None:
            self.first_node = new_node
            self.cur_node = new_node

        tmp_referance = self.cur_node.next  # mellomlagrer referansen til første node
        new_node.next = tmp_referance

        self.cur_node.next = new_node   # refererer den nest siste noden til siste node
        self.cur_node = new_node  # setter siste node som den aktuelle noden

    def get_first_node(self):
        return self.first_node


    def remove_node(self, prev_node, cur_node):
        if cur_node == self.first_node:
            self.first_node = prev_node
        prev_node.next = cur_node.next

    def print_nodes(self):
        cur_node = self.first_node
        while True:
            print(cur_node.data)
            if cur_node.next == self.first_node:
                break
            cur_node = cur_node.next



def JosephProblem(n, step):
    people_list = linked_list()
    for i in range(1,n+1):
        people_list.add_node(i)
    cur_node = people_list.first_node
    prev_node = cur_node
    count = 1
    start = datetime.now()
    while True:
       # print("Data",cur_node.data,"Count",count, "prev_node",prev_node.data,"next_node",cur_node.next.data)
        if count == step:
            prev_node.next = cur_node.next
            #people_list.remove_node(prev_node,cur_node)
            count = 0

        if cur_node == cur_node.next:
            break

        prev_node = cur_node
        cur_node = cur_node.next
        count += 1
    print("Time to find person in line with",n,"people:",(datetime.now()-start))
    return cur_node.data


#Kompleksitet Delta(N*M)



#print(JosephProblem(41,3))



class Stakk:
    def __init__(self):
        self.innhold = []
    def add(self,data):
        self.innhold.append(data)
    def pop(self):
        return self.innhold.pop()
    def peek(self):
        return self.innhold[len(self.innhold)-1]
    def isEmpty(self):
        return self.innhold == []
    def __str__(self):
        print(self.innhold)


def syntax_sjekker(filnavn):
    fil = open(filnavn, 'r')
    stakk = Stakk()
    linje_nummer = 0
    string = False
    substring_open = "[{("
    substring_close = "]})"
    for linje in fil:
        linje_nummer += 1

        char_nummer = 0
        for char in linje:
            char_nummer += 1
            if not string:
                if char == '#':
                    break
                elif substring_open.find(char) >= 0:
                    stakk.add(char)
                elif substring_close.find(char) >= 0:
                    try:
                        if not substring_open.index(stakk.pop()) == substring_close.index(char):
                            return "Error på linje:", linje_nummer, "plass:", char_nummer, "char:", char
                    except:
                        return "Error på linje:", linje_nummer, "plass:", char_nummer, "char:", char
                elif char == '"' or char == "'":
                    string = True
            else:
                if char == '"' or char == "'":
                    string = False
    if stakk.isEmpty():
        return "Fil godkjent, fant ingen feil."
    else:
        return "En klamme er ikke lukket"

print(syntax_sjekker("Binærletning.py"))


