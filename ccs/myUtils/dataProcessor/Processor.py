import numpy as np
import time

def process_data(data_arr, fps):
    n_arr = np.array(data_arr)
    if len(data_arr) > 5*int(round(fps)):
        del data_arr[0]
        return data_arr, int(round(np.sqrt(np.mean(n_arr**2))))
    else:
        return data_arr, int(round(np.sqrt(np.mean(n_arr**2))))


def process_time(ts):
    return time.strftime("%D %H:%M:%S", time.localtime(int(ts)))
