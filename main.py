from time import sleep
from datetime import *
import os

# import API call methods
import weather_get_MAIN
import current_weather_get_MAIN
# import train_departure
# import next_train_time


# import PIL
# from PIL import Image
import glob

# font specification


# path to directory of icons
PATH = os.path.dirname(__file__)

# drawingpanel import & settings, background
from DrawingPanel import *
panel_width, panel_height = 400, 300
panel = DrawingPanel(panel_width,panel_height)
panel.set_background("white")
panel.draw_image(os.path.join(PATH,"weather_resources/inky-display_background.png"),0,0)
panel.set_title("Trains & Weather")
panel.set_color("black")
#add invisible obj that ignores user input


# define & draw today's date
today_date = date.today().strftime("%a, %m/%d")
panel.draw_string(today_date,10,10,color="black")

# forecast_parser formatter & placement
def forecast_plot(forecast):
    forecast_x = 5
    forecast_y = 200
    forecast_icon_x = 50
    forecast_icon_y = 200
    for day in forecast:
        forecast_icon = day['weather_icon']
        panel.draw_string(day['date'][5:7] + "/" + day['date'][8:10], forecast_x, forecast_y)
        panel.draw_string("Max: " + str(round(day['temp_max'])) + "°F", forecast_x, forecast_y+45)
        panel.draw_string("Min: " + str(round(day['temp_min'])) + "°F", forecast_x, forecast_y+60)
        panel.draw_string("Precip: " + str(day['precipitation_chance']) + "%", forecast_x, forecast_y+75)
        forecast_x += 100

forecast_plot(weather_get_MAIN.forecast_parser())