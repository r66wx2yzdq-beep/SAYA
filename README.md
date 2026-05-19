# SAYA — Intelligent Voice Assistant System

An AI-powered voice assistant built on Raspberry Pi and Arduino, featuring real-time speech recognition and synthesis in **Kazakh and Russian**, IoT sensor integration, and GPT-based conversational dialogue.

Originally developed as a research project at Nazarbayev Intellectual School of Physics and Mathematics (Kostanay, Kazakhstan). The system was awarded **Silver Medal at Infomatrix Asia International Project Competition**.

> **Note:** This repository was previously hosted under the name EWA — an earlier working title for the same project.

---

## What it does

SAYA is a fully offline-capable multimodal voice assistant that:

- Understands and responds in **Kazakh** and **Russian** via natural speech
- Reads real-time environmental data from IoT sensors (CO₂, temperature, humidity, gas)
- Solves mathematical problems via Wolfram Alpha
- Answers factual questions via Wikipedia
- Holds open-ended conversations via GPT (OpenAI)
- Controls external devices remotely over Bluetooth (Arduino Uno)
- Translates between Kazakh, Russian, and English on voice command
- Designed with **accessibility in mind** — built for visually impaired users

---

## Architecture

```
[Microphone] → [Vosk STT] → [Keyword Router] → [Module]
                                                    ├── Wikipedia
                                                    ├── Wolfram Alpha
                                                    ├── GPT Dialogue
                                                    ├── Sensor Readout
                                                    ├── Bluetooth Control
                                                    └── Translation

[Module Output] → [RHVoice TTS] → [Speaker]

[Arduino Nano] → sensors (CO₂, temp, humidity, gas, alcohol, hydrogen)
[Arduino Uno]  → Bluetooth relay for remote device control
[Raspberry Pi] → main processing unit running Python
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Speech Recognition | [Vosk](https://alphacephei.com/vosk/) + `vosk-model-small-kz-0.15` / `vosk-model-small-ru-0.22` |
| Speech Synthesis | [RHVoice](https://github.com/RHVoice/RHVoice) (Kazakh voices: talgat, nazgul / Russian: anna, elena) |
| Dialogue | OpenAI GPT (`text-davinci-003`) |
| Math & Search | Wolfram Alpha API |
| Knowledge | Wikipedia API |
| Translation | Google Translate (`googletrans`) |
| IoT Hardware | Arduino Nano + Uno, sensors: DHT11, MQ-2, MQ-3, MQ-8, BMP180 |
| Connectivity | Bluetooth (HC-05 module), Serial (USB) |
| Platform | Raspberry Pi (Debian), Python 3 |

---

## Files

| File | Description |
|---|---|
| `MWTKZCH.py` | Main Kazakh-language assistant — full pipeline with sensor readout, Wikipedia, Wolfram, GPT, Bluetooth control |
| `main_with.py` | Russian-language mode — voice-activated GPT dialogue and Wolfram queries |

---

## Hardware Setup

- **Raspberry Pi** — central processing unit
- **Arduino Nano** — reads from environmental sensors (CO₂, temperature, humidity, gas, alcohol vapor, hydrogen)
- **Arduino Uno** — receives Bluetooth commands to control external devices
- **Bluetooth module (HC-05)** — wireless communication between devices
- **Microphone + Speaker** — audio I/O via USB audio adapter

Sensor thresholds monitored:

| Sensor | Safe Range | Critical |
|---|---|---|
| CO₂ | 400–1000 ppm | > 1000 ppm |
| Temperature | 20–25 °C | Outside range |
| Humidity | 40–60% | Outside range |
| Methane | < 1861 ppb | > 1.95 ppm |

---

## Installation

Full setup instructions (Debian-based, tested on Raspberry Pi):

```bash
# 1. System dependencies
sudo apt update && sudo apt upgrade
sudo apt install python3-pip git
sudo apt install python3-pyaudio
sudo apt install gcc pkg-config scons
sudo apt install libpulse-dev pulseaudio
sudo apt install lame opus-tools flac
sudo apt install libasound2-dev

# 2. Python libraries
pip install pkgconfig==1.5.5
pip install SCons==4.4.0
pip3 install vosk
pip3 install openai
pip3 install beepy simpleaudio
pip3 install rhvoice-wrapper
pip3 install wolframalpha wikipedia pyaudio
pip3 install googletrans==4.0.0rc1

# 3. RHVoice (Kazakh + Russian TTS) — build from source
git clone --recursive https://github.com/RHVoice/RHVoice.git
cd RHVoice
scons spd_module_dir=/usr/lib/speech-dispatcher
sudo scons install
sudo ldconfig
```

A pre-configured Debian VM image with all dependencies installed is available on request.

---

## Usage

**Kazakh mode:**
```bash
python3 MWTKZCH.py
```
Say *"Сәлем"* to wake the assistant. Then:
- *"сұрақ"* — Wikipedia search
- *"есеп"* — math problem (Wolfram Alpha)
- *"сенсор"* — read environmental sensors
- *"аударма"* — translate a phrase
- *"көмек"* — open GPT conversation
- *"қос / өшір"* — turn device on/off via Bluetooth
- *"сау"* — exit

**Russian mode:**
```bash
python3 main_with.py
```
Say *"Привет"* to wake. Then: *"задача"* for Wolfram, *"вопрос"* for GPT chat.

---

## Copyright

This software is officially registered with the **Republic of Kazakhstan State Register of Rights to Objects Protected by Copyright**.

> **Certificate No. 39591** — dated October 12, 2023
> *"Virtual avatar with voice assistant function for recognition and synthesis of natural speech in the Kazakh language"*
> Issued by the National Institute of Intellectual Property of the Republic of Kazakhstan.

---

## Research Background

This project was developed as an academic research paper titled:

> *"Integration of Virtual Voice Assistant with Speech Recognition and Synthesis in Kazakh into the Intelligent Information Management System SAYA on Raspberry Pi and Arduino Platform with Biometric Authentication"*

The work addresses the gap in domestic Kazakh-language AI tooling and was designed to support accessibility for visually impaired users. It was presented at the Infomatrix Asia International Project Competition (Silver Medal).

---

## Authors

- **Dilnaz Bektenbergenova** — Lead Developer
- **Yeldana Batrkhanova** — Co-Developer
- Scientific supervisor: A.I. Shertser, Computer Science teacher, NIS PhMD Kostanay

Nazarbayev Intellectual School of Physics and Mathematics, Kostanay, Kazakhstan — 2023
