import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from imutils.video import VideoStream
import imutils
import time

exit_flag = False

def draw_close_button(frame):
    x1, y1, x2, y2 = 370, 30, 390, 45
    button_color = (0, 0, 200)
    cv2.rectangle(frame, (x1, y1), (x2, y2), button_color, -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)
    cv2.rectangle(frame, (x1 + 2, y1 + 2), (x2 + 2, y2 + 2), (0, 0, 100), 1)

    # Adjust font size for the smaller button
    font = cv2.FONT_HERSHEY_PLAIN
    label = "X"
    font_scale = 0.7
    thickness = 1

    # Measure text and center it
    text_size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    text_x = x1 + ((x2 - x1 - text_size[0]) // 2)
    text_y = y1 + ((y2 - y1 + text_size[1]) // 2) + text_size[1]
    cv2.putText(frame, label, (text_x, text_y), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

def click_event(event, x, y, flags, param):
    global exit_flag
    if event == cv2.EVENT_LBUTTONDOWN:
        if 380 <= x <= 390 and 35 <= y <= 45:
            exit_flag = True

def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()

    faces, locs, preds = [], [], []

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    return (locs, preds)

# Load models
prototxtPath = "face_detector/deploy.prototxt"
weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model("mask_detector.model")

# Start stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_event)

while True:
    if exit_flag:
        break

    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        label = "Mask" if mask > withoutMask else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
        cv2.putText(frame, label, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    draw_close_button(frame)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
