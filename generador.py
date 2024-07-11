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
                print("< (%d , %d) : %1.2f >, " % (i, j, r.random()), end="")
        print()
    print()

#nodes1()
#edges1()
#nodes2(10)
#edges2(5)

def verificar1():
    o = {0 : 0.38, 1 : 0.71, 2 : 0.55, 3 : 0.92, 4 : 0.86}
    lst = [((0 , 2), 0.60), ((0 , 4) , 0.23),
           ((1 , 2), 0.69), ((1 , 3) , 0.45),
           ((2 , 3), 0.60),
           ((3 , 0), 0.79), ((3 , 1) , 0.68), ((3 , 4), 0.37),
           ((4 , 0), 0.74), ((4 , 1) , 0.19)]
    subsets = [[]]
    for element in lst:
        new_subsets = []
        for subset in subsets:
            new_subset = subset + [element]
            new_subsets.append(new_subset)
        subsets.extend(new_subsets)
    for se in subsets:
        o1 = o.copy()
        for n in o1:
            le = []
            w = 0
            for e in se:
                if n == e[0][1]:
                    le.append(e)
                    w += e[1]
            for e in le:
                o1[n] += ((o[e[0][0]] - o[e[0][1]]) * (e[1] / w))
        c = 0
        for n in o1:
            for n1 in o1:
                if abs(o1[n] - o1[n1]) > 0.01:
                    c = 1
                    break
            if c:
                break
        if not c:
            print("si")

def verificar2():
    o = {0 : 0.279, 1 : 0.3, 2 : 0.1, 3 : 0.279, 4 : 0.5, 5 : 0.5, 6 : 0.8}
    lst = [((0 , 1), 0.9478), ((0 , 5), 0.9322),
           ((1 , 0), 0.6500), ((1 , 4), 0.8154), ((1 , 5), 0.4587),
           ((2 , 3), 0.0705),
           ((3 , 2), 0.3792), ((3 , 4), 0.3792), ((3 , 6), 0.9274),
           ((4 , 0), 0.1261), ((4 , 6), 0.3672),
           ((5 , 0), 0.0200), ((5 , 1), 0.3429), ((5 , 2), 0.6859),
           ((6 , 3), 0.0242)]
    subsets = [[]]
    for element in lst:
        new_subsets = []
        for subset in subsets:
            new_subset = subset + [element]
            new_subsets.append(new_subset)
        subsets.extend(new_subsets)
    for se in subsets:
        o1 = o.copy()
        for n in o1:
            le = []
            w = 0
            for e in se:
                if n == e[0][1]:
                    le.append(e)
                    w += e[1]
            for e in le:
                o1[n] += ((o[e[0][0]] - o[e[0][1]]) * (e[1] / w))
        c = 0
        for n in o1:
            for n1 in o1:
                if abs(o1[n] - o1[n1]) > 0.01:
                    c = 1
                    break
            if c:
                break
        if not c:
            print("si")

#verificar1()
#verificar2()
            
import subprocess
import re
import sys
import time

def prueba():
    process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"], stdin=subprocess.PIPE)
    command = f"search init =>* STATE such that consensus(STATE) .\n"
    process.communicate(command.encode())

prueba()