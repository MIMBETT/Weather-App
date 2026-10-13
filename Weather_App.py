from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                            QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, 
                            QCheckBox, QRadioButton, QButtonGroup, QLineEdit)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt


import requests
import sys

class Weather_app(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title_label = QLabel("World Wide Weather App", self)
        self.select_label = QLabel("Enter city name:", self)
        self.city_or_error_label = QLabel(self)

        #parameters
        self.main_emoji_label = QLabel(self)
        self.general_info_label = QLabel(self)
        self.overall_temp_label = QLabel(self)
        self.feels_like_label1 = QLabel(self)
        self.feels_like_label2 = QLabel(self)
        self.humidity_label1 = QLabel(self)
        self.humidity_label2 = QLabel(self)
        self.preassure_label1 = QLabel(self)
        self.preassure_label2 = QLabel(self)
        self.temp_range_label1 = QLabel(self)
        self.temp_range_label2 = QLabel(self)
        self.wind_speed_label1 = QLabel(self)
        self.wind_speed_label2 = QLabel(self)
        self.wind_direction1 = QLabel(self)
        self.wind_direction2 = QLabel(self)
        
        self.city_line_edit = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        
        self.initUI()

        #To centralize labels
    def centralize_label(self, label_name, y_coord):
        label_name.adjustSize()
        label_width = label_name.width()
        label_height = label_name.height()
        window_width = self.width()
        x_coord = (window_width - label_width) // 2
        label_name.setGeometry(x_coord, y_coord, label_width, label_height)
        label_name.adjustSize()

    def initUI(self):

        #Window Setup
        self.setWindowTitle("World Wide Weather App")
        self.setGeometry(0, 0, 500, 750)
        self.setWindowIcon(QIcon("C:/Users/IMBETT/Desktop/IMAGENES/WORLD WIDE WEATHER APP.png"))

    #To define labels & other stuff

        #Title_label
        self.title_label.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.title_label.setFont(QFont("Arial", 25))
        self.centralize_label(self.title_label, 50)  
        self.title_label.setAlignment(Qt.AlignCenter)
        
        
        #select_label 
        self.select_label.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.select_label.setFont(QFont("Arial", 20))
        self.centralize_label(self.select_label, 145)  
        self.select_label.setAlignment(Qt.AlignCenter)
        

        #city_line_edit
        self.city_line_edit.setPlaceholderText("Ex: Los Angeles")
        self.city_line_edit.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.city_line_edit.setFont(QFont("Arial", 20))
        self.centralize_label(self.city_line_edit, 185) 
        self.city_line_edit.setAlignment(Qt.AlignCenter) 
        

        #get_weather_button
        self.get_weather_button.setStyleSheet("""
        color: black;
        font-family: Arial;
        background-color: lightgrey
        """)
        self.get_weather_button.setFont(QFont("Arial", 20))
        self.centralize_label(self.get_weather_button, 230) 

        self.get_weather_button.clicked.connect(self.api_climate_text_call)

    
    def api_climate_text_call(self):

        self.clear_labels()

        #API setup
        city_name = self.city_line_edit.text().lower()
        api_key = "0d62bb4a030ca2085172b22fa6295dfa"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
        
        #Exception Handling in case of Errors
        try:
            response = requests.get(url)
            code = requests.get(url).status_code

            response.raise_for_status() #Mandatory

            if code == 200:
                code = response.json()
                country_name = code["sys"]["country"]
                self.display_basic_info(city_name, country_name, code)
 
        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad Requests:\nPlease check your input")
                case 401:
                    self.display_error("Unaothorized:\nAccess denied, please register")
                case 403:
                    self.display_error("Forbidden:\nAccess denied, no permission allowed")
                case 404:
                    self.display_error("Not Found:\nCity Not Found\nPlease try again")
                case 500:
                    self.display_error("Internal Server Error:\nThe server does not respond")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nPlease try again later")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response")
                case _:
                    self.display_error(f"HTTP Error Ocurred:\n{requests.exceptions.HTTPError}")
        
        except requests.exceptions.ConnectionError:
            self.display_error(f"Connection Error:\n{requests.exceptions.ConnectionError}")
        except requests.exceptions.Timeout:
            self.display_error(f"Timeout Error:\n{requests.exceptions.Timeout}")
        except requests.exceptions.RequestException:
            self.display_error(f"request Error:\n{requests.exceptions.RequestException}")
        except requests.exceptions.TooManyRedirects:
            self.display_error(f"Too Many Redirects:\n{requests.exceptions.TooManyRedirects}")

        #To display the city, country, temp, and general description
    def display_basic_info(self, city_name, country_name, code):

        #To show city & country
        city_name = city_name.title()
        self.city_or_error_label.setText(city_name + ", " + country_name + ":")

        self.city_or_error_label.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.city_or_error_label.setFont(QFont("Arial", 20))
        self.city_or_error_label.setAlignment(Qt.AlignCenter)
        self.centralize_label(self.city_or_error_label, 285)

        #To show & extract emoji
        id = code["weather"][0]["id"]

        if id >= 200 and id <= 232:
            self.main_emoji_label.setText("⛈️")
        elif id >= 300 and id <= 321:
            self.main_emoji_label.setText("☔")
        elif id >= 500 and id <= 504:
            self.main_emoji_label.setText("🌦️")
        elif id >= 520 and id <= 531:
            self.main_emoji_label.setText("🌧️")
        elif id >= 600 and id <= 622 or id == 511:
            self.main_emoji_label.setText("🌨️")
        elif id >= 701 and id <= 761 or id == 771:
            self.main_emoji_label.setText("🌁")
        elif id == 762:
            self.main_emoji_label.setText("🌋")
        elif id == 781:
            self.main_emoji_label.setText("🌪️")
        elif id == 800:
            self.main_emoji_label.setText("☀️")
        elif id >= 801 and id <= 804:
            self.main_emoji_label.setText("🌤️")
        
        self.main_emoji_label.setFont(QFont("Segoe UI Emoji", 50))
        self.main_emoji_label.setGeometry(130, 335, 300, 300)
        self.main_emoji_label.adjustSize()

        description = code["weather"][0]["description"].title()
        self.general_info_label.setText(description)
        self.general_info_label.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.general_info_label.setFont(QFont("Arial", 17))
        self.general_info_label.setAlignment(Qt.AlignCenter)
        self.centralize_label(self.general_info_label, 320) 

        #To show & extract general description
        temp = code["main"]["temp"]
        celcius = float(temp - 273.15)

        self.overall_temp_label.setText(f"{celcius:.1f} °C")
        self.overall_temp_label.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.overall_temp_label.setFont(QFont("Arial", 30))
        self.overall_temp_label.setGeometry(225, 290, 200, 200)

        #To invoke the rest of the funcs & show the rest of the parameters
        self.display_temp_feels_like(code)
        self.display_humidity(code)
        self.display_pressure(code)
        self.display_temp_range(code)
        self.display_wind_speed(code)
        self.display_wind_direction(code)

    def display_temp_feels_like(self, code):

        feels_like = code["main"]["feels_like"]
        feels_like = float(feels_like - 273.15)
        

        self.feels_like_label1.setText("🌡️Feels Like:")
        self.feels_like_label1.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.feels_like_label1.setFont(QFont("Arial", 17))
        self.feels_like_label1.setGeometry(20, 360, 200, 200)
        self.feels_like_label2.setText(f"{feels_like:.1f} °C")
        self.feels_like_label2.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.feels_like_label2.setFont(QFont("Arial", 17))
        if len(str(feels_like//1)) == 4:
            self.feels_like_label2.setGeometry(65, 385, 200, 200)
        elif len(str(feels_like//1)) == 3:
            self.feels_like_label2.setGeometry(70, 385, 200, 200)


    def display_humidity(self, code):
        humidity = code["main"]["humidity"]
        humidity = str(humidity)

        self.humidity_label1.setText("💧Humidity:")
        self.humidity_label1.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.humidity_label1.setFont(QFont("Arial", 17))
        self.humidity_label1.setGeometry(20, 450, 200, 200)
        self.humidity_label2.setText(f"{humidity} %")
        self.humidity_label2.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        #To centralize depending on humidity
        self.humidity_label2.setFont(QFont("Arial", 17))
        if len(str(humidity)) == 2:
            self.humidity_label2.setGeometry(72, 475, 200, 200)
        elif len(str(humidity)) == 1:
            self.humidity_label2.setGeometry(78, 475, 200, 200)
        elif humidity == "100":
            self.humidity_label2.setGeometry(60, 475, 200, 200)

    def display_pressure(self, code):
        pressure = code["main"]["pressure"]
        pressure = int(pressure)

        self.preassure_label1.setText("⬇️Pressure:")
        self.preassure_label1.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.preassure_label1.setFont(QFont("Arial", 17))
        self.preassure_label1.setGeometry(20, 540, 200, 200)
        self.preassure_label2.setText(f"{pressure} hPa")
        self.preassure_label2.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.preassure_label2.setFont(QFont("Arial", 17))
        self.preassure_label2.setGeometry(47, 565, 200, 200)

    def display_temp_range(self, code):
        temp_min = code["main"]["temp_min"]
        temp_min = float(temp_min - 273.15)

        temp_max = code["main"]["temp_max"]
        temp_max = float(temp_max - 273.15)

        temp_range = f"{temp_max:.1f} - {temp_min:.1f}"

        self.temp_range_label1.setText("🔍Temperature Range:")
        self.temp_range_label1.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.temp_range_label1.setFont(QFont("Arial", 17))
        self.temp_range_label1.setGeometry(250, 360, 350, 200)

        self.temp_range_label2.setText(f"{temp_range} °C")
        self.temp_range_label2.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.temp_range_label2.setFont(QFont("Arial", 17))

        #To centralize depending on temp
        if len(str(temp_max//1)) == len(str(temp_min//1)) == 4:
            self.temp_range_label2.setGeometry(312, 385, 200, 200)
        
        elif len(str(temp_max//1)) == len(str(temp_min//1)) == 3:
            self.temp_range_label2.setGeometry(325, 385, 200, 200)
        
        elif len(str(temp_max//1)) == 3 and len(str(temp_min//1)) == 4 or len(str(temp_max//1)) == 4 and len(str(temp_min//1)) == 3:
            self.temp_range_label2.setGeometry(320, 385, 200, 200)

    def display_wind_speed(self, code):
        wind_speed = code["wind"]["speed"]
        wind_speed = float(wind_speed)

        self.wind_speed_label1.setText("💨Wind Speed:")
        self.wind_speed_label1.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.wind_speed_label1.setFont(QFont("Arial", 17))
        self.wind_speed_label1.setGeometry(290, 450, 200, 200)
        self.wind_speed_label2.setText(f"{wind_speed:.1f} m/s")
        self.wind_speed_label2.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.wind_speed_label2.setFont(QFont("Arial", 17))

        #To centralize depending on wind speed
        if len(str(wind_speed//1)) == 3:
            self.wind_speed_label2.setGeometry(347, 475, 200, 200)

        elif len(str(wind_speed//1)) == 4:
            self.wind_speed_label2.setGeometry(340, 475, 200, 200)

    def display_wind_direction(self, code):

        degrees = code["wind"]["deg"]

        #To transform degrees into a direction
        directions = [
        "North", "NNE", "North East", "ENE",
        "East", "ESE", "South East", "SSE",
        "South", "SSW", "South West", "WSW",
        "West", "WNW", "North West", "NNW"
        ]
        # 360° / 16 = 22.5° per direction
        index = int((degrees + 11.25) % 360 // 22.5)
        wind_direction =  directions[index]

        self.wind_direction1.setText("🧭Wind Direction:")
        self.wind_direction1.setStyleSheet("""
        color: black;
        font-family: Arial;
        """)
        self.wind_direction1.setFont(QFont("Arial", 17))
        self.wind_direction1.setGeometry(280, 540, 200, 200)
        self.wind_direction2.setText(wind_direction)
        self.wind_direction2.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.wind_direction2.setFont(QFont("Arial", 17))
        if len(wind_direction) == 3:
            self.wind_direction2.setGeometry(370, 565, 200, 200)

        elif len(wind_direction) == 4 or len(wind_direction) == 5:
            self.wind_direction2.setGeometry(355, 565, 200, 200)
        
        elif len(wind_direction) > 5:
            self.wind_direction2.setGeometry(320, 565, 200, 200)

        #To display errors
    def display_error(self, message):

        # Set the text first
        self.city_or_error_label.setText(message)
        
        # To style the text
        self.city_or_error_label.setStyleSheet("""
        color: black;
        font-weight: bold;
        font-family: Arial;
        """)
        self.city_or_error_label.setFont(QFont("Arial", 20))
        self.city_or_error_label.setAlignment(Qt.AlignCenter)
        self.centralize_label(self.city_or_error_label, 285) 

        self.clear_labels()

    def clear_labels(self):
        #To set labels to empty
        for label in(self.main_emoji_label,
                    self.general_info_label, 
                    self.overall_temp_label, 
                    self.feels_like_label1,
                    self.feels_like_label2, 
                    self.humidity_label1,
                    self.humidity_label2,
                    self.preassure_label1,
                    self.preassure_label2, 
                    self.temp_range_label1,
                    self.temp_range_label2, 
                    self.wind_speed_label1,
                    self.wind_speed_label2,
                    self.wind_direction1,
                    self.wind_direction2):
            
            label.setText("")


def main():
    app = QApplication(sys.argv)
    window = Weather_app()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
