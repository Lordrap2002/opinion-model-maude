def DeGroot(nodos, aristas):
    return aristas

def S5(nodos, aristas):
    prom = sum(nodos.values()) / len(nodos)
    aristasSel = []
    for x, y, w in aristas:
        if nodos[y] >= prom and nodos[x] < nodos[y]:
            aristasSel.append((x, y, w))
        elif nodos[y] < prom and nodos[x] > nodos[y]:
            aristasSel.append((x, y, w))
    return aristasSel

def BuscarConsenso(grafo, tipo, maxPasos):
    com, pasos, epsilon = 0, 0, 0.005
    nodos, aristas = grafo
    opiniones = [0, 1]
    while pasos < maxPasos and max(opiniones) - min(opiniones) > epsilon:
        if tipo == "degroot":
            aristasSel = DeGroot(nodos, aristas)
        elif tipo == "s5":
            aristasSel = S5(nodos, aristas)
        else:
            aristasSel = DeGroot(nodos, aristas)
        #print(max(nodos.values()), " ", min(nodos.values()), " ", len(aristasSel))
        #print(nodos)
        nuevasOp = {}
        com += len(aristasSel)
        for nodo in nodos:
            aristasEnt = [(o, w) for (o, d, w) in aristasSel if d == nodo]
            SCOUNT = sum(w for _, w in aristasEnt)
            if SCOUNT == 0:
                nuevasOp[nodo] = nodos[nodo]
            else:
                SUMW = sum((nodos[origen] - nodos[nodo]) * w for origen, w in aristasEnt)
                nuevasOp[nodo] = nodos[nodo] + (SUMW / SCOUNT)
        nodos = nuevasOp
        opiniones = list(nodos.values())
        pasos += 1
    return nodos, pasos, com, (max(opiniones) - min(opiniones) <= epsilon)