import speech_recognition as sr
import os
from gtts import gTTS
from transformers import BartForConditionalGeneration, BartTokenizer
from geopy.distance import geodesic
import wikipedia
from newsapi import NewsApiClient
import requests
import json

# Load BART model for summarization
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

#data
with open('datafile.json', 'r') as file:
    data = json.load(file)

# Functions for emergency services feature

def get_nearby_services_from_overpass(location, service_type):
    lat, lon = location
    radius = 1000  # in meters
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # If the service type is "car_repair", then adjust the amenity type for Overpass API query.
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

    # Get the location using `geocoder` or any other method
    # For now, let's use a dummy location for Hyderabad, India. 
    # You should replace this with a call to fetch the car's actual location.
    location = (17.385044, 78.486671)  #(lat, lon)

    services = get_nearby_services_from_overpass(location, service_type)

    # Calculate distances and sort services based on distance.
    # services_sorted_by_distance = sorted(services, key=lambda x: geodesic(location, (x['lat'], x['lon'])).km)

    # Fetch the top 5 nearest services
    nearest_services = services[:5]

    if nearest_services:
        talkToMe(f"The nearest {service_type}s are:")
        for service in nearest_services:
            talkToMe(service)
    else:
        talkToMe(f"Sorry, I couldn't find any nearby {service_type}s.")


BASE_URL = 'https://wttr.in/{}?format=%25C+%25w+%25t'

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


def get_current_weather(city='Hyderabad'):
    """Fetches the current weather for a city"""
    url = BASE_URL.format(city)
    response = requests.get(url)
    if response.status_code == 200:
        temperature, wind, weather = response.text.split()
        # Extracting just the numeric value for wind speed
        wind_speed = ''.join(filter(str.isdigit, wind))
        return weather, float(wind_speed)
    else:
        print("Error fetching the weather data")
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
            # Using a fixed location for Hyderabad for now; adjust as needed
            location = (17.385044, 78.486671)
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


talkToMe('Hello! Please name a place you want to know about, say "emergency" for emergency services, or "news" for the latest news.')

while True:
    provide_weather_alerts()  # Check for weather updates
    user_input = myCommand()
    if user_input == "News":
        news_mode()
    elif user_input == "Emergency":
        emergency_assistant()
    elif user_input in data:
        assistant()
    elif user_input and "thanks" in user_input:
        talkToMe("You're welcome! Goodbye.")
        break
    else:
        talkToMe("Sorry, I didn't understand your request. Please try again.")