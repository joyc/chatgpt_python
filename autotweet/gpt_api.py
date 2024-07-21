from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# ChatGPTにリクエストを送信する関数を定義
def make_tweet():
    # chatgptに対する命令文を設定
    requests = "私はweb3業界solidity開発関係のブロックチェーン企業に勤める入社一年目の新入社員です。\n\n"\
               "日々ブロックチェーン関連知識を勉強しています。私に代わってTwitterに投稿するツイートを140文字以内で作成してください。\n\n"\
               "ブロックチェーン技術やスマートコントラクト開発Tipsに関する豆知識紹介"\
               "に関わるコンテンツを投稿してください。"
               # "作成内容は2023年以降出て来た人気な面白いDappsに関する知識紹介"\
               # "- 2024年7月現在暗号資産市場トレンドのまとめ文 \n\n"\
               # "- 面白いDappsの紹介"

    #例文として与える投稿文を設定
    # tweet1 = "例文1:仕事でsolidityを使うことになりそうだから、現在勉強中！プログラミングとか難しくてよく分からないよ...\n\n"
    # tweet2 = "例文2:最近ChatGPTについていろいろ調べてるんだけど、あれってなんでも質問に答えてくれてすごいよね！とりあえずsolidityを使って"\
    #          "簡単な自動売買ボートを書いてみるつもり。上手くできるかな？\n\n"
    # tweet3 = "例文3:最近はPythonを使って機械学習の勉強をしているんだけど、機械学習の勉強は難しいなぁ...\n\n"

    content = requests # + tweet1 + tweet2
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content},
        ],
        max_tokens=140,
        # n=1,
        temperature=0.6,
        top_p=1,
        # frequency_penalty=0.0,
        # presence_penalty=0.6,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(make_tweet())
