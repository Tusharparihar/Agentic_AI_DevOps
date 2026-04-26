import subprocess
import json

def run_command(command):
    """Helper to run shell commands and return output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command {' '.join(command)}: {e.stderr}"

def get_running_containers():
    """Returns a list of ALL containers (running and exited) and their statuses."""
    output = run_command(["docker", "ps", "-a", "--format", "{{.ID}}|{{.Names}}|{{.Status}}"])
    containers = []
    for line in output.strip().split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) == 3:
                cid, name, status = parts
                containers.append({"id": cid, "name": name, "status": status})
    return containers

def get_container_stats(container_id):
    """Returns stats for a specific container to detect resource anomalies."""
    output = run_command(["docker", "stats", "--no-stream", "--format", "json", container_id])
    try:
        return json.loads(output)
    except:
        return output

def get_container_health(container_id):
    """Checks the health status of a container."""
    output = run_command(["docker", "inspect", "--format", "{{.State.Health.Status}}", container_id])
    return output.strip()

def get_error_logs(container_id):
    """Fetches logs and filters for errors."""
    output = run_command(["docker", "logs", "--tail", "50", container_id])
    errors = [line for line in output.split('\n') if any(keyword in line.lower() for keyword in ["error", "exception", "failed", "critical"])]
    return "\n".join(errors) if errors else "No obvious errors found in recent logs."

if __name__ == "__main__":
    # Quick test
    containers = get_running_containers()
    print(f"Containers: {containers}")
    if containers:
        cid = containers[0]['id']
        print(f"Health: {get_container_health(cid)}")
        print(f"Errors: {get_error_logs(cid)}")
