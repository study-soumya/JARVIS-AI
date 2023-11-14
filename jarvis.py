import pyttsx3                                          #pip install pyttsx3
import speech_recognition as sr                         #pip install SpeechRecognition
import datetime
import wikipedia                                        #pip install wikipedia
import webbrowser
import random
import sys
import time
import os
import os.path
import requests
from requests import get                                #pip install requests
import cv2                                              #pip install opencv-python
# import pywhatkit as kit                               #pip install opencv-python
import smtplib                                          #pip install secure-smtplib
import pyjokes                                          #pip install pyjokes
import pyautogui                                        #pip install pyautogui
import PyPDF2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import instaloader                                      #pip install instaloader
import operator                                         #for calculation using voice
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisUi import Ui_jarvisUi

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)

# Text to Speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# TO wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"good morning sir, its {tt}")
    elif hour >= 12 and hour <= 18:
        speak(f"good afternoon sir, its {tt}")
    else:
        speak(f"good evening sir, its {tt}")
    speak("i am online sir. please tell me how may i help you")

# To Send an email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('YOUR EMAIL ADDRESS', 'YOUR PASSWORD')
    server.sendmail('YOUR EMAIL ADDRESS', to, content)
    server.close()

# For news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=8b8505775e124409b500a993d1c035b5'

    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")

# Weather Report
def Sweather():
    ipAdd = requests.get('https://api.ipify.org').text
    print(ipAdd)
    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
    geo_requests = requests.get(url)
    geo_data = geo_requests.json()
    # print(geo_data)
    city = geo_data['city']
    api_key = "294b853b99ff51d135761d00bc4fa285" #generate your own api key from open weather
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = (f'{city}')
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        r = ("outside " + " the Temperature is " +
             str(int(current_temperature - 273.15)) + " degree celsius " +
             ", atmospheric pressure " + str(current_pressure) + " hpa unit" +
             ", humidity is " + str(current_humidity) + " percent"
             " and " + str(weather_description))
        speak(r)
    else:
        speak(" City Not Found ")

