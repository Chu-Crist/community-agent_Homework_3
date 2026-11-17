"""Community summaries (Person 4).

summarize_community(df, community_id) -> str

Expects df to have the columns: user, text, timestamp, reply_to, community.
The 'community' column is added by agent.tool_detect_communities().
"""
import re
from collections import Counter

import pandas as pd

STOPWORDS = set("""
the a an and or but if of to in on for with is are was were be been being this that
these those it its as at by from i you we they he she not no have has had do does did
so just about what when who whom how why my your their our me them his her can could
will would should there here than then too very really like get got one also more some
any all im ive dont doesnt didnt isnt thats youre theyre cant wont much many even still
into out up down over only other which while where because though yeah yes lol use
using used make made want need think know see going way thing things people something
""".split())

# Tiny sentiment lexicon, used only if vaderSentiment is not installed.
_POS = set("""good great love like best better nice awesome amazing fast excellent
helpful thanks thank cool perfect fun works happy impressive solid smart useful
enjoy favorite wonderful""".split())
_NEG = set("""bad worse worst hate slow terrible awful broken bug bugs wrong useless
problem problems issue issues fail fails failed annoying garbage trash stupid
disappointing sucks lose loses lost crash crashes""".split())


def _keywords(texts, n=8):
    words = []
    for t in texts:
        words += [w for w in re.findall(r"[a-z][a-z0-9\.\-]{2,}", str(t).lower())
                  if w not in STOPWORDS and not w.startswith("http")]
    return [w for w, _ in Counter(words).most_common(n)]


def _sentiment(texts):
    """Average sentiment in [-1, 1]. VADER if available, else a small lexicon."""
    if not texts:
        return 0.0, "lexicon"
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
        scores = [sia.polarity_scores(str(t))["compound"] for t in texts]
        return sum(scores) / len(scores), "VADER"
    except ImportError:
        scores = []
        for t in texts:
            toks = re.findall(r"[a-z']+", str(t).lower())
            pos = sum(w in _POS for w in toks)
            neg = sum(w in _NEG for w in toks)
            scores.append((pos - neg) / (pos + neg) if (pos + neg) else 0.0)
        return sum(scores) / len(scores), "lexicon"


def _label(score):
    if score > 0.15:
        return "positive"
    if score < -0.15:
        return "negative"
    return "neutral/mixed"


def _llm_describe(keywords, samples):
    """2-3 sentence LLM description. Imported lazily so tests work without .env."""
    from openai import OpenAI
    import config

    client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
    prompt = (
        "You are describing one user community from a Reddit discussion.\n"
        f"Top keywords: {', '.join(keywords)}\n"
        "Sample posts:\n- " + "\n- ".join(s[:300] for s in samples) +
        "\n\nIn 2-3 sentences, describe what this community discusses and its "
        "overall tone. Use only the information above; do not invent details."
    )
    resp = client.chat.completions.create(
        model=config.MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return (resp.choices[0].message.content or "").strip()


def summarize_community(df: pd.DataFrame, community_id) -> str:
    """Summarize one community: size, keywords, active users, sentiment,
    sample posts, and an LLM-written description."""
    if "community" not in df.columns:
        return "Error: no 'community' column. Run detect_communities first."

    try:
        community_id = int(community_id)
    except (TypeError, ValueError):
        return f"Error: community_id must be an integer, got {community_id!r}."

    sub = df[df["community"] == community_id]
    if sub.empty:
        valid = sorted(int(c) for c in df["community"].dropna().unique())
        return (f"Error: community {community_id} not found. "
                f"Valid ids: {valid[:30]}{' ...' if len(valid) > 30 else ''}")

    texts = sub["text"].astype(str).tolist()
    users = sub["user"].nunique()
    kws = _keywords(texts)
    top_users = sub["user"].value_counts().head(3).to_dict()
    samples = sub.sample(min(3, len(sub)), random_state=0)["text"].astype(str).tolist()
    score, method = _sentiment(texts)

    if len(sub) < 2:
        desc = "Too few posts for a reliable description (single-post community)."
    else:
        try:
            desc = _llm_describe(kws, samples)
        except Exception as e:  # API failure must not crash the agent
            desc = f"(LLM description unavailable: {e})"

    sample_lines = "\n".join(f"  - {s[:200].strip()}" for s in samples)
    return (
        f"Community {community_id}: {len(sub)} posts from {users} users\n"
        f"Top keywords: {', '.join(kws) if kws else 'n/a'}\n"
        f"Most active users: {top_users}\n"
        f"Sentiment ({method}, -1 to 1): {score:.2f} ({_label(score)})\n"
        f"Description: {desc}\n"
        f"Sample posts:\n{sample_lines}"
    )
