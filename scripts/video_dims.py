import cv2
import glob
import os

# directory = "C:/Users/gabof/Downloads/rap_videos/examples_vid"
# vids = glob.glob(f"{directory}/*mp4")
directory = "C:/Users/gabof/Downloads/rap_videos/"
vids = glob.glob(f"{directory}/*avi")
print(vids)

for video in vids:
    video = os.path.basename(video)
    cap = cv2.VideoCapture(f"{directory}/{video}")
    
    if not cap.isOpened():
        print("Error reading video", video)
        continue
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    print(video, frame_width, frame_height)
    cap.release()