from datetime import datetime
import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-real-tim-4a64a-default-rtdb.firebaseio.com/",
    'storageBucket': "face-attendance-real-tim-4a64a.appspot.com"
 }
)

bucket = storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imageBackground = cv2.imread('resource/background.png')

#Importing the mode images into the list
folderModePath = 'resource/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
# print(modePathList)

for modePath in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, modePath)))
# print(len(imgModeList))


#Load the encoding file.
print("Loading Encode File ...")
file = open('EncodFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")


modeType = 0
counter = 0
id = -1
imgStudent = []


while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, faceCurrentFrame)

    imageBackground[162:162+480, 55:55+640] = img
    imageBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    if faceCurrentFrame:
        for encodeFace, faceLocation in zip(encodeCurrentFrame, faceCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("Matches", matches)
            # print("Face Distance", faceDis)

            matchIndex = np.argmin(faceDis)


            if matches[matchIndex]:
                # print("Acurate face detected.")
                # print(studentIds[matchIndex])

                y1, x2, y2, x1 = faceLocation
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imageBackground = cvzone.cornerRect(imageBackground, bbox, rt = 0)
                id = studentIds[matchIndex]
                # print(id)

                if counter == 0:
                    cvzone.putTextRect(imageBackground, "Loading", (275, 400))
                    cv2.imshow("Face Recogintion", imageBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1    

            if counter != 0:

                if counter == 1:

                    # Get the data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)


                    # Get the image from storage
                    blob = bucket.get_blob(f'images/{id}.jpg')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    # Update data the attendance

                    datetimeObject = datetime.strptime(studentInfo['last attendance time'], 
                                                    "%Y-%m-%d %H:%M:%S")
                                                    
                    secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                    print(secondsElapsed)

                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total attendance'] += 1
                        ref.child('total attendance').set(studentInfo['total attendance'])
                        ref.child('last attendance time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        print("Already attendance taken.")
                        modeType = 3
                        counter = 0
                        imageBackground[44:44+633, 808:808+414] = imgModeList[modeType]


                if 5 < counter < 10:
                    modeType = 2

                imageBackground[44:44+633, 808:808+414] = imgModeList[modeType]

                
                
                if modeType != 3:
                    if counter <= 5:

                        cv2.putText(imageBackground, str(studentInfo['total attendance']), (860, 125), 
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imageBackground, str(studentInfo['company']), (1010, 550), 
                                    cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)
                        cv2.putText(imageBackground, str(studentInfo['id']), (1010, 493), 
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (70, 70, 70), 1)
                        cv2.putText(imageBackground, str(studentInfo['gender']), (1012, 625), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (70, 70, 70), 2)
                        cv2.putText(imageBackground, str(studentInfo['Joined year']), (1125, 625), 
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (70, 70, 70), 2)
                        cv2.putText(imageBackground, str(studentInfo['nationality']), (905, 625), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (70, 70, 70), 2)

                        
                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_ITALIC, 1, 3)
                        offset = (414 - w) // 2
                        cv2.putText(imageBackground, str(studentInfo['name']), (808 + offset, 445), 
                                    cv2.FONT_ITALIC, 1, (50, 50, 50), 3)
                        
                        imageBackground[175:175 + 216, 909:909 + 216] = imgStudent



                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imageBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0




    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Recogintion", imageBackground)
    # cv2.waitKey(1)
    if cv2.waitKey(20) == ord('n'):
        print("Video processing interrupted by user.")
        break


cv2.destroyAllWindows()