from sys import stdin, stdout, stderr
import re
import subprocess

patronEstado = r'state\s+(\d+)'
patronNodos = r'<\s*(\d+)\s*:\s*([\d\.e\-\+]+)\s*>'
patronAristas = r'<\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*:\s*([\d\.e\-\+]+)\s*>'
patronStepComm = r'step:\s+(\d+)\s+comm:\s+(\d+)'
patronStrat = r'<\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*:\s*([\d\.e\-\+]+)\s*>'
patronRadio = r'\d+\.\d+'

def limpiar():
    file = open("debug2.txt", "r")
    grafos = file.readlines()
    file.close()
    i = 1
    for grafo in grafos:
        #Buscar el camino donde se genera el consenso
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 40] " + grafo + " =>* STATE such that consensus(STATE) .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()
        #Guardar el camino donde se genera el consenso
        estado = re.search(patronEstado, output).group(1)
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command1 = command + "show path " + estado +  " .\n"
        output1, error = process.communicate(command1.encode())
        output1 = output1.decode()
        output1 = output1.split("second")[-1]
        estados = output1.split("state")[1:]
        #Guardar el radio del grafo
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command2 = "rew eccentricities(nodes(" + grafo + "), edges(" + grafo + ")) .\n"
        output2, error = process.communicate(command2.encode())
        output2 = output2.decode()
        output2 = output2.split("result")[-1]
        radio = min([float(num) for num in re.findall(patronRadio, output2)])

        print("Grafo %d\n" % (i))
        print("radio: %s" % (radio))
        i += 1
        for text in estados:
            t1, t2 = text.split("strat:")
            dataNodos = re.findall(patronNodos, t1)
            nodos = [(int(x), round(float(y), 3)) for x, y in dataNodos]
            info = re.search(patronStepComm, t1)
            step, comm = info.group(1), info.group(2)
            dataStrat = re.findall(patronStrat, t2)
            strat = [(int(x), int(y)) for x, y, z in dataStrat]
            nodos1 = [nodos[i:i+8] for i in range(0, len(nodos), 8)]
            print("nodos:")
            for n in nodos1:
                print(n)
            print()
            print("step: %s, comm: %s" % (step, comm))
            print()
            strat1 = [strat[i:i+10] for i in range(0, len(strat), 10)]
            print("strategia:")
            for n in strat1:
                print(n)
            print("-------------------------------------------------------------------------------------\n")
        print("=====================================================================================\n")

limpiar()

def metricas():
    promDif, promCam = 0, 0
    with open("log3.txt", "r") as file:
        n = 0
        for linea in file:
            x, y, z, w = list(map(float, linea.split()))
            promCam += (y - x) - (w - z)
            promDif += (w - z)
            n += 1
        promCam /= n
        promDif /= n
    file = open("metricas.txt", "a")
    file.write("%f | %f\n" % (promDif, promCam))
    file.close()

#metricas()