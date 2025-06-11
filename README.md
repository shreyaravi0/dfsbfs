# 🎥 Graph Traversal & Social Network Simulator

An interactive Streamlit web app for visualizing **BFS** and **DFS** traversal on both **directed/undirected** and **weighted/unweighted** graphs. It also simulates real-world **social network analysis** features like friend recommendations, top influencers, and community detection.

## 🚀 Features

- ✅ **Add nodes and edges** manually or generate random graphs.
- ✅ Choose between **directed** or **undirected** graph.
- ✅ Visualize **BFS** or **DFS traversal** step-by-step with animation.
- ✅ Simulate **friend suggestions**, **community detection**, and **top influencers**.
- ✅ Real-time graph updates and visual feedback.
- ✅ Clean and user-friendly UI with custom CSS enhancements.

## 🧠 Social Network Use Cases

- **Friend Detection**: Suggest friends based on mutual connections.
- **Top Influencers**: Identify users with the highest centrality.
- **Community Detection**: Group users into communities using modularity algorithms.

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** – Interactive UI for Python apps.
- **[NetworkX](https://networkx.org/)** – Graph creation and analysis.
- **Python** – Core language.
- **Matplotlib** – For graph plotting (via `draw_graph()`).
- **Custom CSS** – For UI enhancement.


## 🧑‍💻 Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shreyaravi0/dfsbfs
   cd DFSBFS

## 🐍 Create and Activate a Virtual Environment

### On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
```
### On Windows: 
   ```bash
      python -m venv venv
      venv\Scripts\activate
   ``` 


## 📄 Install Required Packages

Make sure you're inside the virtual environment, then run:

```bash
pip install -r requirements.txt
```

## 📂 Navigate to Project Folder 

If your app is inside a subfolder (like label), go into it:

```bash
cd label
```

## 🚀 Run the Application

```bash
streamlit run app.py
```
