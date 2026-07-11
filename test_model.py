import cv2
from ultralytics import YOLO

model = YOLO("best.pt")  # make sure path is correct

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # Run YOLO directly on full frame (no crop)
    results = model(frame, conf=0.15, verbose=False)[0]
    annotated = results.plot()

    # Show count
    count = len(results.boxes)
    cv2.putText(annotated, f"Detections: {count}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    cv2.imshow("YOLO Direct Test", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()