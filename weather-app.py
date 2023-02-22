from tkinter import *
from tkinter import ttk,messagebox
from datetime import datetime
from PIL import ImageTk, Image
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import requests
import pytz

# Framework

master = Tk()

class App(Tk):

    def __init__(self, *args, **kwargs):

        master.title("Weather Forecast") # App's title
        master.resizable(False,False) # Making the window unresizable

        self.icon_img = PhotoImage(file="sun-icon.png") # Changing the icon of the window
        master.iconphoto(False,self.icon_img)
        
        self.canvas = Canvas(master,height=500,width=950) # Creating a canvas
        self.canvas.pack()

        self.weather_photo = ImageTk.PhotoImage(Image.open("weather-icon1.png")) # Inserting the photo
        self.weather_photo_label = Label(master,image=self.weather_photo)
        self.weather_photo_label.place(x=450,y=120)

        self.search_bar_photo = ImageTk.PhotoImage(Image.open("search-bar.jpg")) # Inserting the photo
        self.search_bar_photo_label = Label(master,image=self.search_bar_photo) 
        self.search_bar_photo_label.place(x=20,y=20)

        self.frame = Frame(master,height=370,width=399,bg="#e6a52e") # Creating a Frame
        self.frame.place(x=20,y=100)

        self.city_field = Entry(master,justify="center",width=13,font=("poppins",25),border=0) # Creating a entry and replacing it over the photo
        self.city_field.place(x=52,y=25)

        self.search_icon_photo = ImageTk.PhotoImage(Image.open("search-icon.png")) # Inserting the photo
        self.search_icon_button = Button(master,image=self.search_icon_photo,borderwidth=0,cursor="hand2",bg="#ffffff",command=self.get_weather) # Creating a button to search and get weather
        self.search_icon_button.place(x=305,y=30)

        # Labels

        self.wind_label = Label(self.frame,bg="#e6a52e",fg="#000000",text="WIND",font=("Helvetica",17,"bold"))
        self.wind_label.place(x=18,y=20)

        self.wind_label = Label(self.frame,bg="#e6a52e",fg="#000000",text="HUMIDITY",font=("Helvetica",17,"bold"))
        self.wind_label.place(x=18,y=105)

        self.wind_label = Label(self.frame,bg="#e6a52e",fg="#000000",text="DESCRIPTION",font=("Helvetica",17,"bold"))
        self.wind_label.place(x=18,y=190)

        self.wind_label = Label(self.frame,bg="#e6a52e",fg="#000000",text="PRESSURE",font=("Helvetica",17,"bold"))
        self.wind_label.place(x=18,y=280)

        self.temp_label = Label(master,text="...",font=("Arial",65,"bold"))
        self.temp_label.place(x=730,y=170)

        self.celcius_label = Label(master,text="...",font=("Arial",20,"bold"))
        self.celcius_label.place(x=740,y=275)

        self.wind_num_label = Label(self.frame,text="...",bg="#e6a52e",fg="#000000",font=("Helvetica",25,"bold"))
        self.wind_num_label.place(x=250,y=15)

        self.humidity_num_label = Label(self.frame,text="...",bg="#e6a52e",fg="#000000",font=("Helvetica",25,"bold"))
        self.humidity_num_label.place(x=250,y=100)

        self.description_num_label = Label(self.frame,text="...",bg="#e6a52e",fg="#000000",font=("Helvetica",25,"bold"))
        self.description_num_label.place(x=250,y=187)

        self.pressure_num_label = Label(self.frame,text="...",bg="#e6a52e",fg="#000000",font=("Helvetica",25,"bold"))
        self.pressure_num_label.place(x=250,y=275)

        self.time_label = Label(master,font=("Helvetica",20,"bold"),text="Current Time:")
        self.time_label.place(x=550,y=30)

        self.time = Label(master,font=("Helvetica",20,"bold"),text="...")
        self.time.place(x=750,y=30)


    # Button Method:

    def get_weather(self):
        
        try:
            self.city_name = self.city_field.get() # Getting the city name from the entry
            self.geolocator = Nominatim(user_agent="geoapiExercises") # API
            self.location = self.geolocator.geocode(self.city_name) # Finding the location
            self.timeZoneFinder = TimezoneFinder() # Creating a TimezoneFinder object
            self.result = self.timeZoneFinder.timezone_at(lng=self.location.longitude,lat=self.location.latitude) # Finding the timezone from location
            
            self.home = pytz.timezone(self.result)
            self.local_time = datetime.now(self.home)
            self.current_time = self.local_time.strftime("%I:%M %p")

            self.time.config(text=self.current_time)

            # Weather

            self.weather_api = "https://api.openweathermap.org/data/2.5/weather?q=" + self.city_name + "&appid=91a81aaa10d812504c3c730bf7b3ab01"

            self.json_data = requests.get(self.weather_api).json()
            self.condition = self.json_data['weather'][0]['main']
            self.description = self.json_data['weather'][0]['description']
            self.temparature = int(self.json_data['main']['temp']-273.15)
            self.pressure = self.json_data['main']['pressure']
            self.humidity = self.json_data['main']['humidity']
            self.wind = self.json_data['wind']['speed']

            self.temp_label.config(text=(str(self.temparature))+ " °")
            self.celcius_label.config(text=(self.condition))

            self.wind_num_label.config(text=self.wind)
            self.description_num_label.config(text=self.description.capitalize())
            self.humidity_num_label.config(text=self.humidity)
            self.pressure_num_label.config(text=self.pressure)
            

        except Exception as err:

            self.message = "Please check your city name."
            messagebox.showerror("Invalid City Name",self.message)

weather_app = App()
master.mainloop()