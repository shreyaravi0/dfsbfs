import streamlit as st
import networkx as nx
from graph_utils import init_graph, add_node, add_edge, generate_random_graph, draw_graph
from traversal import bfs_dfs_traversal
from recommendations import social_media_simulation
import time
st.set_page_config(page_title="Graph Visualizer", layout="wide")
st.markdown("""
    <style>
    /* Center the main title and give it some style */
    .main > div:first-child { 
        padding-top: 2rem;
    }

    h1 {
        text-align: center;
        color: #4A90E2;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f0f2f6;
        border-right: 2px solid #e0e0e0;
    }

    /* Buttons */
    .stButton > button {
        color: white;
        background: #4A90E2;
        border-radius: 10px;
        padding: 0.4em 1em;
        font-weight: bold;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #357ABD;
        transform: scale(1.03);
    }

    /* Highlight the current visiting node */
    .visiting-node {
        font-size: 1.5em;
        font-weight: bold;
        color: #d72638;
        background-color: #fce8e8;
        padding: 0.5em;
        border-radius: 8px;
        text-align: center;
    }

    /* Graph container spacing */
    .element-container:has(h2) {
        margin-top: 2rem;
    }

    /* Custom subheader colors */
    h2 {
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
        border-bottom: 2px solid #eee;
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)



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
                st.markdown(f"<div class='visiting-node'>🔍 Visiting: {current}</div>", unsafe_allow_html=True)
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



