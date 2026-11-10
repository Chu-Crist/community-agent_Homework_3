import pandas as pd
import networkx as nx


def load_data(topic, limit):
    data = {
        "user": ["alice", "bob", "carol", "dave", "alice", "bob"],
        "text": [
            f"I think {topic} is really important",
            f"I disagree, {topic} is overrated",
            f"Has anyone read the latest news about {topic}?",
            f"Yes, the news about {topic} worries me",
            f"@bob why do you say {topic} is overrated?",
            f"@alice because the data on {topic} is mixed",
        ],
        "timestamp": [
            "2026-11-01 09:00",
            "2026-11-01 09:05",
            "2026-11-01 09:10",
            "2026-11-01 09:15",
            "2026-11-01 09:20",
            "2026-11-01 09:25",
        ],
        "reply_to": [None, "alice", None, "carol", "bob", "alice"],
    }
    df = pd.DataFrame(data)
    df = df.head(limit)
    return df


def build_graph(df):
    graph = nx.Graph()
    for _, row in df.iterrows():
        graph.add_node(row["user"])
        if pd.notna(row["reply_to"]):
            graph.add_edge(row["user"], row["reply_to"])
    return graph

def detect_communities(graph):
    communities = {}
    for community_id, members in enumerate(nx.connected_components(graph)):
        for user in sorted(members):
            communities[user] = community_id
    return communities

def summarize_community(df, community_id):
    members = df[df["community"] == community_id]
    users = sorted(members["user"].unique())
    return f"Community {community_id} has {len(members)} posts by {', '.join(users)}."

def plot_network(graph, communities):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    colors = [communities[user] for user in graph.nodes]
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, node_color=colors, cmap=plt.cm.Set2,
            with_labels=True, node_size=800)
    plt.savefig("network.png")
    plt.close()
    return "network.png"