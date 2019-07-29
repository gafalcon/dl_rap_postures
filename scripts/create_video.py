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

joints = ["LEar", "REar", "REye", "LEye", "Nose", "Neck", "RShoulder", "LShoulder", "LElbow", "RElbow", 
"LWrist", "RWrist", "MidHip", "RHip", "LHip", "LKnee", "RKnee", "LAnkle", "RAnkle", "RHeel", "LHeel", "RBigToe",
"LBigToe", "LSmallToe", "RSmallToe"]

id_to_posture = ["bolsillos", "brazos_cruzados", "gesticulando", "manos abajo", "manos atrás", "manos juntas", "apuntando"]

def validate_joint(joint):
    return joint[0] != 0 and joint[1] != 0

def create_skeleton(frame, line):
    for joint1, joint2 in bones:
        j1 = int(line[joint1+"_x"]), int(line[joint1+"_y"])
        j2 = int(line[joint2+"_x"]), int(line[joint2+"_y"])
        if validate_joint(j1) and validate_joint(j2):
           cv2.line(frame, j1, j2,(0,255,0),5) 

def draw_joints(frame, line, i_start):
    for joint in joints:
        center = int(line[joint+"_x"]), int(line[joint+"_y"])
        if validate_joint(center):
            cv2.circle(frame, center, 7, (0,255,255), thickness=2, lineType=8, shift=0)

def print_preds(frame, line):
    pred_b = "Good" if line["pred_b"] >= 0.5 else "Bad"
    predb_color = (0,255,0) if pred_b == "Good" else (0, 0, 255)
    pred = id_to_posture[int(line["pred"])]
    pred_color = (0, 255, 0) if pred in ("gesticulando", "apuntando") else (0, 0,255)
    cv2.putText(frame, pred_b, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, predb_color, 1)
    cv2.putText(frame, pred, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, pred_color, 1)


def create_video(videofile, csvfile):
    df = pd.read_csv(csvfile)
    df.columns = [col.strip() for col in df.columns]
    write_preds = "pred" in df.columns
    if write_preds:
        print("Writing Predictions...")
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

    i_start = df.columns.values.tolist().index("Nose_x")
    row = 0
    while(True):
        ret, frame = cap.read()
        if ret == True: 
            # Write the frame into the file 'output.avi'
            linea = df.iloc[row, :]
            draw_joints(frame, linea, i_start)
            create_skeleton(frame, linea)
            if write_preds:
                print_preds(frame, linea)
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

if len(sys.argv) < 3:
    print("Use: python create_video.py videofile csvfile ")
videofile = sys.argv[1]
csvfile = sys.argv[2]
print(videofile, csvfile)
create_video(videofile, csvfile)