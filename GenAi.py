import speech_recognition as sr
import os
from gtts import gTTS
from transformers import BartForConditionalGeneration, BartTokenizer
from geopy.distance import geodesic
import wikipedia
from newsapi import NewsApiClient
import requests
import json
import openai  # Add the OpenAI import statement

# Load BART model for summarization
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

# Set your OpenAI API key here
openai.api_key = "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"

#dataxs
with open('datafile.json', 'r') as file:
    data = json.load(file)

def get_nearby_services_from_overpass(location, service_type):
    lat, lon = location
    radius = 1000  # in meters
    overpass_url = "https://overpass-api.de/api/interpreter"

    amenity_type = "car_repair" if service_type == "car_repair" else service_type

    query = f"""
    [out:json];
    node
      ["amenity"="{amenity_type}"]
      ({lat - 0.01},{lon - 0.01},{lat + 0.01},{lon + 0.01});
    out;
    """

    response = requests.get(overpass_url, params={'data': query})
    if response.status_code != 200:
        talkToMe(f"Sorry, I couldn't connect to the service to find nearby {service_type}s. Please try again later.")
        return []

    try:
        results = response.json().get('elements', [])
        return [result.get('tags', {}).get('name', 'Unknown name') for result in results]
    except json.decoder.JSONDecodeError:
        talkToMe(f"Sorry, I encountered an issue while fetching details for nearby {service_type}s. Please try again later.")
        return []

def emergency_assistant():
    talkToMe("Which emergency service are you looking for? Hospital or Police?")
    service_type = myCommand().lower()

    while not (service_type == "hospital" or service_type == "police"):
        talkToMe("Sorry, I did not hear your request. Please say either 'Hospital' or 'Police'.")
        service_type = myCommand().lower()

    location = (17.385044, 78.486671)  # Using a fixed location for Hyderabad for now; adjust as needed
    services = get_nearby_services_from_overpass(location, service_type)
    nearest_services = services[:5]

    if nearest_services:
        talkToMe(f"The nearest {service_type}s are:")
        for service in nearest_services:
            talkToMe(service)
    else:
        talkToMe(f"Sorry, I couldn't find any nearby {service_type}s.")

def get_latest_news():
    newsapi = NewsApiClient(api_key='33457d841a8d490c8882a70685353a43')  # Replace with your News API key

    top_headlines = newsapi.get_top_headlines(language='en')
    articles = top_headlines['articles']
    return articles

def summarize_news(article):
    title = article['title']
    content = article['content']
    if content:
        inputs = f'summarize: {title}. {content}'
        input_ids = tokenizer.encode(inputs, return_tensors='pt', max_length=1024, truncation=True)
        summary_ids = model.generate(input_ids, num_beams=4, min_length=30, max_length=3000, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    return None

def news_mode():
    talkToMe("News mode activated. Fetching the latest news headlines.")
    articles = get_latest_news()
    if articles:
        for i, article in enumerate(articles):
            if i == 5:
                break
            summary = summarize_news(article)
            if summary:
                talkToMe(f"News {i + 1}: {summary}")
                talkToMe("Do you want to read the complete article?")
                user_response = myCommand()
                while user_response and 'yes' not in user_response.lower() and 'no' not in user_response.lower():
                    talkToMe("Sorry, I didn't understand your response. Please say 'Yes' or 'No'.")
                    user_response = myCommand()
                if user_response and 'yes' in user_response.lower():
                    talkToMe("Reading the complete article.")
                    talkToMe(f"Title: {article['title']}")
                    talkToMe(f"Description: {article['description']}")
                    talkToMe(f"Content: {article['content']}")
                else:
                    talkToMe("Moving on to the next news.")
            else:
                talkToMe("Sorry, I couldn't summarize this news article. Moving on to the next one.")
    else:
        talkToMe("I couldn't fetch the latest news. Please try again later.")

OPENWEATHERMAP_API_KEY = 'd4be7a22708ef64cf2edc30d330ecf1a'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_current_weather(city='Hyderabad'):
    params = {
        'q': city,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric',  # Use 'imperial' for Fahrenheit
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        wind_speed = data['wind']['speed']
        weather_description = data['weather'][0]['description']
        return weather_description, wind_speed
    else:
        print(f"Error fetching weather data from OpenWeatherMap. Status code: {response.status_code}")
        print(response.text)  # Print the response content for further analysis
        return None, None

def provide_weather_alerts():
    weather, wind_speed = get_current_weather()
    if weather and wind_speed:
        if "rain" in weather.lower():
            talkToMe("It's raining outside. Please drive safely and keep your headlights on. Remember to maintain a safe distance from the vehicle ahead.")
        elif "snow" in weather.lower():
            talkToMe("There's snowfall in the area. Drive with caution and consider using snow chains if necessary.")
        elif "fog" in weather.lower():
            talkToMe("It's foggy outside. Reduce your speed and use low beam headlights.")
        elif wind_speed > 10:
            talkToMe("It's quite windy outside. Ensure all windows are rolled up and be cautious of potential debris on the road.")

def talkToMe(audio):
    """Speak out the audio"""
    print(audio)
    tts = gTTS(text=audio, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    os.system(f"afplay {filename}")
    os.remove(filename)

def myCommand():
    """Capture voice input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).title()  # Using title to match the data dict format
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
    voice_input = myCommand()

    if voice_input:
        if "thanks" in voice_input.lower():
            talkToMe("You're welcome! Goodbye.")
            return False  # Indicating the loop should stop

        elif "emergency" in voice_input.lower():
            talkToMe("Which emergency service are you looking for? Hospital or Police?")
            service_type = myCommand().lower()
            location = (17.385044, 78.486671)  # Using a fixed location for Hyderabad for now; adjust as needed
            services = get_nearby_services_from_overpass(location, service_type)
            for service in services[:5]:
                talkToMe(service)

        elif voice_input in data:
            details = data[voice_input]
            info = f"For {voice_input.title()}, {details['description']}. Best time to visit is {details['best_time_to_visit']}. Activities include {details['activities']}. Address: {details['address']}"
            talkToMe(info)

            talkToMe('Do you want more insights on this place?')
            further_insights = myCommand()
            if further_insights and "yes" in further_insights.lower():
                wikipedia_summary = get_wikipedia_summary(voice_input)
                if wikipedia_summary:
                    talkToMe(f"Here's more about {voice_input} from Wikipedia: {wikipedia_summary}")
                else:
                    talkToMe(f"Sorry, I couldn't fetch more information from Wikipedia about {voice_input}.")
            else:
                talkToMe("Okay! Let me know if you need any other information.")
                return False
        else:
            talkToMe(f"Sorry, I don't have information on {voice_input}.")

    return True

def chatgpt_interaction(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def universal_mode():
    talkToMe("Universal mode activated. Please provide a topic or question.")
    user_query = myCommand()

    if user_query:
        conversation_history = f"You: {user_query}\nAssistant:"
        response = chatgpt_interaction(conversation_history)
        talkToMe(response)
    else:
        talkToMe("Sorry, I didn't catch that. Please repeat your question.")

talkToMe('Hello! Please name a place you want to know about, say "emergency" for emergency services, or "news" for the latest news, or "universal" for universal mode.')

while True:
    provide_weather_alerts()  # Check for weather updates
    user_input = myCommand()
    if user_input == "News":
        news_mode()
    elif user_input == "Emergency":
        emergency_assistant()
    elif user_input == "Universal":
        universal_mode()
    elif user_input and "thanks" in user_input:
        talkToMe("You're welcome! Goodbye.")
        break
    else:
        talkToMe("Sorry, I didn't understand your request. Please try again.")
