import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

def scan_products():
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=4, min_detection_confidence=0.9)
    mpDraw = mp.solutions.drawing_utils

    # pdict = {}


    # Load the gesture recognizer model
    model = load_model('mp_hand_gesture')

    # Load class names
    f = open('gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()

    thumbs_up = 0
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read each frame from the webcam
        _, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        # print(result)

        className = ''

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]
                print(className)
                if className == 'thumbs up':
                    thumbs_up += 1
                    if thumbs_up >= 5:
                        # print("Scanned")
                        cv2.destroyAllWindows()
                        cap.release()
                        return 1


        # Show the final output
        cv2.imshow("Output", frame)

        if cv2.waitKey(1) == ord('q'):
            # release the webcam and destroy all active windows
            cv2.destroyAllWindows()
            cap.release()
            return []

if "__main__" == __name__:
    prddict = scan_products()
    if not prddict:
        print("No products scanned")
    else:
        print("Products scanned: ", prddict)
