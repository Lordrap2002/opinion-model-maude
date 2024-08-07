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
import time

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

from collections import deque

def prueba2():
    r.seed(time.time())
    iter = 1
    maxN = 20
    buenas = 0
    maxAdy = 5
    for i in range(iter):
        malo = 1
        nodos = []
        adyacencia = {}
        while malo:
            lados = []
            lados2 = []
            for x in range(maxN):
                nodos.append(x)
                adyacencia[x] = 0
                for y in range(maxN):
                    p = r.random()
                    if p < 0.5 and x != y:
                        lados.append((x, y))
                        lados2.append((y, x))
                        adyacencia[x] += 1
                    if adyacencia[x] == maxAdy:
                        break
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
        for x in range(maxN):
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
        for x in range(maxN):
            nodos += f" < {str(x)} : {str(o[x])} >"
            if x != maxN - 1:
                nodos += ","
        aristas = " ; edges:"
        for (x, y) in lados:
            aristas += f" < ( {str(x)} , {str(y)} ) : {str(r.random())} >"
            if x != lados[-1][0] or y != lados[-1][1]:
                aristas += ","
        final = "in step: 0 comm: 0 strat: empty"
        grafo = nodos + aristas + " > " + final
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 10] " + grafo + " =>* STATE such that consensus(STATE) .\n"
        print(command)
        output, error = process.communicate(command.encode())
        output = output.decode() 
        #print(output)
        if not "No solution" in output:
            buenas += 1
        if not i % 1:
            print(i)
    print("Buenas: %d, Porcentaje: %f" % (buenas, buenas / iter))

prueba2()

