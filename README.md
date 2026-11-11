# Community Analysis AI Agent

## 1. Project Overview

The Community Analysis AI Agent is a Python-based AI application that helps users analyse discussions and relationships within an online community.

It uses a Large Language Model (LLM) through the Zhipu BigModel API to understand user questions, select appropriate tools, execute analysis operations, and explain the results in natural language.

The current implementation uses a simulated dataset containing sample community posts.

## 2. Main Features

- Load sample community posts about a specified topic.
- Build a network graph representing relationships between users.
- Detect communities of connected users.
- Identify community members and their post counts.
- Summarize the posts belonging to a particular community.
- Generate a network visualization.
- Support multi-step tool execution through an AI agent loop.
- Maintain conversation history during a session.
- Handle tool execution errors and invalid arguments.

## 3. Technologies Used

- Python
- Zhipu BigModel GLM API
- OpenAI Python SDK
- Pandas
- NetworkX
- Matplotlib
- python-dotenv

## 4. Project Structure

```text
community-agent/
│
├── agent.py
├── main.py
├── config.py
├── .env
├── .gitignore
├── README.md
│
├── tools/
│   ├── __init__.py
│   └── stubs.py
│
├── tests/
│   └── queries.md
│
└── network.png
```

Note: Some files, such as `tests/queries.md` and `network.png`, may be generated or added during development.

## 5. Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/Chu-Crist/community-agent_Homework_3.git
cd community-agent_Homework_3
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install openai pandas networkx matplotlib python-dotenv
```

## 6. API Configuration

Create a `.env` file in the project root directory.

Add the following configuration:

```env
LLM_API_KEY=your_api_key_here
MODEL=glm-5.3
BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

Replace `your_api_key_here` with your own BigModel API key.

**Important:** Never upload your `.env` file or expose your API key on GitHub.

## 7. Running the Agent

Start the application using:

```bash
python main.py
```

The agent will display a welcome message and allow users to enter questions.

To terminate the application, type:

```text
exit
```

or:

```text
quit
```

## 8. Available Agent Tools

| Tool | Description |
|---|---|
| `load_data` | Loads sample posts about a selected topic. |
| `build_graph` | Builds a network graph from the loaded posts. |
| `detect_communities` | Identifies groups of connected users. |
| `summarize_community` | Summarizes the members and posts of a selected community. |
| `plot_network` | Generates and saves a network visualization. |

## 9. Agent Workflow

The agent follows this general workflow:

1. Receive a question from the user.
2. Send the question and available tool descriptions to the GLM model.
3. Allow the model to select the appropriate tool.
4. Execute the selected Python function.
5. Return the tool result to the model.
6. Continue tool execution when additional operations are required.
7. Generate a natural-language response for the user.

## 10. Current Limitations

- The current dataset is simulated and contains predefined sample posts.
- The application does not currently collect live posts from social-media platforms.
- Community detection currently uses connected components in the network graph.
- The analysis is limited to the information available in the loaded dataset.

## 11. Future Improvements

- Integrate real community data sources.
- Implement more advanced community detection algorithms.
- Improve sentiment and discussion analysis.
- Support larger datasets.
- Add interactive network visualizations.