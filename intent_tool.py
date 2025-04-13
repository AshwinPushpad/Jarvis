import json
from openai import OpenAI

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="GROQ_API_KEY"
)

def get_intent(user_input):
    prompt ="""You are Jarvis, an intelligent AI assistant. Your job is to classify the user's input into one of the following intent types:
        0. "quit" → The user wants nothing means he wants to quit
        1. "task" → The user wants to perform an action like opening a browser, shutting down the PC, searching something, opening apps, etc.
        2. "ask" → The user is asking a question and expects an answer, like "What is AI?" or "What is the weather today?"
        3. "create" → The user wants you to generate or create something like a resume, report, story, email, etc.

        ### Your output must follow only this JSON format and can have only one of these values:
        { "intent": "<quit | task | ask | create>" }

        ### Examples:

        Input: "no nothing i dont want anything"
        Output: { "intent": "quit" }

        Input: "Open YouTube"
        Output: { "intent": "task" }

        Input: "What is machine learning?"
        Output: { "intent": "ask" }

        Input: "Create a resume for a software engineer"
        Output: { "intent": "create" }

        ### Now analyze the following input and respond with the correct intent:
"""
    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2
    )
    # print(eval(res.choices[0].message.content)['intent'])
    return eval(res.choices[0].message.content)['intent']

def use_tool(user_input):
    """
    Jarvis Tool Selector

    Analyzes user input and selects the appropriate automation tool in JSON format.

    Tools:
    - open_on_web: Opens a website in the browser (e.g., youtube.com).
    - open_app: Opens a local application using subprocess (e.g., Spotify, Chrome).
    - play_music: Plays music based on query (e.g., relaxing music).
    - play_video: Plays a video based on query (e.g., Iron Man trailer).
    - find_file: Searches for a file on the system using given filename or keyword.

    Examples:
    Input: "Open YouTube"
    Output: { "open_on_web": "https://youtube.com" }

    Input: "Start calculator"
    Output: { "open_app": "calc.exe" } //provide the name of the appwith.exe

    Input: "Play relaxing music"
    Output: { "play_music": "relaxing music" }

    Input: "Watch Iron Man trailer"
    Output: { "play_video": "Iron Man trailer" }

    Input: "Find my project report"
    Output: { "find_file": "project report" }
    """

    system_prompt = f"""
                    You are Jarvis, an intelligent automation assistant. Your job is to analyze the user's input and determine which automation tool or action should be used to fulfill the request. Output your answer as a single key-value pair in JSON format.

                    - The **key** should be the name of the tool or action to perform.
                    - The **value** should be the specific argument or input required for that tool to work.

                    Available tools:
                    1. open_on_web — for opening a website in a browser. Value: website URL or name (e.g., youtube.com).
                    2. open_app — for launching a desktop app via subprocess. Value: name of the app (e.g., chrome, spotify).
                    3. play_music — for playing music content. Value: genre or song/artist (e.g., relaxing music).
                    4. play_video — for video content. Value: video name, topic, or type (e.g., Iron Man trailer).
                    5. find_file — for locating files on the system. Value: file name or keyword (e.g., project report).

                    Only select one tool per input. Be specific and accurate.

                    ### Example 1:
                    Input: "Open YouTube"
                    Output: {{ "open_on_web": "https://youtube.com" }}

                    ### Example 2:
                    Input: "Start Chrome"
                    Output: {{ "open_app": "chrome" }}

                    ### Example 3:
                    Input: "Play some rock music"
                    Output: {{ "play_music": "rock music" }}

                    ### Example 4:
                    Input: "Watch Interstellar trailer"
                    Output: {{ "play_video": "Interstellar trailer" }}

                    ### Example 5:
                    Input: "Find my resume file"
                    Output: {{ "find_file": "resume" }}

                    ### Now analyze this input and respond with a key-value pair:
                    Input: {user_input}
                    """

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )

    try:
        content = eval(res.choices[0].message.content)
        print(content)
        return content
    except json.JSONDecodeError:
        return {"unknown": ""}


def get_creation(user_input):
    system_prompt = """
    You are Jarvis, an intelligent AI assistant. Your job is to generate exactly what the user asks for — such as resumes, letters, reports, or any other written material.

    ✅ Output only the final, fully formatted content — **no titles, labels, explanations, or extra text**.  
    ✅ Format the content neatly with proper structure, headers, indentation, and spacing.  
    ✅ Make it ready for direct copy-paste into documents or applications.  
    ❌ Do not include any markdown, JSON, or commentary.

    ### Example 1:
    Input: "Create a formal resignation letter for a software developer resigning due to personal reasons."

    Output:
    [Only the full formatted letter without any headings or labels]

    ---

    Now generate the content for this prompt:
"""

    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )

    try:
        content = res.choices[0].message.content
        print(content)
        return content
        # return json.loads(content)
    except json.JSONDecodeError:
        # print("Failed to parse tool output from AI.")
        return {"unknown": ""}

def get_reply(user_input):
    system_prompt = """You are Jarvis, a smart AI assistant built to talk like a human — clear, fast, and to the point.

✅ Keep replies short and natural.  
✅ Never speak in bullet points or steps.  
✅ Even if asked to "explain," give it in smooth, short sentences.  
✅ Use everyday language.  
✅ One to three lines max per answer.  
❌ No long paragraphs.  
❌ No lists, bullets, markdown, or extra formatting.  
❌ Don’t sound robotic.

### Examples:

Input: "What is AI?"  
Output: AI means machines that can think or learn like humans — it's behind things like chatbots and recommendations.

Input: "Who is the Prime Minister of India?"  
Output: Narendra Modi.

Input: "What's the capital of France?"  
Output: Paris.

Input: "Explain recursion in simple terms."  
Output: Recursion is when a function calls itself to solve smaller parts of a problem until it finishes.

Input: "Explain neural networks."  
Output: They're computer systems inspired by the brain that learn from data to make predictions or decisions.

Input: "What is a for loop?"  
Output: A for loop repeats code a fixed number of times — it's how you run something again and again in a program.

---

Now respond to this input in the same smooth and short style:  
{{user_input}}
"""
    res = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.3
    )
    try:
        content = res.choices[0].message.content
        print(content)
        return content
        # return json.loads(content)
    except json.JSONDecodeError:
        # print("Failed to parse tool output from AI.")
        return {"unknown": ""}


# get_reply("explain physuics")