import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodi = None
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getDateRange(self):
        return DAO.getDateRange()
    def getCat(self):
        return DAO.getAllCategories()

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self,s,di,df):
        self._grafo.clear()
        self._idMap = {}
        self._nodi = DAO.getAllNodes(s)
        for n in self._nodi:
            self._grafo.add_node(n)
            self._idMap[n.product_id] = n
        self.addEdges(s,di,df)

    def addEdges(self, c,di,df):
        edges = DAO.getAllEdges(c,di,df)
        for e in edges:
            n1 = self._idMap.get(e[0])
            n2 = self._idMap.get(e[1])
            if n1 is None or n2 is None:
                continue
            if e[2] < e[3]:
                self._grafo.add_edge(n2, n1, weight=e[2]+e[3])
            if e[2] > e[3]:
                self._grafo.add_edge(n1, n2, weight=e[2]+e[3])
            if e[3] == e[2]:
                self._grafo.add_edge(n2, n1, weight=e[2] + e[3])
                self._grafo.add_edge(n1, n2, weight=e[2] + e[3])

    def get_top5_Prodotti(self):
        nodi = []
        for n in self._grafo.nodes():
            nodi.append(n)
        nodi.sort(key=lambda x: self._grafo.out_degree(x,'weight') - self._grafo.in_degree(x,'weight'), reverse=True)
        return nodi[:5]


