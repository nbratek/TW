from collections import deque


class FoataNormalForm:
    def __init__(self, alphabet, dependency_rel):
        self.alphabet = alphabet
        self.dependency_relations = dependency_rel.dependency_relations
        self.word = []
        self.graph_edges = []
        self.graph_labels = []

    def compute_dependency_graph(self, word):
        self.word = word
        labels = []
        self.word = word
        self.graph_labels = list(self.word)
        self.graph_edges = []
        for idx, current_symbol in enumerate(self.graph_labels):
            for prev_idx in range(idx):
                prev_symbol = self.graph_labels[prev_idx]
                if (prev_symbol, current_symbol) in self.dependency_relations:
                    self.graph_edges.append((prev_idx, idx))
        for v in range(len(labels)):
            self.__bfs(v)

    def __bfs(self, source_node):
        visited = [False] * len(self.graph_labels)
        reach_count = [0] * len(self.graph_labels)
        queue = deque([source_node])
        while queue:
            current_node = queue.popleft()
            for edge_start, edge_end in self.graph_edges:
                if edge_start == current_node:
                    if not visited[edge_end]:
                        queue.append(edge_end)
                        visited[edge_end] = True
                    reach_count[edge_end] += 1
        updated_edges = []
        for start, end in self.graph_edges:
            if not (start == source_node and reach_count[end] > 1):
                updated_edges.append((start, end))
        self.graph_edges = updated_edges

    def compute_foata_form(self):
        in_degree = {i: 0 for i in range(len(self.graph_labels))}
        for edge in self.graph_edges:
            in_degree[edge[1]] += 1
        queue = [i for i in range(len(self.graph_labels)) if in_degree[i] == 0]
        group = [-1] * len(self.graph_labels)
        current_group = 0
        while queue:
            next_queue = []
            for node in queue:
                group[node] = current_group

                for edge in self.graph_edges:
                    if edge[0] == node:
                        in_degree[edge[1]] -= 1
                        if in_degree[edge[1]] == 0:
                            next_queue.append(edge[1])
            queue = next_queue
            current_group += 1
        fnf = [[] for _ in range(current_group)]
        for i, g in enumerate(group):
            fnf[g].append(self.graph_labels[i])
        return fnf

    @staticmethod
    def is_symbol_pair_dependent(dependency_set, symbol1, symbol2):
        return any(pair for pair in dependency_set if pair == (symbol1, symbol2))

    @staticmethod
    def fnf_to_string(fnf):
        return ''.join(f"({''.join(sorted(layer))})" for layer in fnf)





