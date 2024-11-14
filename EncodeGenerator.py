import pickle
import cv2
import os
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# ... (Firebase initialization code)

folderPath = 'images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

for imgPath in pathList:
    img = cv2.imread(os.path.join(folderPath, imgPath))  # Load image

    # Ensure RGB format before face encoding
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    studentIds.append(os.path.splitext(imgPath)[0])

    # ... (Firebase upload code)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started ....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print(encodeListKnown)
print("Encoding Complete.")

file = open("EncodFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File saved.")