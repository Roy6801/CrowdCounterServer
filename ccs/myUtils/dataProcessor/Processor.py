import numpy as np
import time

def process_data(data_arr, fps, mAP):
    n_arr = np.array(data_arr)
    erf = (1 - mAP)/mAP
    val = np.sqrt(np.mean(n_arr**2))
    rect_val = val + erf*val
    if len(data_arr) > 5*int(round(fps)):
        del data_arr[0]
        return data_arr, int(round(rect_val))
    else:
        return data_arr, int(round(rect_val))


def process_time(ts):
    return time.strftime("%D %H:%M:%S", time.localtime(int(ts)))
