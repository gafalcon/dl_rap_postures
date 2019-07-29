import json
import sys
import glob

points = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"]
columns = [[point+"_x", point+"_y"] for point in points]
columns = ["Frame"] + sum(columns, [])
print("Num points", len(points))
print(columns)
def create_dataset(filedir):
    files = glob.glob(f"{filedir}/*json")
    files = sorted(files)
    print(files[:15])
    outfile = open(filedir+".csv", "w")

    outfile.write(",".join(columns) + "\n")
    for frame, f in enumerate(files, 1):
        with open(f, "r") as jsonfile:
            jfile = json.load(jsonfile)
            if len(jfile["people"]) != 0:
                keypoints = jfile["people"][0]["pose_keypoints_2d"]
                keypoints2 = []
                for i in range(0, len(keypoints), 3):
                    keypoints2.append(str(keypoints[i]))
                    keypoints2.append(str(keypoints[i+1]))

                print(keypoints2, len(keypoints2))
                outfile.write(f"{frame}," + ",".join(keypoints2) + "\n")
            else:
                outfile.write(f"{frame},"+ ",".join(["0"]*(len(points)*2)) + "\n")
    outfile.close()

files = glob.glob("C:/Users/gabof/Downloads/rap_videos/Nolabeled/*avi")
print(files)
for f in files:
    print(f[:-4])
    # create_dataset("C:/Users/gabof/Downloads/rap_videos/gabrielBad4")
    create_dataset(f[:-4])