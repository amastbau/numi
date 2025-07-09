import cv2
import mediapipe as mp
import pyautogui
import numpy as np

def main():
    """
    Main function to run the eye tracking mouse control application.
    """
    # 1. Initialization
    screen_width, screen_height = pyautogui.size()
    print(f"Screen dimensions: {screen_width}x{screen_height}")

    # Initialize MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Initialize OpenCV Video Capture
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Cannot open webcam.")
            return
    except Exception as e:
        print(f"Error initializing webcam: {e}")
        return

    # Smoothing parameters
    smooth_factor = 5 
    prev_x, prev_y = 0, 0
    
    print("\nEye tracking started. Look around to move the mouse.")
    print("Press 'q' to quit the application.")

    # 2. Main Application Loop
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        image.flags.setflags(write=False)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        image.flags.setflags(write=True)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_corner = face_landmarks.landmark[362]
                right_corner = face_landmarks.landmark[263]
                pupil_center = face_landmarks.landmark[468]

                eye_width = right_corner.x - left_corner.x
                if eye_width != 0:
                    horizontal_ratio = (pupil_center.x - left_corner.x) / eye_width
                    screen_x = screen_width * (1 - horizontal_ratio)
                    
                    eye_center_y = (face_landmarks.landmark[386].y + face_landmarks.landmark[374].y) / 2
                    vertical_ratio = (pupil_center.y - eye_center_y) * 15
                    screen_y = screen_height / 2 + vertical_ratio * screen_height

                    current_x = prev_x + (screen_x - prev_x) / smooth_factor
                    current_y = prev_y + (screen_y - prev_y) / smooth_factor
                    
                    pyautogui.moveTo(current_x, current_y)
                    
                    prev_x, prev_y = current_x, current_y

        cv2.imshow('Eye Tracking Mouse Control - Press Q to Quit', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # 3. Cleanup
    face_mesh.close()
    cap.release()
    cv2.destroyAllWindows()
    print("\nApplication closed.")

if __name__ == '__main__':
    pyautogui.FAILSAFE = False
    main()
