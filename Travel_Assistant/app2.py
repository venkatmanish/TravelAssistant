import speech_recognition as sr
import os
from gtts import gTTS
from transformers import BartForConditionalGeneration, BartTokenizer
import wikipedia

model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

def talkToMe(audio):
    """Speak out the audio"""
    print(audio)
    tts = gTTS(text=audio, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    os.system(f"afplay {filename}")
    os.remove(filename)

def recognize_speech():
    """Capture voice input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).title()  
        print('You said: ' + command + '\n')
        return command
    except sr.UnknownValueError:
        talkToMe('Sorry, I did not hear your request. Please repeat.')
        return None
    except sr.RequestError:
        talkToMe('Sorry, there seems to be an issue connecting to the service.')
        return None

def get_wikipedia_summary(place_name):
    """Fetches content summary about a place from Wikipedia."""
    try:
        return wikipedia.summary(place_name, sentences=5)  # fetching a 5-sentence summary for brevity
    except:
        return None

def assistant():
    voice_input = recognize_speech()
    response = ""

    if voice_input:
        if "thank you" in voice_input:
            response = "You're welcome! Goodbye."
            talkToMe(response)
            return False  # Using return statement to indicate that the loop should stop
        else:  
            # Fetching content from Wikipedia
            wikipedia_summary = get_wikipedia_summary(voice_input)
            if wikipedia_summary:
                response = f"Here's what I found about {voice_input} on Wikipedia: {wikipedia_summary}"
                talkToMe(response)
            else:
                response = f"Sorry, I couldn't find information on {voice_input}"
                talkToMe(response)

    return True  # Continue the loop if 'thank you' wasn't said

# The main loop:
talkToMe('Hello! Please name a place you want to know about.')
continue_loop = True
while continue_loop:
    continue_loop = assistant()  # This will return False if 'thank you' is the input
