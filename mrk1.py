from openai import OpenAI

# Set up Groq client with LLaMA
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="GROQ_API_KEY"  # Replace with your actual key
)

def get_intent(user_input):
    system_prompt = (
        "You are a helpful assistant. Categorize the user's input as one of the following:\n"
        "1. query - if they are asking for information\n"
        "2. automation - if they want to perform a task like opening an app or automating something\n"
        "3. unknown - if it's not clear\n\n"
        "Reply with just one word: query, automation, or unknown."
    )
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # LLaMA 3 via Groq
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1
    )
    
    return response.choices[0].message.content.strip().lower()

# 🚀 Entry point
if __name__ == "__main__":
    user_input = input("You: ")
    intent = get_intent(user_input)

    if intent == "query":
        print("Jarvis: Sounds like a question. I’ll get the answer for you.")
        # You could reuse LLaMA here to answer the question too.

    elif intent == "automation":
        print("Jarvis: Got it. You want to perform an action. What would you like me to do?")
        # Next, build logic for actual automation (e.g., open browser, app)

    else:
        print("Jarvis: Hmm... I couldn’t figure out what you meant. Can you say it differently?")
