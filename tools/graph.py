import networkx as nx
import pandas as pd


def build_graph(df):
    """
    Build an undirected interaction graph from cleaned Reddit comments.

    Nodes represent users.
    Edges represent replies from one user to another.
    Edge weights represent the number of replies between two users.
    """

    required_columns = {"user", "reply_to"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    graph = nx.Graph()

    # Add all users as nodes, including users without replies.
    users = df["user"].dropna().astype(str).str.strip()
    users = users[users != ""]
    graph.add_nodes_from(users.unique())

    # Build reply relationships.
    for _, row in df.iterrows():
        user = row["user"]
        reply_to = row["reply_to"]

        if pd.isna(reply_to):
            continue

        user = str(user).strip()
        reply_to = str(reply_to).strip()

        # Ignore invalid names and self-replies.
        if not user or not reply_to or user == reply_to:
            continue

        # Count repeated interactions.
        if graph.has_edge(user, reply_to):
            graph[user][reply_to]["weight"] += 1
        else:
            graph.add_edge(user, reply_to, weight=1)

    return graph