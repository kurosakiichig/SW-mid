# client.py (DeepSeek版)
import os
import requests
import json

DEEPSEEK_API_KEY = "sk-b44c2b6a72684c718c0851bbf6dbf146"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_status",
            "description": "查询机器库存",
            "parameters": {
                "type": "object",
                "properties": {
                    "machine_id": {"type": "string"},
                    "item_name": {"type": "string"}
                },
                "required": ["machine_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_win",
            "description": "记录娃娃中奖",
            "parameters": {
                "type": "object",
                "properties": {
                    "machine_id": {"type": "string"},
                    "item_name": {"type": "string"}
                },
                "required": ["machine_id", "item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ranking",
            "description": "获取热门娃娃排行",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

def call_api(func_name, args):
    url_map = {
        "check_status": "http://localhost:5000/status",
        "record_win": "http://localhost:5000/win",
        "get_ranking": "http://localhost:5000/ranking"
    }
    if func_name == "check_status":
        return requests.get(url_map[func_name], params=args).json()
    else:
        return requests.post(url_map[func_name], json=args).json()

def chat(prompt):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # DeepSeek提供的聊天模型名
        "messages": [{"role": "user", "content": prompt}],
        "tools": tools,
        "tool_choice": "auto"
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    data = response.json()

    message = data['choices'][0]['message']

    if 'tool_calls' in message:
        tool_call = message['tool_calls'][0]
        fname = tool_call['function']['name']
        fargs = json.loads(tool_call['function']['arguments'])

        result = call_api(fname, fargs)

        # 把调用结果继续交给DeepSeek
        second_payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "tool_calls": [tool_call]},
                {"role": "tool", "tool_call_id": tool_call['id'], "content": json.dumps(result)}
            ]
        }
        second_response = requests.post(DEEPSEEK_API_URL, headers=headers, json=second_payload)
        second_data = second_response.json()
        return second_data['choices'][0]['message']['content']
    else:
        return message['content']

if __name__ == "__main__":
    while True:
        user_input = input("你: ")
        if user_input.lower() in ("exit", "quit"):
            break
        print("ChatGPT:", chat(user_input))
