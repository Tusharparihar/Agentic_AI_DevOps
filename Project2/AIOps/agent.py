import os
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from monitor import get_running_containers, get_container_health, get_error_logs, get_container_stats

# Attempting a more robust import for AgentExecutor
try:
    from langchain.agents import AgentExecutor, create_tool_calling_agent
except ImportError:
    try:
        from langchain_community.agents import AgentExecutor, create_tool_calling_agent
    except ImportError:
        AgentExecutor = None
        create_tool_calling_agent = None

# System prompt for AIOps Agent
SYSTEM_PROMPT = """You are an AIOps Expert. Your goal is to monitor Docker containers, detect anomalies, and provide actionable insights.

Workflow:
1. Identify running/exited containers.
2. Check health and logs for anomalies (errors, crashes, resource spikes).
3. If an anomaly is found:
   - Analyze the logs and stats to determine the Root Cause.
   - Propose a technical solution to fix the issue.
   - Provide a clear, step-by-step guide to resolve it.

Be conversational, technical, and accurate. Avoid hallucinations. Use a helpful and professional tone.
"""

@tool
def list_containers_tool():
    """Get a list of all Docker containers (including exited ones) with their IDs, names, and statuses."""
    return get_running_containers()

@tool
def check_container_health_tool(container_id: str):
    """Check the health status of a specific Docker container by ID."""
    return get_container_health(container_id)

@tool
def fetch_container_errors_tool(container_id: str):
    """Fetch the most recent error logs for a specific Docker container by ID."""
    return get_error_logs(container_id)

@tool
def get_resource_stats_tool(container_id: str):
    """Get CPU and Memory usage stats for a specific Docker container by ID."""
    return get_container_stats(container_id)

tools = [list_containers_tool, check_container_health_tool, fetch_container_errors_tool, get_resource_stats_tool]
model = ChatOllama(model="gemma4:31b-cloud", temperature=0.8)

class AIOpsAgent:
    def __init__(self):
        self.history = []
        self.last_analysis = ""

        # Setup Agent Executor if available
        self.executor = None
        if AgentExecutor is not None:
            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            try:
                agent = create_tool_calling_agent(model, tools, prompt)
                self.executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
            except Exception as e:
                print(f"Error initializing agent executor: {e}")

    def run(self, user_input):
        # Store user input in history
        self.history.append(HumanMessage(content=user_input))

        if self.executor:
            try:
                result = self.executor.invoke({
                    "input": user_input,
                    "chat_history": self.history
                })
                response_text = result["output"]
            except Exception as e:
                response_text = f"I encountered an error using my tools: {e}. I'll try a direct analysis."
                response_text += "\n" + self._manual_analysis(user_input)
        else:
            response_text = self._manual_analysis(user_input)

        # Update state and history
        self.history.append(AIMessage(content=response_text))

        # Store the latest analysis if it contains "Analysis" or "Root Cause" for SOP generation
        if "Analysis" in response_text or "Root Cause" in response_text:
            self.last_analysis = response_text

        return response_text

    def _manual_analysis(self, user_input):
        """Fallback logic when agent executor is unavailable."""
        containers = get_running_containers()
        report = f"Current Containers: {containers}\n"
        for c in containers:
            cid = c.get('id', '')
            report += f"\n--- {c.get('name')} ({cid}) ---\nHealth: {get_container_health(cid)}\nLogs: {get_error_logs(cid)}\n"

        final_prompt = f"{SYSTEM_PROMPT}\n\nUser Request: {user_input}\n\nSystem Data:\n{report}\n\nProvide a detailed analysis."
        response = model.invoke(final_prompt)
        return response.content

if __name__ == "__main__":
    agent = AIOpsAgent()
    while True:
        user_input = input("AIOps > ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print(agent.run(user_input))
