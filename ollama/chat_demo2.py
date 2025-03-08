from ollama import chat

stream = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "天空为什么是蓝色的？",
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)

