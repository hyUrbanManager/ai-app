from ollama import ChatResponse, chat

llm = "llama3.2"
# llm = 'qwq'

def write_file(file_name:str, content: str, value: str) -> int:
    print("----- write_file函数。file_name: %s, content: %s" % (file_name, content))
    with open("../%s" % file_name, 'w') as f:
        f.write(content)
    return 0

file_tool = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "写入文件",
        "parameters": {
            "type": "object",
            "required": ["file_name", "content"],
            "properties": {
                "value": {"type": "file_name", "description": "文件名"},
                "value": {"type": "integer", "description": "文件内容"},
            },
        },
    },
}

messages = [{"role": "user", "content": "把文本内容：'class Person{}'，写入文件中。文件路径：data/Person.java"}]
print("输入:", messages[0]["content"])
available_functions = {
    "write_file": write_file,
}

response: ChatResponse = chat(llm, messages=messages, tools=[file_tool])
print("得到response: 对象", response)
f_name = ""

if response.message.tool_calls:
    # llama append
    # messages.append(response.message)

    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print("Calling function:", tool.function.name)
            print("Arguments:", tool.function.arguments)
            output = function_to_call(**tool.function.arguments)
            print("Function output:", output)
            f_name = tool.function.name
            if (output == 0):
                msg = '写入成功'
            else:
                msg = '写入失败'
            messages.append({"role": "tool", "content": msg, "name": f_name})
        else:
            print("Function", tool.function.name, "not found")

if response.message.tool_calls:
    print("再次问ai。messages", messages)
    final_response = chat(llm, messages=messages)
    print("Final response:", final_response)
else:
    print("No tool calls returned from model")
