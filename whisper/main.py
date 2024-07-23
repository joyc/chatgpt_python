import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI


client = OpenAI()
openai_model = os.environ.get("OPENAI_MODEL")
whisper_model = os.environ.get("WHISPER_MODEL")
file = open("sample.wav", "rb")

transcription = client.audio.transcriptions.create(
    model=whisper_model,
    file=file
)

# print(transcription.text)
# chatgptで要約する
summary = client.chat.completions.create(
    model=openai_model,
    messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        {"role": "system", "content": f"以下の文章を3行の箇条書きで要約してください:\n{transcription.text}"}
    ],
    temperature=0.7,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
)
print(summary.choices[0].message.content)