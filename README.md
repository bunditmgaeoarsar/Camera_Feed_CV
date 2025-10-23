# 🎥 Camera Feed Computer Vision (CV) Project

This project allows you to:
- Monitor multiple live camera streams (HTTP, RTSP)
- Check connection 
- Capture snapshots of online streams
- Convert HTTP MJPEG feeds into RTSP streams using **FFmpeg + MediaMTX**

---

## 🧩 Step 1: Clone the Repository

```bash
git clone https://github.com/bunditmgaeoarsar/Camera_Feed_CV.git
cd Camera_Feed_CV
```

## ⚙️ Step 2: Install Required Software

This project requires:

-   **Python 3.9+**
    
-   **FFmpeg**
    
-   **MediaMTX (RTSP server)**
    

### 🐍 Install Python

Check if Python is installed:
```bash
python3 --version
```
If not, install it via Homebrew (macOS/Linux):
```bash
brew install python
```
### 🎞️ Install FFmpeg

FFmpeg is required to convert and stream video feeds.
```bash
brew install ffmpeg
```
To verify:
```bash
ffmpeg -version
```
### 📡 Install MediaMTX

MediaMTX (formerly `rtsp-simple-server`) is the RTSP streaming server.
```bash
brew install mediamtx
```
Or manually download it from:   [https://github.com/bluenviron/mediamtx](https://github.com/bluenviron/mediamtx)

Check version:
```bash
mediamtx --version
```
## 🧱 Step 3: Create a Python Virtual Environment

Inside the project folder, create a `venv`:
```bash
python3 -m venv venv
```

----------

## 📦 Step 4: Install Packages from `requirements.txt`

Activate your environment (see next step), then install the dependencies.

----------

## 🧠 Step 5: Activate the Virtual Environment

### On macOS / Linux:
```bash
source venv/bin/activate
```
### On Windows (PowerShell):
```bash
.\venv\Scripts\Activate.ps1
```
Once activated, install packages:
```bash
pip install -r requirements.txt
```
## 📝 Step 6: Edit `camera_urls.txt`

Open the file `camera_urls.txt` and add your camera names and URLs.

Example:
```
Exterior Street View,http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard
Interior Warehouse View,http://61.211.241.111/nphMotionJpeg?Resolution=320x240&Quality=Standard
```

Each line represents one camera feed (HTTP or RTSP).

----------

## 🔍 Step 7: Run the Stream Checker

The script `simple_stream_check.py` will:

-   Check each camera connection
    
-   Log results in `simple_stream_log.txt`
    
-   Save snapshots in `output/`
    

Run:
```bash
python3 simple_stream_check.py
```
Output example:
<img width="1580" height="65" alt="image" src="https://github.com/user-attachments/assets/1632e2c8-5af3-4d71-8573-10822cc7a6ea" />


## Convert HTTP (MJPEG) to RTSP Streams

If you have an HTTP MJPEG stream that you want to use as an RTSP source (for CV models, or to unify feeds),  
you can use the provided **`convert_http_to_rtsp.sh`** script.

### Step 1: Start MediaMTX

### Step 2: Run the conversion
```bash
./convert_http_to_rtsp.sh "http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard" live
```

This will:

-   Read from the MJPEG source
    
-   Transcode it via FFmpeg
    
-   Re-stream it via MediaMTX as:
    
    `rtsp://127.0.0.1:8554/camera1` 
    

💡 You can open this in VLC or OpenCV directly.


----------

## 🧩 4. Re-run Stream Checker with RTSP Feeds

Once your HTTP streams are converted and listed in `camera_urls.txt` (as RTSP URLs),  
you can re-run:
```bash
python3 simple_stream_check.py
```
You’ll now be checking **RTSP streams** (from MediaMTX) instead of raw HTTP MJPEG links.
