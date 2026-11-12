\# Community AI Agent Architecture



```mermaid

flowchart TD

&#x20;   A\["User input: Topic + comment limit"] --> B\["Agent Orchestrator"]

&#x20;   B --> C\["load\_data(topic, limit)"]

&#x20;   C --> D\["Cleaned and standardized DataFrame"]

&#x20;   D --> E\["build\_graph(df)"]

&#x20;   E --> F\["Weighted NetworkX Interaction Graph"]

&#x20;   F --> G\["detect\_communities(graph)"]

&#x20;   D --> H\["summarize\_community(df, community\_id)"]

&#x20;   G --> H

&#x20;   F --> I\["plot\_network(graph, communities)"]

&#x20;   G --> I

&#x20;   H --> J\["Community summaries"]

&#x20;   I --> K\["Network visualization"]

&#x20;   J --> L\["Agent results"]

&#x20;   K --> L

```



\*\*Person 2 contribution:\*\* `tools/data.py` and `tools/graph.py`.

