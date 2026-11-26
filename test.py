d={"c":1}
for elemento in d:
    print(d[elemento])


import networkx as nx

g = nx.Graph()
g.add_edge("A", "B", weight=300)
g.add_edge("B", "C", weight=150)

for arco in g.edges(data=True):
    print(arco)
    print(g.edges.data("weight", default=1))