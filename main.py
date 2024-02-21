# import os
# from constant import openai_key
from langchain.llms import OpenAI
# import streamlit as st
# import speech_recognition as sr
# from gtts import gTTS

# openai_key = 'f3b28a10a6d941bf94d1667cffc2e408'
# os.environ["OPENAI_API_KEY"]=openai_key

# # # streamlit framework

# # st.title('Celebrity Search Results')
# # input_text=st.text_input("Search the topic u want")

# llm = OpenAI(temperature=0.8)

# # if input_text:
# #     st.write(llm(input_text))

# r = sr.Recognizer()
# text = ""
# with sr.Microphone() as source:
#     print("Speak:")
#     r.energy_threshold =1000
#     r.adjust_for_ambient_noise(source,1.2)
#     try:
#         audio = r.listen(source, timeout=10)  # Adjust the timeout as needed
#         text = r.recognize_google(audio)
#         print("You said: {}".format(text))
#     except sr.UnknownValueError:
#         print("Could not understand audio")
#     except sr.RequestError as e:
#         print("Error with the API request; {0}".format(e))
#     except Exception as e:
#         print("An unexpected error occurred: {0}".format(e))

# # text_to_speak = "आप कैसे हो "
# input_text = text
# text_to_speak = text

# if input_text:
#     text_to_speak = llm(input_text)

# language = 'hi'

# tts = gTTS(text=text_to_speak, lang=language, slow=False)


# audio_file = "output.mp3"

# # Save the audio file
# tts.save(audio_file)

# # Play the audio file (optional)
# os.system("start " + audio_file)


import os
from mutagen.mp3 import MP3
import requests
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from langchain.llms import OpenAI
import time
# from transformers import MBartForConditionalGeneration, MBartTokenizer


azure_openai_key = 'f3b28a10a6d941bf94d1667cffc2e408'

os.environ["OPENAI_API_KEY"] = azure_openai_key
endpoint = 'https://hiwimobileapp-createopenai.openai.azure.com'  # Replace with your actual Azure OpenAI endpoint

headers = {
    # 'Authorization': 'Bearer ' + azure_openai_key,
    'Content-Type': 'application/json',
    'api-key'  : azure_openai_key
 
}
conversation = [
    {"role": "system", "content": "You are an AI assistant that helps people find information."},
    {"role": "user", "content": "Tell me a joke."}
]
body = {
    "messages": conversation,
    "temperature": 0.7,
    "top_p": 0.95,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "max_tokens": 800,
    "stop": 'null'
}

# our Azure OpenAI endpoint URL
azure_openai_url = f'{endpoint}/openai/deployments/Hiwi-Mobile-App-Chatbot/chat/completions?api-version=2023-07-01-preview'

# streamlit framework
# st.title('Celebrity Search Results')
# input_text = st.text_input("Search the topic u want")

response = requests.post(azure_openai_url, headers=headers, json=body)
generated_text = response.json().get('choices', [])[0].get('message', {}).get('content', '')


while True:
    r = sr.Recognizer()
    text = ""
    
    with sr.Microphone() as source:
        print("Speak:")
        r.energy_threshold = 1000
        r.adjust_for_ambient_noise(source, 1.2)
        
        try:
            audio = r.listen(source, timeout=10)  # Adjust the timeout as needed
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error with the API request; {0}".format(e))
        except Exception as e:
            print("An unexpected error occurred: {0}".format(e))
    
    new_user_message = {"role": "user", "content": text}
    conversation.append(new_user_message)
    
    body = {
        "messages": conversation,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 800,
        "stop": 'null'
    }
    
    # Make a request to Azure OpenAI API for the continued conversation

    response = requests.post(azure_openai_url, headers=headers, json=body)
    new_generated_text = response.json().get('choices', [])[0].get('message', {}).get('content', '')
    input_text = "Hello, how are you?"
   
   



    # Convert the generated text to speech
    text_to_speak = new_generated_text
    language = 'hi'  # Choose the appropriate language code
    
    
    tts = gTTS(text=text_to_speak, lang=language, slow=False)

   
    audio_file = "output.mp3"
    
    # # Save the audio file
    tts.save(audio_file)
    
    # # Get the duration of the audio file
    audio = MP3(audio_file)
    duration_in_seconds = audio.info.length
    
    
    
    os.system("start " + audio_file)
    time.sleep(duration_in_seconds)
    
    if text in text.lower() == "bye" or text in text.lower() == "thank you" :
        break
