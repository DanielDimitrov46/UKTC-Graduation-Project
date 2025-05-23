# import face_recognition
# import os,sys
# # os.environ['QT_QPA_PLATFORM'] = 'xcb'
# import cv2
# import numpy as np
# import math

# def face_confidence(face_distance, face_match_threshold=0.6):
#     range = (1.0 - face_match_threshold)
#     linear_val = (1.0 - face_distance) / (range * 2.0)

#     if face_distance > face_match_threshold:
#         return str(round(linear_val*100, 2))+ '%'
#     else:
#         value = (linear_val+((1.0-linear_val)*math.pow((linear_val-0.5)*2, 2.0)))*100
#         return str(round(value, 2)) + '%'
    
# class FaceRecognition:
#     face_locations = []
#     face_encodings = []
#     face_names = []
#     known_face_encodings = []
#     known_face_names = []
#     process_current_frame = True
#     match = False

#     def __init__(self):
#         self.encode_faces()
#     def encode_faces(self):
#         for image in os.listdir('/home/daniel/Pneaumatic control Tessis/UKTC-Graduation-Project/sensors/faces'):
#             face_image = face_recognition.load_image_file('/home/daniel/Pneaumatic control Tessis/UKTC-Graduation-Project/sensors/faces/' + image)
#             face_encoding = face_recognition.face_encodings(face_image)[0]

#             self.known_face_encodings.append(face_encoding)
#             self.known_face_names.append(image)
#         print(self.known_face_names)
        
#     def run_recognition(self):
#         video_capture = cv2.VideoCapture(0)
#         if not video_capture.isOpened():
#             return False

#         ret, frame = video_capture.read()
#         if not ret:
#             return False

#         small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#         rgb_small_frame = small_frame[:, :, ::-1]

#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)


#         for face_encoding in face_encodings:
#             matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#             face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)

#             if matches[best_match_index]:
#                 confidence = face_confidence(face_distances[best_match_index])
#                 if float(confidence.strip('%')) >= 75:
#                     video_capture.release()
#                     return True

#         video_capture.release()
#         return False

#     # def run_recognition(self):
#     #     video_capture = cv2.VideoCapture(0)

#     #     if not video_capture.isOpened():
#     #         sys.exit("Video source not found ...")

#     #     while True:
#     #         ret, frame = video_capture.read()

#     #         if self.process_current_frame:
#     #             small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     #             rgb_small_frame = np.array(small_frame, dtype=np.uint8)

#     #             self.face_locations = face_recognition.face_locations(rgb_small_frame)
#     #             print(self.face_locations)
#     #             if self.face_locations:
#     #                 self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
#     #             else:
#     #                 self.face_encodings = []

#     #             self.face_names = []
#     #             for face_encoding in self.face_encodings:
#     #                 matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
#     #                 name = "Unknown"
#     #                 confidence = 'Unklnows'

#     #                 face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
#     #                 best_match_index = np.argmin(face_distances)

#     #                 if matches[best_match_index]:
#     #                     name = self.known_face_names[best_match_index]
#     #                     confidence = face_confidence(face_distances[best_match_index])
                    
#     #                 self.face_names.append(f'{name} ({confidence})')
#     #                 if float(self.face_names[0].split(' ')[1].strip('('')%')) >=70:
#     #                     return True
#     #                     # print('Match')
#     #                     # exit()
#     #                 else:
#     #                     print('No match')
#     #                 # print(self.face_names[0].split(' ')[1].strip('('')%'))
#     #                 # print(self.face_names[0].split(' ')[1])
#     #         self.process_current_frame = not self.process_current_frame

#     #         for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
#     #             top *= 4
#     #             right *= 4
#     #             bottom *= 4
#     #             left *= 4

#     #             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#     #             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), -1)
#     #             font = cv2.FONT_HERSHEY_DUPLEX
#     #             cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

#     #         cv2.imshow('Face Recognition', frame)

#     #         if cv2.waitKey(1) & 0xFF == ord('q'):
#     #             break

#     #     video_capture.release()
#     #     cv2.destroyAllWindows()
#     #     return False

# # if __name__ == '__main__':
# #     fr = FaceRecognition()
# #     fr.run_recognition()
import face_recognition
import os
import cv2
import numpy as np
import math

def face_confidence(face_distance, face_match_threshold=0.6):
    range_val = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range_val * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 2.0))) * 100
        return str(round(value, 2)) + '%'

class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.encode_faces()

    def encode_faces(self):
        faces_path = '/home/daniel/Pneaumatic control Tessis/UKTC-Graduation-Project/sensors/faces'
        for filename in os.listdir(faces_path):
            file_path = os.path.join(faces_path, filename)
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue

            image = face_recognition.load_image_file(file_path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                self.known_face_encodings.append(encodings[0])
                self.known_face_names.append(os.path.splitext(filename)[0])
            else:
                print(f"Warning: No face found in {filename}, skipping.")

        print("Loaded known faces:", self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("Camera not found.")
            return False

        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            video_capture.release()
            return False

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Get face locations
        face_locations = face_recognition.face_locations(rgb_small_frame)

    # Check if any face is found before encoding
        if not face_locations:
            print("No face detected.")
            video_capture.release()
            return False

        try:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        except Exception as e:
            print(f"Encoding error: {e}")
            video_capture.release()
            return False

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                confidence = face_confidence(face_distances[best_match_index])
                print(f"Match with {self.known_face_names[best_match_index]} ({confidence})")
                if float(confidence.strip('%')) >= 75:
                    video_capture.release()
                    return True

        video_capture.release()
        return False
