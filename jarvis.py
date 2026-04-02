import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import pyaudio

# Initialize the voice engine

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# voices[0] -> Male voice
# voices[1] -> Female voice

try:
    engine = pyttsx3.init('sapi5') 
except Exception as e:
    print(f"Driver error: {e}. Falling back to default.")
    engine = pyttsx3.init()

# Test the engine immediately
engine.say("Testing speakers")
engine.runAndWait()

voices = engine.getProperty('voices')
if len(voices) > 0:
    # Use index 1 (usually a female voice) if 0 is not working
    engine.setProperty('voice', voices[0].id) 

def speak(audio):
    # Print the text so you can see if the function is even being called
    print(f"JARVIS: {audio}") 
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the time of day"""

    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am your Assistant. How can I help you today?")


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()

    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("Sorry, I could not understand what you said.")
        return None

    except sr.RequestError:
        print("Speech service is unavailable")
        speak("Sorry, speech service is unavailable.")
        return None


if __name__ == "__main__":
    speak("Initializing JARVIS...")
    wishMe()

    while True:
        query = takeCommand()

        if query is None:
            continue

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            search_query = query.replace("wikipedia", "").strip()

            try:
                results = wikipedia.summary(search_query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception:
                speak("Sorry, I couldn't find information on that.")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
            

        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")
            

        elif 'open leetcode' in query:
            speak("Opening LeetCode")
            webbrowser.open("https://leetcode.com")
            

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'stop' in query or 'exit' in query:
            speak("Goodbye! Have a great day.")
            break


