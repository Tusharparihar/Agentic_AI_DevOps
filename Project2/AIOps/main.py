import argparse
import sys
from agent import AIOpsAgent
from sop_generator import generate_sop

def main():
    print("====================================================")
    print("🚀 Welcome to AIOps Conversational CLI")
    print("Your AI-powered SRE for Docker Monitoring & Fixing")
    print("====================================================")
    print("\nYou can ask me things like:")
    print("- 'Scan my containers for any issues'")
    print("- 'Why is my database container crashing?'")
    print("- 'Check the health of all services'")
    print("- 'Generate an SOP for the last issue found'")
    print("\n(Type 'exit' or 'quit' to stop)\n")

    # Initialize the conversational agent
    aiops = AIOpsAgent()

    while True:
        try:
            user_input = input("AIOps > ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! Happy Ops! 👋")
                break

            # Check if the user wants to generate an SOP
            if "sop" in user_input.lower() or "generate a document" in user_input.lower():
                if aiops.last_analysis:
                    print("📝 Generating SOP document based on the last analysis...")
                    result = generate_sop(aiops.last_analysis)
                    print(f"✅ {result}")
                    # We still run the agent to give a conversational confirmation
                    response = aiops.run(user_input)
                    print(f"\n{response}")
                else:
                    print("\n⚠️ I haven't performed any analysis yet. Please ask me to 'scan' or 'check' your containers first!")

            else:
                # Standard conversational request
                response = aiops.run(user_input)
                print(f"\n{response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! Happy Ops! 👋")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
