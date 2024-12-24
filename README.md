# school-project

 Computer vision project for controling media(next and previous track, play and pause, volume up and down and mute)

## How to use
- Start the program using python3
- Accept access to the camera
- Use your fingers to control media

| previous | next | play | pause | volume down | volume up | mute |
| -------- | ---- | ---- | ----- | ----------- | --------- | ---- |
| interlock index and thumb fingers | interlock middle and thumb fingers | interlock index, thumb and middle fingers | the same as for play | interlock ring and thumb fingers | interlock little and thumb fingers | interlock ring, thumb and little fingers |

## main.py
- `draw_landmark(image: numpy.array, landmark: landmark, radius: int, color: tuple(int), thickness: int)` – it draws landmark(uses `cv2.circle` for drawing(`image`, `radius`, `color`, `thickness` the same)
### class Processor
- `processor(self, image:numpy.array, landmarks: landmarks)` - the main function to process hands and control media
- `_length(self, landmarks, image, n1, n2` - private function to measure length from one finger to another(`n1` and `n2` are numbers of fingers(from mediapipe's documentation))
- `previous(self)` - jump to the previous track
- `next(self)` - jump to the next track
- `play(self)` - play track
- `pause(self)` - pause track
- `volume_down(self)` - makes volume down to the point(it depends on the system you use)
- `volume_up(self)` - makes volume up to the point(it on the system you use)
- `mute(self)` - mute the volume
