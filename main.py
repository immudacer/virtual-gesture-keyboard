from time import sleep
import pyautogui
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Initialize detector
detector = HandDetector(detectionCon=0.7, maxHands=1)
cap = cv2.VideoCapture(0)
cap.set(3, 1080)  # Width
cap.set(4, 720)  # Height


class Button():
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.size = size
        self.text = text


def designKeys(img, buttonList):
    overlay = img.copy()
    for button in buttonList:
        x, y = button.pos
        w, h = button.size

        # Rounded rectangle background
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (40, 40, 40), -1, cv2.LINE_AA)

        # Draw gradient effect
        gradient = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(h):
            c = 60 + int(120 * (i / h))
            gradient[i, :, :] = (c, c, c)
        img[y:y + h, x:x + w] = cv2.addWeighted(img[y:y + h, x:x + w], 0.5, gradient, 0.5, 0)

        # Key label
        cv2.putText(img, button.text, (x + 15, y + int(h * 0.7)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 230, 255), 2, cv2.LINE_AA)

        # Soft shadow
        cv2.rectangle(img, (x + 3, y + 3), (x + w + 3, y + h + 3), (0, 0, 0), 2, cv2.LINE_AA)

    return img


# Keyboard layouts
lower_case = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "@"]
]

upper_case = [
    ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
    ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "="]
]

symbols = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"],
    ["-", "+", "=", "{", "}", "[", "]", "\\", "|", ";"],
    ["_", "/", ":", ";", "\"", "'", "~", "`", ":)", ":("]
]

# Initial state
current_layout = lower_case
shift_on = False
symbols_on = False
buttonList = []


def create_buttons(layout, mode="lower"):
    buttons = []
    for i in range(len(layout)):
        for j, key in enumerate(layout[i]):
            x_pos = 75 * j + 275
            y_pos = 65 * i + 50
            buttons.append(Button([x_pos, y_pos], key))

    special_buttons = []

    # Bottom row buttons with extra spacing
    base_y = 50 * 5 + 65
    special_buttons.append(Button([80 * 3 + 275, base_y], "SPACE", [290, 50]))
    special_buttons.append(Button([70 * 9 + 275, base_y], "<x", [90, 50]))

    if mode == "lower":
        special_buttons.append(Button([35 * 1 + 275, base_y], "$/", [90, 50]))
        special_buttons.append(Button([70 * 2 + 275, base_y], "aA", [90, 50]))
    elif mode == "upper":
        special_buttons.append(Button([35 * 1 + 275, base_y], "$/", [90, 50]))
        special_buttons.append(Button([70 * 2 + 275, base_y], "Aa", [90, 50]))
    elif mode == "symbols":
        special_buttons.append(Button([35 * 1 + 275, base_y], "ab", [90, 50]))

    return buttons + special_buttons


buttonList = create_buttons(current_layout, "lower")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)

    # Keep camera video visible but darken background (excluding keyboard area)
    overlay_bg = img.copy()
    dark_layer = np.zeros_like(img, dtype=np.uint8)
    dark_layer[:] = (0, 0, 0)
    img = cv2.addWeighted(dark_layer, 0.5, img, 0.5, 0)

    hands, img = detector.findHands(img)
    img = designKeys(img, buttonList)

    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if len(lmList) > 8:
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), 2, cv2.LINE_AA)
                    cv2.putText(img, button.text, (x + 15, y + int(h * 0.7)), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 0)

                    fingers = detector.fingersUp(hand1)
                    if fingers[1] and fingers[2]:
                        l, _, _ = detector.findDistance(lmList[8], lmList[4], img)

                        if l < 50:
                            if button.text == "aA":
                                shift_on = True
                                symbols_on = False
                                current_layout = upper_case
                                buttonList = create_buttons(current_layout, "upper")

                            elif button.text == "Aa":
                                shift_on = False
                                symbols_on = False
                                current_layout = lower_case
                                buttonList = create_buttons(current_layout, "lower")

                            elif button.text == "$/":
                                symbols_on = True
                                current_layout = symbols
                                buttonList = create_buttons(current_layout, "symbols")

                            elif button.text == "ab":
                                symbols_on = False
                                shift_on = False
                                current_layout = lower_case
                                buttonList = create_buttons(current_layout, "lower")

                            elif button.text == "<x":
                                pyautogui.press('backspace')

                            elif button.text == "SPACE":
                                pyautogui.press('space')

                            else:
                                if button.text.isalpha() and shift_on and not symbols_on:
                                    with pyautogui.hold('shift'):
                                        pyautogui.press(button.text.lower())
                                else:
                                    if button.text == ":":
                                        with pyautogui.hold('shift'):
                                            pyautogui.press(';')
                                    elif button.text == "\"":
                                        with pyautogui.hold('shift'):
                                            pyautogui.press('\'')
                                    elif button.text == "?":
                                        with pyautogui.hold('shift'):
                                            pyautogui.press('/')
                                    else:
                                        pyautogui.press(button.text)

                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 200, 0), 2, cv2.LINE_AA)
                            sleep(0.1)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
