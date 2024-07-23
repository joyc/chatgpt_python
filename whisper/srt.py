# API版本最好切换到whisper local版本节省成本
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI


client = OpenAI()

audio_file = open("sample.wav", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="srt"
)
print(transcription)
