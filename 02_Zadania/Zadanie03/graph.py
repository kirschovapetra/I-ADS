from collections import defaultdict


# pridanie hrany
def add_edge(edges_dict, source, destination):
    if destination not in edges_dict[source]:
        edges_dict[source].append(destination)


# transpozicia hran
def transpose(edges):
    transposed_edges = defaultdict(list)
    for i in edges:
        for j in edges[i]:
            add_edge(transposed_edges, j, i)
    return transposed_edges


class Graph:

    def __init__(self, nb_var, nb_clauses, literalsA, literalsB):
        self.nb_var = nb_var
        self.nb_clauses = nb_clauses
        self.literalsA = literalsA
        self.literalsB = literalsB
        self.edges = self.fill_graph()  # {id, list of adj vertices [] }

    # naplnenie grafu hranami
    def fill_graph(self):
        edges = defaultdict(list)

        for i in range(self.nb_clauses):
            # A v B  --->  ( -A => B ) & ( -B => A )
            A = self.literalsA[i] if self.literalsA[i] > 0 else (self.nb_var - self.literalsA[i])
            B = self.literalsB[i] if self.literalsB[i] > 0 else (self.nb_var - self.literalsB[i])
            A_neg = (self.nb_var + self.literalsA[i]) if self.literalsA[i] > 0 else (-self.literalsA[i])
            B_neg = (self.nb_var + self.literalsB[i]) if self.literalsB[i] > 0 else (-self.literalsB[i])

            add_edge(edges, A_neg, B)
            add_edge(edges, B_neg, A)

        return edges

    # 1. DFS cez graf - naplni sa stack
    def DFS1_fill_stack(self, destination, visited, vertices_stack):

        if visited[destination]:
            return

        visited[destination] = True

        for i in self.edges[destination]:
            self.DFS1_fill_stack(i, visited, vertices_stack)

        vertices_stack.append(destination)

    # 2. DFS cez transponovany graf - naplni sa SCC
    def DFS2_fill_SCC(self, SCC, edges_transp, source, component_id):
        SCC[source] = component_id
        for destination in edges_transp[source]:
            if SCC[destination] == -1:
                self.DFS2_fill_SCC(SCC, edges_transp, destination, component_id)

    # riesenie SAT - Kosaraju's algorithm
    def is_2SAT(self):

        nb_vertices = self.nb_var * 2
        vertices_stack = []

        # keys = self.edges.keys()
        visited = dict([(k, False) for k in sorted(self.edges.keys())])

        ''' ************* 1. DFS prechod cez graf, naplneni sa stack[] ************** '''

        for i in sorted(visited.keys()):
            if not visited[i]:
                self.DFS1_fill_stack(i, visited, vertices_stack)

        ''' ******** 2. DFS prechod cez transponovany graf, naplni sa SCC[] ******** '''

        # comp.assign(n, -1);
        SCC = dict([(k, -1) for k in sorted(self.edges.keys())])

        component_id = 0
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

    # depth-first search
    # def dfs(self, destination, visited):
    #     visited[destination] = True
    #     print(destination, end=' ')
    #     for i in self.edges[destination]:
    #         if not visited[i]:
    #             self.dfs(i, visited)

    # vypis strongly-connected komponentov
    # def print_SCC(self):
    #
    #     nb_vertices = self.nb_var * 2
    #     stack = []
    #
    #     # 1. krok - naplnenie stacku
    #     visited = [False] * nb_vertices
    #     for i in range(nb_vertices):
    #         if not visited[i]:
    #             self.DFS1_fill_stack(i, visited, stack)
    #
    #     # 2. krok - naplnenie a vypis SCC
    #     graph_trans = self.transpose()
    #     visited = [False] * nb_vertices
    #     while stack:
    #         i = stack.pop()
    #         if not visited[i]:
    #             print("{ ", end="")
    #             graph_trans.dfs(i, visited)
    #             print("}")
