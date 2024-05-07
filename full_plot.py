from time import sleep
from datetime import *
import os

# path to directory
PATH = os.path.dirname(__file__)

# import API call methods
import weather_get_MAIN
import current_weather_get_MAIN
import train_departure


#import pillow to create PNG with plotted weather & trains
from PIL import Image, ImageDraw, ImageFont
ImageFont.load_default()
import glob

# font specification
big_font = ImageFont.truetype(os.path.join(PATH,"weather_resources/Roboto/Roboto-Bold.ttf"),28)
medium_font = ImageFont.truetype(os.path.join(PATH,"weather_resources/Roboto/Roboto-Regular.ttf"),15)
small_font = ImageFont.truetype(os.path.join(PATH,"weather_resources/Roboto/Roboto-Regular.ttf"),12)

def full_plot():
    # train schedule & weather condition calls
    sleep(1)
    train_schedule = train_departure.train_call()
    forecast = weather_get_MAIN.forecast_parser()
    current_weather = current_weather_get_MAIN.current_parser()
    
    # open background image as the canvas
    all_plot = Image.open(os.path.join(PATH, "weather_resources/inky-display_background.png"))
    draw = ImageDraw.Draw(all_plot)
    
    today_day = date.today().strftime("%A")
    today_date = date.today().strftime("%B %#d")
    draw.text((10,10),today_day,(0),big_font)
    draw.text((10,40),today_date,(0),big_font)
    # plot the current weather conditions
    current_x = 210
    current_y = 10
    current_icon_x = 285
    current_icon_y = 15
    for todaycurrent in current_weather:
        current_weather_icon = todaycurrent["current weather icon"]
        draw.text((current_x, current_y), str(round(todaycurrent['current temperature'])) + "°F",(0),big_font)
        draw.text((current_x, current_y+80), "Max: " + str(round(todaycurrent["temp_max"])) + "°F",(0),medium_font)
        draw.text((current_x, current_y+100), "Min: " + str(round(todaycurrent["temp_min"])) + "°F",(0),medium_font)
        draw.text((current_x, current_y+120), "Rise: " + todaycurrent["sunrise"].strftime('%I:%M %p'),(0),medium_font)
        draw.text((current_x, current_y+140), "Set: " + todaycurrent["sunset"].strftime('%I:%M %p'),(0),medium_font)
        draw.text((current_x, current_y+160), "Precip: " +str(todaycurrent["precipitation_chance"]) + "%",(0),medium_font)
    
    # paste the current conditions icon
        icons = {}
        for icon in glob.glob(os.path.join("weather_resources/icon-*.png")):
            icon_name = icon.split("icon-")[1].replace(".png", "")
            icon_image = Image.open(icon)
            icons[icon_name] = icon_image.resize((100, 100), resample=Image.LANCZOS)
        if current_weather_icon is not None:
            all_plot.paste(icons[current_weather_icon], (current_icon_x, current_icon_y))


    # plot the forecast for the next four days
    forecast_x = 5
    forecast_y = 205
    forecast_icon_x = 50
    forecast_icon_y = 205
    for day in forecast:
        forecast_icon = day["weather_icon"]
        draw.text((forecast_x, forecast_y), day["date"][5:7] + "/" + day["date"][8:10],(0),medium_font)
        draw.text((forecast_x, forecast_y+40), "Max: " + str(round(day["temp_max"])) + "°F",(0),small_font)
        draw.text((forecast_x, forecast_y+55), "Min: " + str(round(day["temp_min"])) + "°F",(0),small_font)
        draw.text((forecast_x, forecast_y+70), "Precip: " + str(day["precipitation_chance"]) + "%",(0),small_font)
        forecast_x += 100

    # paste the forecast icon
        icons = {}
        for icon in glob.glob(os.path.join("weather_resources/icon-*.png")):
            icon_name = icon.split("icon-")[1].replace(".png", "")
            icon_image = Image.open(icon)
            icons[icon_name] = icon_image.resize((40, 40), resample=Image.LANCZOS)
        if forecast_icon is not None:
            all_plot.paste(icons[forecast_icon], (forecast_icon_x, forecast_icon_y))
        forecast_icon_x += 100
    
    # plot the trains
    train_x = 10
    train_y = 90
    if train_schedule != False:
        for i in range(len(train_schedule)):
            draw.text((train_x, train_y), str(f"Train {i+1} at: {train_schedule[i].strftime('%I:%M %p')}"),(0),medium_font)
            train_y += 25
    else:
        draw.text((train_x, train_y), "No trains predicted",(0),medium_font)
        draw.text((train_x, train_y+25), "currently.",(0),medium_font)

    # save all_plot as a png, as DrawingPanel doesn't seem to take all_plot as a returned image object
    all_plot.save(os.path.join(PATH, "all_plot.png"))

full_plot()