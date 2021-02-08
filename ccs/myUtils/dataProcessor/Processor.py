import numpy as np
import time

def process_data(data_arr, fps):
    if data_arr.size > 5*int(round(fps)):
        arr = np.delete(data_arr, 0)
        return arr, int(round(np.sqrt(np.mean(arr**2))))
    else:
        return data_arr, int(round(np.sqrt(np.mean(data_arr**2))))


def process_time(ts):
    return time.strftime("%D %H:%M:%S", time.localtime(int(ts)))
