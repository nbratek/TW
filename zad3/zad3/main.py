from GaussianElimination import GaussianElimination
import numpy as np
from fnf import FoataNormalForm
import textwrap


def load_matrix(filepath="in.txt"):
    try:
        with open(filepath, 'r') as file:
            data = file.readlines()
        if not data:
            raise ValueError("The file is empty.")
        size = int(data[0].strip())
        matrix = [list(map(float, line.split())) for line in data[1:size + 1]]
        additional_column = list(map(float, data[size + 1].strip().split()))
        for index, value in enumerate(additional_column):
            matrix[index].append(value)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found")
    except ValueError as e:
        raise ValueError(f"Error processing data: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
    numpy_matrix = np.array(matrix)
    return numpy_matrix, size


def write_matrix_to_file(matrix, size, file_path="result.txt"):
    with open(file_path, 'w') as output_file:
        output_file.write(f"{size}\n")
        for row in matrix:
            row_data = ' '.join(map(str, row[:-1])) + '\n'
            output_file.write(row_data)
        last_column_data = ' '.join(map(str, matrix[:, -1])) + '\n'
        output_file.write(last_column_data)


def run_gaussian_elimination(filepath_source="in/in.txt", filepath_result="result/result.txt"):
    try:
        matrix, n = load_matrix(filepath_source)
        gauss = GaussianElimination(matrix, n)
        matrix = gauss.run()
        write_matrix_to_file(matrix, n, filepath_result)
        print(f"Results saved to file: {filepath_result}")
        return True
    except Exception as e:
        print(f"An error during testing: {e}")
        return False


def main():
    n = 3
    fnf = FoataNormalForm(n)
    run_gaussian_elimination()
    wrapper = textwrap.TextWrapper(width=150)
    print("Alphabet and Dependency Relations")
    alphabet_output = "Alphabet = {" + ", ".join(sorted(i.idx_task_name for i in fnf.alphabet)) + "}"
    print(wrapper.fill(alphabet_output))
    dependency_output = "Dependency Relations = (" + ", ".join(f"({a.idx_task_name}, {b.idx_task_name})" for a, b in fnf.dependency_relations) + ")"
    print(wrapper.fill(dependency_output))
    print("Foata Normal Form (FNF)")
    fnf_output = "FNF = (" + ")(".join(", ".join(i.idx_task_name for i in sublist) for sublist in fnf.fnf) + ")"
    print(wrapper.fill(fnf_output))
    fnf.graph.draw_graph(save_path=f"graphs/graph_{fnf.n}")


if __name__ == "__main__":
    main()