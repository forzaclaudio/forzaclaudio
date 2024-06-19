import logging
import pickle
import sys

import cv2
import face_recognition
import numpy as np

from nano_vision import Overlays, read_face_data

logger = logging.getLogger(__name__)

def face_detector(trained_datapath):
    """Detects the faces stored in the trained data file."""
    overlays = Overlays()
    Names, Encodings = read_face_data(trained_datapath)
    scale = 0.5
    inputImage = face_recognition.load_image_file(sys.argv[1])
    inputImage = cv2.resize(inputImage, (0, 0), fx=scale, fy=scale)
    facePositions = face_recognition.face_locations(inputImage)
    allEncodings = face_recognition.face_encodings(inputImage,facePositions)
    inputImage = cv2.cvtColor(inputImage,cv2.COLOR_RGB2BGR)
    blk = np.zeros(inputImage.shape, np.uint8)
    people = []
    count = 0
    for (top,right,bottom,left), face_encoding in zip(facePositions,allEncodings):
        name = 'Unknown Person'
        matches = face_recognition.compare_faces(Encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            color = (0,255,0)
            name = Names[first_match_index]
            people.append(name)
        else:
            color = (0,0,255)
        count += 1
        overlays.roi(inputImage, top, right, bottom, left, color, text=name)
        inputImage = overlays.blur(inputImage, left, top, right, bottom)
        overlays.mask(blk, top, right, bottom, left, color)
    logger.info('{} People Detected. Recognized people: {}'.format(count,people))
    out = overlays.blend(inputImage, blk)
    overlays.total_faces(out, count)
    cv2.imshow('Face Detector', out)
    cv2.imwrite('face_detector.jpg',out)
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    face_detector("train.pkl")
