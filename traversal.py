import time
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from graph_utils import draw_graph

def bfs_dfs_traversal(G, algo, start, speed, col1):
    """Perform BFS/DFS traversal and display the process."""
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
        st.success(f"{algo} Complete! Path: {' → '.join(visited)}")
