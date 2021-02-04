from myUtils.pyrebaseConnector.Connector import Connection
import imutils
import numpy as np
import cv2

outputFrame = dict()
counter = 0


def capture(vid):
    global outputFrame
    print(vid)
    if vid in outputFrame:
        while True:
            img = outputFrame[vid]
            flag, eImg = cv2.imencode(".jpg", img)
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(eImg) + b'\r\n'


def detect(cid, cap, host):
    global outputFrame, counter
    net = cv2.dnn.readNet("model/yolov3_model.weights", "model/yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    conn = Connection(cid, host)
    while True:
        img = cap.read()
        if img is None:
            continue
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (host["quality"], host["quality"]), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        confidences = []
        boxes = []
        for out in outs:
            for detects in out:
                scores = detects[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    center_x = int(detects[0] * width)
                    center_y = int(detects[1] * height)
                    w = int(detects[2] * width)
                    h = int(detects[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        counter = range(len(boxes))
        if len(counter) != 0:
            conn.set_count(counter[-1])
        for i in counter:
            if i in indexes:
                x, y, w, h = boxes[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), (69, 177, 255), 2)
        outputFrame[cid] = imutils.resize(img, width=500)
