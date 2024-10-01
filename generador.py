from sys import stdin
import random as r
import subprocess
import time
from collections import deque
import re

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

def prueba():
    r.seed(time.time())
    iter = 1000
    buenas = 0
    for i in range(iter):
        nodos = "< nodes:"
        o = []
        for x in range(6):
            a = r.random()
            f = 1
            while f:
                f = 0
                for y in o:
                    if abs(y - a) < 0.01:
                        a = r.random()
                        f = 1
                        break
            o.append(a)
        for x in range(6):
            nodos += f" < {str(x)} : {str(o[x])} >"
            if x != 5:
                nodos += ","
        aristas = " ; edges:"
        lados = [(0, 1), (0, 3), (1, 2), (1, 4), (2, 3), (2, 5),
                (3, 0), (3, 4), (4, 1), (4, 5), (5, 0), (5, 2)]
        for (x, y) in lados:
            aristas += f" < ( {str(x)} , {str(y)} ) : {str(r.random())} >"
            if x != 5 or y != 2:
                aristas += ","
        final = "in step: 0 comm: 0 strat: empty"
        grafo = nodos + aristas + " > " + final
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 2] " + grafo + " =>* STATE such that consensus(STATE) .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()
        if not "No solution" in output:
            print(output)
            buenas += 1
        if not i % 100:
            print(i)
    print("Buenas: %d, Porcentaje: %f" % (buenas, buenas / iter))

#prueba()

def prueba2():
    r.seed(time.time())
    iter = 1000
    maxN = 50
    buenas = 0
    N = []
    for i in range(maxN):
        N.append(i)
    for i in range(iter):
        malo = 1
        nodos = []
        adyacencia = {}
        while malo:
            lados = []
            lados2 = []
            for x in range(maxN):
                maxAdy = r.randint(2, 5)
                nodos.append(x)
                adyacencia[x] = 0
                for y in N:
                    p = r.random()
                    if p < 0.25 and x != y:
                        lados.append((x, y))
                        lados2.append((y, x))
                        adyacencia[x] += 1
                    if adyacencia[x] == maxAdy:
                        break
                N.append(N[0])
                N.pop(0)
            normal, invertido = 0, 0
            q = deque()
            q.append(0)
            vis = [1] * maxN
            while(len(q)):
                n = q.popleft()
                if(vis[n]):
                    vis[n] -= 1
                    normal += 1
                    for (x, y) in lados:
                        if x == n and vis[y]:
                            q.append(y)
            q = deque()
            q.append(0)
            vis = [1] * maxN
            while(len(q)):
                n = q.popleft()
                if(vis[n]):
                    vis[n] -= 1
                    invertido += 1
                    for (x, y) in lados2:
                        if x == n and vis[y]:
                            q.append(y)
            if normal == maxN and invertido == maxN:
                malo = 0
        nodos = "< nodes:"
        o = []
        w = []
        for x in range(maxN):
            a = r.random()
            f = 1
            while f:
                f = 0
                for y in o:
                    if abs(y - a) < 0.005:
                        a = r.random()
                        f = 1
                        break
            o.append(a)
        for x in range(maxN):
            nodos += f" < {str(x)} : {str(o[x])} >"
            if x != maxN - 1:
                nodos += ","
        aristas = " ; edges:"
        for (x, y) in lados:
            val = r.random()
            w.append((x, y, val))
            aristas += f" < ( {str(x)} , {str(y)} ) : {str(val)} >"
            if x != lados[-1][0] or y != lados[-1][1]:
                aristas += ","
        final = "in step: 0 comm: 0 strat: empty"
        grafo = nodos + aristas + " > " + final
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 40] " + grafo + " =>* STATE such that consensus(STATE) .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()
        #print(command)
        if not "No solution" in output:
            #print(output)
            #for x in range(maxN):
                #print(f" < {str(x)} : {str(o[x])} >")
            #print(w)
            print(grafo)
            buenas += 1
        if not i % 10:
            print(i)
    print("Buenas: %d, Porcentaje: %.2f%%" % (buenas, (buenas / iter) * 100))

