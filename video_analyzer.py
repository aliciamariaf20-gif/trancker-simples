import cv2
from collections import Counter

def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, first_frame = cap.read()
    if not ret:
        return {"error": "Invalid video"}

    # ⚠️ ROI fixo temporário (Render não abre janela)
    h, w, _ = first_frame.shape
    roi = (w//4, h//3, w//6, h//4)

    tracker = cv2.TrackerCSRT_create()
    tracker.init(first_frame, roi)

    positions = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ok, bbox = tracker.update(frame)
        if ok:
            x, y, bw, bh = bbox
            cx = int(x + bw / 2)
            cy = int(y + bh / 2)
            positions.append((cx, cy))

    cap.release()

    if len(positions) < 10:
        return {"error": "Tracking failed"}

    frame_width = w
    last_positions = positions[-30:]

    zones = [zone(p[0], frame_width) for p in last_positions]
    count = Counter(zones)

    final_zone = count.most_common(1)[0][0]
    confidence = round((count[final_zone] / len(zones)) * 100, 2)

    final_x, final_y = last_positions[-1]

    return {
        "resultado_final": final_zone,
        "coordenadas": {"x": final_x, "y": final_y},
        "confianca": f"{confidence}%"
    }

def zone(x, width):
    third = width // 3
    if x < third:
        return "esquerda"
    elif x < 2 * third:
        return "meio"
    return "direita"
