# Copyright (c) 2018 Bart Massey

# Graph Representations

import random

# These classes support edge-list, adjacency-list and
# adjacency-matrix graph representations. The graphs
# may be directed or undirected. Undirected
# graphs will be explicitly represented with pairs
# of directed edges in all representations.

class GraphEL(object):
    def __init__(self, nvertices, edges, directed=True):
        "Create an edge-list graph."
        self.nvertices = nvertices
        self.directed = directed
        if directed:
            self.edges = edges
        else:
            self.edges = set()
            for v1, v2 in edges:
                self.edges.add((v1, v2))
                self.edges.add((v2, v1))
            self.edges = list(self.edges)

    def undirected(self):
        "Return the undirected version of a directed edge-list graph."
        assert self.directed
        return GraphEL(self.nvertices, self.edges, directed=False)

    def toGraphAL(self):
        "Return the adjacency-list representation of an edge-list graph."
        return GraphAL(self.nvertices, self.edges, self.directed)

    def __repr__(self):
        return "GraphEL({}, {}, directed={})".format(
            self.nvertices,
            self.edges,
            self.directed
        )

    def __eq__(self, g):
        if type(g) is GraphAL:
            g = g.toGraphEL()
        if self.directed != g.directed:
            return False
        if self.nvertices != g.nvertices:
            return False
        return set(self.edges) == set(g.edges)

class GraphAL(object):
    def __init__(self, nvertices, edges, directed=True):
        "Create an adjacency-list graph."
        self.nvertices = nvertices
        self.directed = directed
        if directed:
            self.neighbors = [[] for _ in range(nvertices)]
            for v1, v2 in edges:
                self.neighbors[v1].append(v2)
        else:
            neighbors = [set() for _ in range(nvertices)]
            for v1, v2 in edges:
                neighbors[v1].add(v2)
                neighbors[v2].add(v1)
            self.neighbors = []
            for v in range(nvertices):
                self.neighbors.append(list(neighbors[v]))

    def toGraphEL(self):
        "Return the edge-list representation of an adjacency-list graph."
        edges = []
        for v1 in range(self.nvertices):
            for v2 in self.neighbors[v1]:
                edges.append((v1, v2))
        return GraphEL(self.nvertices, edges, self.directed)

    def __repr__(self):
        return "GraphAL({}, {}, directed={})".format(
            self.nvertices,
            self.neighbors,
            self.directed
        )

    def __eq__(self, g):
        self.toGraphEL() == g

def cycle_shuffle(l):
    "Produce a permutation of l in cyclic order."
    n = len(l)
    for i in range(n-1):
        j = random.randrange(i+1, n)
        l[i], l[j] = l[j], l[i]

def randgraph(nvertices, nedges):
    """Produce a random connected directed graph
       with nvertices vertices and nedges "extra" edges."""
    assert nedges <= nvertices * (nvertices - 1) - (nvertices - 1)
    edges = set()
    line = list(range(nvertices))
    cycle_shuffle(line)
    for i in range(len(line) - 1):
        edges.add((line[i], line[i+1]))
    all_edges = [(v1, v2) 
                   for v1 in range(nvertices)
                     for v2 in range(nvertices)
                         if v1 != v2]
    assert len(all_edges) == nvertices * (nvertices - 1)
    random.shuffle(all_edges)
    if nedges > 0:
        for e in all_edges:
            if e not in edges:
                edges.add(e)
                nedges -= 1
                if nedges <= 0:
                    break
    return GraphEL(nvertices, list(edges))

g = randgraph(4, 0)
print(g)
print(g.toGraphAL())

g = g.undirected()
print(g)
print(g.toGraphAL())

for _ in range(100):
    nvertices = random.randrange(2, 20)
    max_edges = nvertices * (nvertices - 1)
    max_nedges = max_edges - nvertices + 1
    nedges = random.randrange(max_nedges + 1)

    def roundtrip(g_el):
        g_al = g_el.toGraphAL()
        assert g_el == g_al.toGraphEL()

    g_el = randgraph(nvertices, nedges)
    roundtrip(g_el)
    roundtrip(g_el.undirected())
