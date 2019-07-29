import os
import glob
import sys
import cv2
import pandas as pd

bones = [("LEar", "LEye"), ("REar", "REye"),("LEye", "Nose"), ("REye", "Nose"), 
("Nose", "Neck"), ("Neck", "RShoulder"), ("Neck", "LShoulder"), ("LShoulder", "LElbow"), 
("LElbow", "LWrist"), ("RShoulder", "RElbow"), ("RElbow", "RWrist"), ("Neck", "MidHip"),
 ("MidHip", "LHip"), ("LHip", "LKnee"), ("LKnee", "LAnkle"), ("LAnkle", "LHeel"), 
 ("LAnkle", "LBigToe"), ("LBigToe", "LSmallToe"), ("MidHip", "RHip"), ("RHip", "RKnee"),
  ("RKnee", "RAnkle"), ("RAnkle", "RHeel"), ("RAnkle", "RBigToe"), ("RBigToe", "RSmallToe")]

# bones = [
#     # ("lear", "leye"),
#     # ("rear", "reye"),
#     # ("reye", "nose"),
#     # ("reye", "nose"), 
#     ("nose", "neck"),
#     ("neck", "rshoulder"),
#     ("neck", "lshoulder"),
#     ("lshoulder", "lelbow"), 
#     ("lelbow", "lwrist"),
#     ("rshoulder", "relbow"), 
#     ("relbow", "rwrist"), 
#     ("neck", "rhip"),
#     ("neck", "lhip"), 
#     ("lhip", "lknee"), 
#     ("lknee", "lankle"),
#     ("rhip", "rknee"),
#     ("rknee", "rankle")
#     ]

def validate_join(joint):
    return joint[0] != 0 and joint[1] != 0

def create_skeleton(frame, line):
    for joint1, joint2 in bones:
        j1 = int(line[joint1+"_x"]), int(line[joint1+"_y"])
        j2 = int(line[joint2+"_x"]), int(line[joint2+"_y"])
        if validate_join(j1) and validate_join(j2):
           cv2.line(frame, j1, j2,(0,0,255),5) 

def draw_joints(frame, line):
    for i in range(1, len(line.index), 2):
        center = int(line[i]), int(line[i+1])
        if validate_join(center):
            cv2.circle(frame, center, 5, (0,255,0), thickness=1, lineType=8, shift=0)

def create_video(videofile, csvfile):
    df = pd.read_csv(csvfile)
    df.columns = [col.strip() for col in df.columns]
    cap = cv2.VideoCapture(videofile)
    vidname = os.path.basename(videofile).split(".")[0]
    # Check if camera opened successfully
    if (cap.isOpened() == False): 
      print("Unable to read camera feed")
      sys.exit()

    property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
    length = int(cv2.VideoCapture.get(cap, property_id))
    df_len = len(df)
    if length != df_len:
        print("Length of video({}) doesnt match len of df({})!".format(length, df_len))
        sys.exit()
    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter(vidname+"_skeleton.avi",cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

    row = 0
    while(True):
        ret, frame = cap.read()
        if ret == True: 
            # Write the frame into the file 'output.avi'
            linea = df.iloc[row, :]
            draw_joints(frame, linea)
            create_skeleton(frame, linea)
            out.write(frame)
            # Display the resulting frame    
            cv2.imshow(vidname,frame)
            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            row += 1
        else:
            break 
 
    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()
 
    # Closes all the frames
    cv2.destroyAllWindows() 


videofile = sys.argv[1]
csvfile = sys.argv[2]
print(videofile, csvfile)
create_video(videofile, csvfile)