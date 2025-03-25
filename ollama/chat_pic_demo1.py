from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "user",
            "content": "这是什么主板？有几个内存插槽？",
            "images": ["/Users/hy/Pictures/A520M-A.png"],
        },
    ],
)

print(response)

# or access fields directly from the response object
# print(response.message.content)
