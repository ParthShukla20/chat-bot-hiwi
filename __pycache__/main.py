import os
from constant import openai_key
from langchain.llms import OpenAI
import streamlit as st
import speech_recognition as sr
from gtts import gTTS

openai_key = 'f3b28a10a6d941bf94d1667cffc2e408'
os.environ["OPENAI_API_KEY"]=openai_key

# # streamlit framework

# st.title('Celebrity Search Results')
# input_text=st.text_input("Search the topic u want")

llm = OpenAI(temperature=0.8)

# if input_text:
#     st.write(llm(input_text))

r = sr.Recognizer()
text = ""
with sr.Microphone() as source:
    print("Speak:")
    r.energy_threshold =1000
    r.adjust_for_ambient_noise(source,1.2)
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

# text_to_speak = "आप कैसे हो "
input_text = text
text_to_speak = text

if input_text:
    text_to_speak = llm(input_text)

language = 'hi'

tts = gTTS(text=text_to_speak, lang=language, slow=False)


audio_file = "output.mp3"

# Save the audio file
tts.save(audio_file)

# Play the audio file (optional)
os.system("start " + audio_file)
