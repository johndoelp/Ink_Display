import sys
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
panel_width = 400
panel_height = 300
panel = DrawingPanel(panel_width,panel_height)
panel.set_background("white")
panel.draw_image(os.path.join(PATH,"weather_resources/inky-display_background.png"),0,0)
panel.set_title("Trains & Weather")
#add invisible obj that ignores user input

# create "canvas" with background .png
# img = Image.open(os.path.join(PATH,"weather_resources/inky-display_background.png"))
# draw = ImageDraw.Draw(img)

# define & draw today's date
today_date = date.today().strftime("%a, %m/%d")
panel.draw_string(today_date,10,10,color="black")

# forecast_parser formatter & placement
def forecast_plot(forecast):
    forecast_x = 5
    forecast_y = 200
    # forecast_icon_x = 50
    # forecast_icon_y = 200
    for day in forecast:
        date = day['date']
        temp_max = "Max: " + str(round(day['temp_max'])) + "°F"
        temp_min = "Min: " + str(round(day['temp_min'])) + "°F"
        precip_chance = "Precip: " + str(str(day['precipitation_chance']) + "%")
        forecast_icon = day['weather_icon']
        day_date = date[5:7] + "/" + date[8:10]
        panel.draw_string(day_date, forecast_x, forecast_y, color="black")
        panel.draw_string(temp_max, forecast_x, forecast_y+45, color="black")
        panel.draw_string(temp_min, forecast_x, forecast_y+60, color="black")
        panel.draw_string(precip_chance, forecast_x, forecast_y+75, color="black")
        forecast_x += 100

forecast_plot(weather_get_MAIN.forecast_parser())