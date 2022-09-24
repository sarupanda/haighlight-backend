import cv2
from statistics import mean
import pandas
import math

def extract_luminosity_data(file_name, interval):
    cap = cv2.VideoCapture(file_name)
    all_vals = pandas.DataFrame(columns=["timestamp", "luminosity"])
    interval_vals = []
    insert_counter = 0
    while True:
        ret, frame = cap.read()
        if ret:
            hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            interval_vals.append(cv2.mean(hsv_image)[2])
            timestamp = math.floor(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
            print(timestamp)
            if timestamp > 0 and timestamp % interval == 0 and timestamp not in all_vals.timestamp.values:
                all_vals.loc[insert_counter] = [timestamp, mean(interval_vals)]
                insert_counter += 1
                interval_vals = []
        else:
            break
    return all_vals

extract_luminosity_data('test_low_res.mp4', 5)
