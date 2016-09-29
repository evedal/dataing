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

class Graph():
    N = None
    K = None
    nodes = []

    def initprev(self,s):
        for i in range(self.N-1,-1,-1):
            self.nodes[i].d = Prev()
        s.d.dist = 0

    def read_file(self,filename):
        file = open(filename,'r')
        info = file.readline().split(" ")
        self.N = int(info[0])
        self.K = int(info[1])
        self.nodes = []
        for i in range(int(self.N)):
            self.nodes.append(Node(i))

        for i in range(self.K):
            line = file.readline().split(" ")

            fratil = []
            for n in line:
                if n is not '':
                    fratil.append(n.replace("\n",""))
            fra = int(fratil[0])
            til = int(fratil[1])
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
            while e.next is not None:
                f = e.end.d
                if f.dist == f.infinity:
                    f.dist = n.d.dist + 1
                    f.prev = n
                    queue.append(e.end)
                e = e.next
        return self.nodes




def main():
    nodenummer = 5
    filnavn = "L7g1.txt"
    graph = Graph()
    nodes = graph.read_file(filnavn)
    nodes = graph.bfs(nodenummer)
    print("Node | Forgj | Dist")
    for i in range(len(nodes)):
        if nodes[i].d.prev is not None:
            print(i,"   |  ",nodes[i].d.prev.id,"  |  ",nodes[i].d.dist)



main()