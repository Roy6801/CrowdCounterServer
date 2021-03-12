from myUtils.pyrebaseConnector.Connector import Connection
from myUtils.dataProcessor.Processor import overlap
import imutils
import numpy as np
import time
import cv2


outputFrame = dict()


def capture(vid):
    global outputFrame
    print(vid)
    if vid in outputFrame:
        while True:
            img = outputFrame[vid]
            flag, eImg = cv2.imencode(".jpg", img)
            if not flag:
                continue
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(eImg) + b'\r\n'


def detect(cid, cap, host):
    global outputFrame
    net = cv2.dnn.readNet("model/yolov3_model.weights", "model/yolov3.cfg")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    conn = Connection(cid, host)
    counter = 0
    classes = ["Body", "Head"]
    itr = 0
    fps = 10
    while True:
        start = time.time()
        img = cap.read()
        if img is None:
            continue
        itr += 1
        if itr % 5 != 0:
            continue
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (host["quality"], host["quality"]), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        confidences = []
        boxes = []
        class_ids = []
        for out in outs:
            for detects in out:
                scores = detects[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.73:
                    center_x = int(detects[0] * width)
                    center_y = int(detects[1] * height)
                    w = int(detects[2] * width)
                    h = int(detects[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.73, 0.6)
        counter = range(len(boxes))
        head = []
        head_id = []
        body = []
        temp = set()
        for i in counter:
            if i in indexes:
                label = str(classes[class_ids[i]])
                if label == "Head":
                    head.append(boxes[i])
                    head_id.append(i)
                else:
                    body.append(boxes[i])
        for (i,k) in zip(head,head_id):
            for j in body:
                iou = overlap(i, j)
                if iou > 30.0:
                    temp.add(k)
        if len(counter) != 0:
            if counter[-1] > len(temp):
                conn.set_count(counter[-1] - len(temp))
                cv2.putText(img, "Count : "+str(counter[-1] - len(temp)), (int(0.05*width), int(0.1*height)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            else:
                conn.set_count(counter[-1])
                cv2.putText(img, "Count : "+str(counter[-1]), (int(0.05*width), int(0.1*height)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, "FPS : "+str(round(fps, 2)), (int(0.6*width), int(0.1*height)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        for i in counter:
            if i in indexes and i not in temp:
                x, y, w, h = boxes[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 98, 255), 2)
        outputFrame[cid] = imutils.resize(img, width=500)
        itr = 0
        fps = 1/(time.time() - start)
