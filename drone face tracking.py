from djitellopy import Tello
import cv2
import time
from ultralytics import YOLO

model = YOLO(r'C:\Users\Bibizhan\Desktop\myface\my_model\my_model.pt')

tello = Tello()
tello.connect(wait_for_state=False)
tello.streamon()
time.sleep(2)
tello.takeoff()

while True:
    try:
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (640, 480))

        results = model.predict(source=frame, conf=0.5, verbose=False)
        result = results[0]
        annotated = result.plot()

        if len(result.boxes) > 0:
            box = result.boxes[0].xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = box
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            box_width = x2 - x1

            dx = x_center - 320
            dy = y_center - 240

            if dx < -50:
                tello.rotate_counter_clockwise(10)
            elif dx > 50:
                tello.rotate_clockwise(10)

            if dy < -50:
                tello.move_up(20)
            elif dy > 50:
                tello.move_down(20)

            if box_width < 100:
                tello.move_forward(20)
            elif box_width > 150:
                tello.move_back(20)

        cv2.imshow("Face Tracking", annotated)

    except Exception as e:
        print("error", e)
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


tello.land()
tello.streamoff()
cv2.destroyAllWindows()
