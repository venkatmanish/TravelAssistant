import speech_recognition as sr
from gtts import gTTS
# import playsound
from IPython.display import Audio, display
import os
from ipywidgets import interact, widgets
from transformers import BartForConditionalGeneration, BartTokenizer

# Load BART model for summarization
model_name = "facebook/bart-large-cnn"
model = BartForConditionalGeneration.from_pretrained(model_name)
tokenizer = BartTokenizer.from_pretrained(model_name)

data = {
    "Charminar": {
        "description": "A historical monument and mosque located in Hyderabad, globally recognized as the symbol of the city.",
        "best_time_to_visit": "October to March",
        "activities": "Monument exploration, Local market shopping, Local cuisine sampling",
        "address": "Char Kaman, Ghansi Bazaar, Hyderabad, Telangana 500002, India"
    },
    "Golkonda": {
        "description": "A renowned fortified citadel, known for its history and architectural magnificence.",
        "best_time_to_visit": "November to February",
        "activities": "Historical tours, Light and Sound Show in evenings",
        "address": "Khair Complex, Ibrahim Bagh, Hyderabad, Telangana 500008, India"
    },
    "Ramoji Film City": {
        "description": "The world's largest integrated film studio complex, offering diverse entertainment options.",
        "best_time_to_visit": "All year round",
        "activities": "Studio tours, Theme parks, Film set experiences",
        "address": "Anaspur Village, Hayathnagar Mandal, Hyderabad, Telangana 501512, India"
    },
    "Hussain Sagar": {
        "description": "A heart-shaped lake in Hyderabad, famed for its watersports and the monolithic Buddha statue.",
        "best_time_to_visit": "October to February",
        "activities": "Boating, Watersports, Evening strolls",
        "address": "Hussain Sagar, Hyderabad, Telangana, India"
    },
    "Chowmahalla Palace": {
        "description": "A historical place known for its unique style and elegance, formerly the seat of the Asaf Jahi dynasty.",
        "best_time_to_visit": "October to March",
        "activities": "Palace tour, Vintage car display",
        "address": "20-4-236, Motigalli, Khilwat, Hyderabad, Telangana 500002, India"
    },
    "Salar Jung Museum": {
        "description": "One of the largest museums in the world, it houses the collection of Salar Jung III.",
        "best_time_to_visit": "October to March",
        "activities": "Explore historical artifacts, Art appreciation",
        "address": "Salar Jung Rd, Darulshifa, Hyderabad, Telangana 500002, India"
    },
    "Qutb Shahi Tombs": {
        "description": "A grand necropolis that houses the tombs of the seven Qutub Shahi kings.",
        "best_time_to_visit": "November to February",
        "activities": "Historical exploration, Photography",
        "address": "Toli Chowki, Hyderabad, Telangana 500008, India"
    },
    "Nehru Zoological Park": {
        "description": "A natural habitat housing diverse species, offering safari experiences.",
        "best_time_to_visit": "October to May",
        "activities": "Wildlife safari, Children's train ride, Aquatic animal exhibit",
        "address": "Bahadurpura W, Hyderabad, Telangana 500064, India"
    },
    "Shilparamam": {
        "description": "A cultural village showcasing arts and crafts of India.",
        "best_time_to_visit": "All year round",
        "activities": "Craft shopping, Cultural events, Workshops",
        "address": "Hi Tech City Main Rd, Sri Ram Nagar, CBI Colony, Jubilee Hills, Hyderabad, Telangana 500081, India"
    },
    "Birla Mandir": {
        "description": "A white marble temple dedicated to Lord Venkateshwara, offering panoramic views of the city.",
        "best_time_to_visit": "All year round",
        "activities": "Spiritual rituals, City view",
        "address": "Hill Fort Rd, Ambedkar Colony, Khairatabad, Hyderabad, Telangana 500004, India"
    },
    "Falaknuma Palace": {
        "description": "A palatial house in the shape of a scorpion, it's a blend of Italian and Tudor architecture.",
        "best_time_to_visit": "October to March",
        "activities": "Palace tour, Luxury dining, Photography",
        "address": "Engine Bowli, Fatima Nagar, Falaknuma, Hyderabad, Telangana 500053, India"
    },
    "Osman Sagar": {
        "description": "An artificial lake holding water sourced from the Musi River.",
        "best_time_to_visit": "October to February",
        "activities": "Boating, Picnics, Scenic drives",
        "address": "Osman Sagar, Hyderabad, Telangana, India"
    },
    "Nizam's Museum": {
        "description": "Located in Purani Haveli, it exhibits souvenirs, gifts, and mementos given to the last Nizam on his silver jubilee celebration.",
        "best_time_to_visit": "October to March",
        "activities": "Museum tour, Historical exploration",
        "address": "Purani Haveli, Pathar Gatti, Hyderabad, Telangana 500002, India"
    },
    "Lumbini Park": {
        "description": "A public urban park named after Lumbini of Nepal, dedicated to Lord Buddha.",
        "best_time_to_visit": "October to March",
        "activities": "Boating, Laser shows, Musical fountain shows",
        "address": "Opposite Secretariat New Gate, Khairatabad, Hyderabad, Telangana 500004, India"
    },
    "KBR National Park": {
        "description": "A national park that's a home to varied species of animals and birds.",
        "best_time_to_visit": "October to May",
        "activities": "Bird watching, Nature walks, Flora exploration",
        "address": "Jubilee Hills, Hyderabad, Telangana 500034, India"
    },
    "Jalavihar": {
        "description": "A family water park located beside Hussain Sagar.",
        "best_time_to_visit": "March to June",
        "activities": "Water rides, Family outings",
        "address": "Necklace Road, Hyderabad, Telangana 500063, India"
    },
    "Makkah Masjid": {
        "description": "One of the oldest mosques in Hyderabad, and one of the largest in India.",
        "best_time_to_visit": "October to March",
        "activities": "Historical exploration, Spiritual rituals",
        "address": "Charminar, Ghansi Bazaar, Hyderabad, Telangana 500002, India"
    },
    "Durgam Cheruvu": {
        "description": "A freshwater lake hidden amidst the rocky terrain.",
        "best_time_to_visit": "October to March",
        "activities": "Boating, Rock climbing, Trekking",
        "address": "Road No. 45, Jubilee Hills, Hyderabad, Telangana 500033, India"
    },
    "Snow World": {
        "description": "India's first and largest snow theme park.",
        "best_time_to_visit": "All year round",
        "activities": "Snow games, Ice skating, Snow slides",
        "address": "Lower Tank Bund Road, Bharath Seva Ashram Marg, Hyderabad, Telangana 500080, India"
    },
    "Koti Women's College": {
        "description": "A historic educational institution that stands as a testament to the Indo-European architectural grandeur.",
        "best_time_to_visit": "October to March",
        "activities": "Educational tours, Historical exploration",
        "address": "Koti Main Rd, Esamiya Bazaar, Kachiguda, Hyderabad, Telangana 500095, India"
    },
    "Himayat Sagar": {
        "description": "An artificial lake named after the youngest son of the 7th Nizam of Hyderabad.",
        "best_time_to_visit": "October to March",
        "activities": "Boating, Picnics, Cycling",
        "address": "Himayath Sagar, Hyderabad, Telangana, India"
    },
    "Taramati Baradari": {
        "description": "A historical sarai as part of Ibrahim Bagh, a Persian style garden built during the reign of Ibrahim Quli Qutub Shah.",
        "best_time_to_visit": "October to March",
        "activities": "Historical tours, Musical programs, Dance shows",
        "address": "Ibrahim Bagh, Hyderabad, Telangana 500031, India"
    },
    "Paigah Tombs": {
        "description": "The resting place of the esteemed Paigah family, showcasing Indo-Islamic architecture.",
        "best_time_to_visit": "October to March",
        "activities": "Historical exploration, Architectural appreciation, Photography",
        "address": "Santosh Nagar, Kanchan Bagh, Hyderabad, Telangana 500058, India"
    },
    "Buddha Statue": {
        "description": "A monolithic statue of Gautama Buddha on the Hussain Sagar island, the largest monolithic Buddha statue in India.",
        "best_time_to_visit": "October to March",
        "activities": "Boat ride, Statue exploration, Photography",
        "address": "Hussain Sagar, Hyderabad, Telangana, India"
    },
    "Paradise": {
        "description": "Famous for its biryani, Paradise is more than a restaurant; it's a culinary landmark.",
        "best_time_to_visit": "All year round",
        "activities": "Dining, Sampling Hyderabadi Biryani",
        "address": "Sarojini Devi Rd, Secunderabad, Telangana 500003, India"
    },
    "Sudha Cars Museum": {
        "description": "A museum that displays handmade automobiles and bikes.",
        "best_time_to_visit": "October to March",
        "activities": "Museum tours, Vintage car appreciation",
        "address": "19-5-15/1/D, Bahadurpura X Roads, beside Zoo Park, Hyderabad, Telangana 500064, India"
    },
    "Public Gardens": {
        "description": "One of the oldest parks in Hyderabad, housing several government offices, museums, and a zoo.",
        "best_time_to_visit": "October to March",
        "activities": "Nature walks, Museum tours, Zoo visit",
        "address": "Public Garden Rd, Red Hills, Lakdikapul, Hyderabad, Telangana 500004, India"
    },
    "Rajiv Gandhi International Airport": {
        "description": "A world-class international airport, providing modern amenities and efficient services.",
        "best_time_to_visit": "All year round",
        "activities": "Flying, Shopping, Dining",
        "address": "Shamshabad, Hyderabad, Telangana 500409, India"
    },
    "Sanjeevaiah Park": {
        "description": "An open green space named after the former President of India, Dr. Neelam Sanjeeva Reddy.",
        "best_time_to_visit": "October to March",
        "activities": "Picnics, Nature walks, Bird watching",
        "address": "Necklace Road, Hussain Sagar, Hyderabad, Telangana 500003, India"
    },
    "Laad Bazaar": {
        "description": "A vibrant market known for its bangles, jewelry, and pearls.",
        "best_time_to_visit": "October to March",
        "activities": "Shopping, Local cuisine sampling, Photography",
        "address": "Laad Bazaar Rd, Char Kaman, Ghansi Bazaar, Hyderabad, Telangana 500002, India"
    },

    "Jagannath Temple": {
        "description": "A Hindu temple known for its architectural beauty and spiritual significance.",
        "best_time_to_visit": "All year round",
        "activities": "Temple visit, Spiritual rituals",
        "address": "Plot No. 1269, Road No. 12, Banjara Hills, Hyderabad, Telangana 500034, India"
    },
    "Dhola-ri-Dhani": {
        "description": "A traditional Rajasthani village-themed resort, offering cultural experiences and authentic cuisine.",
        "best_time_to_visit": "All year round",
        "activities": "Cultural performances, Village experience, Rajasthani food",
        "address": "Medchal Road, Near Bank Of India, Brundavan Colony, Kompally, Hyderabad, Telangana 500014, India"
    },
    "Hyderabad Botanical Gardens": {
        "description": "A lush green park housing a diverse collection of plants, trees, and flowers.",
        "best_time_to_visit": "October to March",
        "activities": "Nature walks, Botanical exploration",
        "address": "Gachibowli, Hyderabad, Telangana 500032, India"
    },
    "Jala Vihar Water Park": {
        "description": "A water park offering thrilling water rides and family entertainment.",
        "best_time_to_visit": "March to June",
        "activities": "Water rides, Family outings, Fun in the sun",
        "address": "22/9, Necklace Road, Hyderabad, Telangana 500063, India"
    },
    "Indira Park": {
        "description": "A public park featuring a large musical fountain, a children's play area, and lush greenery.",
        "best_time_to_visit": "October to March",
        "activities": "Relaxation, Picnics, Musical fountain show",
        "address": "Lower Tank Bund Road, Kavadiguda, Hyderabad, Telangana 500029, India"
    },
    "NTR Gardens": {
        "description": "A garden with a range of attractions, including a toy train, boat ride, and Japanese garden.",
        "best_time_to_visit": "October to March",
        "activities": "Garden exploration, Toy train ride, Boating",
        "address": "NTR Marg, Central Secretariat, Khairatabad, Hyderabad, Telangana 500004, India"
    },
    "Chilkur Balaji Temple": {
        "description": "A temple known for its unique practice of granting wishes to devotees.",
        "best_time_to_visit": "All year round",
        "activities": "Temple visit, Prayers, Receiving blessings",
        "address": "Chilkur, Hyderabad, Telangana 501504, India"
    },
    "Jawaharlal Nehru Architecture and Fine Arts University": {
        "description": "An educational institution specializing in architecture and fine arts.",
        "best_time_to_visit": "October to March",
        "activities": "Educational tour, Art appreciation",
        "address": "Masab Tank, Hyderabad, Telangana 500028, India"
    },
    "Mrugavani National Park": {
        "description": "A national park serving as a sanctuary for various species of birds, reptiles, and plants.",
        "best_time_to_visit": "October to March",
        "activities": "Bird watching, Nature walks, Wildlife photography",
        "address": "Chilkur, Moinabad Mandal, Near Chilkur Balaji Temple, Hyderabad, Telangana 500075, India"
    },
    "Ananda Buddha Vihara Temple": {
        "description": "A beautiful Buddhist temple with traditional architecture and serene surroundings.",
        "best_time_to_visit": "All year round",
        "activities": "Temple visit, Meditation, Peaceful surroundings",
        "address": "Mahendra Hills, East Marredpally, Secunderabad, Telangana 500026, India"
    },
    "Kala Bhavan": {
        "description": "An institution of artistic excellence offering various courses in fine arts.",
        "best_time_to_visit": "October to March",
        "activities": "Art appreciation, Educational tours",
        "address": "Osmania University, Amberpet, Hyderabad, Telangana 500007, India"
    },
    "Necklace Road": {
        "description": "A scenic road along the Hussain Sagar lake, offering picturesque views and recreational facilities.",
        "best_time_to_visit": "October to March",
        "activities": "Strolls, Boating, Recreational activities",
        "address": "Necklace Road, Hyderabad, Telangana 500032, India"
    },
    "ISKCON Temple Hyderabad": {
        "description": "A temple dedicated to Lord Krishna, known for its spirituality and architecture.",
        "best_time_to_visit": "All year round",
        "activities": "Temple visit, Prayers, Spiritual experiences",
        "address": "Hare Krishna Land, Nampally Station Rd, Abids, Hyderabad, Telangana 500001, India"
    },
    "Chiran Palace": {
        "description": "A palace now converted into a luxurious hotel, known for its regal ambiance and hospitality.",
        "best_time_to_visit": "All year round",
        "activities": "Luxury stay, Dining, Royalty experience",
        "address": "Palace Road, Jubilee Hills, Hyderabad, Telangana 500033, India"
    },
    "Saroornagar Lake": {
        "description": "A scenic lake offering a serene escape from the hustle and bustle of the city.",
        "best_time_to_visit": "October to March",
        "activities": "Nature walks, Bird watching, Relaxation",
        "address": "Saroornagar, Kothapet, Hyderabad, Telangana 500035, India"
    },
    "Birla Science Museum": {
        "description": "A repository of innovation, it's a modern institution of learning.",
        "best_time_to_visit": "October to March",
        "activities": "Interactive exhibits, Science tours, Planetarium shows",
        "address": "Adarsh Nagar, Hyderabad, Telangana 500063, India"
    },
    "Spanish Mosque": {
        "description": "Known for its distinctive architecture, it's also called the Masjid Iqbal Ud Daula and Aiwan-E-Begumpet.",
        "best_time_to_visit": "October to March",
        "activities": "Architectural appreciation, Spiritual rituals",
        "address": "22, Sardar Patel Rd, Balamrai, Secunderabad, Telangana 500003, India"
    },
    "Mrugavani National Park": {
        "description": "An urban national park with diverse flora and fauna.",
        "best_time_to_visit": "October to May",
        "activities": "Wildlife safari, Nature walks, Photography",
        "address": "Chilkur, Moinabad Mandal, Hyderabad, Telangana 500075, India"
    },
    "Mahavir Harina Vanasthali National Park": {
        "description": "A deer national park located in Vanasthalipuram.",
        "best_time_to_visit": "October to May",
        "activities": "Deer spotting, Bird watching, Nature treks",
        "address": "Vanasthalipuram, Hyderabad, Telangana 500070, India"
    },
    "NTR Gardens": {
        "description": "A leisure and entertainment center in the heart of the city.",
        "best_time_to_visit": "October to March",
        "activities": "Leisure walks, Children rides, Bonsai garden",
        "address": "NTR Marg, Central Secretariat, Khairatabad, Hyderabad, Telangana 500004, India"
    },
    "Chilkoor Balaji Temple": {
        "description": "Popularly known as the Visa Balaji Temple, it's located on the banks of Osman Sagar.",
        "best_time_to_visit": "All year round",
        "activities": "Religious rituals, Spirituality",
        "address": "Chilkur, Hyderabad, Telangana 501504, India"
    },
    "Ocean Park": {
        "description": "An amusement park offering water rides and fun activities.",
        "best_time_to_visit": "March to June",
        "activities": "Water rides, Fun games, Family outings",
        "address": "Shankarpalli Road, Near CBIT College, Kokapet Village, Gandipet, Hyderabad, Telangana 500075, India"
    },
    "Qutb Shahi Heritage Park": {
        "description": "A unique blend of Persian and Indian architectural styles, showcasing the grandeur of the Qutb Shahi dynasty.",
        "best_time_to_visit": "October to March",
        "activities": "Historical exploration, Architectural appreciation, Photography",
        "address": "Toli Chowki, Hyderabad, Telangana 500008, India"
    },
    "Hyderabad Botanical Garden": {
        "description": "A vast expanse showcasing diverse flora species.",
        "best_time_to_visit": "October to March",
        "activities": "Nature walks, Flora exploration, Photography",
        "address": "Gachibowli, Hyderabad, Telangana 500032, India"
    },
    "Laserium at Lumbini Park": {
        "description": "A stunning laser show offering a visual narrative of Hyderabad's history.",
        "best_time_to_visit": "All year round",
        "activities": "Laser show, History narrative",
        "address": "Opposite Secretariat New Gate, Khairatabad, Hyderabad, Telangana 500004, India"
    },
    "Wonderla": {
        "description": "A top-notch amusement park offering thrilling rides and attractions.",
        "best_time_to_visit": "All year round",
        "activities": "Roller coasters, Water rides, High-thrill attractions",
        "address": "Outer Ring Road, Exit No. 13, Ravirala, Hyderabad, Telangana 501510, India"
    },
    "Shamirpet Lake": {
        "description": "A serene spot ideal for picnics and nature appreciation.",
        "best_time_to_visit": "October to March",
        "activities": "Picnics, Bird watching, Relaxation",
        "address": "Shamirpet, Secunderabad, Telangana 500078, India"
    },
    "Peddamma Temple": {
        "description": "One of the oldest temples in Hyderabad, dedicated to Goddess Peddamma.",
        "best_time_to_visit": "All year round",
        "activities": "Religious rituals, Festivals, Spirituality",
        "address": "Road No.55, Jubilee Hills, Hyderabad, Telangana 500033, India"
    },
    "Keesaragutta Temple": {
        "description": "A historic temple dedicated to Lord Shiva, it's located on a hillock.",
        "best_time_to_visit": "All year round",
        "activities": "Religious rituals, Panoramic views, Spirituality",
        "address": "Keesara, Telangana 501301, India"
    },
    "Salajung Museum": {
        "description": "One of the largest museums in the world, with a unique collection of sculptures, paintings, carvings, and textiles.",
        "best_time_to_visit": "October to March",
        "activities": "Art appreciation, Historical exploration",
        "address": "Salar Jung Rd, Darulshifa, Hyderabad, Telangana 500002, India"
    },
    "Hussain Sagar Lake": {
        "description": "A large lake in Hyderabad, famous for its monolithic statue of Gautama Buddha.",
        "best_time_to_visit": "October to March",
        "activities": "Boating, Evening strolls, Photography",
        "address": "Hussain Sagar, Hyderabad, Telangana, India"
    },
    "Jagannath Temple": {
        "description": "A modern temple built by the Oriya community in Hyderabad, resembling the historic Jagannath Temple of Puri.",
        "best_time_to_visit": "All year round",
        "activities": "Religious rituals, Temple tours",
        "address": "Plot No. 1269, Road No. 12, Banjara Hills, Hyderabad, Telangana 500034, India"
    },
    "Ravindra Bharathi": {
        "description": "A renowned theater for performing arts, named after Rabindranath Tagore.",
        "best_time_to_visit": "October to March",
        "activities": "Watch performances, Cultural exploration",
        "address": "Lakdikapul Rd, near State Assembly, Saifabad, Hyderabad, Telangana 500004, India"
    },
    "AP State Archaeological Museum": {
        "description": "A museum showcasing historical artifacts and exhibits from the region.",
        "best_time_to_visit": "October to March",
        "activities": "Historical exploration, Art appreciation",
        "address": "Public Gardens, Red Hills, Lakdikapul, Hyderabad, Telangana 500004, India"
    },
    "Hyderabad International Convention Center": {
        "description": "The leading venue for conventions in India, known for its state-of-the-art facilities.",
        "best_time_to_visit": "All year round",
        "activities": "Attend events, Business conferences",
        "address": "Hitex Road, Izzat Nagar, Hyderabad, Telangana 500084, India"
    },
    "Chowmahalla Palace": {
        "description": "The palace of the Nizams of Hyderabad, showcasing the grandeur of bygone eras.",
        "best_time_to_visit": "October to March",
        "activities": "Palace tour, Historical exploration",
        "address": "20-4-236, Motigalli, Khilwat, Hyderabad, Telangana 500002, India"
    },
    "Salar Jung Bridge": {
        "description": "A historic bridge over the Musi River, known for its architectural beauty.",
        "best_time_to_visit": "October to March",
        "activities": "Photography, Riverside strolls",
        "address": "Afzal Gunj, Hyderabad, Telangana, India"
    },
    "Sri Ramakrishna Math": {
        "description": "A monastery dedicated to Ramakrishna Paramahamsa, offering spiritual teachings.",
        "best_time_to_visit": "All year round",
        "activities": "Meditation, Spiritual learning",
        "address": "Lower Tank Bund Road, Domalguda, Indira Park, Hyderabad, Telangana 500029, India"
    },
    "Toli Masjid": {
        "description": "A revered mosque and a heritage site, showcasing architectural brilliance.",
        "best_time_to_visit": "October to March",
        "activities": "Architectural appreciation, Spiritual rituals",
        "address": "Karwan, Hyderabad, Telangana 500006, India"
    },
    "Hyderguda Church": {
        "description": "A landmark church, offering spiritual solace and architectural beauty.",
        "best_time_to_visit": "All year round",
        "activities": "Prayers, Architectural exploration",
        "address": "3-6-142/2, Opposite Skyline Theatre, Hyderguda, Hyderabad, Telangana 500029, India"
    },
    "Indira Park": {
        "description": "A green oasis in the city, named after former Prime Minister Indira Gandhi.",
        "best_time_to_visit": "October to March",
        "activities": "Picnics, Nature walks, Relaxation",
        "address": "Lower Tank Bund Road, Kavadiguda, Hyderabad, Telangana 500029, India"
    },
    "Aziz Bagh Mosque": {
        "description": "A beautiful mosque with unique architectural elements, located in Aziz Bagh.",
        "best_time_to_visit": "October to March",
        "activities": "Architectural appreciation, Prayers",
        "address": "Aziz Bagh, Tolichowki, Hyderabad, Telangana, India"
    },
    "Hyderabad Race Club": {
        "description": "The go-to destination for horse racing enthusiasts.",
        "best_time_to_visit": "July to March",
        "activities": "Horse racing, Betting",
        "address": "Race Course Road, Malakpet, Hyderabad, Telangana 500036, India"
    },
    "Tomb of Abdullah Qutb Shah": {
        "description": "The resting place of the seventh Sultan of the Qutb Shahi dynasty.",
        "best_time_to_visit": "October to March",
        "activities": "Historical exploration, Architectural appreciation",
        "address": "Qutb Shahi Tombs, Toli Chowki, Hyderabad, Telangana 500008, India"
    }
}

# def summarize(text):
#     inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
#     summary_ids = model.generate(inputs["input_ids"])
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary
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

def assistant():
    place_name = myCommand()
    if place_name and place_name in data:
        details = data[place_name]
        info = f"For {place_name}, {details['description']}. Best time to visit is {details['best_time_to_visit']}. Activities include {details['activities']}. Address: {details['address']}"
        talkToMe(info)
    elif place_name:
        talkToMe(f"Sorry, I don't have information on {place_name}")

talkToMe('Hello! Please name a place you want to know about.')
while True:
    voice_input = myCommand()
    if voice_input:
        if "Thanks" in voice_input:
            talkToMe("You're welcome! Goodbye.")
            break
        elif voice_input in data:
            details = data[voice_input]
            info = f"For {voice_input.title()}, {details['description']}. Best time to visit is {details['best_time_to_visit']}. Activities include {details['activities']}. Address: {details['address']}"
            talkToMe(info)
        else:
            talkToMe(f"Sorry, I don't have information on {voice_input}")

