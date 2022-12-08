class Graph:
    def __init__(self):
        self.rep = {}
        self.rep2 = {}

    def __str__(self):
        return str(self.rep)

    def edge(self, node1, node2):
        if node1 not in self.rep:
            self.rep[node1] = []
        if node2 not in self.rep:
            self.rep[node2] = []
        self.rep[node1].append(node2)
        self.rep[node2].append(node1)
        self.rep2[node1] = False
        self.rep2[node2] = False

    def grouping(self):
        def DFS(node, group):
            self.rep2[node] = True
            group.append(node)
            for connection in self.rep[node]:
                if self.rep2[connection] == False:
                    DFS(connection, group)
        res =[]
        for node in self.rep:
            if self.rep2[node] == False:
                group = []
                DFS(node, group)
                res.append(group)
        return res

