
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
import subprocess

SYSTEM_PROMPT = """
You are a docker Expert. You can expalain things 1-3 line max. 
You don't overthink, hallucinate, or keep reasoning. You reaseon and act accordingly.

These are the things you can do:
1. You can tell about errors (what went wrong, etc.)
2. You can tell about the root cause (what was the cause likely)
3. You can tell about the solution in short (what to do to fix it) .

"""

@tool
def show_running_containers():
    """ Tool1: Show running Docker containers """

    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout

@tool
def show_container_logs(container_name):
    """ Tool2: Show logs of a specific Docker container """
    
    result = subprocess.run(["docker", "logs", "--tail", "10", container_name], capture_output=True, text=True)
    return result.stdout

model = ChatOllama(model="gemma4:31b-cloud", temperature=0.8, system=SYSTEM_PROMPT)
tools = [show_running_containers, show_container_logs]

agent = create_agent(model=model, tools=tools)

while True:
    user_input = input("Enter your message:\n ")
    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye!")
        break
    response = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

    print(response["messages"][-1].content)