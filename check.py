import os
import requests
import speech_recognition as sr
from gtts import gTTS
import pygame
from io import BytesIO
import threading

def text_to_speech(text):
    # Text-to-speech conversion
    tts = gTTS(text=text, lang='en', slow=False)
    audio_data = BytesIO() 
    tts.write_to_fp(audio_data)
    audio_data.seek(0)
    return audio_data

def play_audio(audio_data):
    # Initialize Pygame mixer
    pygame.mixer.init()
    # Load and play audio from the stream
    pygame.mixer.music.load(audio_data)
    pygame.mixer.music.play()
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue

# Text to be converted to speech
text_to_speak = '''The cost of living in the US for students can vary widely depending on the location and type of accommodation. Housing expenses, including rent and utilities, can range from $450 to $3,600 monthly, depending on whether the student opts for hostel, rental, homestay, or campus accommodation [doc5]. Other living expenses such as food, groceries,  and clothing can be approximately $1,200 per month [doc5]. Additionally, students should consider transport expenses, which can be around $80 for a monthly pass, and other miscellaneous expenses that can range from $100 to $300 monthly [doc5]. It's important to note that these are indicative figures and actual costs can vary.'''

# Convert text to speech
audio_data = text_to_speech(text_to_speak)

# Create threads for audio playback
print(audio_data)
audio_thread = threading.Thread(target=play_audio, args=(audio_data,))

# Start the thread for audio playback

audio_thread.start()

# Join the thread to wait for it to finish
audio_thread.join()
