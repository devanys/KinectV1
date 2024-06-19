import numpy as np
import cv2
from primesense import openni2


openni2.initialize()


dev = openni2.Device.open_any()


ir_stream = dev.create_ir_stream()


ir_stream.set_video_mode(openni2.c_api.OniVideoMode(
    pixelFormat=openni2.c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16,
    resolutionX=640,
    resolutionY=480,
    fps=30
))


ir_stream.start()


cv2.namedWindow('Infrared', cv2.WINDOW_NORMAL)

try:
    while True:
        ir_frame = ir_stream.read_frame()
        ir_data = ir_frame.get_buffer_as_uint16()

        ir_image = np.frombuffer(ir_data, dtype=np.uint16).reshape(480, 640)
        ir_image = cv2.normalize(ir_image, None, 0, 255, cv2.NORM_MINMAX)
        ir_image = np.uint8(ir_image)

        cv2.imshow('Infrared', ir_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    ir_stream.stop()
    openni2.unload()

# Close the window
cv2.destroyAllWindows()
