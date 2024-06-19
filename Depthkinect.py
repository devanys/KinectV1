import numpy as np
import cv2
from openni import openni2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def calculate_distance(depth_frame, face):
    x, y, w, h = face
    x_center = x + w // 2
    y_center = y + h // 2
    depth_value = depth_frame.get_buffer_as_uint16()[y_center * depth_frame.width + x_center]
    depth_in_meters = depth_value / 1000.0
    return depth_in_meters

def draw_face(frame, face):
    x, y, w, h = face
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

if __name__ == '__main__':
    openni2.initialize()
    dev = openni2.Device.open_any()
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    color_stream = dev.create_color_stream()
    color_stream.start()
    depth_scale_factor = 255.0 / depth_stream.get_max_pixel_value()
    cv2.namedWindow('depth')
    
    while True:
        
        depth_frame = depth_stream.read_frame()       
        h, w = depth_frame.height, depth_frame.width
        depth = np.ctypeslib.as_array(
            depth_frame.get_buffer_as_uint16()).reshape(h, w)     
        depth_uint8 = cv2.convertScaleAbs(depth, alpha=depth_scale_factor)
        depth_colored = cv2.applyColorMap(depth_uint8, cv2.COLORMAP_HSV)
        # Get color
        color_frame = color_stream.read_frame()
        color = np.ctypeslib.as_array(color_frame.get_buffer_as_uint8()).reshape(h, w, 3)
        color = cv2.cvtColor(color, cv2.COLOR_RGB2BGR)

        
        faces = detect_face(color)
        if len(faces) > 0:
            closest_face = min(faces, key=lambda face: face[2] * face[3])  # Select the face with smallest area
            distance_mm = calculate_distance(depth_frame, closest_face) * 1000
            print(f'Jarak: {distance_mm:.2f} mm')  # Print distance in millimeters
            cv2.putText(color, f'Jarak: {distance_mm:.2f} mm', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            draw_face(color, closest_face)

        
        depth_colored_small = cv2.resize(depth_colored, (320, 240))
        color_small = cv2.resize(color, (320, 240))

        
        cv2.imshow('depthRGB', depth_colored_small)
        cv2.imshow('color', color_small)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    depth_stream.stop()
    openni2.unload()
    cv2.destroyAllWindows()
