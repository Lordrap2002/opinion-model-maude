from sys import stdin, stdout, stderr
import re
import subprocess
import time

patronEstado = r'state\s+(\d+)'
patronNodos = r'<\s*(\d+)\s*:\s*([\d\.e\-\+]+)\s*>'
patronAristas = r'<\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*:\s*([\d\.e\-\+]+)\s*>'
patronStepComm = r'step:\s+(\d+)\s+comm:\s+(\d+)'
patronStrat = r'<\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*:\s*([\d\.e\-\+]+)\s*>'

def limpiar():
    file = open("debug.txt", "r")
    grafos = file.readlines()
    file.close()
    for grafo in grafos:
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command = "search [, 40] " + grafo + " =>* STATE such that consensus(STATE) .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()
        estado = re.search(patronEstado, output).group(1)
        process = subprocess.Popen(["maude.linux64", "ex-vacc-hybrid.maude"],
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        command += "show path " + estado +  " .\n"
        output, error = process.communicate(command.encode())
        output = output.decode()


        output = output.split("second")[-1]
        estados = output.split("state")[1:]
        print("Grafo\n")
        for text in estados:
            t1, t2 = text.split("strat:")
            dataNodos = re.findall(patronNodos, t1)
            nodos = [(int(x), round(float(y), 3)) for x, y in dataNodos]
            #dataAristas = re.findall(patronAristas, t1)
            #aristas = [(int(x), int(y)) for x, y, z in dataAristas]
            info = re.search(patronStepComm, t1)
            step, comm = info.group(1), info.group(2)
            dataStrat = re.findall(patronStrat, t2)
            strat = [(int(x), int(y)) for x, y, z in dataStrat]
            nodos1 = [nodos[i:i+8] for i in range(0, len(nodos), 8)]
            for n in nodos1:
                print(n)
            print()
            print(step, " ", comm)
            print()
            strat1 = [strat[i:i+10] for i in range(0, len(strat), 10)]
            for n in strat1:
                print(n)
            print("-------------------------------------------------------------------------------------\n")
        print("=====================================================================================\n")

limpiar()