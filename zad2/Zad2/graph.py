from graphviz import Digraph
from foata_normal_form import FoataNormalForm
import os
from vertex_and_edge import VertexAndEdge


class DependencyGraphBuilder:
    def __init__(self, word, dependency_rel):
        self.word = word
        self.dependency_rel = dependency_rel
        self.dependency_rel = dependency_rel.dependency_relations
        self.vertices = []

    def is_linked(self, source_vertex, target_vertex):
        for edge in source_vertex.outgoing_edges:
            if (target_vertex.label, edge.label) in self.dependency_rel:
                return True
        return False

    def build_graph(self):
        processed_vertices = []
        self.vertices = [VertexAndEdge(symbol, idx) for idx, symbol in enumerate(self.word)]
        for vertex in self.vertices:
            for processed in processed_vertices:
                if self.should_add_edge(vertex, processed):
                    vertex.outgoing_edges.append(processed)
            processed_vertices.insert(0, vertex)

    def should_add_edge(self, vertex, processed):
        is_dependent = FoataNormalForm.is_symbol_pair_dependent(self.dependency_rel, vertex.label, processed.label)
        is_not_linked = not self.is_linked(vertex, processed)
        return is_dependent and is_not_linked

    def save_graph_to_file(self, output_name='graph2'):
        graph = Digraph(format='png')
        for vertex in self.vertices:
            graph.node(str(vertex.id), label=vertex.label)
        for vertex in self.vertices:
            for edge in vertex.outgoing_edges:
                graph.edge(str(edge.id), str(vertex.id))

        results_folder = "results"
        output_path = os.path.join(results_folder, output_name)
        output_file = graph.render(output_path)
        print(f"Graf został zapisany jako obraz: {output_file}")




