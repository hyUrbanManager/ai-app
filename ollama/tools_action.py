from ollama import ChatResponse, chat

# llm = "llama3.2"
llm = 'qwq'


def air(value: int) -> int:
    print("空调调到 %d 度" % value)
    return 0


def fan(value: int) -> int:
    print("风扇调到 %d 档" % value)
    return 0


air_tool = {
    "type": "function",
    "function": {
        "name": "air",
        "description": "空调",
        "parameters": {
            "type": "object",
            "required": ["value"],
            "properties": {
                "value": {"type": "integer", "description": "温度"},
            },
        },
    },
}

fan_tool = {
    "type": "function",
    "function": {
        "name": "fan",
        "description": "风扇",
        "parameters": {
            "type": "object",
            "required": ["value"],
            "properties": {
                "value": {"type": "integer", "description": "档位"},
            },
        },
    },
}


messages = [{"role": "user", "content": "帮我把风扇调到5档，空调调到29度."}]

print("输入:", messages[0]["content"])

available_functions = {
    "air": air,
    "fan": fan,
}

response: ChatResponse = chat(llm, messages=messages, tools=[air_tool, fan_tool])

print("得到response: 对象", response)

f_name = ""

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
            messages.append(response.message)
            if (output == 0):
                msg = '调节成功'
            else:
                msg = '调节失败'
            messages.append({"role": "tool", "content": msg, "name": f_name})
        else:
            print("Function", tool.function.name, "not found")

# Only needed to chat with the modelusing the tool call results
if response.message.tool_calls:
    # # Add the function response to messages for the model to use
    # messages.append(response.message)
    # # 把参数给llm
    # messages.append({"role": "tool", "content": str(output), "name": f_name})

    # Get final response from model with function outputs
    final_response = chat(llm, messages=messages)
    print("Final response:", final_response.message.content)

else:
    print("No tool calls returned from model")
