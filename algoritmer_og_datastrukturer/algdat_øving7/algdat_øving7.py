from collections import deque

class Node():
    id = 0
    edge1 = None
    d = None
    def __init__(self,id):
        self.id = id

class Edge():
    end = None
    next = None
    def __init__(self,end,next):
        self.next = next
        self.end = end


class Prev():
    dist = None
    prev = None

    infinity = 1000000000

    def find_dist(self):
        return self.dist

    def __init__(self):
        self.dist = self.infinity

class Topo_1st():
    found = None
    next = None
    id = None
    def __init__(self,id):
        self.id = id


class Graph():
    N = None
    K = None
    nodes = []

    def initprev(self,s):
        for i in range(self.N-1,-1,-1):
            self.nodes[i].d = Prev()
        s.d.dist = 0

    #Opens file, formats input and adds to class variables
    def read_file(self,filename):
        file = open(filename,'r')
        info = file.readline().split(" ")
        self.N = int(info[0])
        self.K = int(info[1])
        self.nodes = []
        for i in range(int(self.N)):
            self.nodes.append(Node(i))
        lines = file.read().split("\n")
        for line in lines:
            if line:
                l = list(filter(None, line.split(" "))) #filters out input equal to none (empty strings) and returns a list
                fra, til = list(map(int,l))
                e = Edge(self.nodes[til],self.nodes[fra].edge1)
                self.nodes[fra].edge1 = e
        return self.nodes



    def bfs(self,s):
        self.initprev(self.nodes[s])
        queue = deque([])
        queue.append(self.nodes[s])
        while len(queue) != 0:
            n = queue.popleft()
            e = n.edge1
            while e is not None:
                f = e.end.d
                if f.dist == f.infinity:
                    f.dist = n.d.dist + 1
                    f.prev = n
                    queue.append(e.end)
                e = e.next
        return self.nodes


    def df_topo(self,n,l):
        nd = n.d
        if(nd.found):return l
        nd.found = True
        e = n.edge1
        while e:
            l = self.df_topo(e.end,l)
            e = e.next
        nd.next = l
        return n

    def topologisort(self):
        l = None
        count = 0
        for node in reversed(self.nodes):
            node.d = Topo_1st(count)
            count += 1
        for i in reversed(range(self.N)):
            l = self.df_topo(self.nodes[i],l)

        return l



def main2():
    nodenummer = 5
    filnavn = "L7g5.txt"
    graph = Graph()
    n = graph.read_file(filnavn)
    l = graph.topologisort()
    print("Node")
    while l:
        print(l.d.id)
        l = l.d.next

def main1():
    nodenummer = 5
    filnavn = "L7g3.txt"
    graph = Graph()
    n = graph.read_file(filnavn)
    nodes = graph.bfs(nodenummer)

    print("Node | Forgj | Dist")
    for i in range(len(nodes)):
        if nodes[i].d.prev is not None:
            print(i,"   |  ",nodes[i].d.prev.id,"  |  ",nodes[i].d.dist)


#main1()
main2()