import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph() # mi creo un grafo
        self._nodes = DAO.getAllNodes()

        # dizionario che associa ad ogni chiave primaria (object_id)
        # l'oggetto corrispondente
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.object_id] = n

        # ricorsione
        self._optPath = []
        self._optCost = 0

    def getOptPath(selfself, source, lun):
        parziale = [source]

        for n in self._graph.neighbors(source):
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale,lun)
                parziale.pop()
        return self._optPath, self._optCost

    def _ricorsione(self, parziale, lun):
        if len(parziale) == lun:
            # condizione di terminazione, allora parziale è lunga esattamente lun
            # per cui verifico che questa parziale sia meglio del mio best (condizione di ottimalità),
            # ed in ogni caso esco

            if self._costoPath(parziale) > self._optCost:
                self._optCost = self._costoPath(parziale)
                self._optPath = copy.deepcopy(parziale)
            return

        # se arrivo qui posso ancora aggiungere nodi
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()

    def _costoPath(self, path):
        costo = 0
        for i in range(0, len(path)-1):
            costo += self._graph[path[i]][path[i+1]["weight"]]




    def getInfoCompConnessa(self, id_oggetto):
        # cercare la componente connessa che contiene id_oggetto

        if not self.hasNode(id_oggetto):
            return None

        source = self._idMapAO[id_oggetto]

        # Strategia 1
        # faccio una ricerca di tipo dfs e conto il numero di nodi dell'albero
        dfsTree = nx.dfs_tree(self._graph, source)
        print(("size connessa con dfs_tree", len(dfsTree.nodes)))

        # Strategia 2
        dfsPred = nx.dfs_predecessors(self._graph, source)
        print(("size connessa con dfs_predecessors", len(dfsPred.values())))

        # Strategia 3 ( quella che utilizzeremo sempre)
        conn = nx.node_connected_component(self._graph, source)
        print("size connessa con node_connected_component", len(conn))
        return len(conn)


    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO

    def buildGraph(self):
        # aggiunge i nodi
        self._graph.add_nodes_from(self._nodes)

        # aggiunge gli archi
        self.addEdgesV2()

    # Primo metodo
    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getEdgePeso(u, v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)
                print(f"Aggiunto arco fra {u} e {v} con {peso}")

    # Secondo metodo, molto più efficiente
    def addEdgesV2(self):
        allEdges = DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight = e.peso)

    # per sapere quanti nodi ha il grafo
    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    # dato l'id dell'oggetto mi recupero l'oggetto intero
    def getNodeFromId(self, id_oggetto):
        return self._idMapAO[id_oggetto]