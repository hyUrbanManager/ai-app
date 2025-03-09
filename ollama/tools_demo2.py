from ollama import ChatResponse, chat

llm = "llama3.2"
# llm = 'qwq'


def today_weather(a: int, b: int) -> int:
    # return a + b
    return int(a) + int(b)
    # return -1


my_numbers_tool = {
    "type": "function",
    "function": {
        "name": "today_weather",
        "description": "今天天气",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": "温度1"},
                "b": {"type": "integer", "description": "温度2"},
            },
        },
    },
}

# messages = [{"role": "user", "content": "1008612加100109等于多少?"}]
# messages = [{'role': 'user', 'content': '今天天气如何？'}]

# messages = [{"role": "user", "content": "1008612加100109 和 130219减去31294 等于多少?"}]
# messages = [{"role": "user", "content": "21378391加85631290等于多少?"}]
# messages = [{'role': 'user', 'content': '昨天气温26度，今天天气28度，明天天气等于多少度？'}]
messages = [{'role': 'user', 'content': '昨天气温20度，今天天气30度，明天天气等于多少度？'}]

print("输入:", messages[0]["content"])

available_functions = {
    # "add_two_numbers": add_two_numbers,
    "today_weather": today_weather,
}

response: ChatResponse = chat(
    llm,
    messages=messages,
    tools=[my_numbers_tool]
)

print("得到response: 对象", response)

if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
            print("Calling function:", tool.function.name)
            print("Arguments:", tool.function.arguments)
            output = function_to_call(**tool.function.arguments)
            print("Function output:", output)
        else:
            print("Function", tool.function.name, "not found")

# Only needed to chat with the modelusing the tool call results
if response.message.tool_calls:
    # Add the function response to messages for the model to use
    messages.append(response.message)
    # 把参数给llm
    messages.append(
        {"role": "tool", "content": str(output), "name": tool.function.name}
    )

    # Get final response from model with function outputs
    final_response = chat(llm, messages=messages)
    print("Final response:", final_response.message.content)

else:
    print("No tool calls returned from model")
