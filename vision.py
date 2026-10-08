import cv2, numpy as np

def get_controls(frame, h_min, s_min, v_min, h_max, s_max, v_max):
    # BGR ke HSV agar mudah atur cahaya
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #thresholding for masking
    #ambil nilai trackbar
    lower_palm = np.array([h_min, s_min, v_min])
    upper_palm = np.array([h_max, s_max, v_max])
    #buat threshold dengan filter
    mask = cv2.inRange(hsv, lower_palm, upper_palm)
    mask = cv2.medianBlur(mask, 11) #filter spatial
    kernel = np.ones((11,11), np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel) #morphology closing
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel) #morphology opening

    #mapping frame
    height, width = frame.shape[:2]
    divider_x = width // 2
    divider_y = height // 2
    dead_width = int(width * 0.3)
    dead_height = int(height * 0.7)
    dead_x1 = divider_x - dead_width // 2
    dead_y1 = divider_y - 50
    dead_x2 = divider_x + dead_width // 2
    dead_y2 = divider_y + dead_height // 2

    #kotak kontur
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected_objects = []
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
            pos = (0, 0)
            if (dead_x1 <= center_x <= dead_x2 and dead_y1 <= center_y <= dead_y2):
                #pos = (20, height - 50)
                zone = None
            elif center_x < divider_x and center_y < divider_y:
                pos = (20, height - 50)
                zone = 1
            elif center_x >= divider_x and center_y < divider_y:
                pos = (width - 120, height - 50)
                zone = 2
            elif center_x < divider_x and center_y >= divider_y:
                pos = (20, height - 30)
                zone = 3
            else:
                pos = (width - 120, height - 30)
                zone = 4

            if zone is not None:
                active_controls.append(zone)
            detected_objects.append((x, y, w, h, center_x, center_y, pos, zone))

    #control key
    commands = []
    for zone in active_controls:
        commands.append(control_map[zone])

    return active_controls, commands, mask, detected_objects, divider_x, divider_y, dead_x1, dead_y1, dead_x2, dead_y2