#No asegura nodos con diferente opinion
def prueba3():
    r.seed(time.time())
    iter = 1000
    maxN = 100
    buenas = 0
    N = []
    for i in range(maxN):
        N.append(i)
    for i in range(iter):
        malo = 1
        nodos = []
        adyacencia = {}
        while malo:
            lados = []
            lados2 = []
            for x in range(maxN):
                maxAdy = r.randint(2, 5)
                nodos.append(x)
                adyacencia[x] = 0
                for y in N:
                    p = r.random()
                    if p < 0.25 and x != y:
                        lados.append((x, y))
                        lados2.append((y, x))
                        adyacencia[x] += 1
                    if adyacencia[x] == maxAdy:
                        break
                N.append(N[0])
                N.pop(0)
            normal, invertido = 0, 0
            q = deque()
            q.append(0)
            vis = [1] * maxN
            while(len(q)):
                n = q.popleft()
                if(vis[n]):
                    vis[n] -= 1
                    normal += 1
                    for (x, y) in lados:
                        if x == n and vis[y]:
                            q.append(y)
            q = deque()
            q.append(0)
            vis = [1] * maxN
            while(len(q)):
                n = q.popleft()
                if(vis[n]):
                    vis[n] -= 1
                    invertido += 1
                    for (x, y) in lados2:
                        if x == n and vis[y]:
                            q.append(y)
            if normal == maxN and invertido == maxN:
                malo = 0
        nodos = "< nodes:"
        o = []
        w = []
        for x in range(maxN):
            a = r.random()
            f = 1
            o.append(a)
        for x in range(maxN):
            nodos += f" < {str(x)} : {str(o[x])} >"
            if x != maxN - 1:
                nodos += ","
        aristas = " ; edges:"
        for (x, y) in lados:
            val = r.random()
            w.append((x, y, val))
            aristas += f" < ( {str(x)} , {str(y)} ) : {str(val)} >"
            if x != lados[-1][0] or y != lados[-1][1]:
                aristas += ","
        final = "in step: 0 comm: 0 strat: empty"
        grafo = nodos + aristas + " > " + final
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 40] " + grafo + " =>* STATE such that consensus(STATE) .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()
        if not "No solution" in output:
            f = open("debug3.txt", "a")
            f.write(grafo + "\n")
            f.close()
            print("Buena")
            buenas += 1
        if not i % 10:
            print(i)
    print("Buenas: %d, Porcentaje: %.2f%%" % (buenas, (buenas / iter) * 100))

#prueba3()

patronNodos = r'<\s*(\d+)\s*:\s*([\d\.e\-\+]+)\s*>'
#Guarda las diferencias de las opiniones extremas
def prueba4():
    r.seed(time.time())
    iter = 2000
    maxN = 100
    buenas = 0
    N = []
    for i in range(maxN):
        N.append(i)
    for i in range(iter):
        malo = 1
        nodos = []
        adyacencia = {}
        while malo:
            lados = []
            lados2 = []
            for x in range(maxN):
                maxAdy = r.randint(2, 5)
                nodos.append(x)
                adyacencia[x] = 0
                for y in N:
                    p = r.random()
                    if p < 0.25 and x != y:
                        lados.append((x, y))
                        lados2.append((y, x))
                        adyacencia[x] += 1
                    if adyacencia[x] == maxAdy:
                        break
                N.append(N[0])
                N.pop(0)
            normal, invertido = 0, 0
            q = deque()
            q.append(0)
            vis = [1] * maxN
            while(len(q)):
                n = q.popleft()
                if(vis[n]):
                    vis[n] -= 1
                    normal += 1
                    for (x, y) in lados:
                        if x == n and vis[y]:
                            q.append(y)
            q = deque()
            q.append(0)
            vis = [1] * maxN
            while(len(q)):
                n = q.popleft()
                if(vis[n]):
                    vis[n] -= 1
                    invertido += 1
                    for (x, y) in lados2:
                        if x == n and vis[y]:
                            q.append(y)
            if normal == maxN and invertido == maxN:
                malo = 0
        nodos = "< nodes:"
        o = []
        w = []
        for x in range(maxN):
            a = r.random()
            f = 1
            o.append(a)
        for x in range(maxN):
            nodos += f" < {str(x)} : {str(o[x])} >"
            if x != maxN - 1:
                nodos += ","
        aristas = " ; edges:"
        for (x, y) in lados:
            val = r.random()
            w.append((x, y, val))
            aristas += f" < ( {str(x)} , {str(y)} ) : {str(val)} >"
            if x != lados[-1][0] or y != lados[-1][1]:
                aristas += ","
        final = "in step: 0 comm: 0 strat: empty"
        grafo = nodos + aristas + " > " + final
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 40] " + grafo + " =>* STATE such that consensus(STATE) .\nshow path 40 .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()
        if not "No solution" in output:
            f = open("debug2.txt", "a")
            f.write(grafo + "\n")
            f.close()
            print("Buena")
            buenas += 1
        output = output.split("state 40")[-1]
        dataNodos = re.findall(patronNodos, output)
        opF = [round(float(y), 6) for x, y in dataNodos]
        limI = [min(o), max(o)]
        limF = [min(opF), max(opF)]
        f = open("log2.txt", "a")
        f.write("%f %f %f %f\n" % (limI[0], limI[1], limF[0], limF[1]))
        f.close()
        if not i % 10:
            print(i)
    print("Buenas: %d, Porcentaje: %.2f%%" % (buenas, (buenas / iter) * 100))

prueba4()