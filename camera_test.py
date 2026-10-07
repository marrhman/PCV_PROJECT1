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
    frame = cv2.flip(frame, 1)

    # BGR ke HSV agar mudah atur cahaya
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #thresholding for masking
    lower_palm = np.array([cv2.getTrackbarPos("H Min", "Threshold Configuration"),
                           cv2.getTrackbarPos("S Min", "Threshold Configuration"),
                           cv2.getTrackbarPos("V Min", "Threshold Configuration")])
    upper_palm = np.array([cv2.getTrackbarPos("H Max", "Threshold Configuration"),
                           cv2.getTrackbarPos("S Max", "Threshold Configuration"),
                           cv2.getTrackbarPos("V Max", "Threshold Configuration")])
    mask = cv2.inRange(hsv, lower_palm, upper_palm)
    kernel = np.ones((11,11), np.uint8)
    mask = cv2.medianBlur(mask, 11) #filter spatial
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel) #morphology closing
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel) #morphology opening

    # Overlay informasi ke frame
    #overlay = frame.copy() #buat yang perlu opacity rendah, tapi kalo makan resource hapus aja. ga ngerti
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    font_color = (15, 2, 6)
    thickness = 2

    #overlay guidance frame
    height, width = frame.shape[:2]
    divider_x = width // 2
    divider_y = height // 2
    dead_width = int(width * 0.3)
    dead_height = int(height * 0.7)
    dead_x1 = divider_x - dead_width // 2
    dead_y1 = divider_y - 50
    dead_x2 = divider_x + dead_width // 2
    dead_y2 = divider_y + dead_height // 2
    cv2.line(frame, (divider_x, 0), (divider_x, height), (255, 0, 0), 2) #line vertikal
    cv2.line(frame, (0, divider_y), (width, divider_y), (255, 0, 0), 2) #line horizontal
    cv2.rectangle(frame,(dead_x1, dead_y1),(dead_x2, dead_y2),(200, 0, 0),2)

    #kotak kontur
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    active_controls = []
    control_map = {
        1: "WHISTLE",
        2: "HALT",
        3: "FIX",
        4: "GO"
    }
    for outliners in contours:
        area = cv2.contourArea(outliners) #simpan semua area kontur
        if area > 10000:
            x, y, w, h = cv2.boundingRect(outliners)
            center_x = x + w // 2
            center_y = y + h // 2
            if (dead_x1 <= center_x <= dead_x2 and dead_y1 <= center_y <= dead_y2):
                #pos = (20, height - 50)
                zone = None
            elif center_x < divider_x and center_y < divider_y:
                pos = (20, 90)
                zone = 1
            elif center_x >= divider_x and center_y < divider_y:
                pos = (width - 120, 90)
                zone = 2
            elif center_x < divider_x and center_y >= divider_y:
                pos = (20, height - 30)
                zone = 3
            else:
                pos = (width - 120, height - 30)
                zone = 4

            if zone is not None:
                active_controls.append(zone)
                cv2.rectangle(frame,(x, y),(x + w, y + h),(0, 255, 0),2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                #cv2.putText(frame, f"Zone {zone}", (x, y - 10), font, scale, (0, 255, 0), thickness)
                cv2.putText(frame, f"Zone: {zone}", (pos), font, scale*0.8, (0, 255, 0), thickness)

    #control key
    commands = []
    for zone in active_controls:
        commands.append(control_map[zone])

    #info overlay
    cv2.putText(frame, f"Resolution: {width} x {height}", (20, 30), font, scale, font_color, thickness)
    cv2.putText(frame, f"Channels: {channels}", (20, 60), font, scale, font_color, thickness)
    cv2.putText(frame, f"Controls: {active_controls}", (20, 90), font, scale, font_color, thickness)
    cv2.putText(frame, f"Commands: {commands}", (20, 120), font, scale, font_color, thickness)

    cv2.imshow("Camera Test - BGR", frame)
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