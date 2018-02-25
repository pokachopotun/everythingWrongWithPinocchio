import queue



class graph:
    def __init__(self):
        self.g = dict()

    def add_vertex(self, v):
        if(v in self.g):
            raise Exception("vertex already exists: " + str(v))
        self.g[v] = dict()

    def add_edge(self, from_i, to_i, w):
        if(from_i not in self.g):
            raise Exception("no such vertex: " + str(from_i))
        if (to_i not in self.g):
            raise Exception("no such vertex: " + str(to_i))
        if(to_i not in self.g[from_i]):
            self.g[from_i][to_i] = dict()
        if(w not in self.g[from_i][to_i]):
            self.g[from_i][to_i][w] = 0
        self.g[from_i][to_i][w] += 1

    def remove_edge(self, from_i, to_i, w):
        if( from_i in self.g):
            if(to_i in self.g[from_i]):
                if(w in self.g[from_i][to_i]):
                    self.g[from_i][to_i][w] -= 1
                    if(self.g[from_i][to_i][w] == 0):
                        self.g[from_i][to_i].pop(w)
                if(len(self.g[from_i][to_i]) == 0):
                    self.g[from_i].pop(to_i)

    def check_vertex(self, v):
        return v in self.g

    def is_connected(self, from_i, to_i):
        flag = self.check_vertex(from_i) and self.check_vertex(to_i)
        if(not flag):
            return False
        return to_i in self.g[from_i]

    def is_connected_weight(self, from_i, to_i, w):
        if not self.check_vertex(from_i) or not self.check_vertex(to_i):
            return False
        used = [False for i in range(len(self.g))]

        q = queue.Queue()
        q.put(from_i)
        used[from_i] = True
        while(not q.empty()):
            v = q.get()
            if(v == to_i):
                return True
            for to in self.g[v]:
                if(used[to]):
                    continue
                if(w in self.g[v][to]):
                    q.put(to)
                    used[to] = True
        return False

if __name__ == "__main__":
    g = graph()
    g.add_vertex(0)
    g.add_vertex(1)
    g.add_vertex(2)

    g.add_edge(0, 1, 10)
    g.add_edge(0, 1, 5)
    g.add_edge(1, 2, 10)
    g.add_edge(1, 2, 2)
    print(g.is_connected_weight(0, 2, 10))
    print(g.is_connected_weight(0, 2, 5))

    print( g.g )