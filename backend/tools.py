# backend/tools.py
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Ollama MedGemma function (keep as you had it)
import ollama

def query_medgemma(prompt: str) -> str:
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist...
    (keep your same system prompt here)
    """
    try:
        response = ollama.chat(
            model='alibayram/medgemma:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={'num_predict': 350, 'temperature': 0.7, 'top_p': 0.9}
        )
        return response['message']['content'].strip()
    except Exception as e:
        # log or print for local debugging
        print("Ollama error:", repr(e))
        return "I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."

# Location search using OpenStreetMap (Nominatim)
def find_support_nearby(location: str) -> str:
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{location} mental health OR hospital OR counseling",
            "format": "json",
            "limit": 5,
        }
        response = requests.get(url, params=params, headers={"User-Agent": "SafeSpaceAI/1.0"}, timeout=10)
        results = response.json()
        if results:
            centers = []
            for place in results:
                name = place.get("display_name", "Unknown place")
                lat = place.get("lat", "")
                lon = place.get("lon", "")
                # Google maps link for usability
                centers.append(f"- {name} (📍 https://www.google.com/maps?q={lat},{lon})")
            return f"Here are some mental health support options near {location}:\n" + "\n".join(centers)
        # Fallback helplines
        return (
            f"Sorry, I couldn't find specific centers in {location}.\n\n"
            "📞 Here are some mental health helplines you can call:\n"
            "- KIRAN (India): 1800-599-0019\n"
            "- Vandrevala: 1860-266-2345\n"
            "- Find a Helpline (Global): https://findahelpline.com\n"
            "\n🌐 Online options: Wysa, YourDOST"
        )
    except Exception as e:
        print("find_support_nearby error:", repr(e))
        return (
            "⚠️ Technical issue while searching for locations. Meanwhile please reach out to:\n"
            "- KIRAN (India): 1800-599-0019\n"
            "- Vandrevala: 1860-266-2345\n            "
        )

# Twilio emergency call — returns a status string
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def call_emergency(phone: str | None = None) -> str:
    """
    Initiates a call to `phone` or EMERGENCY_CONTACT. Returns a status string.
    """
    target = phone or EMERGENCY_CONTACT
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        return "Twilio credentials not configured."
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=target,
            from_=TWILIO_FROM_NUMBER,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        return f"Call initiated. SID: {call.sid}"
    except Exception as e:
        print("Twilio error:", repr(e))
        return "Failed to initiate emergency call. Check Twilio logs."
