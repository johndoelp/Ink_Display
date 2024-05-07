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
def time_determiner():
    train_schedule = train_departure.train_call()
    # if train API returned >=1 departure_time value, calculate the timeleft until next train
    if train_schedule != False:
        next_train = train_schedule[0]
        now_time = datetime.now().astimezone()
        timeleft = next_train-now_time
        print(round(timeleft.total_seconds()))
        drawsleep_time = timeleft/timedelta(milliseconds=1)
        det_time = [drawsleep_time, timeleft.total_seconds(),next_train]
    # if train API returned a False, refresh in 60s
    else:
        now_time = datetime.now().astimezone()
        time_buff = now_time+timedelta(0,60)
        timeleft = time_buff-now_time
        print(round(timeleft.total_seconds()))
        drawsleep_time = timeleft/timedelta(milliseconds=1)
        det_time = [drawsleep_time, timeleft.total_seconds(),time_buff]

    return det_time

def train_time_compare(upcoming_time):
    now_time = datetime.now().astimezone()
    timeleft = upcoming_time-now_time
    print(round(timeleft.total_seconds()))
    drawsleep_time = timeleft/timedelta(milliseconds=1)
    return [drawsleep_time, timeleft.total_seconds(), upcoming_time]

# initial display on DrawingPanel
full_plot.full_plot()
panel.draw_image(os.path.join(PATH, "all_plot.png"),0,0)
print("initial drawn")
det_time = time_determiner()

while True:
    if round(det_time[1]) > 60:
        det_time = train_time_compare(det_time[2])
        print("waiting")
        DrawingPanel.sleep(panel,det_time[0])
        
    else:
        print("loopplot")
        DrawingPanel.sleep(panel,timedelta(0,1)/timedelta(milliseconds=1))
        full_plot.full_plot()
        DrawingPanel.sleep(panel,timedelta(0,1)/timedelta(milliseconds=1))
        panel.draw_image(os.path.join(PATH, "all_plot.png"),0,0)
        DrawingPanel.sleep(panel,timedelta(0,1)/timedelta(milliseconds=1))
        print("refreshed")
        det_time = time_determiner()
        print("fullrun")