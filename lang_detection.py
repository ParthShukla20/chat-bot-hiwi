from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

with open("path/to/audio/file.wav", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(language_code=None)  # Let the API detect the language

response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))
    print("Detected language: {}".format(result.language_code))
