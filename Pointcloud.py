import numpy as np
import cv2
from primesense import openni2

# Initialize OpenNI
openni2.initialize()

# Open a device
dev = openni2.Device.open_any()

# Create RGB and depth streams
rgb_stream = dev.create_color_stream()
depth_stream = dev.create_depth_stream()

# Configure the streams
rgb_stream.set_video_mode(openni2.c_api.OniVideoMode(
    pixelFormat=openni2.c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
    resolutionX=640,
    resolutionY=480,
    fps=60
))

depth_stream.set_video_mode(openni2.c_api.OniVideoMode(
    pixelFormat=openni2.c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
    resolutionX=640,
    resolutionY=480,
    fps=30
))

# Start the streams
rgb_stream.start()
depth_stream.start()

# Camera intrinsic parameters
fx = 525.0  # Focal length in x-axis
fy = 525.0  # Focal length in y-axis
cx = 319.5  # Optical center in x-axis
cy = 239.5  # Optical center in y-axis

try:
    while True:
        # Read a frame from the RGB stream
        rgb_frame = rgb_stream.read_frame()
        rgb_data = rgb_frame.get_buffer_as_triplet()

        # Read a frame from the depth stream
        depth_frame = depth_stream.read_frame()
        depth_data = depth_frame.get_buffer_as_uint16()

        # Convert the frame to a numpy array and normalize it
        rgb_image = np.frombuffer(rgb_data, dtype=np.uint8).reshape(480, 640, 3)
        depth_image = np.frombuffer(depth_data, dtype=np.uint16).reshape(480, 640)
        depth_image = np.float32(depth_image)

        # Convert RGB image from RGB to BGR for OpenCV
        rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

        # Create a list of points for point cloud
        points = []

        for v in range(depth_image.shape[0]):
            for u in range(depth_image.shape[1]):
                z = depth_image[v, u]
                if z > 0:
                    x = (u - cx) * z / fx
                    y = (v - cy) * z / fy
                    points.append((int(x), int(y)))

        # Draw points on RGB image
        for point in points:
            cv2.circle(rgb_image, point, radius=1, color=(0, 255, 0), thickness=-1)

        # Display the RGB image with points
        cv2.imshow('Point Cloud', rgb_image)

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop the streams and close OpenNI
    rgb_stream.stop()
    depth_stream.stop()
    openni2.unload()

    # Close OpenCV windows
    cv2.destroyAllWindows()
