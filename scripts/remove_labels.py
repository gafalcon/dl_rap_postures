import glob
import cv2
import os
import sys

dir="C:/Users/gabof/Downloads/rap_videos/Unlabeled"
videos = glob.glob(dir + "/*avi")
for video in videos:
    print(video)
    vidname=os.path.basename(video).split(".")[0]
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print("Error openning video!")
        cap.release()
        sys.exit()
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter(vidname+"_no_lbl.avi",cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))
    while(True):
        ret, frame = cap.read()
        if ret == True: 
            # Write the frame into the file 'output.avi'
            cv2.rectangle(frame, (0,0), (200,50), (0,0,0),-1)
            cv2.imshow(vidname,frame)
            out.write(frame)
            # Display the resulting frame    
            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break 
    cap.release()
    out.release()
 
    # Closes all the frames
    cv2.destroyAllWindows() 