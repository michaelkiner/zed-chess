import pyzed.sl as sl
import cv2
from datetime import datetime

# Create ZED camera
zed = sl.Camera()

# Camera parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD2K
init_params.camera_fps = 15

# Open camera
status = zed.open(init_params)
if status != sl.ERROR_CODE.SUCCESS:
    print(f"Failed to open camera: {status}")
    exit(1)

# Let auto exposure stabilize
for _ in range(30):
    zed.grab()

image = sl.Mat()

print("Press ENTER to save an image.")
print("Press 'q' to quit.")

while True:
    if zed.grab() != sl.ERROR_CODE.SUCCESS:
        continue

    zed.retrieve_image(image, sl.VIEW.LEFT)

    # Convert ZED image (RGBA) to OpenCV image (BGR)
    frame = image.get_data()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    cv2.imshow("ZED Camera", frame)

    key = cv2.waitKey(1)

    # Enter key
    if key == 13:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"zed_{timestamp}.png"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

    # q key
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
zed.close()