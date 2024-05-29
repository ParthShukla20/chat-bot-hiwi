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
from googletrans import Translator
import json
import psycopg2
import keyboard


connection = psycopg2.connect(database="testdb", user="read_user", password="read_user", host="20.219.159.30", port=5431)
cursor = connection.cursor()

query1 = "SELECT u.email, u.latest_jwt,u.user_hash_id , l.hiwi_id from user_service.users as u  join transaction_service.ledger l on l.user_hash_id = u.user_hash_id where u.latest_jwt is not NULL order by u.updated_at desc, l.updated_at desc limit 1;"

query2 = "SELECT u.email, u.latest_jwt,u.user_hash_id , l.hiwi_id from user_service.users as u  join transaction_service.ledger l on l.user_hash_id = u.user_hash_id where u.email='ujwal.tamminedi@hiwipay.com' and u.latest_jwt is not NULL order by u.updated_at desc, l.updated_at desc LIMIT 1;"

cursor.execute(query2)

pygame.init()
translator = Translator()
azure_openai_key = 'f3b28a10a6d941bf94d1667cffc2e408'

os.environ["OPENAI_API_KEY"] = azure_openai_key

url = "https://hiwimobileapp-createopenai.openai.azure.com/openai/deployments/Hiwi-Mobile-App-Chatbot/extensions/chat/completions?api-version=2023-09-15-preview"  

headers = {
    # 'Authorization': 'Bearer ' + azure_openai_key,
    'Content-Type': 'application/json',
    'api-key'  : azure_openai_key
  
}
content = "what is tcs"
conversation = [
    {
      "role": "system",
      "content": "You are an AI assistant that helps people find information."
    },
    {
      "role": "user",
      "content": content

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

# response = requests.post(azure_openai_url, headers=headers, json=body)


# print(response.json().get('choices', [])[0].get('messages', [])[1].get('content', '')
#  )
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)        
engine.say("Hello I am Emmma. I am here to help you. Please select your conversational language")
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
            print("Error fetching results: {0}".format(e))

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
   
    print(f"API call failed with status code: {response.status_code}")
    print(response.text)


record = cursor.fetchall()

print(record)

email = record[0][0]
jwt = record[0][1]
user_hash_id = record[0][2]
hiwi_id = record[0][3]
# print(record)
flag_api_url = "http://20.219.159.30:8000/mobile/txn/get-status-flag"
flag_headers = {
    'Authorization': f'Bearer {jwt}'
}

flag_body  = {
    "userHashId":user_hash_id ,
    "email":email ,
    "role": "STUDENT",
    "deviceId": "xyz",
    "details": {
        "userHashId": user_hash_id,
        
        "hiwiId":hiwi_id ,
        "hiwiSubId": hiwi_id 
    }
}
# print(json.dumps(flag_body, indent=4))
flag_api_res = requests.post(flag_api_url,json=flag_body,headers=flag_headers)
final_res   =flag_api_res.content.decode('utf-8')
status = json.loads(final_res)
print(status)

statement = ""
if(status.get("a2formSign")):
    statement ="I see you completed signing the A2 Form, You can now complete your payment"
   
elif(status.get("finalAmount")):
     statement = "I see you confirmed the amount to send, you will now have to sign the A2 form declaration"
    
elif(status.get("sourceOfFunds")):
     statement = "Please confirm the amount you would like to remit abroad"
   
elif(status.get("moneyOrder")):
     statement = "Please enter your Source of funds here."
   
elif(status.get("payer")):
     statement = "Would you like to continue the transaction here or send a money request to the relative?"

elif(status.get("universityStudentDetails")):
     statement = "Now, please select who will be making the payment."

elif(status.get("payee")):
    statement = "You would like to remit funds to a University Account. Please go ahead and enter your Year of Completion, Program Type, Student ID, and Payment Type."
else:
    statement = "can you please say at which step of challan generation you are?"

content = statement      

print(statement)
statement = translator.translate(statement, src='en', dest=source_lang).text
tts = gTTS(text=statement, lang=source_lang, slow=False)

print(statement)

audio_data = BytesIO()
tts.write_to_fp(audio_data)
audio_data.seek(0)

pygame.mixer.init()
pygame.mixer.music.load(audio_data)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue

new_user_message = {"role": "user", "content": statement}
conversation.append(new_user_message)
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

        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        pygame.mixer.init()
        print(text_to_speak)
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()
        keyboard.on_press_key('q', lambda event: pygame.mixer.music.stop())

  
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
