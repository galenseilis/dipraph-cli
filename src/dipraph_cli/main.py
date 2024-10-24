import ast
import os
import networkx as nx
import matplotlib.pyplot as plt
import argparse

def find_python_files(directory):
    """Recursively find all Python files in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def analyze_imports(file_path):
    """Parse a Python file and extract all imports."""
    imports = []
    with open(file_path, 'r') as file:
        try:
            tree = ast.parse(file.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    # Collect imports from modules
                    for alias in node.names:
                        imports.append(alias.name)  # e.g., 'foo' in 'from foo import bar'
                elif isinstance(node, ast.Import):
                    # Collect absolute imports
                    for alias in node.names:
                        imports.append(alias.name)  # e.g., 'foo' in 'import foo'
        except SyntaxError as e:
            print(f"Syntax error in {file_path}: {e}")
    return imports

def build_import_graph(directory):
    """Build a directed graph of imports among Python files."""
    python_files = find_python_files(directory)
    graph = nx.DiGraph()

    for file_path in python_files:
        # Extract the imports from the file
        imports = analyze_imports(file_path)
        # Get the relative file name for nodes
        current_file = os.path.relpath(file_path, directory).replace('.py', '')

        # Debug: print the current file and its imports
        print(f"File: {current_file}, Imports: {imports}")

        for imp in imports:
            graph.add_edge(current_file, imp)

    return graph

def draw_graph(graph):
    """Draw the directed graph using matplotlib."""
    if graph.number_of_edges() == 0:
        print("No imports found, the graph is empty.")
        return
    pos = nx.spring_layout(graph)  # positions for all nodes
    nx.draw(graph, pos, with_labels=True, arrows=True)
    plt.title("Directed Graph of Imports")
    plt.show()

def main():
    # Create the CLI parser
    parser = argparse.ArgumentParser(description="Construct a digraph of imports among Python files.")
    parser.add_argument('directory', type=str, help='Path to the directory containing Python files')
    
    args = parser.parse_args()
    
    import_graph = build_import_graph(args.directory)
    draw_graph(import_graph)

if __name__ == "__main__":
    main()

