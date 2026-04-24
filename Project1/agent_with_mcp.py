
import asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

SYSTEM_PROMPT = """
You are a docker Expert. You can expalain things 1-3 line max. 
You don't overthink, hallucinate, or keep reasoning. You reaseon and act accordingly.

These are the things you can do:
1. You can tell about errors (what went wrong, etc.)
2. You can tell about the root cause (what was the cause likely)
3. You can tell about the solution in short (what to do to fix it) .

"""

async def main():

    #this brings all the tools from mcp server.
    client = MultiServerMCPClient(
        {
            "docker-mcp": {
                "transport": "stdio",  # Local subprocess communication
                "command": "python",
                # Absolute path to your mcp_server.py file
                "args": ["mcp_server.py"],
            }
        }
    )

    tools = await client.get_tools()

    llm = ChatOllama(model="gemma4:31b-cloud", temperature=0.8, system=SYSTEM_PROMPT)   
    
    ##agent with mcp tools
    agent = create_agent(model=llm, tools=tools)

    messages = []

    while True:
        try:
            user_input = input("Enter your message (or 'exit' to quit):\n").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        response = await agent.ainvoke({"messages": messages})
        assistant_message = response["messages"][-1].content
        messages.append({"role": "assistant", "content": assistant_message})

        print(assistant_message)

if __name__ == "__main__":
    asyncio.run(main())    