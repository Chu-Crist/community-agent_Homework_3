
from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "data"
    / "comments"
    / "subreddit=LocalLLaMA"
    / "part-0.parquet"
)


def load_data(topic, limit):
    """
    Load and clean Reddit comments for a requested topic.

    Parameters
    ----------
    topic : str
        Subreddit name or keyword to filter the comments.
    limit : int
        Maximum number of comments to return.

    Returns
    -------
    pandas.DataFrame
        Cleaned DataFrame with columns:
        user, text, timestamp, reply_to.
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative or None")

    # Load the original dataset
    df = pd.read_parquet(DATASET_PATH)

    # Check required source columns
    required_columns = {
        "id", "subreddit", "parent_id",
        "author", "created_utc", "body"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing dataset columns: {missing_columns}"
        )

    # Remove comments without valid authors
    df = df.dropna(subset=["author", "body", "id"]).copy()

    df["author"] = df["author"].astype(str).str.strip()
    df["body"] = df["body"].astype(str).str.strip()

    # Remove deleted or empty users and comments
    invalid_authors = ["", "[deleted]", "[removed]"]
    invalid_bodies = ["", "[deleted]", "[removed]"]

    df = df[
        ~df["author"].str.lower().isin(
            [x.lower() for x in invalid_authors]
        )
    ]

    df = df[
        ~df["body"].str.lower().isin(
            [x.lower() for x in invalid_bodies]
        )
    ]

    # Remove duplicate comments
    df = df.drop_duplicates(subset=["id"])

    # Filter by subreddit or keyword
    if topic and str(topic).strip():
        topic = str(topic).strip()

        subreddit_match = (
            df["subreddit"]
            .astype(str)
            .str.contains(topic, case=False, regex=False, na=False)
        )

        text_match = (
            df["body"]
            .str.contains(topic, case=False, regex=False, na=False)
        )

        df = df[subreddit_match | text_match]

    # Build a mapping from comment ID to its author
    comment_authors = dict(zip(df["id"], df["author"]))

    # Resolve parent comment IDs to parent authors
    def find_parent_author(parent_id):
        if pd.isna(parent_id):
            return None

        parent_id = str(parent_id)

        if parent_id not in comment_authors:
            return None

        return comment_authors[parent_id]

    df["reply_to"] = df["parent_id"].apply(find_parent_author)

    # A comment replying to the original submission
    # does not represent a user-to-user interaction.
    df.loc[
        df["parent_id"] == df["link_id"],
        "reply_to"
    ] = None

    # Convert Unix timestamps into readable UTC datetimes
    df["timestamp"] = pd.to_datetime(
        df["created_utc"],
        unit="s",
        utc=True
    )

    # Rename columns to the shared project format
    df = df.rename(
        columns={
            "author": "user",
            "body": "text"
        }
    )

    # Select the four agreed columns
    df = df[
        ["user", "text", "timestamp", "reply_to"]
    ].copy()

    # Apply the requested limit
    if limit is not None:
        df = df.head(limit)

    return df.reset_index(drop=True)
