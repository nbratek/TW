from dependency import Dependency
from foata_normal_form import FoataNormalForm
from fnf import Foata
from graph import DependencyGraphBuilder


def main():
    alphabet = {"a", "b", "c", "d"}
    transactions = {
        "a": "x=x+y",
        "b": "y=y+2z",
        "c": "x=3x+z",
        "d": "z=y-z"
    }
    word = list("baadcb")

    # alphabet = {"a", "b", "c", "d", "e", "f"}
    # transactions = {
    #     "a": "x=y+z",
    #     "b": "y=x+w+y",
    #     "c": "x=x+y+v",
    #     "d": "w=v+z",
    #     "e": "v=x+v+w",
    #     "f": "z=y+z+v"
    # }
    # word = list("acdcfbbe")

    print("Dependency Test")
    dependency_object = Dependency(alphabet, transactions)
    print("Dependency Relations:")
    print(sorted(dependency_object.dependency_relations))
    print("Independency Relations:")
    print(sorted(dependency_object.independency_relations))

    print("\nFoataNormalForm Test")
    fnf_calculator = FoataNormalForm(alphabet, dependency_object)
    fnf_calculator.compute_dependency_graph(word)
    foata_form = fnf_calculator.compute_foata_form()
    print("Foata Normal Form (FNF):", foata_form)
    print("FNF as string:", fnf_calculator.fnf_to_string(foata_form))

    print("\nFoata Test")
    foata = Foata(alphabet, word, dependency_object)
    foata_fnf = foata.compute_Foata_Normal_Form()
    print("Foata Normal Form (FNF):", foata_fnf)
    print("FNF as string:", foata.fnf_to_string(foata_fnf))

    print("\nDependencyGraphBuilder Test")
    graph_builder = DependencyGraphBuilder(word, dependency_object)
    graph_builder.build_graph()
    graph_builder.save_graph_to_file("graph")


if __name__ == "__main__":
    main()

