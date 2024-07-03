import copy

import networkx as nx
from geopy.distance import distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self.states = DAO.getAllStates()
        self.stateMap = {s.id: s for s in self.states}

        self.grafo = nx.Graph()

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self, year):
        return DAO.getAllShape(year)

    def creaGrafo(self, year, shape):
        self.grafo.clear()
        self.grafo.add_nodes_from(self.states)

        for u, v in DAO.getAllVicini(self.stateMap):
            self.grafo.add_edge(u, v, weight=0)

        pesi = {s: DAO.getPeso(year, shape, s)[0] for s in self.states}

        for s1 in self.grafo.nodes:
            for s2 in self.grafo.neighbors(s1):
                self.grafo.add_edge(s1, s2, weight=pesi[s1]+pesi[s2])

        stats = f"Nodi: {len(self.grafo.nodes)}, Spigoli: {len(self.grafo.edges)}\n"
        for n in self.grafo.nodes:
            peso = 0
            for v in self.grafo.neighbors(n):
                peso += self.grafo[n][v]['weight']
            stats += f"Nodo {n}, peso adiacenti = {peso}\n"

        return stats

    def get_path(self):
        self.solBest = []
        self.maxDist = 0

        for nodo in self.grafo.nodes:
            for vicino in self.grafo.neighbors(nodo):
                self.ricorsione([nodo, vicino], self.grafo[nodo][vicino]['weight'])

        return self.solBest, self.maxDist

    def ricorsione(self, parziale, lastPeso):
        ultimo = parziale[-1]

        if self.getDist(parziale) > self.maxDist:
            self.maxDist = self.getDist(parziale)
            self.solBest = copy.deepcopy(parziale)

        for vicino in self.grafo.neighbors(ultimo):
            peso = self.grafo[ultimo][vicino]['weight']
            if vicino not in parziale and peso > lastPeso:
                parziale.append(vicino)
                self.ricorsione(parziale, peso)
                parziale.pop()

    def getDist(self, parziale):
        tot = 0
        for i in range(len(parziale)-1):
            s1 = parziale[i]
            s2 = parziale[i+1]
            tot += distance((s1.Lat, s1.Lng), (s2.Lat, s2.Lng)).km
        return tot




