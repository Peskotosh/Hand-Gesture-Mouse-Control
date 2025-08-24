import cv2
import mediapipe
import pyautogui

capture_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #set camera resolution
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

x1 = y1 = x2 = y2 = 0

while True:
    ret, image = camera.read()

    image_height, image_width, ret = image.shape

    image = cv2.flip(image,1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    output_hands = capture_hands.process(rgb_image)

    all_hands = output_hands.multi_hand_landmarks

    if all_hands:

        for hand in all_hands:
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark

            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                if id == 12:  # Using middle index as a pointer
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, (0, 255, 0))
                    pyautogui.moveTo(mouse_x, mouse_y)


                if id == 8: # Index finger
                    cv2.circle(image, (x, y), 10, (255, 0, 0))
                    x1 = x
                    y1 = y

                if id == 4: # Thumb
                    x2 = x
                    y2 = y
                    cv2.circle(image, (x, y), 10, (255, 0, 0))

        distance = y2 - y1 # calculating distance
        # print(distance)

        if distance < 25:
            pyautogui.click()

    cv2.imshow("Mouse",image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()