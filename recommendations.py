import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

# Color constants
CURRENT_NODE_COLOR = "orange"
DIRECT_FRIEND_COLOR = "lightgreen"
RECOMMENDED_FRIEND_COLOR = "lightcoral"
OTHER_NODE_COLOR = "lightblue"
WEIGHTED_EDGE_COLOR = "darkgrey"

# Friend recommendation logic
def get_weighted_recommendations(graph, user):
    direct = set(graph.neighbors(user))
    second = set()
    for friend in direct:
        second.update(graph.neighbors(friend))
    
    recommendations = second - direct - {user}
    weighted_scores = {}
    for recommended in recommendations:
        score = 0
        for friend in direct:
            if graph.has_edge(friend, recommended):
                score += graph[friend][recommended].get("weight", 1)
        weighted_scores[recommended] = score

    sorted_recommendations = sorted(weighted_scores, key=weighted_scores.get, reverse=True)
    return sorted_recommendations

# Draw the recommendation graph with colors
def draw_recommendation_graph(G, direct_friends, recommendations, current):
    pos = nx.spring_layout(G, seed=42)
    colors = []
    for node in G.nodes:
        if node == current:
            colors.append(CURRENT_NODE_COLOR)
        elif node in recommendations:
            colors.append(RECOMMENDED_FRIEND_COLOR)
        elif node in direct_friends:
            colors.append(DIRECT_FRIEND_COLOR)
        else:
            colors.append(OTHER_NODE_COLOR)

    plt.clf()
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, edge_color=WEIGHTED_EDGE_COLOR)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(plt.gcf())

# Social media simulation features
def social_media_simulation(G):
    feature = st.sidebar.selectbox("Select Feature",
                                   ["Path Between Users",
                                    "Friend Suggestions",
                                    "Community Detection",
                                    "Top Influencers"], key="social_feature")

    if feature == "Path Between Users":
        user1 = st.sidebar.selectbox("User 1", list(G.nodes), key="path_user1")
        user2 = st.sidebar.selectbox("User 2", list(G.nodes), key="path_user2")
        if st.sidebar.button("Find Path"):
            if nx.has_path(G, user1, user2):
                path = nx.shortest_path(G, source=user1, target=user2)
                st.success(f"Shortest Path: {' → '.join(path)}")
            else:
                st.error("No path exists between the selected users.")

    elif feature == "Friend Suggestions":
        user = st.sidebar.selectbox("Select User", list(G.nodes), key="suggest_user")
        if st.sidebar.button("Suggest"):
            recommendations = get_weighted_recommendations(G, user)
            st.markdown(f"### 🔗 Recommendations for `{user}`:")
            if recommendations:
                for r in recommendations:
                    st.markdown(f"- {r}")
            else:
                st.info("No recommendations available.")
            draw_recommendation_graph(G, set(G.neighbors(user)), recommendations, user)

    elif feature == "Community Detection":
        try:
            import community
            partition = community.best_partition(G)
            st.markdown("### 🧠 Community Detection Result")
            communities = {}
            for node, com_id in partition.items():
                communities.setdefault(com_id, []).append(node)

            for cid, members in communities.items():
                st.markdown(f"- Community {cid + 1}: {', '.join(members)}")

            pos = nx.spring_layout(G)
            plt.clf()
            cmap = plt.get_cmap('viridis')
            colors = [partition[node] for node in G.nodes]
            nx.draw(G, pos, node_color=colors, with_labels=True, node_size=800)
            st.pyplot(plt.gcf())

        except ImportError:
            st.warning("`community` module not installed. Run `pip install python-louvain`.")

    elif feature == "Top Influencers":
        centrality = nx.degree_centrality(G)
        sorted_users = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        top_k = st.sidebar.slider("Top K Influencers", 1, 10, 3)
        st.markdown("### 👑 Top Influencers")
        for i, (user, score) in enumerate(sorted_users[:top_k]):
            st.markdown(f"{i+1}. `{user}` with score **{score:.3f}**")
