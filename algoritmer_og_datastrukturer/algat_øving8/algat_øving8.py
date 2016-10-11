import heapq
from itertools import count
from datetime import datetime

#Class to represent a Node and its first edge
class Node():
    id = "0"
    edge1 = None
    d = None
    def __init__(self,id):
        self.id = id

    def __lt__(self, other):
        return self.d.dist < other.d.dist

#Class to represent distance to previous edge, including previous node
class Prev():
    dist = None
    prev = None

    infinity = 1000000000

    def find_dist(self):
        return self.dist

    def __init__(self):
        self.dist = self.infinity

    def __lt__(self, other):
        return self.dist < other.dist

#Class to represent a weighted edge, stores next edge as variable
class WEdge():

    end = None
    next = None
    weight = None
    def __init__(self,end,next, weight):
        self.next = next
        self.end = end
        self.weight = weight

#Priority queue with implementation for updating priorities
class PriorityQue(object):
    def __init__(self, nodes=[]):
        self.counter = count()
        self.heap = []
        self.entry_finder = dict()
        for node in nodes:
            entry = [node.d.dist,next(self.counter), node]
            self.add_node2(entry)
        self.REMOVED = '<remove_marker>'

    def add_node(self,node,priority=0):
        if node in self.entry_finder:
            self.remove_node(node)
        count = next(self.counter)
        entry = [priority,count,node]
        self.entry_finder[node] = entry
        heapq.heappush(self.heap,entry)

    #Add a node using already created entry, useful for initialization
    def add_node2(self,entry):
        if entry[-1] in self.entry_finder:
            self.remove_node(entry[-1])
        self.entry_finder[entry[-1]] = entry
        heapq.heappush(self.heap,entry)

    def remove_node(self,node):
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED


    def pop_node(self):
        while self.heap:
            priority, count, node = heapq.heappop(self.heap)
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return node
        raise KeyError('pop from an empty priority queue')

class Graph():

    def __init__(self, filename):
        self.N = None
        self.K = None
        self.nodes = self.read_file(filename)
        self.pQue = None

    def shorten(self,node,edge):
        prev1 = node.d
        prev2 = edge.end.d
        if prev2.dist > prev1.dist + edge.weight:
            prev2.dist = prev1.dist+edge.weight
            prev2.prev = node
            self.pQue.add_node(edge.end, priority=prev2.dist)

    def initprev(self,s):
        for i, node in enumerate(self.nodes):
            self.nodes[i].d = Prev()
        s.d.dist = 0

    #Opens file, formats input and adds to class variables
    def read_file(self,filename):

        file = open(filename,'r')
        info = file.readline().split(" ")
        for entry in info:
            entry.replace("\n","")
        self.N = int(info[0])
        self.K = int(info[1])
        nodes = []
        for i in range(int(self.N)):
            nodes.append(Node(i))
        lines = file.read().split("\n")
        for line in lines:
            if line:
                l = list(filter(None, line.split(" "))) #filters out input equal to none (empty strings) and returns a list
                fra, til, weight = list(map(int,l))
                e = WEdge(nodes[til],nodes[fra].edge1, weight)
                nodes[fra].edge1 = e
        return nodes

    def dijkstra(self,s):
        self.initprev(self.nodes[s])
        self.pQue = PriorityQue(self.nodes)
        for i in reversed(range(1,len(self.nodes))):
            node = self.pQue.pop_node()
            wEdge = node.edge1
            while wEdge:
                self.shorten(node, wEdge)
                wEdge = wEdge.next

def main1():
    nodenummer = 0
    filnavn = "vg4.txt"
    start = datetime.now()
    print("-----READING FILE------")
    graph = Graph(filnavn)
    filereadtime = datetime.now() - start
    start = datetime.now()
    print("-----RUNNING ALGORITHM------")
    graph.dijkstra(nodenummer)
    nodes = graph.nodes
    alorithmtime = datetime.now() - start
    print("-----PRINTING OUTPUT------")
    print("Node | Forgj | Dist")
    for i in range(len(nodes)):
        if nodes[i].d.prev is not None:
            print(i,"   |  ",nodes[i].d.prev.id,"  |  ",nodes[i].d.dist)
        elif i == nodenummer:
            print(i, "   | start |  ", nodes[i].d.dist)
        else:
            print(i, "   |       |  nåes ikke")

    print("File reading execution time for",filnavn,":",filereadtime.seconds,"s")
    print("Algorithm execution time for",filnavn,":",alorithmtime.seconds,"s")

main1()