from queue import Queue
from Graph import Graph
from Task import Task


class FoataNormalForm:
    def __init__(self, n):
        self.n = n
        self.alphabet, self.word = self.construct_alphabet()
        self.dependency_relations = self.construct_dependency_relation()
        self.graph = Graph(self.alphabet, self.dependency_relations)
        self.fnf = self.foata_normal_form()

    def task_a(self, i, k):
        return Task("A", i, None, k)

    def task_b_and_c(self, i, k, j):
        B = Task("B", i, j, k)
        C = Task("C", i, j, k)
        return B, C

    def construct_alphabet(self):
        word, alphabet = [], []
        for i in range(1, self.n + 1):
            for k in range(i + 1, self.n + 1):
                A = self.task_a(i, k)
                alphabet.append(A)
                word.append(A)
                for j in range(i, self.n + 2):
                    B, C = self.task_b_and_c(i, k, j)
                    alphabet.extend([B, C])
                    word.extend([B, C])
        return alphabet, word

    def construct_dependency_relation(self):
        dependency_rel = []
        for s in self.alphabet:
            for t in self.alphabet:
                if s.task_name == "A" and t.task_name == "C" and s.i - 1 == t.i and s.i == t.j and (s.i == t.k or s.k == t.k):
                    dependency_rel.append((s, t))
                elif s.task_name == "B" and t.task_name == "A" and s.i == t.i and s.k == t.k:
                    dependency_rel.append((s, t))
                elif s.task_name == "B" and t.task_name == "C" and s.i - 1 == t.i and s.j == t.j and s.k - 1 == t.k:
                    dependency_rel.append((s, t))
                elif s.task_name == "C" and t.task_name == "B" and s.i == t.i and s.j == t.j and s.k == t.k:
                    dependency_rel.append((s, t))
                elif s.task_name == "C" and t.task_name == "C" and s.i - 1 == t.i and s.j == t.j and s.k == t.k:
                    dependency_rel.append((s, t))
        return dependency_rel

    def initialize_classes(self, graph):
        all_targets = set()
        for edges in graph:
            all_targets.update(edges)
        num_vertices = len(graph)
        start_points = {i for i in range(num_vertices) if i not in all_targets}
        classes = [-1] * num_vertices
        for point in start_points:
            classes[point] = 0
        return classes

    def build_foata_normal_form(self, classes):
        graph = self.graph.graph_adj_list
        q = Queue()
        for vertex, cls in enumerate(classes):
            if cls == 0:
                q.put(vertex)
        while not q.empty():
            tmp = q.get()
            for neighbor in graph[tmp]:
                if classes[neighbor] == -1:
                    classes[neighbor] = classes[tmp] + 1
                    q.put(neighbor)
        max_class = max(classes)
        fnf_classes = [[] for _ in range(max_class + 1)]
        for vertex, cls in enumerate(classes):
            if cls != -1:
                fnf_classes[cls].append(self.alphabet[vertex])
        return fnf_classes

    def foata_normal_form(self):
        classes = self.initialize_classes(self.graph.graph_adj_list)
        return self.build_foata_normal_form(classes)

