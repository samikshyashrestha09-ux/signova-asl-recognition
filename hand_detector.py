import cv2
from ultralytics import YOLO

class HandDetector:
    def __init__(self, model_path="best.pt"):
        self.model = YOLO(model_path)
        self.last_label = ""
        self.last_confidence = 0.0

    def process(self, frame):
        results = self.model(frame, conf=0.20, verbose=False)[0]

        if len(results.boxes) > 0:
            # Pick the highest confidence detection
            best_box = max(results.boxes, key=lambda b: float(b.conf[0]))
            confidence = float(best_box.conf[0])
            class_id = int(best_box.cls[0])
            label = self.model.names[class_id]

            self.last_label = label
            self.last_confidence = confidence

            # Draw box and label
            x1, y1, x2, y2 = map(int, best_box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 0), 2)
        else:
            self.last_label = ""
            self.last_confidence = 0.0
            cv2.putText(frame, "No sign detected", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (0, 0, 255), 2)

        return frame