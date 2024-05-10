from flask import Flask, jsonify, render_template,request
import os
import requests
import speech_recognition as sr
from gtts import gTTS

import base64
from pydub.playback import play
from io import BytesIO
import pyttsx3
import pygame
import re
import keyboard
import threading



app = Flask(__name__)

def ai_res(ans):
    return ans


text_to_speak="starting.."


def voicebot():



    pygame.init()
    azure_openai_key = "f3b28a10a6d941bf94d1667cffc2e408"
    os.environ["OPENAI_API_KEY"] = azure_openai_key
    url = "https://hiwimobileapp-createopenai.openai.azure.com/openai/deployments/Hiwi-Mobile-App-Chatbot/extensions/chat/completions?api-version=2023-09-15-preview"
    headers = {
        # 'Authorization': 'Bearer ' + azure_openai_key,
        "Content-Type": "application/json",
        "api-key": azure_openai_key,
    }
    conversation = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information.",
        },
        {"role": "user", "content": "what is tcs"},
    ]
    body = {
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": "https://azure-search-service-hiwi-chatbot.search.windows.net",
                    "indexName": "chatindex02022024-01-index",
                    "semanticConfiguration": "default",
                    "queryType": "simple",
                    "fieldsMapping": {},
                    "inScope": "true",
                    "roleInformation": "You are an AI assistant that helps people find information.",
                    "strictness": 3,
                    "topNDocuments": 5,
                    "key": "ynt3y4kryQb5XQjSOesRzzcqPGKk6mn803SbhSYVXfAzSeByVqSc",
                },
            }
        ],
        "messages": conversation,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "max_tokens": 150,
    }

    # our Azure OpenAI endpoint URL
    azure_openai_url = url



    # response = requests.post(azure_openai_url, headers=headers, json=body)

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 138)
    engine.say(
        "Hello I am Emmma , I am here to help you. Please select your conversational language"
    )
    engine.runAndWait()
    config_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    model = {
        "telugu": "te",
        "tamil": "ta",
        "hindi": "hi",
        "gujarati": "gu",
        "marathi": "mr",
        "english": "en",
        "malyalam": "ml",
    }

    # source_lang = model.get(input("Enter the language you want to talk : ").lower())
    r = sr.Recognizer()

    text = ""
    source_lang = ""

    while True:
        with sr.Microphone() as source:
            print("Speak:")

           
            r.energy_threshold = 1000
            r.adjust_for_ambient_noise(source, 1.2)

            try:
                
                audio = r.listen(source, timeout=10)  # Adjust the timeout as needed
                text = r.recognize_google(audio)
                text = text.lower()
                print("You said:", text)
                if text in model:
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
        "ulcaApiKey": "178685922a-a901-4916-9c13-2bed6eeeedb7",
    }
    ulca_body_config = {
        "pipelineTasks": [
            {"taskType": "asr", "config": {"language": {"sourceLanguage": source_lang}}}
        ],
        "pipelineRequestConfig": {"pipelineId": "64392f96daac500b55c543cd"},
    }
    response = requests.post(config_url, headers=ulca_header_config, json=ulca_body_config)

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
            audio = r.listen(source, timeout=10)  # Adjust the timeout as needed
            with open("captured_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            with open("./captured_audio.wav", "rb") as audio_file:
                encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

            # print(encoded_audio)
            ulca_body_compute = {
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {
                            "language": {"sourceLanguage": source_lang},
                            "serviceId": service_id,
                            "audioFormat": "wav",
                            "samplingRate": 16000,
                        },
                    }
                ],
                "inputData": {"audio": [{"audioContent": encoded_audio}]},
            }
            ulca_header_compute = {
                "Authorization": data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"][
                    "value"
                ]
            }
            ulca_compute_url = data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
            compute_response = requests.post(
                ulca_compute_url, headers=ulca_header_compute, json=ulca_body_compute
            )
            response_data = compute_response.json()
            # print(response_data)
            source_value = response_data["pipelineResponse"][0]["output"][0]["source"]
            print(source_value)

            new_user_message = {"role": "user", "content": source_value}
            conversation.append(new_user_message)

            response = requests.post(azure_openai_url, headers=headers, json=body)
            new_generated_text = response.json()
            choices = new_generated_text["choices"]

            first_choice_content = choices[0]["message"]["content"]

            text_to_speak = first_choice_content
            text_to_speak = re.sub(r"\[doc(\d+)\]", "\b\b", text_to_speak)
            tts = gTTS(text=text_to_speak, lang=source_lang, slow=False)
            print(text_to_speak)

            audio_data = BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)

            pygame.mixer.init()
            pygame.mixer.music.load(audio_data)
            pygame.mixer.music.play()

            keyboard.on_press_key('q', lambda event: pygame.mixer.music.stop())
            while pygame.mixer.music.get_busy():
                continue



@app.route('/voicebot', methods=['POST'])
def voicebot2():
    t1 = threading.Thread(target = voicebot)
    t1.start()
    # return render_template("index2.html")
    # audio_file = request.files['audio']
    # recognizer = sr.Recognizer()

    # with sr.AudioFile(audio_file) as source:
    #     audio_data = recognizer.record(source)

    # try:
    #     text = recognizer.recognize_google(audio_data)
    # except sr.UnknownValueError:
    #     text = "Could not understand audio"
    # except sr.RequestError as e:
    #     text = "Error: {0}".format(e)

    # return jsonify({'text': text})

@app.route('/voicebot', methods=['GET'])
def voicebot3():

   return render_template("index2.html",name="Parth")
   

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4050, debug=True)

