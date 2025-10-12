# vision_engine.py
import cv2
from deepface import DeepFace


def vision_loop():
    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("[ERROR] Could not access webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(
                frame, actions=["emotion"], enforce_detection=False
            )
            dominant_emotion = result[0]["dominant_emotion"]
            cv2.putText(
                frame,
                f"Emotion: {dominant_emotion}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        except Exception as e:
            cv2.putText(
                frame,
                "Emotion: Unknown",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )

        cv2.imshow("Everett Cam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    vision_loop()

