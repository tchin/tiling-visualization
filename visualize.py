import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import sys
import math

def idealStrToEdges(ideal_str):
    comps = ideal_str.split(",")
    terms = [i.split("-") for i in comps]
    vars = [[] for i in comps]
    for i_comp in range(len(terms)):
        for i_term in range(len(terms[i_comp])):
            term_vars = terms[i_comp][i_term].split("*")
            term_edges = [int(i[2:]) for i in term_vars]
            vars[i_comp].append(term_edges)
    return vars

# parse arguments from command line
if (len(sys.argv) != 4):
    print("Usage: visualize.py m n path/to/file")
    sys.exit(1)
f = open(sys.argv[3])

m = int(sys.argv[1])
n = int(sys.argv[2])

# set up vertices and edges in graph
vertices = []
for r in range(n):
    for c in range(m):
        vertices.append((c, -1*r))

edges = []
for r in range(n):
    for c in range(m-1):
        edges.append([r*m+c, r*m+c+1])
for c in range(m):
    for r in range(n-1):
        edges.append([r*m+c, (r+1)*m+c])

# split string into ideals, and process each one
s = f.read()
sp = s.split("),")
sp[-1] = sp[-1][:-2]
ideals = [i[7:] for i in sp]
binomIdeals = filter(lambda x: "-" in x, ideals)
i = 0
w = math.ceil(math.sqrt(len(binomIdeals)))
for ideal in binomIdeals[1:]:
    idealEdges = idealStrToEdges(ideal)
    lines = []
    colors = []
    for comp in idealEdges:
        if len(comp) == 1:
            c = 'b'
        elif len(comp) == 2:
            c = 'r'
        else:
            c = 'g'
        for arr in comp:
            for e in arr:
                v1 = edges[e-1][0]
                v2 = edges[e-1][1]
                p1 = vertices[v1]
                p2 = vertices[v2]
                lines.append([p1, p2])
                colors.append(c)
        # display the vertices first
    plt.subplot(w,w,i+1)
    plt.axis('off')
    plt.scatter([p[0] for p in vertices], [p[1] for p in vertices])
    for line,c in zip(lines,colors):
        plt.plot([line[0][0], line[1][0]], [line[0][1],line[1][1]], c)
    i += 1
plt.show()
