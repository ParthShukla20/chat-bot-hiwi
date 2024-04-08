import os
import requests
import speech_recognition as sr
from gtts import gTTS
from langchain.llms import OpenAI
import base64
from azure_api import azure_api
from ulca_config import ulca_config,ulca_compute
import pygame
from io import BytesIO
import re
import speech_recognition as sr
import keyboard


conversation = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information."
        },
        {
            "role": "user", 
            "content": "what is tcs"
        }
    ]
response,azure_openai_key,azure_openai_url,headers,body = azure_api(conversation)
config_url , ulca_header_config, ulca_body_config, source_lang,service_id,data= ulca_config()
text_to_speak=None
pygame.init()
while True:
    pygame.mixer.init()

    r = sr.Recognizer() 
    text = ""
    with sr.Microphone() as source:
        print("Speak:")
        
        r.energy_threshold = 1200
        r.adjust_for_ambient_noise(source,1.2)
        # try:
        audio = r.listen(source, timeout=10)
        with open("captured_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        with open('./captured_audio.wav', "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
        
       
        text_to_speak,new_convo,new_body = ulca_compute(encoded_audio,source_lang,service_id,data,conversation,azure_openai_url,headers,body)
        conversation= new_convo
        body = new_body
        text_to_speak = re.sub(r'\[doc(\d+)\]','\b\b',  text_to_speak)
        tts = gTTS(text=text_to_speak, lang=source_lang, slow=False)


        print(text_to_speak)

        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        

        
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()
        keyboard.on_press_key('q', lambda event: pygame.mixer.music.stop())
             

        while pygame.mixer.music.get_busy():
            continue
        
        # engine = pyttsx3.init() 
        # voices = engine.getProperty('voices')
        # engine.setProperty('voice', voices[1].id)
        # engine.setProperty('rate', 138)         
        # engine.say(text_to_speak)
        # engine.runAndWait() 
    

    
    
        # audio_file = "output.mp3"
        
        # # # Save the audio file
        # tts.save(audio_file)
        
        # # # Get the duration of the audio file
        # audio = MP3(audio_file)
        # duration_in_seconds = audio.info.length
        
        
        
        # os.system("start " + audio_file)
        # time.sleep(duration_in_seconds)
        
    
    # if text in text.lower() == "bye" or text in text.lower() == "thank you" :
    #     break

