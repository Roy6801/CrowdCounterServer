import numpy as np
import time


def overlap(he, bo):
    a = min(he[1] + he[3], bo[1] + bo[3]) - max(he[1], bo[1])
    b = min(he[0] + he[2], bo[0] + bo[2]) - max(he[0], bo[0])
    intersection = a * b
    return (intersection/(he[2] * he[3])) * 100


def process_time(ts):
    return time.strftime("%D %H:%M:%S", time.localtime(int(ts)))
