import cv2
import mediapipe as mp
from angle_utils import calculate_angle

mpPose = mp.solutions.pose

class PoseEstimator:
    def __init__(self, elbowDownThresh=70, elbowUpThresh=150, hipMin=160, hipMax=180):
        self.pose = mpPose.Pose(static_image_mode = False,
                                 min_detection_confidence = 0.5,
                                 min_tracking_confidence = 0.5)
        self.elbowDown = False
        self.elbowUp = False
        self.elbowOk = False
        self.count = 0

        self.elbowDownThresh = elbowDownThresh
        self.elbowUpThresh = elbowUpThresh
        self.hipMin = hipMin
        self.hipMax = hipMax

    def analyze_pose(self, image):
        # Verilen goruntude kol ve bel-kalca acisini analiz eder, form durumunu dondurur.
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(img_rgb)

        if results.pose_landmarks:
            h, w = image.shape[:2]
            lm = results.pose_landmarks.landmark

            # Dirsek Acisi
            shoulder = [lm[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                        lm[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
            elbow = [lm[mpPose.PoseLandmark.RIGHT_ELBOW.value].x * w,
                     lm[mpPose.PoseLandmark.RIGHT_ELBOW.value].y * h]
            wrist = [lm[mpPose.PoseLandmark.RIGHT_WRIST.value].x * w,
                     lm[mpPose.PoseLandmark.RIGHT_WRIST.value].y * h]

            elbowAngle = calculate_angle(shoulder, elbow, wrist)

            # Kalca Acisi
            shoulder = [lm[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                        lm[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
            hip = [lm[mpPose.PoseLandmark.RIGHT_HIP.value].x * w,
                   lm[mpPose.PoseLandmark.RIGHT_HIP.value].y * h]
            knee = [lm[mpPose.PoseLandmark.RIGHT_KNEE.value].x * w,
                    lm[mpPose.PoseLandmark.RIGHT_KNEE.value].y * h]

            hipAngle = calculate_angle(shoulder, hip, knee)

            # Form Kontrol
            # Asagida olma durumu
            if elbowAngle < self.elbowDownThresh:
                self.elbowDown = True
            # 70 dereceden kücük bir aci sonrası hemen kalkip 150 dereceyi gecmek.
            elif elbowAngle > self.elbowUpThresh and self.elbowDown:
                self.elbowUp = True
            # Iki durum da saglandigi zaman sayimiz bir artiyor. Sonrasinda diger tekrarlar icin Down-Up sifirlaniyor.
            if self.elbowDown and self.elbowUp:
                self.elbowOk = True
                self.elbowDown = False
                self.elbowUp = False
            else:
                self.elbowOk = False

            # Vucut diklik durumu
            self.hipOk = self.hipMin < hipAngle < self.hipMax

            if self.elbowOk and self.hipOk:
                formStatus = "Correct Form"
                formColor = (0, 255, 0)
                self.count += 1
            elif not self.elbowOk and self.hipOk:
                formStatus = "In Progress.."
                formColor = (0, 255, 0)
                if self.count == 0:
                    formColor = (0, 0, 255)
                    formStatus = "Fix Elbow"
            elif not self.hipOk and self.elbowOk:
                formStatus = "Fix hip"
                formColor = (255, 255, 0)
            else:
                formStatus = "Incorrect Form"
                formColor = (0, 0, 255)

            return {
                "formStatus": formStatus,
                "formColor": formColor,
                "elbowAngle": elbowAngle,
                "hipAngle": hipAngle,
                "count": self.count
            }

        else:
            return {
                "formStatus": "No Pose can be found",
                "formColor": (255,255,255),
                "elbowAngle": None,
                "hipAngle": None,
                "count": None
            }
