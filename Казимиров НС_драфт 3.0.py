import cv2
import numpy as np
import math
import time

# Параметры камеры
focal_length = 1.8  # Фокусное расстояние объектива в мм
sensor_width = 5.64  # Размер матрицы в мм
frame_width = 1920  # Ширина кадра
frame_height = 1080  # Высота кадра

# Рассчитываем угол обзора камеры
fov_horizontal = 2 * math.atan((sensor_width / 2) / focal_length)
fov_vertical = 2 * math.atan((sensor_width * frame_height / frame_width) / 2 / focal_length)

# Функция для распознавания самолёта
def detect_airplane(frame):
    # Конвертируем изображение в градации серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Применяем пороговое преобразование для выделения самолёта
    _, thresholded = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    # Находим контуры
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        image_area = frame.shape[0] * frame.shape[1]
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) < image_area * 0.02]
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            return cv2.boundingRect(max_contour)
    return None

def draw_axes(frame):
    cv2.line(frame, (frame_width // 2, 0), (frame_width // 2, frame_height), (0, 0, 255), 2)
    cv2.line(frame, (0, frame_height // 2), (frame_width, frame_height // 2), (0, 0, 255), 2)

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    # Инициализация переменных для FPS
    fps_counter = 0
    fps_display = "FPS: 0"
    time_start = time.time()

    # Определение центра кадра
    center_x, center_y = frame_width // 2, frame_height // 2

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        airplane = detect_airplane(frame)
        if airplane:
            x, y, w, h = airplane
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            pixel_size_mm = sensor_width / frame_width
            airplane_width_real_meters = 50
            distance_to_airplane_meters = (airplane_width_real_meters * focal_length) / (w * pixel_size_mm)
            pixel_size_meters = (2 * math.tan(fov_horizontal / 2) * distance_to_airplane_meters) / frame_width
            deviation_x_meters = (x + w // 2 - center_x) * pixel_size_meters
            deviation_y_meters = (y + h // 2 - center_y) * pixel_size_meters
            cv2.putText(frame, f"Distance: {distance_to_airplane_meters:.2f}m", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"X deviation: {deviation_x_meters:.2f}m", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Y deviation: {deviation_y_meters:.2f}m", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Расчет и вывод FPS
        fps_counter += 1
        time_now = time.time()
        if (time_now - time_start) >= 1.0:  # Обновление FPS каждую секунду
            fps_display = f"FPS: {fps_counter / (time_now - time_start):.2f}"
            time_start = time_now
            fps_counter = 0
        
        # Выводим FPS под отклонениями
        cv2.putText(frame, fps_display, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
        draw_axes(frame)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

process_video('example.mp4')

