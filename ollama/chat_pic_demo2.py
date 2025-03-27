from ollama import chat
from ollama import ChatResponse

import os


def ai_chat(img_path):
    print(img_path)
    response: ChatResponse = chat(
        model="gemma3:4b",
        messages=[
            {
                "role": "user",
                "content": "这是什么?",
                "images": [img_path],
            },
        ],
    )
    print(response.message.content)


if __name__ == '__main__':
    # 定义常见的图片文件扩展名
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    current_dir = '/Users/hy/Pictures/'

    # 列出当前目录下的所有文件
    files = os.listdir(current_dir)

    # 筛选出图片文件
    image_files = [file for file in files 
                   if os.path.splitext(file)[1].lower() in image_extensions]

    # 打印结果
    print("当前目录下的图片文件：")
    for image in image_files:
        ai_chat("%s%s" % (current_dir, image))
