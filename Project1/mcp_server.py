from fastmcp import FastMCP
import subprocess

mcp = FastMCP("Docker MCP Server")

@mcp.tool
def show_running_containers():
    """ Tool1: Show running Docker containers """

    result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
    return result.stdout

@mcp.tool
def show_container_logs(container_name):
    """ Tool2: Show logs of a specific Docker container """
    
    result = subprocess.run(["docker", "logs", "--tail", "10", container_name], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    mcp.run()