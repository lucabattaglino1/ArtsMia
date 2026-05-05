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