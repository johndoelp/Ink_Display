from time import sleep
from datetime import *
import os

# import train API calls
import train_departure
import full_plot

# path to directory
PATH = os.path.dirname(__file__)

# drawingpanel import & settings, background
from DrawingPanel import DrawingPanel
panel_width, panel_height = 400, 300
panel = DrawingPanel(panel_width,panel_height,background="white")
panel.set_title("Trains & Weather")

# determine when the next trains are coming
train_schedule = train_departure.train_call()
next_train = train_schedule[0]
now_time = datetime.now().astimezone()
timeleft = next_train-now_time
print(round(timeleft.total_seconds()))
drawsleep_time = timeleft/timedelta(milliseconds=1)

# initial display on DrawingPanel
full_plot.full_plot()
print("plotted")
panel.draw_image(os.path.join(PATH, "all_plot.png"),0,0)
print("initial drawn")

while True:
    if round(timeleft.total_seconds()) > 60:
        DrawingPanel.sleep(panel,drawsleep_time)
        print("start")
        # train_schedule = train_departure.train_call()
        # next_train = train_schedule[0]
        now_time = datetime.now().astimezone()
        timeleft = next_train-now_time
        drawsleep_time = timeleft/timedelta(milliseconds=1)
    else:
        print("loopplot")
        full_plot.full_plot()
        panel.draw_image(os.path.join(PATH, "all_plot.png"),0,0)
        print("refreshed")
        train_schedule = train_departure.train_call()
        next_train = train_schedule[0]
        now_time = datetime.now().astimezone()
        timeleft = next_train-now_time
        drawsleep_time = timeleft/timedelta(milliseconds=1)
        print("fullrun")