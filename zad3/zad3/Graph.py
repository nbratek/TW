import graphviz


class Graph:
    def __init__(self, alphabet, dependencies):
        self.alphabet = alphabet
        self.dependency_relations = dependencies
        self.graph = graphviz.Digraph()
        self.graph_adj_list = self.build_graph()
        self.reduced_graph = self.remove_edges()

    def build_graph(self):
        dependency_index = {}
        for dep in self.dependency_relations:
            if dep[1] not in dependency_index:
                dependency_index[dep[1]] = []
            dependency_index[dep[1]].append(dep[0])
        graph = []
        for letter in self.alphabet:
            if letter in dependency_index:
                index_set = {self.alphabet.index(dep) for dep in dependency_index[letter]}
            else:
                index_set = set()
            graph.append(index_set)
        return graph

    def remove_edges(self):
        total_vertices = len(self.graph_adj_list)
        for source in range(total_vertices):
            direct_neighbors = self.graph_adj_list[source].copy()
            for neighbor in direct_neighbors:
                self.graph_adj_list[source].remove(neighbor)
                if not self.bfs(source, neighbor):
                    self.graph_adj_list[source].add(neighbor)
        return self.graph_adj_list

    def bfs(self, start, end):
        visited = [False] * len(self.graph_adj_list)
        queue = [start]
        visited[start] = True
        while queue:
            current = queue.pop(0)
            if current == end:
                return True
            for adjacent in self.graph_adj_list[current]:
                if not visited[adjacent]:
                    visited[adjacent] = True
                    queue.append(adjacent)
        return False

    def draw_graph(self, save_path=None):
        [self.graph.node(str(i), elem.idx_task_name) for i, elem in enumerate(self.alphabet)]
        [self.graph.edge(str(i), str(j)) for i, neighbors in enumerate(self.reduced_graph) for j in neighbors]
        if save_path is None:
            save_path = 'output_graph'
        self.graph.render(save_path, format="png", view=True)