"""
search [, 10] < nodes: < 0 : 0.024226196815101297 >, < 1 : 0.7078705194151532 >, < 2 : 0.6839565105030674 >, < 3 : 0.7664257276022937 >, < 4 : 0.22073633626351097 >, < 5 : 0.393519305653127 >, < 6 : 0.12645528186897226 >, < 7 : 0.2662206797262743 >, < 8 : 0.2939459723760993 >, < 9 : 0.8594468072386089 >, < 10 : 0.2087359322619984 >, < 11 : 0.6140576674055431 >, < 12 : 0.8349596610009569 >, < 13 : 0.09190697020054761 >, < 14 : 0.4749050921941078 >, < 15 : 0.5005326748984198 >, < 16 : 0.5310100139827328 >, < 17 : 0.5926090104126044 >, < 18 : 0.9054081430965264 >, < 19 : 0.03796132527905308 > ; 
edges: < ( 0 , 1 ) : 0.6533630121945813 >, < ( 0 , 2 ) : 0.797422756709757 >, < ( 0 , 9 ) : 0.7377787535834851 >, < ( 0 , 11 ) : 0.6003533373842505 >, < ( 0 , 12 ) : 0.7534665662947219 >, < ( 1 , 4 ) : 0.5358120116637866 >, < ( 1 , 5 ) : 0.9301831271162747 >, < ( 1 , 6 ) : 0.15542085525014038 >, < ( 1 , 7 ) : 0.18238881875952284 >, < ( 1 , 10 ) : 0.18597350333517626 >, < ( 2 , 1 ) : 0.20177630594153073 >, < ( 2 , 3 ) : 0.16966099573847349 >, < ( 2 , 4 ) : 0.09259030461519158 >, < ( 2 , 9 ) : 0.9561891175004412 >, < ( 2 , 12 ) : 0.5620166202267926 >, < ( 3 , 0 ) : 0.2944914902936192 >, 
< ( 3 , 1 ) : 0.28593732907741454 >, < ( 3 , 5 ) : 0.49959521794524964 >, < ( 3 , 7 ) : 0.9986469678319215 >, < ( 3 , 9 ) : 0.2222762091977898 >, < ( 4 , 7 ) : 0.17156734732342804 >, < ( 4 , 13 ) : 0.4155156394588072 >, < ( 4 , 14 ) : 0.525585944207478 >, < ( 4 , 15 ) : 0.5124565776383484 >, < ( 4 , 17 ) : 0.4843253311948952 >, < ( 5 , 1 ) : 0.9957935674371867 >, < ( 5 , 4 ) : 0.8993897012366339 >, < ( 5 , 7 ) : 0.5633461178543001 >, < ( 5 , 10 ) : 0.9795019962463851 >, < ( 5 , 11 ) : 0.5667789081909951 >, < ( 6 , 2 ) : 0.7506470387620396 >, < ( 6 , 3 ) : 0.6305237850956142 >, 
< ( 6 , 5 ) : 0.7330829278814914 >, < ( 6 , 7 ) : 0.31661903986141715 >, < ( 6 , 8 ) : 0.7947454950007071 >, < ( 7 , 1 ) : 0.5080950738585864 >, < ( 7 , 3 ) : 0.8339360691895953 >, < ( 7 , 8 ) : 0.3476148596141133 >, < ( 7 , 10 ) : 0.6821014277280385 >, < ( 7 , 13 ) : 0.9864676817386001 >, < ( 8 , 3 ) : 0.7764932887136723 >, < ( 8 , 5 ) : 0.5760307995611796 >, < ( 8 , 6 ) : 0.21600588895233397 >, < ( 8 , 7 ) : 0.7713961385742706 >, < ( 8 , 9 ) : 0.043987653001386295 >, < ( 9 , 0 ) : 0.8200963058907251 >, < ( 9 , 2 ) : 0.07170542143227221 >, < ( 9 , 3 ) : 0.8880078579689572 >, < ( 9 , 4 ) : 0.9009896093764549 >, 
< ( 9 , 6 ) : 0.5912871282917875 >, < ( 10 , 0 ) : 0.2717929011551077 >, < ( 10 , 1 ) : 0.3408265203400126 >, < ( 10 , 3 ) : 0.3075899865813895 >, < ( 10 , 4 ) : 0.044886811045314334 >, < ( 10 , 5 ) : 0.11814682847029667 >, < ( 11 , 1 ) : 0.747130378294767 >, < ( 11 , 3 ) : 0.9780776219033638 >, < ( 11 , 5 ) : 0.397117431041196 >, < ( 11 , 8 ) : 0.9245957305273678 >, < ( 11 , 13 ) : 0.425802156560807 >, < ( 12 , 2 ) : 0.7358691189526244 >, < ( 12 , 3 ) : 0.7126930723133693 >, < ( 12 , 4 ) : 0.20276799324615613 >, < ( 12 , 8 ) : 0.7735916951143045 >, < ( 12 , 9 ) : 0.4812159789732604 >, < ( 13 , 1 ) : 0.04147802754714658 >, 
< ( 13 , 2 ) : 0.43620106932972735 >, < ( 13 , 3 ) : 0.9942829761174573 >, < ( 13 , 5 ) : 0.8398739099676994 >, < ( 13 , 10 ) : 0.5143319950659425 >, < ( 14 , 1 ) : 0.0045815194893035205 >, < ( 14 , 2 ) : 0.18029221430329656 >, < ( 14 , 3 ) : 0.06867298525313392 >, < ( 14 , 4 ) : 0.2086366024167403 >, < ( 14 , 5 ) : 0.10623799202896378 >, < ( 15 , 5 ) : 0.5237345867436565 >, < ( 15 , 8 ) : 0.9250803637688595 >, < ( 15 , 13 ) : 0.8043404196451381 >, < ( 15 , 16 ) : 0.748625818406009 >, < ( 15 , 18 ) : 0.3640200173846566 >, < ( 16 , 2 ) : 0.7360389290694941 >, < ( 16 , 3 ) : 0.0669184799783501 >, < ( 16 , 4 ) : 0.6478077491458307 >,
 < ( 16 , 5 ) : 0.9927138743453296 >, < ( 16 , 7 ) : 0.5834793138003856 >, < ( 17 , 1 ) : 0.2823355947640951 >, < ( 17 , 2 ) : 0.5797796330187206 >, < ( 17 , 4 ) : 0.01583185057352643 >, < ( 17 , 6 ) : 0.9377523464366193 >, < ( 17 , 11 ) : 0.8194572576938538 >, < ( 18 , 0 ) : 0.9820991559494258 >, < ( 18 , 10 ) : 0.41653513035461187 >, < ( 18 , 13 ) : 0.6057363471164916 >, < ( 18 , 19 ) : 0.1131481919517574 >, < ( 19 , 2 ) : 0.8789730979131852 >, < ( 19 , 3 ) : 0.7661253342714109 >, < ( 19 , 4 ) : 0.8850070894673053 >, < ( 19 , 5 ) : 0.21911698346129538 >, < ( 19 , 6 ) : 0.10280895618460162 > > in step: 0 comm: 0 strat: empty =>* STATE such that consensus(STATE) .
"""