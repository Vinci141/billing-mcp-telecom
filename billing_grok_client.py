from groq import Groq
import requests
import json
import os
api_key = os.getenv("GROQ_API_KEY")


client = Groq(api_key="<GROQ_API_KEY>")
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_bills",
            "description": "Call this to list all bills details "
        }
    },
    
    {
        "type": "function",
        "function": {
            "name": "get_overdue",
            "description": "Call this to get overdue details"   # you write this one!
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_revenue",
            "description": "Call this to get revenue details"   # you write this one!
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_revenue_per_user",
            "description": "Call this to get revenue per user details"   # you write this one!
        }
    }
]


user_question = input("Ask something about billing operations: ")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": user_question}
    ],
    tools=tools,
)

tool_call = response.choices[0].message.tool_calls[0]
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)

def handle_tool_call(tool_name, tool_args):
    if tool_name == "get_bills":
        result = requests.get("http://localhost:8000/bills")
        return result.json()
    
    elif tool_name == "get_overdue":
        result = requests.get(f"http://localhost:8000/overdue")
        return result.json()
    
    elif tool_name == "get_revenue":
        result = requests.get("http://localhost:8000/revenue")
        return result.json()
    
    elif tool_name == "get_revenue_per_user":
        result = requests.get("http://localhost:8000/revenue-per-user")
        return result.json()


messages=[
    {"role": "user", "content": user_question}  # ← now dynamic!
]

tool_result = handle_tool_call(tool_name, tool_args)
print('Tool Result:',tool_result)

final_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": user_question},
        {"role": "assistant", "tool_calls": [tool_call]},
        {"role": "tool", "tool_call_id": tool_call.id, "content": str(tool_result)}
    ],
    tools=tools,
)

print('Final:',final_response.choices[0].message.content)
print("Finish reason:", final_response.choices[0].finish_reason)
print("Full message:", final_response.choices[0].message)
