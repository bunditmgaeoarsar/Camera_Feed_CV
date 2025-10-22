import cv2
import os
import time
import logging
from datetime import datetime

# ==============================
#  CONFIGURATION
# ==============================
CAMERA_FILE = "camera_urls.txt"
LOG_FILE = "simple_stream_log.txt"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================
#  LOGGING SETUP
# ==============================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ==============================
#  LOAD CAMERA URLS
# ==============================
def load_camera_list(file_path):
    """Load camera names and URLs from text file."""
    cameras = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                name, url = line.split(",", 1)
                cameras[name.strip()] = url.strip()
            except ValueError:
                logging.warning(f"Skipping malformed line: {line}")
    return cameras

# ==============================
#  CAPTURE SNAPSHOT
# ==============================
def capture_snapshot(name, url, max_wait=10):
    """Try to connect and capture a single frame from the stream."""
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    start_time = time.time()

    # Wait for connection
    while not cap.isOpened() and (time.time() - start_time) < max_wait:
        time.sleep(1)
        cap.open(url)

    if not cap.isOpened():
        logging.warning(f"{name} |  Connection failed | {url}")
        return None

    # Try reading a few frames
    success, frame = False, None
    for _ in range(5):
        success, frame = cap.read()
        if success and frame is not None:
            break
        time.sleep(0.5)

    cap.release()

    if success and frame is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(filepath, frame)
        logging.info(f"{name} |  Connected | {url} | Snapshot: {filepath}")
        return filepath
    else:
        logging.warning(f"{name} | ⚠️ Connected but no valid frame | {url}")
        return None

# ==============================
#  MAIN
# ==============================
if __name__ == "__main__":
    if not os.path.exists(CAMERA_FILE):
        print(f" Error: '{CAMERA_FILE}' not found.")
        exit(1)

    print("📸 Checking simple camera connections...\n")

    cameras = load_camera_list(CAMERA_FILE)

    for name, url in cameras.items():
        print(f"🔍 Checking {name}...")
        capture_snapshot(name, url)
        time.sleep(1)

    print("\n All cameras checked!")
    print(f" Log saved to: {LOG_FILE}")
    print(f" Snapshots saved in: {OUTPUT_DIR}/")