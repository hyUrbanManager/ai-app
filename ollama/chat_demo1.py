from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='qwq', messages=[
  {
    'role': 'user',
    'content': '天空为什么是蓝色的？',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)