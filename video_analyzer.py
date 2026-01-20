import cv2

def analyze_video(video_path, x, y):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        return {"error": "Não foi possível ler o vídeo"}

    tracker = cv2.TrackerCSRT_create()
    bbox = (x - 25, y - 25, 50, 50)
    tracker.init(frame, bbox)

    last_x, last_y = x, y

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        success, box = tracker.update(frame)
        if success:
            bx, by, bw, bh = box
            last_x = int(bx + bw / 2)
            last_y = int(by + bh / 2)

    cap.release()

    return {
        "x": last_x,
        "y": last_y,
        "position": "esquerda" if last_x < frame.shape[1] / 3 else
                    "meio" if last_x < 2 * frame.shape[1] / 3 else
                    "direita",
        "confidence": 0.85
    }
