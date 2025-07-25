from llm_handler import ask_sentinel

print("Connecting to your local AI assistant...")
print("-" * 30)

# A perfect prompt for a Friday evening in Chennai!
test_prompt = "Generate a cool, futuristic, one-line greeting for a user in Chennai who is starting a project on a Friday evening."

ai_response = ask_sentinel(test_prompt)

print(f"SENTINEL: {ai_response}")