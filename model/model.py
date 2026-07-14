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

    def getNodes(self):
        return sorted(self._grafo.nodes(), key=lambda n: n.product_name)

    # ============================================================
    # F1 - CAMMINO DI LUNGHEZZA FISSA A->B, PESO MASSIMO
    # Launcher: azzera lo stato, risolve start/end da id, avvia ricorsione
    # ============================================================
    def cercaCammino(self, startId, endId, lun):
        self._best = None
        self._bestPeso = -1
        start = self._idMap.get(startId)  # -------> idMap keyed su product_id (int)
        end = self._idMap.get(endId)
        if start is None or end is None:
            return None, 0
        self._ricorsione([start], end, lun)
        return self._best, self._bestPeso

    def _ricorsione(self, parziale, end, lun):
        # CASO BASE: raggiunta la lunghezza voluta
        if len(parziale) == lun:  # -------> NODI (==lun). Se "lunghezza"=archi usa (== lun+1)
            if parziale[-1] == end:  # deve terminare nel nodo End
                peso = self._pesoCammino(parziale)
                if peso > self._bestPeso:  # tieni il peso massimo
                    self._bestPeso = peso
                    self._best = list(parziale)  # copia! non il riferimento
            return
        # PASSO RICORSIVO: espandi sui SUCCESSORI (rispetta i versi degli archi)
        for succ in self._grafo.successors(parziale[-1]):  # -------> DiGraph: successors, non neighbors
            if succ not in parziale:  # un nodo non si attraversa piu' volte
                parziale.append(succ)
                self._ricorsione(parziale, end, lun)
                parziale.pop()  # backtracking

    def _pesoCammino(self, cammino):
        tot = 0
        for i in range(len(cammino) - 1):  # -------> len-1: archi tra nodi consecutivi (no off-by-one)
            tot += self._grafo[cammino[i]][cammino[i + 1]]['weight']
        return tot

    # NOTE (F1):
    # - Vincoli mappati: "no nodi ripetuti" -> if succ not in parziale (prima dell'inclusione);
    #   "termina in End" + "lunghezza == Lun" -> caso base; "rispetta i versi" -> successors().
    # - "Lunghezza": qui contati i NODI (len==Lun). Se il tuo docente intende gli ARCHI, cambia
    #   l'unica riga del caso base in (len(parziale) == lun + 1). E' l'unico punto da toccare.
    # - Ottimizzazione opzionale: nel for, "if succ == end and len(parziale)+1 < lun: continue"
    #   (raggiungere End prima della fine e' sempre un ramo morto, End non si puo' ripetere).


