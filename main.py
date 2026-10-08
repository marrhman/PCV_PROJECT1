import cv2
from vision import get_controls

cv2.namedWindow("Threshold Configuration")
cv2.createTrackbar("H Min", "Threshold Configuration", 7, 179, lambda x: None)
cv2.createTrackbar("H Max", "Threshold Configuration", 22, 179, lambda x: None)
cv2.createTrackbar("S Min", "Threshold Configuration", 45, 255, lambda x: None)
cv2.createTrackbar("S Max", "Threshold Configuration", 160, 255, lambda x: None)
cv2.createTrackbar("V Min", "Threshold Configuration", 80, 255, lambda x: None)
cv2.createTrackbar("V Max", "Threshold Configuration", 220, 255, lambda x: None)

h_min = cv2.getTrackbarPos("H Min", "Threshold Configuration")
s_min = cv2.getTrackbarPos("S Min", "Threshold Configuration")
v_min = cv2.getTrackbarPos("V Min", "Threshold Configuration")
h_max = cv2.getTrackbarPos("H Max", "Threshold Configuration")
s_max = cv2.getTrackbarPos("S Max", "Threshold Configuration")
v_max = cv2.getTrackbarPos("V Max", "Threshold Configuration")

video_cam = cv2.VideoCapture(0)

while True:
    safe_status, frame = video_cam.read()
    if not safe_status:
        print("Camera Not Working")
        break
    frame = cv2.flip(frame, 1)

    active_controls, commands, mask, detected_objects, divider_x, divider_y, dead_x1, dead_y1, dead_x2, dead_y2 = get_controls(frame, h_min, s_min, v_min, h_max, s_max, v_max)

    # Overlay informasi ke frame
    #overlay = frame.copy() #buat yang perlu opacity rendah, tapi kalo makan resource hapus aja. ga ngerti
    height, width, channels = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.7
    font_color = (15, 2, 6)
    thickness = 2

    #zones overlay
    cv2.line(frame, (divider_x, 0), (divider_x, height), (255, 0, 0), 2) #line vertikal
    cv2.line(frame, (0, divider_y), (width, divider_y), (255, 0, 0), 2) #line horizontal
    cv2.rectangle(frame,(dead_x1, dead_y1),(dead_x2, dead_y2),(200, 0, 0),2)

    for x, y, w, h, center_x, center_y, pos, zone in detected_objects:
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
        if zone is not None:
            cv2.rectangle(frame,(x, y),(x + w, y + h),(0, 255, 0),2)
            #cv2.putText(frame, f"Zone {zone}", (x, y - 10), font, scale, (0, 255, 0), thickness)
            cv2.putText(frame, f"Zone: {zone}", (pos), font, scale*0.8, (0, 255, 0), thickness)

    #info overlay
    cv2.putText(frame, f"Resolution: {width} x {height}", (20, 30), font, scale, font_color, thickness)
    cv2.putText(frame, f"Channels: {channels}", (20, 60), font, scale, font_color, thickness)
    cv2.putText(frame, f"Controls: {active_controls}", (20, 90), font, scale, font_color, thickness)
    cv2.putText(frame, f"Commands: {commands}", (20, 120), font, scale, font_color, thickness)

    cv2.imshow("Camera", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_cam.release()
cv2.destroyAllWindows()
