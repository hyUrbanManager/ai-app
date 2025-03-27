from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(
    model="gemma3:4b",
    messages=[
        {
            "role": "user",
            "content": "这是什么？",
            "images": ["/Users/hy/Movies/demo.mp4"],
        },
    ],
)

print(response)

# or access fields directly from the response object
print(response.message.content)
