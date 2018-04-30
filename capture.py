import face_recognition
import sqlite3
import glob
import cv2
import os

IP_Webcam = False

if IP_Webcam is True:
    url = "http://192.168.1.100:8080/shot.jpg" # IP Webcam
else:
    video_capture = cv2.VideoCapture(0)

while(True):
    if IP_Webcam is True:
        img_resp = requests.get(url)    # IP Webcam
        img_arr = np.array(bytearray(img_resp.content), dtype = np.uint8)
        frame = cv2.imdecode(img_arr, -1)
    else:
        ret, frame = video_capture.read()

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        unknown_face_encodings = face_recognition.face_encodings(frame)
        if len(unknown_face_encodings) > 0:
            print("Please enter your Name : ")
            name = str(input())
            file_name = name + ".jpg"
            cv2.imwrite(file_name, frame)
            face_encoding = unknown_face_encodings[0]
            break
        else:
            print("There's no face recognized in the image !!")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exited Operation !!")
        exit()

if IP_Webcam is not True:
    video_capture.release()
cv2.destroyAllWindows()

db = sqlite3.connect('db.sqlite3')
print("Opened Database Successfully !!")

cursor = db.cursor()

# Create database
cursor.execute('''CREATE TABLE IF NOT EXISTS FACES
            (ID  INTEGER  PRIMARY KEY  AUTOINCREMENT,
            FACE_NAME    TEXT  NOT NULL,
            FACE_ENCODING   blob  NOT NULL );''')

# Insert Operation
cursor.execute("SELECT count(*) FROM FACES WHERE FACE_NAME = ?", (name, ))
data = cursor.fetchone()[0]
if data == 0:
    cursor.execute("INSERT INTO FACES (FACE_NAME, FACE_ENCODING) VALUES (?, ?)",
            (name, sqlite3.Binary(face_encoding)))
    print("Photo Captured Successfully !!")
else:
    print("Photo Already Exists !!")

# Database Update Operation
print("Updating the Database !!")
for img in sorted(glob.glob("*.jpg")):
    img_name = os.path.basename(img)[:-4]
    cursor.execute("SELECT count(*) FROM FACES WHERE FACE_NAME = ?", (img_name, ))
    data = cursor.fetchone()[0]
    if data == 0:
        image = face_recognition.load_image_file(img)
        image_encoding = face_recognition.face_encodings(image)
        if len(image_encoding) > 0:
            cursor.execute("INSERT INTO FACES (FACE_NAME, FACE_ENCODING) VALUES (?, ?)",
                        (img_name, sqlite3.Binary(image_encoding[0])))

db.commit()
print("Done !!")
db.close()
