from ultralytics import YOLO
import cv2

model = YOLO("C:/Users/rabin/OneDrive/Desktop/sign_language_project/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    results = model(frame, conf=0.5, verbose=True)[0]
    annotated = results.plot()

    cv2.imshow("Test Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()