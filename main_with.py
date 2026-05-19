import os
import openai
import pyaudio
import serial
import time
import vosk
from vosk import Model, KaldiRecognizer
import beepy
from rhvoice_wrapper import TTS
import subprocess
from googletrans import Translator
import wolframalpha


def listen():
    """Listen to microphone and return recognized Russian speech as text."""
    recognizer = KaldiRecognizer(model, 16000)
    cap = pyaudio.PyAudio()
    stream = cap.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )
    beepy.beep(sound="coin")
    stream.start_stream()
    try:
        while True:
            data = stream.read(4096)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()[14:-3]
                return result
    finally:
        stream.stop_stream()
        stream.close()
        cap.terminate()


def say(text, voice="anna"):
    """Synthesize text to speech and play it."""
    data = tts.get(text, voice=voice, format_='wav')
    subprocess.check_output(['aplay', '-q'], input=data)


def wolf():
    """Answer a math or factual question using Wolfram Alpha."""
    say('Задайте вопрос:')
    rec = listen()
    print(rec)
    query_en = translator.translate(rec, dest="en").text
    print(query_en)
    try:
        app_id = os.environ.get("WOLFRAM_API_KEY", "")
        client = wolframalpha.Client(app_id)
        res = client.query(query_en)
        answer = next(res.results).text
        print(answer)
        answer_ru = translator.translate(answer, dest="ru").text
        print(answer_ru)
        say("Ответ: " + answer_ru)
    except Exception as e:
        print(f"Wolfram error: {e}")
        say('Возникли трудности, попробуйте ещё раз')


def chat():
    """Open-ended GPT conversation in Russian."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        say("API ключ не найден")
        return
    prompt = listen()
    print(f"Prompt: {prompt}")
    say("Минутку, я думаю")
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = completion.choices[0].text.strip()
        print(f"GPT: {answer}")
        say(answer)
    except Exception as e:
        print(f"GPT error: {e}")
        say("Возникли трудности, попробуйте ещё раз")


# --- Initialization ---
model = Model(model_name="vosk-model-small-ru-0.22")
tts = TTS(threads=1)
translator = Translator()

WAKE_WORD = "привет"

# --- Main loop ---
print("SAYA (Russian mode) is running. Say 'Привет' to wake.")
while True:
    try:
        say('Привет! Меня зовут Сая. Чтобы продолжить работу, скажите привет!')
        heard = listen()
        if WAKE_WORD in heard:
            say('Чем могу быть полезна?')
            while True:
                query = listen()
                print(f"Query: {query}")
                if "задач" in query:
                    wolf()
                elif "вопрос" in query:
                    chat()
                elif "пока" in query:
                    say("До свидания!")
                    break
    except KeyboardInterrupt:
        print("Shutting down SAYA.")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue