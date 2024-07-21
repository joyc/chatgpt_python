import pandas as pd
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
from typing import List
from scipy import spatial


client = OpenAI(max_retries=3, api_key=os.environ.get("OPENAI_API_KEY"))
openai_model = os.environ.get("OPENAI_MODEL")
embedding_model = os.environ.get("EMBEDDING_MODEL")

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances


def create_context(question: str, df: pd.DataFrame, max_len=1800):
    """
    質問と学習データを比較して、コンテキストを作成する関数
    """
    # 質問をベクトル化
    question_embedding = client.embeddings.create(input=question, model=embedding_model).data[0].embedding
    # 質問と学習データと比較してコサイン類似度を計算し、「distances」という列に類似度を格納
    df['distances'] = distances_from_embeddings(
        question_embedding,df['embeddings'].apply(eval).apply(np.array).values, distance_metric='cosine')

    # コンテキストを格納するためのリスト
    returns = []
    # コンテキストの現在の長さ
    cur_len = 0

    # 学習データを類似度順にソートし、トークン数の上限までコンテキストに追加する
    for _, row in df.sort_values('distances', ascending=True).iterrows():
        # テキストの長さを現在の長さに加える
        cur_len += row['n_tokens'] + 4
        # テキストが長すぎる場合はループを終了
        if cur_len > max_len:
            break
        # コンテキストのリストにテキストを追加する
        returns.append(row["text"])
    # コンテキストを結合して返す
    return "\n\n###\n\n".join(returns)

def answer_question(question, conversation_history):
    """
    コンテキストに基づいて質問に答える関数
    """

    # 学習データを読み込む
    df = pd.read_csv('embeddings.csv', encoding="utf-8")

    context = create_context (question, df, max_len=200)
    # プロンプトを作成し、会話の履歴に追加
    prompt = f"あなたはとあるホテルのスタッフです。コンテキストに基づいて、お客様からの質問に丁寧に答えてください。コンテキストが質問に対して回答できない場合は「わかりません」と答えてください。\n\nコンテキスト: {context}\n\n---\n\n質問: {question}\n回答:"
    conversation_history.append({"role": "user", "content": prompt})

    try:
        # ChatGPTからの回答を生成
        response = client.chat.completions.create(
            model=openai_model,
            messages=conversation_history,
            # max_tokens=200,
            temperature=1,
            # top_p=1,
        )

        # ChatGPTからの回答を返す
        return response.choices[0].message.content.strip()
    except Exception as e:
        # エラーが発生した場合は空の文字列を返す
        print(e)
        return ""