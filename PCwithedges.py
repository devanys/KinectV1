import numpy as np
import cv2
from primesense import openni2

openni2.initialize()

dev = openni2.Device.open_any()

rgb_stream = dev.create_color_stream()
depth_stream = dev.create_depth_stream()

resolution = (480, 640)
fps = 60

rgb_stream.set_video_mode(openni2.c_api.OniVideoMode(
    pixelFormat=openni2.c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
    resolutionX=resolution[1],
    resolutionY=resolution[0],
    fps=fps
))

depth_stream.set_video_mode(openni2.c_api.OniVideoMode(
    pixelFormat=openni2.c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
    resolutionX=resolution[1],
    resolutionY=resolution[0],
    fps=fps
))

rgb_stream.start()
depth_stream.start()

fx = 525.0 
fy = 525.0 
cx = (resolution[1] - 1) / 2  
cy = (resolution[0] - 1) / 2 

try:
    points = np.empty((0, 3), dtype=np.float32)

    while True:
        rgb_frame = rgb_stream.read_frame()
        rgb_data = rgb_frame.get_buffer_as_triplet()

        depth_frame = depth_stream.read_frame()
        depth_data = depth_frame.get_buffer_as_uint16()

        rgb_image = np.frombuffer(rgb_data, dtype=np.uint8).reshape(resolution[0], resolution[1], 3)
        depth_image = np.frombuffer(depth_data, dtype=np.uint16).reshape(resolution[0], resolution[1])

        rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

        depth_image = depth_image.astype(np.float32)

        # Filter out points that are too far or too close
        depth_thresh_min = 300  # Minimum depth threshold in mm
        depth_thresh_max = 8000  # Maximum depth threshold in mm
        depth_image[(depth_image < depth_thresh_min) | (depth_image > depth_thresh_max)] = np.nan

        # Subsample depth image
        subsample_factor = 1
        depth_image = depth_image[::subsample_factor, ::subsample_factor]

        # Perform bilateral filtering on depth image
        depth_image = cv2.bilateralFilter(depth_image, 5, 50, 50)

        # Create grid of indices
        u, v = np.meshgrid(np.arange(0, resolution[1], subsample_factor), np.arange(0, resolution[0], subsample_factor))

        # Calculate 3D coordinates
        x = (u - cx) * depth_image / fx
        y = (v - cy) * depth_image / fy
        z = depth_image

        # Filter points with valid depth
        valid_indices = ~np.isnan(z)
        new_points = np.column_stack((x[valid_indices], y[valid_indices], z[valid_indices]))
        points = np.vstack((points, new_points))

        # Draw points on RGB image
        for point in new_points:
            u, v, _ = point.astype(int)
            cv2.circle(rgb_image, (u, v), radius=1, color=(0, 255, 0), thickness=-1)

        # Perform edge detection on depth image
        edges = cv2.Canny(depth_image.astype(np.uint8), 50, 150)  # Adjust the threshold values if needed

        # Draw edges on RGB image
        rgb_image[::subsample_factor, ::subsample_factor][edges > 0] = [0, 0, 255]

        # Display raw depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imshow('Raw Depth', depth_colormap)

        # Display the RGB image with edges
        cv2.imshow('PointCloud with Edges', rgb_image)

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
