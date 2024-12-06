import cv2
import mediapipe as mp
import numpy as np
import math
from pynput import keyboard
import time

def draw_landmark(image, landmark, radius, color, thickness=-1):
    x = int(landmark.x * image.shape[1])
    y = int(landmark.y * image.shape[0])
    cv2.circle(image, (x, y), radius, color, thickness)

class Processor:
    def __init__(self):
        self.keyboard = keyboard.Controller()
        self.state = "none"

    def processor(self, image, landmarks):
        try:
            fore_thumb = math.hypot(landmarks[4].x * image.shape[1] - landmarks[8].x * image.shape[1], landmarks[4].y * image.shape[0] - landmarks[8].y * image.shape[0])
            fore_middle = math.hypot(landmarks[8].x * image.shape[1] - landmarks[12].x * image.shape[1], landmarks[8].y * image.shape[0] - landmarks[12].y * image.shape[0])
            thumb_middle = math.hypot(landmarks[12].x * image.shape[1] - landmarks[4].x * image.shape[1], landmarks[12].y * image.shape[0] - landmarks[4].y * image.shape[0])
            thumb_ring = self._length(landmarks, image, 4, 16)
            thumb_little = self._length(landmarks, image, 4, 20)
            little_ring = self._length(landmarks, image, 20, 16)

            if fore_thumb < 130 and fore_middle < 130 and thumb_middle < 130:
                print(f"Play/Pause")
                self.pause()
                time.sleep(0.3)
            elif fore_thumb < 130:
                print(f"Previous")
                self.previous()
                time.sleep(0.3)
            elif thumb_middle < 130:
                print(f"Next")
                self.next()
                time.sleep(0.3)
            elif thumb_little < 130 and thumb_ring < 130 and little_ring < 130:
                print(f"Volume Mute")
                self.mute()
                time.sleep(0.3)
            elif thumb_ring < 130:
                print(f"Volume Down")
                self.volume_down()
                time.sleep(0.3)
            elif thumb_little < 130:
                print(f"Volume Up")
                self.volume_up()
                time.sleep(0.3)
            else:
                self.state = "none"
            print(f"State: {self.state}")
        except Exception as e:
            print(e)
    
    def _length(self, landmarks, image, n1, n2):
        return math.hypot(landmarks[n1].x * image.shape[1] - landmarks[n2].x * image.shape[1], landmarks[n1].y * image.shape[0] - landmarks[n2].y * image.shape[0])
    
    def previous(self):
        if self.state == "previous":
            return
        self.keyboard.press(keyboard.Key.media_previous)
        self.keyboard.release(keyboard.Key.media_previous)
        self.state = "previous"

    def next(self):
        if self.state == "next":
            return
        self.keyboard.press(keyboard.Key.media_next)
        self.keyboard.release(keyboard.Key.media_next)
        self.state = "next"

    def play(self):
        if self.state == "play" or self.state == "pause":
            return
        self.keyboard.press(keyboard.Key.media_play_pause)
        self.keyboard.release(keyboard.Key.media_play_pause)
        self.state = "play"

    def pause(self):
        if self.state == "pause" or self.state == "play":
            return
        self.keyboard.press(keyboard.Key.media_play_pause)
        self.keyboard.release(keyboard.Key.media_play_pause)
        self.state = "pause"
            
    def volume_down(self):
        if self.state == "volume_down":
            return
        self.keyboard.press(keyboard.Key.media_volume_down)
        self.keyboard.release(keyboard.Key.media_volume_down)
        self.state = "volume_down"

    def volume_up(self):
        if self.state == "volume_up":
            return
        self.keyboard.press(keyboard.Key.media_volume_up)
        self.keyboard.release(keyboard.Key.media_volume_up)
        self.state = "volume_up"

    def mute(self):
        if self.state == "mute":
            return
        self.keyboard.press(keyboard.Key.media_volume_mute)
        self.keyboard.release(keyboard.Key.media_volume_mute)
        self.state = "mute"

#if len(sys.argv) == 1:
#    print("No files to open")
#    sys.exit(1)
#folder = sys.argv[1]
#tracks = []
#if os.path.isdir(folder):
#    for file in os.listdir(folder):
#        if file.endswith(".mp3"):
#            tracks.append(os.path.join(folder, file))
            
#создаем детектор

tracks = ["/Users/jonhef/Downloads/radiohead-creep.mp3"]
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
processor = Processor()
while(cap.isOpened()):
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
        break
    flipped = np.fliplr(frame)
    # переводим его в формат RGB для распознавания
    flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    # Распознаем
    results = handsDetector.process(flippedRGB)
    # Рисуем распознанное, если распозналось
    if results.multi_hand_landmarks is not None:
        landmarks = results.multi_hand_landmarks[0].landmark
        for i in landmarks:
            draw_landmark(flippedRGB, i, 4, (0, 255, 0))
        processor.processor(flippedRGB, landmarks)
    # переводим в BGR и показываем результат
    res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
    #cv2.imshow("Hands", res_image)

# освобождаем ресурсы
handsDetector.close()
