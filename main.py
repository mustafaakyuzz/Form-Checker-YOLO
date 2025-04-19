import cv2
from scipy.optimize import bracket
from ultralytics import YOLO
from pose_estimator import PoseEstimator
import warnings
warnings.filterwarnings('ignore')

modelPath = 'best.pt'
videoPath = 'myVideo1.mp4'

# Modeli yukle
model = YOLO(modelPath)
pose_estimator = PoseEstimator()

# Input videoyu oynat
cap = cv2.VideoCapture(videoPath)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # YOLO modelini kullanarak sinav tespiti
    results = model.predict(image, conf = 0.70, verbose = False)

    for r in results:
        for box in r.boxes:
            clsId = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[clsId]

            if label == 'pushup':
                # Kutu cizimi
                cv2.rectangle(image, (x1,y1), (x2,y2), (255, 0, 0), 2)
                cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)

                # Poz analizini Yaz
                roi = image[y1:y2, x1:x2]
                analysis = pose_estimator.analyze_pose(roi)

                # Form durumu yazimi
                status = analysis["formStatus"]
                color = analysis["formColor"]

                cv2.putText(image, f"{status}", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

                # Acilari yazdir
                if analysis['elbowAngle']:
                    cv2.putText(image, f"Elbow: {int(analysis['elbowAngle'])}", (x1, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                if analysis['hipAngle']:
                    cv2.putText(image, f"Hip: {int(analysis['hipAngle'])}", (x1, y1 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Dogru Yapilmis Formun Tekrar Sayisini Yazdir
                if analysis['elbowAngle']:
                    cv2.putText(image, f"Count: {int(analysis['count'])}", (x1, y1 + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Form Control", image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()