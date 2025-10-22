#!/bin/bash
# ============================================================
# convert_http_to_rtsp.sh
# Convert HTTP MJPEG stream to RTSP using FFmpeg + MediaMTX
# ============================================================

# ✅ Example usage:
# ./convert_http_to_rtsp.sh "http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard" camera1

# Exit immediately on error
set -e

# Check input arguments
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <HTTP_MJPEG_URL> <RTSP_PATH_NAME>"
  echo "Example: $0 'http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard' camera1"
  exit 1
fi

INPUT_URL="$1"
CAM_NAME="$2"
OUTPUT_URL="rtsp://127.0.0.1:8554/${CAM_NAME}"

echo "============================================================"
echo "🎥 Converting HTTP → RTSP Stream"
echo "------------------------------------------------------------"
echo "Input Stream:  $INPUT_URL"
echo "Output Stream: $OUTPUT_URL"
echo "============================================================"
sleep 1

# ✅ Start FFmpeg conversion
ffmpeg -fflags +genpts -use_wallclock_as_timestamps 1 -re \
  -i "$INPUT_URL" \
  -vf "fps=10,format=yuv420p,scale=trunc(iw/2)*2:trunc(ih/2)*2" \
  -c:v libx264 -preset ultrafast -tune zerolatency \
  -pix_fmt yuv420p -b:v 800k -maxrate 800k -bufsize 1600k \
  -rtsp_transport tcp \
  -f rtsp "$OUTPUT_URL"

# If ffmpeg exits normally
echo "✅ Conversion finished or stopped manually."