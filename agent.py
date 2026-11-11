
import json
from openai import OpenAI

import config

from tools.stubs import (
    load_data,
    build_graph,
    detect_communities,
    summarize_community,
    plot_network,
)


# --------------------------------------------------
# 1. CONNECT TO BIGMODEL
# --------------------------------------------------

client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)


# --------------------------------------------------
# 2. STORE THE AGENT'S DATA
# --------------------------------------------------

state = {}


# --------------------------------------------------
# 3. DEFINE THE FIVE TOOL FUNCTIONS
# --------------------------------------------------

def tool_load_data(topic, limit):

    # Clear results from the previous analysis.
    state.pop("graph", None)
    state.pop("communities", None)

    # Load the new dataset.
    state["df"] = load_data(topic, limit)

    return (
        f"Successfully loaded {len(state['df'])} posts "
        f"about '{topic}'."
    )


def tool_build_graph():

    if "df" not in state:
        raise ValueError("Load data before building the graph.")

    state["graph"] = build_graph(state["df"])

    graph = state["graph"]

    return (
        f"Graph created successfully. "
        f"Users: {graph.number_of_nodes()}, "
        f"Connections: {graph.number_of_edges()}."
    )


def tool_detect_communities():

    if "graph" not in state or "df" not in state:
        raise ValueError(
            "Load data and build the graph before detecting communities."
        )

    state["communities"] = detect_communities(state["graph"])

    state["df"]["community"] = (
        state["df"]["user"].map(state["communities"])
    )

    # Calculate actual members and post counts.
    community_details = []

    for community_id in sorted(set(state["communities"].values())):

        members = sorted(
            user
            for user, assigned_id in state["communities"].items()
            if assigned_id == community_id
        )

        post_count = int(
            (state["df"]["community"] == community_id).sum()
        )

        community_details.append({
            "community_id": community_id,
            "members": members,
            "post_count": post_count
        })

    result = {
        "total_communities": len(community_details),
        "communities": community_details
    }

    return json.dumps(result, indent=2)


def tool_summarize_community(community_id):

    if "df" not in state or "communities" not in state:
        raise ValueError(
            "Load data and detect communities first."
        )

    return summarize_community(state["df"], community_id)


def tool_plot_network():

    if "graph" not in state or "communities" not in state:
        raise ValueError(
            "Build the graph and detect communities first."
        )

    return plot_network(
        state["graph"],
        state["communities"]
    )


# --------------------------------------------------
# 4. REGISTER THE TOOLS
# --------------------------------------------------

TOOLS = {
    "load_data": tool_load_data,
    "build_graph": tool_build_graph,
    "detect_communities": tool_detect_communities,
    "summarize_community": tool_summarize_community,
    "plot_network": tool_plot_network,
}


# --------------------------------------------------
# 5. DESCRIBE THE TOOLS TO GLM
# --------------------------------------------------

TOOL_SPECS = [

    {
        "type": "function",
        "function": {
            "name": "load_data",
            "description": "Load simulated sample community posts about a given topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic for the sample posts."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of posts to load."
                    }
                },
                "required": ["topic", "limit"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "build_graph",
            "description": "Build a network graph from the loaded community posts.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "detect_communities",
            "description": "Detect groups of connected users and return their actual members and post counts.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "summarize_community",
            "description": "Return the actual posts and users belonging to a specific community.",
            "parameters": {
                "type": "object",
                "properties": {
                    "community_id": {
                        "type": "integer",
                        "description": "The ID of the community to summarize."
                    }
                },
                "required": ["community_id"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "plot_network",
            "description": "Create and save a visualization of the community network.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        }
    }

]


# --------------------------------------------------
# 6. EXECUTE A REQUESTED TOOL
# --------------------------------------------------

def run_tool(name, arguments):

    if name not in TOOLS:
        return f"Error: Tool '{name}' does not exist."

    try:
        result = TOOLS[name](**arguments)
        return str(result)

    except TypeError as error:
        return f"Error: Incorrect arguments for {name}: {error}"

    except Exception as error:
        return f"Error while executing {name}: {error}"


# --------------------------------------------------
# 7. INITIALIZE CONVERSATION HISTORY
# --------------------------------------------------

messages = [

    {
        "role": "system",
        "content": """
You are a helpful community analysis AI agent.

Your job is to help users understand community discussions
and relationships between users.

You have five tools:
- load_data
- build_graph
- detect_communities
- summarize_community
- plot_network

IMPORTANT RULES:

1. Use tools when necessary to answer questions.

2. Follow this order when performing a complete analysis:
   a. Load the data.
   b. Build the network graph.
   c. Detect communities.
   d. Summarize communities when requested.
   e. Plot the network when requested.

3. Use actual tool results as the source of truth.

4. Never invent community members, post counts,
   connections, discussion topics, or statistics.

5. If a tool reports an error, explain the error
   instead of claiming the operation succeeded.

6. The sample data is simulated data, not live internet data.
   Never claim that it was collected from the internet.

7. Remember the previous questions and tool results
   in the current conversation.

8. When new data is loaded, use the latest tool results
   for subsequent analysis.

9. Explain findings clearly and simply.
"""
    }

]


# --------------------------------------------------
# 8. BUILD THE AGENT LOOP
# --------------------------------------------------

def ask_agent(user_question):

    # Add the new question to the existing conversation.
    messages.append({
        "role": "user",
        "content": user_question
    })

    max_iterations = 8

    for iteration in range(max_iterations):

        response = client.chat.completions.create(
            model=config.MODEL,
            messages=messages,
            tools=TOOL_SPECS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # If GLM does not request a tool, return its final answer.
        if not assistant_message.tool_calls:

            answer = (
                assistant_message.content
                or "The model returned an empty response."
            )

            messages.append({
                "role": "assistant",
                "content": answer
            })

            return answer

        # Save the assistant's tool request.
        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # Execute every tool requested by GLM.
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:
                arguments = None

            if not isinstance(arguments, dict):
                result = "Error: The tool arguments were not valid JSON."

            else:
                result = run_tool(tool_name, arguments)

            # Send the tool result back to GLM.
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "The agent reached its maximum number of tool-calling rounds."
