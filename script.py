import face_recognition
import numpy as np
import requests
import sqlite3
import cv2

IP_Webcam = False

if IP_Webcam is True:
    url = "http://192.168.1.100:8080/shot.jpg"  # IP Webcam
else:
    video_capture = cv2.VideoCapture(0)

known_face_names = []
known_face_encodings = []

db = sqlite3.connect('db.sqlite3')
print("Opened Database Successfully !!")

cursor = db.cursor()

cursor.execute("SELECT * FROM sqlite_master WHERE name ='FACES' and type='table';")
chk = cursor.fetchone()
if chk is not None:
    data = cursor.execute("SELECT FACE_NAME, FACE_ENCODING FROM FACES")
else:
    print("There's no face entry in the Database !!")
    exit()

for row in data:
    known_face_names.append(row[0])
    known_face_encodings.append(np.frombuffer(row[1]))

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    if IP_Webcam is True:
        img_resp = requests.get(url)    # IP Webcam
        img_arr = np.array(bytearray(img_resp.content), dtype = np.uint8)
        frame = cv2.imdecode(img_arr, -1)
    else:
        ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx = 0.25, fy = 0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        height, width, _ = frame.shape
        if name is not "Unknown":
            cv2.putText(frame, 'Permission Granted !!', (int(width / 4), height - 50), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Permission Denied !!', (int(width / 4), height - 50), font, 1.0, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exited Operation !!")
        break

if IP_Webcam is not True:
    video_capture.release()
cv2.destroyAllWindows()
