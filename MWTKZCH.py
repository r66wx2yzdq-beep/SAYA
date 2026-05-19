import os
from googletrans import Translator
import pyaudio
import serial
import time
import wolframalpha
import wikipedia
import vosk
from vosk import Model, KaldiRecognizer
import beepy
from rhvoice_wrapper import TTS
import subprocess
import openai


def listen():
    """Listen to microphone and return recognized Kazakh speech as text."""
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


def say(text, voice="nazgul"):
    """Synthesize text to speech and play it."""
    data = tts.get(text, voice=voice, format_='wav')
    subprocess.check_output(['aplay', '-q'], input=data)


def wiki():
    say('Сұраңыз')
    rec = listen()
    print(rec)
    query = translator.translate(rec, src='kk', dest='ru').text
    try:
        text = wikipedia.summary(query, sentences=1)
        say(translator.translate(text, src='ru', dest='kk').text)
    except Exception as e:
        print(f"Wiki error: {e}")
        say("Кайталаңыз")


def sensor():
    """Read environmental sensor data from Arduino via serial and announce it."""
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        ser.reset_input_buffer()
        g = 0
        t = 0
        while True:
            line = ser.readline().decode('utf-8').rstrip()
            if "Heavy gases" in line:
                level = line[14:17]
                s1 = f"Коміркышқыл газынын индикаторы текше метрге {level} милиграмм"
                say(s1)
                if int(level) < 600:
                    say('Кауіпсіз денгей')
                else:
                    say('Кауіпті денгей')
                print(s1)
                g += 1
            if "Temp" in line:
                s2 = f"Температура {line[7:9]} градус"
                say(s2)
                print(s2)
                t += 1
            if t == 1 and g == 1:
                break
            time.sleep(1)
    except Exception as e:
        print(f"Sensor error: {e}")
        say("Қате болды")


def wolf():
    """Answer a math or factual question using Wolfram Alpha."""
    say('Сұраңыз')
    rec = listen()
    print(rec)
    que = translator.translate(rec, src='kk', dest='ru').text
    query_en = translator.translate(que, dest="en").text
    print(query_en)
    try:
        app_id = os.environ.get("WOLFRAM_API_KEY", "")
        client = wolframalpha.Client(app_id)
        res = client.query(query_en)
        answer = next(res.results).text
        answer_kk = translator.translate(answer, dest="kk").text
        print(answer_kk)
        say(answer_kk)
    except Exception as e:
        print(f"Wolfram error: {e}")
        say("Кайталаңыз")


def device_on():
    """Send ON command to Arduino Uno over Bluetooth."""
    try:
        ser = serial.Serial('/dev/rfcomm0', 9600)
        ser.write(b'1\n')
        ser.write(b'1\n')
        ser.close()
    except Exception as e:
        print(f"Bluetooth error: {e}")


def device_off():
    """Send OFF command to Arduino Uno over Bluetooth."""
    try:
        ser = serial.Serial('/dev/rfcomm0', 9600)
        ser.write(b'0\n')
        ser.write(b'0\n')
        ser.close()
    except Exception as e:
        print(f"Bluetooth error: {e}")


def word_tr():
    """Translate a spoken phrase into the user's chosen language."""
    say("Тілді таңдау")
    rec = listen()
    print(rec)
    if "орыс" in rec:
        tr_language = "ru"
    elif "ағыл" in rec:
        tr_language = "en"
    elif "қазақ" in rec:
        tr_language = "kk"
    else:
        say("Тілді танымадым")
        return
    say("Жаксы. Айтыныз")
    rec = listen()
    try:
        translated = translator.translate(rec, dest=tr_language).text
        say(translated)
    except Exception as e:
        print(f"Translation error: {e}")
        say("Кайталаңыз")


def chat():
    """Open-ended GPT conversation in Kazakh."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        say("API кілті табылмады")
        return
    rec = listen()
    prompt = translator.translate(rec, src='kk', dest='ru').text
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
        answer_kk = translator.translate(completion.choices[0].text, dest="kk").text
        say(answer_kk)
    except Exception as e:
        print(f"GPT error: {e}")
        say("Қате болды")


# --- Initialization ---
model = Model(model_name="vosk-model-small-kz-0.15")
wikipedia.set_lang("ru")
translator = Translator()
tts = TTS(threads=1)

WAKE_WORDS = ("сәлем", "салем")

# --- Main loop ---
print("SAYA is running. Say 'Сәлем' to wake.")
while True:
    try:
        say('Салем! Менің атым Сая. Жалғастыру үшін сәлем айтыныз')
        heard = listen()
        if any(w in heard for w in WAKE_WORDS):
            say('Немен көмектесе аламын?')
            while True:
                query = listen()
                print(f"Query: {query}")
                if "сұрақ" in query:
                    wiki()
                elif "есеп" in query:
                    wolf()
                elif "қос" in query:
                    device_on()
                elif "өшір" in query:
                    device_off()
                elif "сенсор" in query:
                    sensor()
                elif "аударма" in query:
                    word_tr()
                elif "көмек" in query or "комек" in query:
                    chat()
                elif "орыс" in query:
                    import main_with
                elif "сау" in query:
                    say("Сау болыңыз!")
                    break
    except KeyboardInterrupt:
        print("Shutting down SAYA.")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue
