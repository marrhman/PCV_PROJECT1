import cv2, numpy as np

video_cam = cv2.VideoCapture(0)
while True:
    safe_status, frame = video_cam.read()
    if not safe_status:
        print("Your Camera is Error")
        break

    # Overlay informasi ke frame
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    font_color = (15, 2, 6)
    thickness = 2
    cv2.putText(
        frame,
        f"Resolution: {width} x {height}",
        (20, 30),
        font, scale, font_color, thickness
    )
    cv2.putText(
        frame,
        f"Channels: {channels}",
        (20, 60),
        font, scale, font_color, thickness
    )

    # BGR → HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Memisahkan channel HSV
    h, s, v = cv2.split(hsv)

    cv2.imshow("Camera Test - BGR", frame)
    cv2.imshow("Camera Test - HSV", hsv)

    quit_key = cv2.waitKey(1) & 0xFF
    if quit_key == ord("q"):
        break

#frame information
print("Shape:", frame.shape)
print("Resolution:", width, "x", height)
print("Channels:", channels)

video_cam.release()
cv2.destroyAllWindows()