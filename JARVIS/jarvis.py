import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import cv2
import numpy as np


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)




def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am JARVIS AI. How can i help you today?")
def takeCommand():
    #it takes microphone input from user and return the string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold= 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') #Using google for voice recognition.
        print(f"User said: {query}\n")  #User query will be printed.

    except Exception as e:
        #print(e)    
        print("Can you repeat it once again sir...")   #Say that again will be printed in case of improper voice 
        return "None" #None string will be returned
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587) #here 587 is port no
    server.ehlo()
    server.starttls()
    server.login('murghendraakki10@gmail.com', 'your-password')#put your gmail username and password
    server.sendmail('murghendraakki10@gmail.com', to, content)
    server.close()
    
def getWeather(city):
    api_key = '1bbf1fb279f6f158aac4df7379066d3b'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        response = requests.get(base_url)
        data = response.json()

        if data['cod'] != '404':
            main_info = data['main']
            temperature = main_info['temp']
            humidity = main_info['humidity']
            weather_info = data['weather'][0]['description']

            result = f'The current temperature in {city} is {temperature} Kelvin, humidity is {humidity}%, and the weather is {weather_info}.'
            return result
        else:
            return 'City not found. Please try again.'
    except Exception as e:
        print(f'Error fetching weather information: {str(e)}')
        print(f'Complete JSON response: {response.text}')
        return 'Error fetching weather information. Please try again.'
   
    
def video():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 10000:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                simplified_contour = cv2.approxPolyDP(contour, epsilon, True)

                hull = cv2.convexHull(simplified_contour, returnPoints=False)
                defects = cv2.convexityDefects(simplified_contour, hull)

                if defects is not None:
                    finger_count = 0
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(simplified_contour[s][0])
                        end = tuple(simplified_contour[e][0])
                        far = tuple(simplified_contour[f][0])

                        angle = np.degrees(np.arctan2(far[1] - start[1], far[0] - start[0]))

                        if d > 1000 and angle < 90:
                            finger_count += 1
                            cv2.circle(frame, far, 5, [0, 0, 255], -1)

                    cv2.putText(frame, f"Fingers: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.drawContours(frame, [simplified_contour], 0, (0, 255, 0), 3)

        cv2.imshow("Hand Gesture Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

 



if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open gfg' in query:
            webbrowser.open("Geeksforgeeks.com") 
        
        elif 'open notepad' in query:
            codePath = r"C:\Windows\notepad.exe"
            os.startfile(codePath)
              

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S") 
            print(strTime)   
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = r"C:\Users\Asus\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(codePath)

        elif 'open steam' in query:
            codePath = r"C:\Program Files (x86)\Steam\steam.exe"
            os.startfile(codePath)


        elif 'email to Murghendra' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "yourEmail@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")
                
        elif 'weather' in query:
            speak('Sure, please specify the city.')
            city = takeCommand()
            weather_info = getWeather(city)
            speak(weather_info)
            print(weather_info)
            
        elif 'video' in query:
            video()
 