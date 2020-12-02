import numpy as np
import face_recognition as fr
import cv2


def facePass(fp):
    video_capture = cv2.VideoCapture(0)

    user_image = fr.load_image_file("enter you file name, .jpg")
    user_face_encoding = fr.face_encodings(user_image)[0]

    known_face_encondings = [user_face_encoding]
    known_face_names = ["enter your name"]

    detect = True

    while detect: 
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = fr.compare_faces(known_face_encondings, face_encoding)

            name = "Unknown"

            face_distances = fr.face_distance(known_face_encondings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                fp = "enter your name"
                detect = False
            else:
                fp = "Unknown"
                detect = False
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Webcam_facerecognition', frame)
        k = cv2.waitKey(30) & 0xff

        if k==27:
            fp = "Unknown"
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return fp