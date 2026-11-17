import networkx as nx
import community as community_louvain


def detect_communities(graph):
    """Louvain community detection. Returns dict[user, community_id]."""
    undirected = graph.to_undirected() if graph.is_directed() else graph
    partition = community_louvain.best_partition(undirected, weight="weight", random_state=42)
    return partition


def community_sizes(partition):
    """Return dict[community_id, size], largest first."""
    sizes = {}
    for node, cid in partition.items():
        sizes[cid] = sizes.get(cid, 0) + 1
    return dict(sorted(sizes.items(), key=lambda x: -x[1]))


def top_users_by_centrality(graph, partition, top_k=5):
    """Top-k users per community by degree centrality."""
    centrality = nx.degree_centrality(graph)
    result = {}
    for node, cid in partition.items():
        result.setdefault(cid, []).append((node, centrality[node]))
    return {
        cid: sorted(users, key=lambda x: -x[1])[:top_k]
        for cid, users in result.items()
    }
