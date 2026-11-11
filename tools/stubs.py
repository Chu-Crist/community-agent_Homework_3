
import pandas as pd
import networkx as nx


def load_data(topic, limit):
    """
    Load simulated community posts about a requested topic.
    This is sample data, not live internet data.
    """

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

    df = df.head(limit).copy()
    df["topic"] = topic

    return df


def build_graph(df):
    graph = nx.Graph()

    for _, row in df.iterrows():
        graph.add_node(row["user"])

        if pd.notna(row["reply_to"]):
            graph.add_edge(row["user"], row["reply_to"])

    return graph


def detect_communities(graph):
    """
    Identify connected components in the network.
    """

    communities = {}

    for community_id, members in enumerate(
        nx.connected_components(graph)
    ):
        for user in sorted(members):
            communities[user] = community_id

    return communities


def summarize_community(df, community_id):
    """
    Return the actual posts and members of a community.
    """

    members = df[df["community"] == community_id]

    if members.empty:
        return f"Community {community_id} does not exist or has no posts."

    users = sorted(members["user"].unique())

    posts = "\n".join(
        f"- {row['user']}: {row['text']}"
        for _, row in members.iterrows()
    )

    return (
        f"Community {community_id}\n"
        f"Number of posts: {len(members)}\n"
        f"Members: {', '.join(users)}\n"
        f"Discussion posts:\n{posts}"
    )


def plot_network(graph, communities):
    """
    Create and save a network visualization.
    """

    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    if graph.number_of_nodes() == 0:
        return "Cannot plot an empty network."

    colors = [
        communities.get(user, 0)
        for user in graph.nodes
    ]

    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        node_color=colors,
        cmap=plt.cm.Set2,
        with_labels=True,
        node_size=800,
    )

    plt.savefig("network.png")
    plt.close()

    return "network.png"
