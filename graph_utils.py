import networkx as nx
import random
import streamlit as st
import matplotlib.pyplot as plt

def init_graph(graph_type):
    """Initialize a graph based on the selected graph type."""
    if "G" not in st.session_state or st.session_state["type"] != graph_type:
        if graph_type == "Directed":
            st.session_state.G = nx.DiGraph()
        else:
            st.session_state.G = nx.Graph()
        st.session_state["type"] = graph_type
    return st.session_state.G

def add_node(G, node):
    """Add a node to the graph."""
    G.add_node(node)

def add_edge(G, edge_input):
    """Add an edge to the graph given input."""
    try:
        u, v, weight = edge_input.split(",")
        G.add_edge(u.strip(), v.strip(), weight=int(weight.strip()))
    except:
        st.warning("Enter edge format as A,B,weight")



def generate_random_graph(G, graph_type):
    """Generate a random graph with the given parameters."""
    rand_nodes = st.sidebar.number_input("Number of Nodes", min_value=1, step=1, key="rand_nodes")
    rand_edges = st.sidebar.number_input("Number of Edges", min_value=0, step=1, key="rand_edges")
    generate_random = st.sidebar.button("Generate Random Graph")

    if generate_random:
        max_edges = rand_nodes * (rand_nodes - 1)
        if graph_type == "Undirected":
            max_edges //= 2
            random_G = nx.gnm_random_graph(rand_nodes, rand_edges)
        else:
            random_G = nx.gnm_random_graph(rand_nodes, rand_edges, directed=True)

        if rand_edges <= max_edges:
            G.clear()
            mapping = {i: f"N{i}" for i in range(rand_nodes)}
            G.add_nodes_from([mapping[i] for i in random_G.nodes()])
            for u, v in random_G.edges():
                G.add_edge(mapping[u], mapping[v], weight=random.randint(1, 10))  # Assigning random weights
            st.sidebar.success(f"Generated {graph_type.lower()} graph with {rand_nodes} nodes and {rand_edges} edges.")
        else:
            st.sidebar.warning("Too many edges for the given number of nodes.")

def draw_graph(G, visited, current=None):
    """Draw the graph with colors indicating the traversal."""
    pos = nx.spring_layout(G, seed=42)
    colors = []
    for node in G.nodes:
        if node == current:
            colors.append("orange")
        elif node in visited:
            colors.append("lightgreen")
        else:
            colors.append("lightblue")

    plt.clf()
    edge_labels = nx.get_edge_attributes(G, 'weight')  # Get edge weights
    if isinstance(G, nx.DiGraph):
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_size=14, arrows=True)
    else:
        nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_size=14)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Display edge weights
    st.pyplot(plt.gcf())
