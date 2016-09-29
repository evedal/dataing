class Node():
    edges = []
    def add_edge(self,start,end):
        self.edges.append(Edge(start, end))
class Edge():
    start = None
    end = None
    def __init__(self, start,end):
        self.start = start
        self.end = end
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end

class Prev():
    dist = None
    prev = None
    infinity = 1000000000;

    def find_dist(self):
        return self.dist

    def find_prev(self):
        return self.prev

    def __init__(self):
        self.dist = self.infinity


class Graph():

    def __init__(self):
        pass
    def read_file(self,filename):
        file = open(filename,'r')
        out = [len(file)]
        for line in file:


