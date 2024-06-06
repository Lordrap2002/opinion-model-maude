from sys import stdin
import random as r

def nodes1():
    l = []
    m = []
    o = []
    for i in range(10):
        l.append(1 if r.random() >= 0.5 else -1)
    for i in range(10):
        m.append({})
        y = 0
        while len(m[i]) != 8:
            x = r.randint(0,9)
            if x != i:
                if not x in m[i]:
                    m[i][x] = l[x]
                    if l[x] > 0:
                        y += 1
        o.append((2 * (y / 8)) - 1)
    for i in range(10):
        print("< %d : [\"o\", %1.1f] [\"g\", %1.1f]" % (i, o[i], l[i]), end="")
        for j in m[i]:
            print(" [\"%d\", %1.1f]" % (j, m[i][j]), end="")
        print(" > ,")

def edges1():
    for i in range(10):
        for j in range(10):
            if j != i:
                print("< (%d , %d) : 1.0 > ," % (i, j))

def nodes2(n):
    for i in range(n):
        print("< %d : %1.2f >, " % (i, r.random() * (1 if r.random() >= 0.5 else -1)), end="")
    print()

def edges2(n):
    for i in range(n):
        for j in range(n):
            if j != i:
                print("< (%d , %d) : %1.2f > ," % (i, j, r.random()), end="")
        print()
    print()

nodes2(10)
edges2(10)

#search [3] init =>* STATE such that consensus(STATE) .