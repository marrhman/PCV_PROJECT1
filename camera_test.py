import cv2, numpy as np

video_cam = cv2.VideoCapture(0)

cv2.namedWindow("Threshold Configuration")
cv2.createTrackbar("H Min", "Threshold Configuration", 7, 179, lambda x: None)
cv2.createTrackbar("H Max", "Threshold Configuration", 22, 179, lambda x: None)
cv2.createTrackbar("S Min", "Threshold Configuration", 45, 255, lambda x: None)
cv2.createTrackbar("S Max", "Threshold Configuration", 160, 255, lambda x: None)
cv2.createTrackbar("V Min", "Threshold Configuration", 80, 255, lambda x: None)
cv2.createTrackbar("V Max", "Threshold Configuration", 220, 255, lambda x: None)

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
    #thresholding for masking
    lower_palm = np.array([cv2.getTrackbarPos("H Min", "Threshold Configuration"),
                           cv2.getTrackbarPos("S Min", "Threshold Configuration"),
                           cv2.getTrackbarPos("V Min", "Threshold Configuration")])
    upper_palm = np.array([cv2.getTrackbarPos("H Max", "Threshold Configuration"),
                           cv2.getTrackbarPos("S Max", "Threshold Configuration"),
                           cv2.getTrackbarPos("V Max", "Threshold Configuration")])
    #lower_back = np.array([0, 0, 0]) #rencana ada threshold senditi buat punggung tangan
    #upper_back = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_palm, upper_palm)
    #mask2 = cv2.inRange(hsv, lower_back, upper_back)
    mask_filtered = cv2.medianBlur(mask, 11)
    kernel = np.ones((11,11), np.uint8)
    mask_closing = cv2.morphologyEx(mask_filtered,cv2.MORPH_CLOSE,kernel)
    mask_closing = cv2.morphologyEx(mask_closing,cv2.MORPH_OPEN,kernel)

    #bagin ini blom
    contours, hierarchy = cv2.findContours(mask_closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(fframe,(x, y),(x + w, y + h),(0, 255, 0),2)

    cv2.imshow("Camera Test - BGR", fframe)
    cv2.imshow("Camera Test - Mask", mask_closing)

    quit_key = cv2.waitKey(1) & 0xFF
    if quit_key == ord("q"):
        break

#frame information
print("Shape:", frame.shape)
print("Resolution:", width, "x", height)
print("Channels:", channels)

video_cam.release()
cv2.destroyAllWindows()