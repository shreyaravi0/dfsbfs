import streamlit as st
import networkx as nx
from graph_utils import init_graph, add_node, add_edge, generate_random_graph, draw_graph
from traversal import bfs_dfs_traversal
from recommendations import social_media_simulation
import time

st.set_page_config(page_title="Graph Visualizer", layout="wide")
st.title("🎥 Graph Traversal & Social Network Simulation")

graph_type = st.sidebar.radio("Graph Type", ["Undirected", "Directed"])

G = init_graph(graph_type)

st.sidebar.header("Graph Controls")
node = st.sidebar.text_input("Add Node")
if st.sidebar.button("Add Node"):
    add_node(G, node)

edge_input = st.sidebar.text_input("Add Edge (A,B) with weight")
if st.sidebar.button("Add Edge"):
    add_edge(G, edge_input)

if st.sidebar.button("Clear Graph"):
    G.clear()

st.sidebar.markdown("---")
st.sidebar.subheader("Generate Random Graph")
generate_random_graph(G, graph_type)

col1, col2 = st.columns([3, 1])

with col2:
    st.subheader("Traversal Settings")
    algo = st.radio("Choose Algorithm", ["BFS", "DFS"], key="algo_choice")
    start = st.selectbox("Start Node", list(G.nodes), key="start_node")
    speed = st.slider("Speed (seconds)", 0.2, 2.0, 0.8)
    run = st.button("Run Traversal")

    st.markdown("---")
    st.subheader("Connect Nodes")
    user1 = st.selectbox("User 1", list(G.nodes), key="connect1")
    user2 = st.selectbox("User 2", list(G.nodes), key="connect2")
    weight = st.slider("Edge Weight", 1, 10, 5)
    if st.button("Connect"):
        if user1 != user2:
            G.add_edge(user1, user2, weight=weight)
            st.success(f"Connected {user1} ↔ {user2} with weight {weight}")

# Traversal
if run:
    visited = []
    queue = [start]
    with col1:
        placeholder = st.empty()
    while queue:
        current = queue.pop(0) if algo == "BFS" else queue.pop()
        if current not in visited:
            visited.append(current)
            neighbors = [n for n in G.neighbors(current) if n not in visited and n not in queue]
            queue.extend(neighbors if algo == "BFS" else reversed(neighbors))

            with placeholder.container():
                st.subheader(f"🔍 Visiting: {current}")
                draw_graph(G, visited, current)
                time.sleep(speed)

    with col1:
        st.success(f"{algo} Traversal Done! Path: {' → '.join(visited)}")

# Run social media simulation (Friend Suggestion, Community Detection, etc.)
with col1:
    st.subheader("🌐 Social Media Simulation")
    social_media_simulation(G)

if not run:
    with col1:
        st.subheader("Current Graph")
        draw_graph(G, visited=[], current=None)