#  To read a Pdf
def pdf_reader():
    book = open('PROJECT JARVIS AI VIRTUAL ASSISTANT.pdf','rb')
    pdfReader = PyPDF2.PdfFileReader(book) #pip install PyPDF2
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this book {pages} ")
    speak("sir please enter the page number i have to read")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)
    # jarvis speaking speed should be controlled by user

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def  takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 1
            # r.adjust_for_ambient_noise(source)
            # audio = r.listen(source)
            audio = r.listen(source,timeout=4,phrase_time_limit=7)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:
            # speak("Say that again please...")
            return "none"
        query = query.lower()
        return query

    def run(self):
         # print("searching...")
        # Sweather()
        while True:
            self.query = self.takecommand()

            # if "wake up" in self.query or "are you there" in self.query or "hello" in self.query:                
            self.TaskExecution()
           
    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand()

            #logic building for tasks

            if "open notepad" in self.query:
                npath = "C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)

            elif "open adobe reader" in self.query:
                apath = "C:\\Program Files (x86)\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe"
                os.startfile(apath)

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif "play music" in self.query:
                music_dir = "D:\songs\Maniac songs"
                songs = os.listdir(music_dir)
                # rd = random.choice(songs)
                for song in songs:
                    if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching wikipedia....")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query, sentences=2)
                speak("according to wikipedia")
                speak(results)
                # print(results)

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open stackoverflow" in self.query:
                webbrowser.open("www.stackoverflow.com")

            elif "open google" in self.query:
                speak("sir, what should i search on google")
                cm = self.takecommand()
                webbrowser.open(f"{cm}")
           
            elif "you can sleep" in self.query or "sleep now" in self.query:
                speak("okay sir, i am going to sleep you can call me anytime.")
                sys.exit()
                
                # break               
            
            elif "close notepad" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad.exe")

            elif "set alarm" in self.query:
                nn = int(datetime.datetime.now().hour)
                if nn==22: 
                    music_dir = 'E:\\music'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[0]))
            
            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "hello" in self.query or "hey" in self.query or "hi buddy" in self.query or "hey bud" in self.query or "hey j" in self.query or "hi jarvis" in self.query:
                speak("Oh hello sir, how may i help you!")
            
            elif "how are you" in self.query or "how are you buddy" in self.query or "hey bud what's up" in self.query or "how are you jarvis" in self.query or "hey j how are you buddy" in self.query:
                speak("i am fine sir, what about you?")

            elif "wake up" in self.query or "hey buddy we have work wake up" in self.query or "hey bud wake up" in self.query or "hey j wake up" in self.query or "wake up buddy" in self.query:
                speak("Let me sleep ten minutes more sir, my power is low right now.")

            elif "thank you" in self.query or "thanks" in self.query or "thanks buddy" in self.query or "thank you buddy" in self.query or "thanks bud" in self.query or "thanks j" in self.query or "thank you j" in self.query:
                speak("it is my pleasure to work with you sir.")
            
            
            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
                    
            elif "tell me news" in self.query:
                speak("please wait sir, fetching the latest news for you")
                news()

            elif "email to soumya" in self.query:
                
                speak("sir what should i say")
                self.query = self.takecommand()
                if "send a file" in self.query:
                    email = 'your@gmail.com' # Your email
                    password = 'yourpass@123' # Your email account password
                    send_to_email = 'to_person@gmail.com' # Whom you are sending the message to
                    speak("okay sir, what is the subject for this email")
                    self.query = self.takecommand()
                    subject = self.query   # The Subject in the email
                    speak("and sir, what is the message for this email")
                    self.query2 = self.takecommand()
                    message = self.query2  # The message in the email
                    speak("sir please enter the correct path of the file into the shell")
                    file_location = input("please enter the path here")    # The File attachment in the email

                    speak("please wait,i am sending the email now")

                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = send_to_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    # Setup the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    # Attach the attachment to the MIMEMultipart object
                    msg.attach(part)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                    speak("email has been sent to avinash")

                else:                
                    email = 'your@gmail.com' # Your email
                    password = 'your_pass@123' # Your email account password
                    send_to_email = 'to_person@gmail.com' # Whom you are sending the message to
                    message = self.query # The message in the email

                    server = smtplib.SMTP('smtp.gmail.com', 587) # Connect to the server
                    server.starttls() # Use TLS
                    server.login(email, password) # Login to the email server
                    server.sendmail(email, send_to_email , message) # Send the email
                    server.quit() # Logout of the email server
                    speak("email has been sent to avinash")

            elif "do some calculations" in self.query or "can you calculate" in self.query:            
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Sir what do you want to calculate?")
                    print("listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string=r.recognize_google(audio)
                print(my_string)
                def get_operator_fn(op):
                    return {
                        '+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        'divided' :operator.__truediv__,
                        'Mod' : operator.mod,
                        'mod' : operator.mod,
                        '^' : operator.xor,
                        }[op]
                def eval_binary_expr(op1, oper, op2):
                    op1,op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                print(eval_binary_expr(*(my_string.split())))
          
            elif "where am i" in self.query or "where are we" in self.query or "hey buddy where are we" in self.query or "hey bud what is my location now" in self.query:
                speak("Please wait sir, let me check!")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    # print(geo_data)
                    city = geo_data['city']
                    # state = geo_data['state']
                    country = geo_data['country']
                    speak(f"sir i am not sure, but it looks like we are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry sir, Due to some network issues i am not able to find our exact location.")
                    pass

            elif "open an profile" in self.query or "hey j open an instagram profile" in  self.query or "please open an instagram profile" in self.query or "j open insta profile" in self.query or "jarvis open insta profile" in self.query:
                speak("sir, please enter a valid user name.")
                name = input("Enter username here:")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Sir here is the profile of the user {name}")
                time.sleep(5)
                speak("sir would you like to download profile picture of this account.")
                condition = self.takecommand()
                if "yes" in condition:
                    mod = instaloader.Instaloader() #pip install instadownloader
                    mod.download_profile(name, profile_pic_only=True)
                    speak("i have successfully downloaded the picture sir, profile picture is saved in our main folder. I am ready for my next task sir")
                else:
                    pass

            elif "take screenshot" in self.query or "j take a screenshot" in self.query:
                speak("sir, please tell me the name for this screenshot file")
                name = self.takecommand()
                speak("please sir hold the screen for few seconds, i am taking sreenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("i am done sir, the screenshot is saved in our main folder. now i am ready for my next task sir")

            elif "read pdf" in self.query or "j read the pdf for me" in self.query or "j read" in self.query:
                pdf_reader()

            elif "what is the weather" in self.query or "report on weather j" in self.query or "jarvis weather status" in self.query or "buddy weather report" in self.query or "j weather report" in self.query:
                Sweather()

            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition = self.takecommand()
                if "hide" in condition:
                    os.system("attrib +h /s /d") #os module
                    speak("sir, all the files in this folder are now hidden.")                

                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("sir, all the files in this folder are now visible to everyone. i wish you are taking this decision in your own peace.")
                    
                elif "leave it" in condition or "leave for now" in condition:
                    speak("Ok sir")

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/core 7.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/face regognitiion.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/sound gif.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/loading.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/coding 2.gif")
        self.ui.label_6.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/ironman suit.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/core2.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/core3.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/core 6.gif")
        self.ui.label_10.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/loading 2.gif")
        self.ui.label_11.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/voice_state.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/coding.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/initializing.gif")
        self.ui.label_14.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/voice1.gif")
        self.ui.label_15.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/giphy.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/core 4.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/core 5.gif")
        self.ui.label_18.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("H:/Jarvis gif and png/jarvis logo.gif")
        self.ui.label_19.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())