import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import w2d

name_to_no = {}
no_to_name = {}
model = None

def classify_image(image_base64_data, file_path=None):
    with open('./artifacts/classification.pkl', 'rb') as f:
        model = joblib.load(f)
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)

    result = []
    for img in imgs:
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32 * 32 * 3, 1), scalled_img_har.reshape(32 * 32, 1)))

        len_image_array = 32*32*3 + 32*32   

        final = combined_img.reshape(1,len_image_array).astype(float)
        result.append({
            'class': getname(model.predict(final)[0]),
            'class_probability': np.around(model.predict_proba(final)*100,2).tolist()[0],
            'class_dictionary': name_to_no
        })

    return result

def getname(class_num):
    return no_to_name[class_num]

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global name_to_no
    global no_to_name
    global model
    name_to_no = {'bruce': 0, 'clint': 1, 'natasha': 2, 'steve': 3, 'thor': 4, 'tony': 5}
    no_to_name = {0:'bruce', 1:'clint', 2:'natasha', 3:'steve', 4:'thor', 5:'tony'}


def get_cv2_image_from_base64_string(b64str):
    '''
    https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    :param uri:
    :return:
    '''
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base64_string(image_base64_data)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if len(eyes) >= 2:
                cropped_faces.append(roi_color)
    return cropped_faces

if __name__ == '__main__':
    print(classify_image(None,""))