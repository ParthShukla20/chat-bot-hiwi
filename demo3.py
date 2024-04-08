import os
import requests
import speech_recognition as sr
from gtts import gTTS
from langchain.llms import OpenAI
import base64
from pydub.playback import play
from io import BytesIO
import pyttsx3
import pygame
import re


pygame.init()
azure_openai_key = 'f3b28a10a6d941bf94d1667cffc2e408'

os.environ["OPENAI_API_KEY"] = azure_openai_key

url = "https://hiwimobileapp-createopenai.openai.azure.com/openai/deployments/Hiwi-Mobile-App-Chatbot/extensions/chat/completions?api-version=2023-09-15-preview"  

headers = {
    # 'Authorization': 'Bearer ' + azure_openai_key,
    'Content-Type': 'application/json',
    'api-key'  : azure_openai_key
 
}
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
body ={
  "dataSources": [
    {
      "type": "AzureCognitiveSearch",
      "parameters": {
        "endpoint": "https://azure-search-service-hiwi-chatbot.search.windows.net",
        "indexName": "chatindex02022024-01-index",
        "semanticConfiguration": "default",
        "queryType": "simple",
        "fieldsMapping": {},
        "inScope": 'true',
        "roleInformation": "You are an AI assistant that helps people find information.",
  
        "strictness": 3,
        "topNDocuments": 5,
        "key": "ynt3y4kryQb5XQjSOesRzzcqPGKk6mn803SbhSYVXfAzSeByVqSc"
      }
    }
  ],
  "messages": conversation,
  "temperature": 0.7,
  "top_p": 0.95,
  "frequency_penalty": 0,
  "presence_penalty": 0,
  "max_tokens": 150
}

# our Azure OpenAI endpoint URL
azure_openai_url = url

# streamlit framework
# st.title('Celebrity Search Results')
# input_text = st.text_input("Search the topic u want")

response = requests.post(azure_openai_url, headers=headers, json=body)


# print(response.json().get('choices', [])[0].get('messages', [])[1].get('content', '')
#  )
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 138)        
engine.say("Hello I am Emmma , I am here to help you. Please select your conversational language")
engine.runAndWait()  
config_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
model = {'telugu': 'te', 'tamil': 'ta', 'hindi': 'hi', 'gujarati': 'gu', 'marathi': 'mr', 'english': 'en','malyalam':'ml'}
    
    # source_lang = model.get(input("Enter the language you want to talk : ").lower())
r = sr.Recognizer()

# Initialize an empty string to store the recognized text
text = ""
source_lang=""

# Use a context manager to handle the microphone
while(True):
    with sr.Microphone() as source:
        print("Speak:")
    
    # Adjust recognizer settings
        r.energy_threshold = 1000
        r.adjust_for_ambient_noise(source, 1.2)
    
        try:
        # Listen to the microphone input
            audio = r.listen(source, timeout=10)  # Adjust the timeout as needed
        
        # Convert audio to text
            text = r.recognize_google(audio)
            text = text.lower()
        
       
            print("You said:", text)
            if(text in model):
                source_lang = model.get(text)
                break
            else:
                print("Please say correctly")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError as e:
            print("Error fetching results; {0}".format(e))


print(source_lang)

ulca_header_config = {

    "userID": "e143f6eaa3b344d681cf183673608a4d",
    "ulcaApiKey": "178685922a-a901-4916-9c13-2bed6eeeedb7"
}
ulca_body_config = {
    "pipelineTasks": [
        {
            "taskType": "asr",
            "config": {
                "language": {
                    "sourceLanguage": source_lang
                }
            }
        }
       
    ],
    "pipelineRequestConfig": {
        "pipelineId": "64392f96daac500b55c543cd"
    }
}
response = requests.post(config_url, headers=ulca_header_config, json=ulca_body_config)

# Check the response status
if response.status_code == 200:
    # Successful API call
    data = response.json()
    print("API call successful. Response:")
    # print(data)
    task_type_to_find = "asr"
    service_id = None

    for config in data.get("pipelineResponseConfig", []):
        if config.get("taskType") == task_type_to_find:
            service_id = config.get("config", [{}])[0].get("serviceId")
            break

    print("Service ID for task type 'asr':", service_id)
else:
    # API call failed
    print(f"API call failed with status code: {response.status_code}")
    print(response.text)


while True:
    r = sr.Recognizer()
    text = ""

    with sr.Microphone() as source:
        print("Speak:")
        r.energy_threshold = 1000
        r.adjust_for_ambient_noise(source, 1.2)
        # try:
        audio = r.listen(source, timeout=10)# Adjust the timeout as needed
        with open("captured_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        with open('./captured_audio.wav', "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
        
        # print(encoded_audio)
        ulca_body_compute= { "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": source_lang
                    },
                    "serviceId": service_id,
                    "audioFormat": "wav",
                    "samplingRate": 16000
                }
            }
        ],
        "inputData": {
            "audio": [
                {
                    "audioContent": encoded_audio }]
                    }
        }
        ulca_header_compute = {
                "Authorization" : data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
            }
        ulca_compute_url = data['pipelineInferenceAPIEndPoint']['callbackUrl']
        compute_response = requests.post(ulca_compute_url, headers=ulca_header_compute, json=ulca_body_compute)
        response_data = compute_response.json()
        # print(response_data)
        source_value =response_data["pipelineResponse"][0]["output"][0]["source"]
        print(source_value)

        new_user_message = {"role": "user", "content": source_value}
        conversation.append(new_user_message)
        
        
        response = requests.post(azure_openai_url, headers=headers, json=body)
        new_generated_text = response.json()
        choices =new_generated_text['choices']


        first_choice_content = choices[0]['message']['content']

        text_to_speak = first_choice_content
        text_to_speak = re.sub(r'\[doc(\d+)\]','\b\b',  text_to_speak)
        tts = gTTS(text=text_to_speak, lang=source_lang, slow=False)

        print(text_to_speak)
      
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()


        while pygame.mixer.music.get_busy():
            continue
        
        # print(text_to_speak)

        # audio_file = "output.mp3"
        
        # # # Save the audio file
        # tts.save(audio_file)

        # my_sound = pygame.mixer.Sound('output.mp3')
        # my_sound.play()
        # audio = MP3(audio_file)
        # duration_in_seconds = audio.info.length
        
        # # os.system("start " + audio_file)
        # time.sleep(duration_in_seconds)
        
    
    if text in text.lower() == "bye" or text in text.lower() == "thank you" :
        break
