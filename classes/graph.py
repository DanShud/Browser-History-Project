#class Graph
class Graph:
    def __init__(self): #represntation is a list of adjancy, self.rep2 is bool, showing if the node was grop
        self.rep = {}
        self.rep2 = {}

    def __str__(self): #representation of the graph
        return str(self.rep)

    #preconditions
    #input of the mutator ""edge" is two nodes, the type is browser object
    def edge(self, node1, node2):
        if node1 not in self.rep:
            self.rep[node1] = []
        if node2 not in self.rep:
            self.rep[node2] = []
        self.rep[node1].append(node2)
        self.rep[node2].append(node1)
        self.rep2[node1] = False
        self.rep2[node2] = False
    #postcondition
    #method mutates the graph adding the edge

    #precondions
    #an accessor which grouphs graphs into compound
    #may be called only once for the graph
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
    #postcondition
    #the accesor return the list of the list
    #in which sublist, there are all nodes, which were in on compound 

