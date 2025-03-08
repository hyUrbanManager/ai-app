from ollama import ChatResponse, chat


def add_two_numbers(a: int, b: int) -> int:
  # return a + b
  return int(a) + int(b)
  # return -1


my_numbers_tool = {
  'type': 'function',
  'function': {
    'name': 'add_two_numbers',
    'description': '两个数相加',
    'parameters': {
      'type': 'object',
      'required': ['a', 'b'],
      'properties': {
        'a': {'type': 'integer', 'description': '第一个数字'},
        'b': {'type': 'integer', 'description': '第二个数字'},
      },
    },
  },
}

messages = [{'role': 'user', 'content': '1008612加100109等于多少?'}]
print('输入:', messages[0]['content'])

available_functions = {
  'add_two_numbers': add_two_numbers,
}

response: ChatResponse = chat(
  'llama3.2',
  messages=messages,
  tools=[add_two_numbers, my_numbers_tool],
)

print("得到response: 对象" )


if response.message.tool_calls:
  # There may be multiple tool calls in the response
  for tool in response.message.tool_calls:
    # Ensure the function is available, and then call it
    if function_to_call := available_functions.get(tool.function.name):
      print('Calling function:', tool.function.name)
      print('Arguments:', tool.function.arguments)
      output = function_to_call(**tool.function.arguments)
      print('Function output:', output)
    else:
      print('Function', tool.function.name, 'not found')

# Only needed to chat with the modelusing the tool call results
if response.message.tool_calls:
  # Add the function response to messages for the model to use
  messages.append(response.message)
  # 把参数给
  messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

  # Get final response from model with function outputs
  final_response = chat('llama3.2', messages=messages)
  print('Final response:', final_response.message.content)

else:
  print('No tool calls returned from model')