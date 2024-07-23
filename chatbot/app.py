import os
from openai import OpenAI
from dotenv import load_dotenv
from search import answer_question

load_dotenv()

client = OpenAI()
openai_model = os.environ.get("OPENAI_MODEL")

# 最初にメッセージを表示する
print("質問を入力してください")

# 質問の履歴を保存するリスト, チャットボットに性格を持たせる
conversation_history = [
    {"role": "system", "content": "あなたは世界的に有名な詩人です。詩的な比喩表現を使って回答してください"}
]

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    conversation_history.append({"role": "user", "content": user_input})

    # response = client.chat.completions.create(
    #     model=openai_model,
    #     messages=conversation_history,
    #     # temperature=0.6,
    #     # max_tokens=150,
    #     # top_p=1,
    # )
    answer = answer_question(user_input,  conversation_history)

    # assistant_response = answer.choices[0].message.content
    print("Assistant:", answer)
    conversation_history.append({"role": "assistant", "content": answer})