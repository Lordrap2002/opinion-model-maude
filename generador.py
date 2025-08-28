from sys import stdin
import random as r
import subprocess
import time
from collections import deque
import re
import ModeloGeneral

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
    
def generarGrafo(maxN, minA, maxA, prom):
    N = []
    for i in range(maxN):
        N.append(i)
    malo = 1
    adyacencia = {}
    while malo:
        lados = []
        for x in range(maxN):
            maxAdy = r.randint(minA, maxA)
            adyacencia[x] = 0
            for y in N:
                p = r.random()
                if p < 0.25 and x != y:
                    lados.append((x, y))
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
                for (y, x) in lados:
                    if x == n and vis[y]:
                        q.append(y)
        if normal == maxN and invertido == maxN:
            malo = 0
    nodos = "< nodes:"
    o = []
    w = []
    for x in range(maxN):
        o.append(r.triangular(0, 1, prom))
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
    return nodos + aristas + " > in step: 0 comm: 0 strat: empty", min(o), max(o), sum(o) / len(o)

def grado(n, aristas):
    grado = 1
    for (x, y) in aristas:
        if(x == n):
            grado += 1
    return grado

def generarGrafoBarabasiAlbert(maxN, minA, maxA, opuesto):
    malo = 1
    while malo:
        N = [0, 1]
        lados = []
        lados2 = []
        for x in range(2, maxN):
            for y in N:
                if(r.random() < grado(y, lados) / (len(lados) + len(N) + 1)):
                    lados.append((y, x))
                    lados2.append((x, y))
                if(r.random() < grado(x, lados) / (len(lados) + len(N) + 1)):
                    lados.append((x, y))
                    lados2.append((y, x))
            N.append(x)
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
        o.append(r.random())
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
    return nodos + aristas + " > in step: 0 comm: 0 strat: empty", min(o), max(o), sum(o) / len(o)


patronNodos = r'<\s*(\d+)\s*:\s*([\d\.e\-\+]+)\s*>'
patronComm = r'comm:\s*(\d+)'
patronStep = r'step:\s*(\d+)'

