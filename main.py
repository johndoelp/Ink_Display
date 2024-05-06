from time import sleep
from datetime import *
import os
from tempfile import TemporaryFile

# import API call methods
import weather_get_MAIN
import current_weather_get_MAIN
import train_departure

#import pillow to create PNG with plotted weather & trains
from PIL import Image, ImageDraw, ImageFont
ImageFont.load_default()
# import glob

# font specification


# path to directory
PATH = os.path.dirname(__file__)
temp_all_plot = TemporaryFile()

# drawingpanel import & settings, background
from DrawingPanel import DrawingPanel
panel_width, panel_height = 400, 300
panel = DrawingPanel(panel_width,panel_height,background="white")
panel.set_title("Trains & Weather")
#add invisible obj that ignores user input

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

# current conditions formatter & placement
def current_plot(current_weather):
    current_x = 210
    current_y = 10
    current_icon_x = 310
    current_icon_y = 25
    for todaycurrent in current_weather:
        current_weather_icon = todaycurrent["current weather icon"]
        panel.draw_string(str(round(todaycurrent['current temperature'])) + "°F", current_x, current_y)
        panel.draw_string("Max: " + str(round(todaycurrent["temp_max"])) + "°F", current_x, current_y+80)
        panel.draw_string("Min: " + str(round(todaycurrent["temp_min"])) + "°F", current_x, current_y+100)
        panel.draw_string("Rise: " + todaycurrent["sunrise"].strftime('%I:%M %p'), current_x, current_y+120)
        panel.draw_string("Set: " + todaycurrent["sunset"].strftime('%I:%M %p'), current_x, current_y+140)
        panel.draw_string("Precip: " +str(todaycurrent["precipitation_chance"]) + "%", current_x, current_y+160)

# train_schedule formatter & placement
def train_plot(train_schedule):
    train_x = 10
    train_y = 60
    for i in range(len(train_schedule)):
        # train_time_formatted = datetime.strptime(train_schedule[i],"%H:%M:%S")
        train_text = str(f"Train {i+1} at: {train_schedule[i].strftime('%I:%M %p')}")
        panel.draw_string(train_text, train_x, train_y)
        train_y += 25

def full_plot(forecast,current_weather,train_schedule):
    # open background image as the canvas
    all_plot = Image.open(os.path.join(PATH, "weather_resources/inky-display_background.png"))
    draw = ImageDraw.Draw(all_plot)
    
    today_date = date.today().strftime("%a, %m/%d")
    draw.text((10,10),today_date,(0))
    # plot the current weather conditions
    current_x = 210
    current_y = 10
    current_icon_x = 310
    current_icon_y = 25
    for todaycurrent in current_weather:
        current_weather_icon = todaycurrent["current weather icon"]
        draw.text((current_x, current_y), str(round(todaycurrent['current temperature'])) + "°F",(0))
        draw.text((current_x, current_y+80), "Max: " + str(round(todaycurrent["temp_max"])) + "°F",(0))
        draw.text((current_x, current_y+100), "Min: " + str(round(todaycurrent["temp_min"])) + "°F",(0))
        draw.text((current_x, current_y+120), "Rise: " + todaycurrent["sunrise"].strftime('%I:%M %p'),(0))
        draw.text((current_x, current_y+140), "Set: " + todaycurrent["sunset"].strftime('%I:%M %p'),(0))
        draw.text((current_x, current_y+160), "Precip: " +str(todaycurrent["precipitation_chance"]) + "%",(0))
    
    # plot the forecast for the next four days
    forecast_x = 5
    forecast_y = 200
    forecast_icon_x = 50
    forecast_icon_y = 200
    for day in forecast:
        forecast_icon = day['weather_icon']
        draw.text((forecast_x, forecast_y), day['date'][5:7] + "/" + day['date'][8:10],(0))
        draw.text((forecast_x, forecast_y+45), "Max: " + str(round(day['temp_max'])) + "°F",(0))
        draw.text((forecast_x, forecast_y+60), "Min: " + str(round(day['temp_min'])) + "°F",(0))
        draw.text((forecast_x, forecast_y+75), "Precip: " + str(day['precipitation_chance']) + "%",(0))
        forecast_x += 100
    
    # plot the trains
    train_x = 10
    train_y = 60
    for i in range(len(train_schedule)):
        # train_time_formatted = datetime.strptime(train_schedule[i],"%H:%M:%S")
        # train_text = str(f"Train {i+1} at: {train_schedule[i].strftime('%I:%M %p')}")
        draw.text((train_x, train_y), str(f"Train {i+1} at: {train_schedule[i].strftime('%I:%M %p')}"),(0))
        train_y += 25

    # save all_plot as a png, as DrawingPanel doesn't seem to take all_plot as a returned image object
    all_plot.save(os.path.join(PATH, "all_plot.png"))

# determine when the next trains are coming
train_schedule = train_departure.train_call()
next_train = train_schedule[0]
now_time = datetime.now().astimezone()
timeleft = next_train-now_time
print(round(timeleft.total_seconds()))

# grab current weather conditions & four day forecast
forecast = weather_get_MAIN.forecast_parser()
current_weather = current_weather_get_MAIN.current_parser()

# initial display on DrawingPanel
full_plot(forecast,current_weather,train_schedule)
panel.draw_image(os.path.join(PATH, "all_plot.png"),0,0)

# while True:
#     if timeleft.total_seconds() > 60:
#         sleep(160)
#         train_schedule = train_departure.train_call()
#         current_weather = current_weather_get_MAIN.current_parser()
#         forecast = weather_get_MAIN.forecast_parser()
#         panel.clear()
#         full_plot(forecast,current_weather,train_schedule)
#         next_train = train_schedule[0]
#         now_time = datetime.now().astimezone()
#         timeleft = next_train-now_time
#     else:
#         sleep(60)
#         now_time = datetime.now().astimezone()
#         timeleft = next_train-now_time
#         print(next_train-now_time)
