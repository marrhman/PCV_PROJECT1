import cv2, numpy as np

video_cam = cv2.VideoCapture(0)

cv2.namedWindow("HSV Threshold Settings")
cv2.createTrackbar("H Min", "HSV Threshold Settings", 7, 179, lambda x: None)
cv2.createTrackbar("H Max", "HSV Threshold Settings", 22, 179, lambda x: None)
cv2.createTrackbar("S Min", "HSV Threshold Settings", 45, 255, lambda x: None)
cv2.createTrackbar("S Max", "HSV Threshold Settings", 160, 255, lambda x: None)
cv2.createTrackbar("V Min", "HSV Threshold Settings", 80, 255, lambda x: None)
cv2.createTrackbar("V Max", "HSV Threshold Settings", 220, 255, lambda x: None)

while True:
    safe_status, frame = video_cam.read()
    if not safe_status:
        print("Your Camera is Error")
        break
    fframe = cv2.flip(frame, 1)

    # Overlay informasi ke frame
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    font_color = (15, 2, 6)
    thickness = 2
    cv2.putText(
        fframe,
        f"Resolution: {width} x {height}",
        (20, 30),
        font, scale, font_color, thickness
    )
    cv2.putText(
        fframe,
        f"Channels: {channels}",
        (20, 60),
        font, scale, font_color, thickness
    )

    # BGR ke HSV agar mudah atur cahaya
    hsv = cv2.cvtColor(fframe, cv2.COLOR_BGR2HSV)
    # Memisahkan channel HSV
    h, s, v = cv2.split(hsv)
    #thresholding from masking
    lower_palm = np.array([cv2.getTrackbarPos("H Min", "HSV Threshold Settings"),
                           cv2.getTrackbarPos("S Min", "HSV Threshold Settings"),
                           cv2.getTrackbarPos("V Min", "HSV Threshold Settings")])
    upper_palm = np.array([cv2.getTrackbarPos("H Max", "HSV Threshold Settings"),
                           cv2.getTrackbarPos("S Max", "HSV Threshold Settings"),
                           cv2.getTrackbarPos("V Max", "HSV Threshold Settings")])
    #lower_back = np.array([0, 0, 0]) #rencana ada threshold senditi buat punggung tangan
    #upper_back = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_palm, upper_palm)
    #mask2 = cv2.inRange(hsv, lower_back, upper_back)

    cv2.imshow("Camera Test - BGR", fframe)
    cv2.imshow("Camera Test - Mask", mask)

    quit_key = cv2.waitKey(1) & 0xFF
    if quit_key == ord("q"):
        break

#frame information
print("Shape:", frame.shape)
print("Resolution:", width, "x", height)
print("Channels:", channels)

video_cam.release()
cv2.destroyAllWindows()