#Guarda las metricas
def experimentarEstrategia(iter, maxN, minA, maxA, prom, tipoGrafo, archivo, pasos, nombre, nuevos, datos):
    r.seed(time.time())
    buenas = 0
    promedioOpinion = 0
    if(not nuevos):
        file = open(datos, "r")
        grafos = file.readlines()
        file.close()
    for i in range(iter):
        if(nuevos):
            if(tipoGrafo):
                grafo, minO, maxO, pr = generarGrafo(maxN, minA, maxA, prom)
            else:
                grafo, minO, maxO, pr = generarGrafoBarabasiAlbert(maxN, minA, maxA, prom)
        else:
            grafo = grafos[i]
            opiniones = [round(float(y), 6) for x, y in re.findall(patronNodos, grafo)]
            minO, maxO, pr = min(opiniones), max(opiniones), sum(opiniones) / len(opiniones)
        promedioOpinion += pr
        process = subprocess.Popen(["maude.linux64", archivo],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        command = "search " + ("[1 , " + str(pasos) + "] " if pasos else "") + grafo + " =>* STATE such that consensus(STATE) .\nshow search graph .\n"
        tiempo = time.time()
        output, error = process.communicate(command.encode())
        tiempo = time.time() - tiempo
        output = output.decode()
        f = open("grafos" + nombre + ".txt", "a")
        f.write(grafo + "\n")
        f.close()
        if not "No solution" in output:
            #print("Buena")
            buenas += 1
        output = output.split(("state"))[-1]
        dataNodos = re.findall(patronNodos, output)
        opF = [round(float(y), 6) for x, y in dataNodos]
        limI = [minO, maxO]
        limF = [min(opF), max(opF)]
        estado = int(re.search(patronStep, output).group(1))
        comm = int(re.search(patronComm, output).group(1))
        f = open("log" + nombre + ".txt", "a")
        f.write("%f %f %f %f %f %d %s\n" % (limI[0], limI[1], limF[0], limF[1], tiempo, comm, estado))
        f.close()
        if not i % 10:
            print(i)
    print("Buenas: %d, Porcentaje: %.2f%%, Promedio Opinión: %.3f" % (buenas, (buenas / iter) * 100, promedioOpinion / iter))

#experimentarEstrategia(100, 190, 2, 5, 0.5, 1, "ex-vacc-dgroot.maude", 1000, "DG-PruebaTiempo-190N", 1, "")
#experimentarEstrategia(100, 220, 2, 5, 0.5, 1, "ex-vacc-hybrid.maude", 1000, "S5-PruebaTiempo-220N", 1, "grafosDG-PruebaTiempo-200N.txt")
    
#experimentarEstrategia(100, 100, 2, 5, 0, 0, "ex-vacc-dgroot.maude", 0, "DG-5", 1, "")
#experimentarEstrategia(1, 50, 2, 5, 0, 0, "ex-vacc-hybrid.maude", 30, "S5-10", 1, "grafosDG-5.txt")

# GRAFOS SOM

def generarGrafoSOM(maxN, minA, maxA, tipo):
    N = []
    for i in range(maxN):
        N.append(i)
    malo = 1
    adyacencia = {}
    while malo:
        lados = []
        lados2 = []
        for x in range(maxN):
            maxAdy = r.randint(minA, maxA)
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
    i = {}
    for x in range(maxN):
        o.append(r.random())
        i[x] = o[x]
        if(tipo == "-"):
            nodos += f" < {str(x)} : [{str(o[x])}, 1.0, {str(r.random())}] >"
        else:
            nodos += f" < {str(x)} : [{str(o[x])}, 1.0, {str(r.random())}, {str(o[x])}] >"
        if x != maxN - 1:
            nodos += ","
    aristas = " ; edges:"
    for (x, y) in lados:
        val = r.random()
        w.append((x, y, val))
        i[y] += val
    for (x, y, val) in w:
        aristas += f" < ( {str(x)} , {str(y)} ) : {str(val / i[y])} >"
        if x != w[-1][0] or y != w[-1][1]:
            aristas += ","
    return nodos + aristas + " > in step: 0 comm: 0 strat: empty", min(o), max(o), sum(o) / len(o)

patronNodosSOM1 = r'<\s*(\d+)\s*:\s*\[\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?),\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?),\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*\]\s*>'
patronNodosSOM2 = r'<\s*(\d+)\s*:\s*\[\s*([\d\.\-e]+),\s*([\d\.\-e]+),\s*([\d\.\-e]+),\s*([\d\.\-e]+)\s*\]'

def experimentarSOM(iter, maxN, minA, maxA, tipoGrafo, archivo, pasos, nombre, nuevos, datos):
    r.seed(time.time())
    buenas = 0
    promedioOpinion = 0
    if(not nuevos):
        file = open(datos, "r")
        grafos = file.readlines()
        file.close()
    for i in range(iter):
        if(nuevos):
            grafo, minO, maxO, pr = generarGrafoSOM(maxN, minA, maxA, tipoGrafo)
        else:
            grafo = grafos[i]
            opiniones = [round(float(y), 6) for x, y in re.findall(patronNodos, grafo)]
            minO, maxO, pr = min(opiniones), max(opiniones), sum(opiniones) / len(opiniones)
        promedioOpinion += pr
        process = subprocess.Popen(["maude.linux64", archivo],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        command = "search " + ("[1 , " + str(pasos) + "] " if pasos else "") + grafo + " =>* STATE such that consensus(STATE) .\nshow search graph .\n"
        tiempo = time.time()
        output, error = process.communicate(command.encode())
        tiempo = time.time() - tiempo
        output = output.decode()
        f = open("grafos" + nombre + ".txt", "a")
        f.write(grafo + "\n")
        f.close()
        if not "No solution" in output:
            buenas += 1
        output = output.split(("state"))[-1]
        dataNodos = re.findall(patronNodosSOM1 if tipoGrafo == "-" else patronNodosSOM2, output)
        if(tipoGrafo == "-"):
            opF = [round(float(y), 6) for x, y, z, w in dataNodos]
        else:
            opF = [round(float(y), 6) for x, y, z, w, zz in dataNodos]
        limI = [minO, maxO]
        limF = [min(opF), max(opF)]
        estado = int(re.search(patronStep, output).group(1))
        comm = int(re.search(patronComm, output).group(1))
        f = open("log" + nombre + ".txt", "a")
        f.write("%f %f %f %f %f %d %s\n" % (limI[0], limI[1], limF[0], limF[1], tiempo, comm, estado))
        f.close()
        if not i % 1:
            print(i)
    print("Buenas: %d, Porcentaje: %.2f%%, Promedio Opinión: %.3f" % (buenas, (buenas / iter) * 100, promedioOpinion / iter))

#experimentarSOM(100, 100, 2, 5, "+", "prueba-SOM.maude", 60, "SOM-2", 1, "")
    
##############################################################################################################################
patron_nodos = r"<\s*(\d+)\s*:\s*([0-9.eE+-]+)\s*>"
patron_aristas = r"<\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*:\s*([0-9.eE+-]+)\s*>"

def generarGrafoPy(maxN, prom, probArista):
    N = []
    for i in range(maxN):
        N.append(i)
    malo = 1
    while malo:
        lados = []
        for x in range(maxN):
            for y in N:
                p = r.random()
                if p < probArista and x != y:
                    lados.append((x, y))
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
                for (y, x) in lados:
                    if x == n and vis[y]:
                        q.append(y)
        if normal == maxN and invertido == maxN:
            malo = 0
    nodos = "< nodes:"
    o = []
    w = []
    for x in range(maxN):
        o.append(r.random())
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
    return nodos + aristas + " > in step: 0 comm: 0 strat: empty", min(o), max(o), sum(o) / len(o)


def leerGrafo(grafo):
    opiniones = {int(id_): float(op) for id_, op in re.findall(patron_nodos, grafo)}
    aristas = [(int(src), int(dst), float(peso))
               for src, dst, peso in re.findall(patron_aristas, grafo)]
    return opiniones, aristas

def experimentarEstrategiaPy(iter, maxN, minA, maxA, prom, tipoGrafo, tipoSeleccion, pasos, nombre, nuevos, datos):
    r.seed(time.time())
    tiempoInicial = time.time()
    tiempoBusqueda, buenas, promedioOpinion = 0, 0, 0
    if not nuevos:
        file = open(datos, "r")
        grafos = file.readlines()
        file.close()
    for i in range(iter):
        if nuevos:
            if tipoGrafo:
                grafo, minO, maxO, pr = generarGrafoPy(maxN, prom, maxA / maxN)
                #grafo, minO, maxO, pr = generarGrafo(maxN, minA, maxA, prom)
            else:
                grafo, minO, maxO, pr = generarGrafoBarabasiAlbert(maxN, minA, maxA, prom)
        else:
            grafo = grafos[i].strip()
            opiniones = [round(float(y), 6) for x, y in re.findall(patronNodos, grafo)]
            minO, maxO, pr = min(opiniones), max(opiniones), sum(opiniones) / len(opiniones)
        promedioOpinion += pr
        tiempo = time.time()
        dataNodos, step, comm, consenso = ModeloGeneral.BuscarConsenso(leerGrafo(grafo), tipoSeleccion, pasos)
        tiempo = time.time() - tiempo
        tiempoBusqueda += tiempo
        f = open("grafos" + nombre + ".txt", "a")
        f.write(grafo + "\n")
        f.close()
        if consenso:
            buenas += 1
        opF = [round(float(y), 6) for y in dataNodos.values()]
        limI = [minO, maxO]
        limF = [min(opF), max(opF)]
        f = open("log" + nombre + ".txt", "a")
        f.write("%f %f %f %f %f %d %d\n" % (limI[0], limI[1], limF[0], limF[1], tiempo, comm, step))
        f.close()
        if not i % 10:
            print(i)
    tiempoFinal = (time.time() - tiempoInicial) / 60
    tiempoBusqueda /= 60
    print("Buenas: %d, Porcentaje: %.2f%%, Promedio Opinión: %.3f" % (buenas, (buenas / iter) * 100, promedioOpinion / iter))
    print("Tiempo Total (Min): %.2f, Tiempo Busqueda (Min): %.2f, Porcentaje Busqueda: %.2f%%" % (tiempoFinal, tiempoBusqueda, (tiempoBusqueda / tiempoFinal) * 100))

#experimentarEstrategiaPy(100, 3000, 2, 10, 0.5, 1, "degroot", 1000, "TestDG-PruebaTiempo-3000N-Py", 1, "")
#experimentarEstrategiaPy(100, 5000, 2, 10, 0.5, 1, "s5", 1000,
#                         "S5-PruebaTiempo-5000N-Py", 0,
#                         "experimentos\\PruebaTiempo\\DeGrootPython\\AristasProbabilidad\\10\\grafosDG-PruebaTiempo-5000N-Py.txt")
#experimentarEstrategiaPy(1, 300, 2, 5, 0.5, 1, "degroot", 1000, "PruebaTiempo", 1, "")
#experimentarEstrategiaPy(1, 10, 2, 10, 0.5, 1, "degroot", 1000, "TestDG-1000N-Py", 1, "")
#experimentarEstrategiaPy(1, 10, 2, 10, 0.5, 1, "s5", 1000, "TestS5-1000N-Py", 0, "grafosTestDG-1000N-Py.txt")

##############################################################################################################################

def generarGrafoPy2(maxN, grafoBase, probArista):
    N = []
    for i in range(maxN):
        N.append(i)
    malo = 1
    while malo:
        lados = []
        for x in range(maxN):
            for y in N:
                p = r.random()
                if p < probArista and x != y:
                    lados.append((x, y))
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
                for (y, x) in lados:
                    if x == n and vis[y]:
                        q.append(y)
        if normal == maxN and invertido == maxN:
            malo = 0
    nodos = "< nodes:"
    o = []
    w = []
    for x in range(maxN):
        o.append(r.random())
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
    return nodos + aristas + " > in step: 0 comm: 0 strat: empty", min(o), max(o), sum(o) / len(o)

def experimentarEstrategiaPy2(iter, maxN, maxA, base, tipoSeleccion, pasos, nombre, nuevos, datos):
    r.seed(time.time())
    tiempoInicial = time.time()
    tiempoBusqueda, buenas, promedioOpinion = 0, 0, 0
    fileBase = open(base, "r")
    grafosBase = fileBase.readlines()
    fileBase.close()
    if not nuevos:
        file = open(datos, "r")
        grafos = file.readlines()
        file.close()
    for i in range(iter):
        if nuevos:
            grafo, minO, maxO, pr = generarGrafoPy2(maxN, leerGrafo(grafosBase[i].strip()), maxA / maxN)
        else:
            grafo = grafos[i].strip()
            opiniones = [round(float(y), 6) for x, y in re.findall(patronNodos, grafo)]
            minO, maxO, pr = min(opiniones), max(opiniones), sum(opiniones) / len(opiniones)
        promedioOpinion += pr
        tiempo = time.time()
        dataNodos, step, comm, consenso = ModeloGeneral.BuscarConsenso(leerGrafo(grafo), tipoSeleccion, pasos)
        tiempo = time.time() - tiempo
        tiempoBusqueda += tiempo
        f = open("grafos" + nombre + ".txt", "a")
        f.write(grafo + "\n")
        f.close()
        if consenso:
            buenas += 1
        opF = [round(float(y), 6) for y in dataNodos.values()]
        limI = [minO, maxO]
        limF = [min(opF), max(opF)]
        f = open("log" + nombre + ".txt", "a")
        f.write("%f %f %f %f %f %d %d\n" % (limI[0], limI[1], limF[0], limF[1], tiempo, comm, step))
        f.close()
        if not i % 10:
            print(i)
    tiempoFinal = (time.time() - tiempoInicial) / 60
    tiempoBusqueda /= 60
    print("Buenas: %d, Porcentaje: %.2f%%, Promedio Opinión: %.3f" % (buenas, (buenas / iter) * 100, promedioOpinion / iter))
    print("Tiempo Total (Min): %.2f, Tiempo Busqueda (Min): %.2f, Porcentaje Busqueda: %.2f%%" % (tiempoFinal, tiempoBusqueda, (tiempoBusqueda / tiempoFinal) * 100))

#experimentarEstrategiaPy2(100, 3000, 2, 10, 0.5, 1, "degroot", 1000, "TestDG-PruebaTiempo-3000N-Py", 1, "")
#experimentarEstrategiaPy2(100, 5000, 2, 10, 0.5, 1, "s5", 1000,
#                         "S5-PruebaTiempo-5000N-Py", 0,
#                         "experimentos\\PruebaTiempo\\DeGrootPython\\AristasProbabilidad\\10\\grafosDG-PruebaTiempo-5000N-Py.txt")