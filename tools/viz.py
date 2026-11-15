import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def plot_network(graph, communities, out_path="outputs/network.png"):
    """Draw graph colored by community. Returns the image path."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    undirected = graph.to_undirected() if graph.is_directed() else graph

    pos = nx.spring_layout(undirected, seed=42, k=0.3)
    cmap = plt.get_cmap("tab20")
    node_colors = [cmap(communities.get(n, 0) % 20) for n in undirected.nodes()]

    plt.figure(figsize=(12, 9))
    nx.draw_networkx_nodes(undirected, pos, node_color=node_colors,
                           node_size=40, alpha=0.85)
    nx.draw_networkx_edges(undirected, pos, alpha=0.15)
    plt.title(f"Community Structure ({len(set(communities.values()))} communities)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path
