from langdetect import detect, detect_langs
 
def detect_language(sentence):
    detected_lang = detect(sentence)
    return detected_lang
 
def get_language_name(language_code):
    # You can use a language mapping dictionary to get the language name from the language code
    language_mapping = {
        'en': 'English',
        'fr': 'French',
        'es': 'Spanish',
        'hi':'Hindi',
        'pa':'Punjabi',
        # Add more language codes and names as needed
    }
    return language_mapping.get(language_code, 'Unknown')
 
# Example usage
sentence = "ਤੁਸੀ ਕਿਵੇਂ ਹੋ"
detected_language = detect_language(sentence)
print (detected_language)
language_name = get_language_name(detected_language)
print(f"The detected language is: {language_name}")
