from collections import defaultdict


def add_edge(edges, source, destination):
    """
    Pridanie novej hrany
    :param edges: hrany = dict {id uzla : susediace uzly[] }
    :param source: zdrojovy vrchol
    :param destination: cielovy vrchol
    """
    if destination not in edges[source]:
        edges[source].append(destination)


def transpose(edges):
    """
    Transpozicia hran
    :param edges: hrany = dict {id uzla : susediace uzly[] }
    :return: transposed_edges (transponovane hrany)
    """
    transposed_edges = defaultdict(list)
    for i in edges:
        for j in edges[i]:
            add_edge(transposed_edges, j, i)
    return transposed_edges


class Graph:

    def __init__(self, nb_var, nb_clauses, literalsA, literalsB):
        self.nb_var = nb_var            # pocet premennych
        self.nb_clauses = nb_clauses    # pocet klauzul
        self.literalsA = literalsA      # literaly #1 v klauzulach
        self.literalsB = literalsB      # literaly #2 v klauzulach
        self.edges = self.fill_graph()  # hrany = dict {id uzla : susediace uzly[] }

    def fill_graph(self):
        """
        Prevod na implicative normal form, naplnenie grafu
        A v B  <=>  (-A => B) & (-B => A)
        :return: edges
        """

        # inicializacia hran
        edges = defaultdict(list)
        for i in range(self.nb_var * 2):
            edges[i + 1] = []

        for i in range(self.nb_clauses):
            ''' normalny tvar:
                * vo formule X > 0 (normalne) ... ostava povodny tvar X
                * vo formule X < 0 (negovane) ... mapuje sa na (nb_var - X) '''
            A = self.literalsA[i] if self.literalsA[i] > 0 else (self.nb_var - self.literalsA[i])
            B = self.literalsB[i] if self.literalsB[i] > 0 else (self.nb_var - self.literalsB[i])
            ''' negacia:
                * vo formule X > 0 (normalne) ... mapuje sa na (nb_var + X)
                * vo formule X < 0 (negovane) ... mapuje sa na (-X) '''
            A_neg = (self.nb_var + self.literalsA[i]) if self.literalsA[i] > 0 else (-self.literalsA[i])
            B_neg = (self.nb_var + self.literalsB[i]) if self.literalsB[i] > 0 else (-self.literalsB[i])

            add_edge(edges, A_neg, B)  # (-A => B)
            add_edge(edges, B_neg, A)  # (-B => A)

        return edges

    def DFS1_fill_stack(self, destination, visited, vertices_stack):
        """
        1. krok = DFS cez graf - naplni sa stack
        :param destination: cielovy vrchol
        :param visited: dict {id vrcholu: ci bol navstiveny (True/False)}
        :param vertices_stack: stack vrcholov
        """

        if visited[destination]:
            return

        visited[destination] = True
        for i in self.edges[destination]:
            self.DFS1_fill_stack(i, visited, vertices_stack)

        vertices_stack.append(destination)

    def DFS2_fill_SCC(self, SCC, edges_transp, source, component_id):
        """
        # 2 krok = DFS cez transponovany graf - naplni sa SCC
        :param SCC: dict {id vrcholu: id SCC, do ktoreho patri}
        :param edges_transp: transponovane hrany
        :param source: zdrojovy vrchol
        :param component_id: id aktualneho SCC
        """

        SCC[source] = component_id
        for destination in edges_transp[source]:
            if SCC[destination] == -1:
                self.DFS2_fill_SCC(SCC, edges_transp, destination, component_id)

    def is_2SAT(self):
        """
        riesenie SAT - Kosaraju's algorithm
        :return:  True/False (splnitelna/nesplnitelna), assignment (priradenie pravd. hodnot)
        """

        ''' ************* 1. DFS prechod cez graf, naplneni sa stack[] ************** '''

        visited = dict([(k, False) for k in sorted(self.edges.keys())])
        vertices_stack = []
        for i in visited.keys():
            if not visited[i]:
                self.DFS1_fill_stack(i, visited, vertices_stack)

        ''' ******** 2. DFS prechod cez transponovany graf, naplni sa SCC[] ******** '''

        component_id = 0
        SCC = dict([(k, -1) for k in sorted(self.edges.keys())])
        while len(vertices_stack) > 0:
            source = vertices_stack.pop()  # zoberie sa z vrchu zasobnika
            if SCC[source] == -1:
                self.DFS2_fill_SCC(SCC, transpose(self.edges), source, component_id)
                component_id += 1

        ''' ****************** 3. priradenie pravdivostnych hodnot ***************** '''

        assignment = [False] * self.nb_var
        for i in range(1, self.nb_var + 1):
            if SCC[i] == SCC[i + self.nb_var]:
                return False, []
            assignment[i - 1] = SCC[i] > SCC[i + self.nb_var]

        return True, assignment
