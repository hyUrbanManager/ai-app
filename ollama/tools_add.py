from ollama import ChatResponse, chat

llm = "llama3.2"
# llm = 'qwq'


def add(a: int, b: int) -> int:
    return int(a) + int(b)


my_numbers_tool = {
    "type": "function",
    "function": {
        "name": "add",
        "description": "",
        "parameters": {
            "type": "object",
            "required": ["a", "b"],
            "properties": {
                "a": {"type": "integer", "description": ""},
                "b": {"type": "integer", "description": ""},
            },
        },
    },
}

# messages = [{"role": "user", "content": "1008612加100109等于多少?"}]
messages = [{"role": "user", "content": "12345 + 56789 + 97641等于多少?"}]

print("输入:", messages[0]["content"])

available_functions = {
    "add": add,
}

response: ChatResponse = chat(
    llm,
    messages=messages,
    tools=[my_numbers_tool]
)

print("得到response: 对象", response)

f_name = ''

if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
        # Ensure the function is available, and then call it
        if function_to_call := available_functions.get(tool.function.name):
            print("Calling function:", tool.function.name)
            print("Arguments:", tool.function.arguments)
            output = function_to_call(**tool.function.arguments)
            print("Function output:", output)
            f_name = tool.function.name
        else:
            print("Function", tool.function.name, "not found")

# Only needed to chat with the modelusing the tool call results
if response.message.tool_calls:
    # Add the function response to messages for the model to use
    messages.append(response.message)
    # 把参数给llm
    messages.append(
        {"role": "tool", "content": str(output), "name": f_name}
    )

    # Get final response from model with function outputs
    final_response = chat(llm, messages=messages)
    print("Final response:", final_response.message.content)

else:
    print("No tool calls returned from model")
