from intent_tool import get_intent, use_tool, get_reply, get_creation
from tools import TOOL_MAP
import pyperclip


def handle_command(user_input):
    # user_input = input("You: ")
    intent = get_intent(user_input)

    if intent == "quit":
        return "Goodbye!"
    
    elif intent == "create":
        creation = get_creation(user_input)
        print(creation)
        pyperclip.copy(creation)
        return "Sir! I have created the content, you may now paste it."
    
    # elif intent == "task":
    #     tool_data = use_tool(user_input)
    #     for key, value in tool_data.items():
    #         fn = TOOL_MAP[key]
    #         res= fn(value)

    #     print(res)

    else:
        answer = get_reply(user_input)
        print("Jarvis:", answer)
        return answer

# if __name__ == "__main__":
#     main()
# user_input = input("You: ")
# handle_command("open youtube")
