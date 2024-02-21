from transformers import MBartForConditionalGeneration, MBartTokenizer
import langid
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load the mBART model and tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"
model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBartTokenizer.from_pretrained(model_name)

# Input text in Hinglish
input_text = "mjhe bhuk lgi hai"

# Detect the language of the input text using langid
input_language, _ = langid.classify(input_text)

# Map the detected language to the corresponding language code
decoder_language_code = {"en": "en_XX", "hi": "hi_IN"}  # Adjust as needed
decoder_start_token_id = tokenizer.lang_code_to_id[decoder_language_code.get(input_language, "en_XX")]

# Tokenize the input text
input_ids = tokenizer.encode(input_text, return_tensors="pt")

# Generate translation
translated_ids = model.generate(input_ids, max_length=100, num_beams=4, length_penalty=2.0, early_stopping=True, decoder_start_token_id=decoder_start_token_id)
translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

print("Input Text:", input_text)
print(f"Detected Language: {input_language}")
print(f"Translated Text ({decoder_language_code[input_language]}):", translated_text)