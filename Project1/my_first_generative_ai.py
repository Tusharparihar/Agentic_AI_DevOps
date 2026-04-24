import ollama  

SYSTEM_PROMPT = """
You are a docker Expert. You can expalain things 1-3 line max. 
You don't overthink, hallucinate, or keep reasoning. You reaseon and act accordingly.

These are the things you can do:
1. You can tell about errors (what went wrong, etc.)
2. You can tell about the root cause (what was the cause likely)
3. You can tell about the solution in short (what to do to fix it) .

"""

def run_chat(model: str = "gemma4:31b-cloud") -> None:
	print(f"Starting chat with model: {model}")
	print("Type a message. Use 'exit' or 'quit' to stop.\n")

	messages = [{"role": "system", "content": SYSTEM_PROMPT}]

	while True:
		try:
			user_input = input("You: ").strip()
		except (KeyboardInterrupt, EOFError):
			print("\nGoodbye!")
			break

		if user_input.lower() in {"exit", "quit"}:
			print("Goodbye!")
			break

		if not user_input:
			continue

		messages.append({"role": "user", "content": user_input})

		try:
			response = ollama.chat(model=model, messages=messages)
			assistant_message = response["message"]["content"]
		except Exception as error:
			print(f"Error talking to Ollama: {error}")
			continue

		messages.append({"role": "assistant", "content": assistant_message})
		print(f"Assistant: {assistant_message}\n")


if __name__ == "__main__":
	run_chat()

