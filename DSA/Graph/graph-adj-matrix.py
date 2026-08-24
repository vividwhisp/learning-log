class Graph:
    def __init__(self, vertex):
        self.mat = [ [0]*vertex for x in range(vertex) ]
        self.size = vertex

    def add_edge(self, src, dest):
        if 0<= src < self.size and 0<= dest < self.size:
            self.mat[src][dest] = 1
            self.mat[dest][src] = 1
        else:
            print("Invalid Edge")

    def printGraph(self):
        for row in self.mat:
            print(' , '.join(map(str, row)))

g = Graph(5)
g.add_edge(0,1)
g.add_edge(0,2)
g.add_edge(1,3)
g.add_edge(2,4)
g.add_edge(3,4)
g.add_edge(2,3)
g.printGraph()

        