import cv2
import os
import sys

id_to_posture = ["bolsillos", "brazos_cruzados", "gesticulando", "manos abajo", "manos atrás", "manos juntas", "apuntando"]

def tag_image(frame, frame_n, img_dir):
    keypressed = cv2.waitKey(0) & 0xFF
    i = 0
    while keypressed != ord(str(i)) and i < 7:
        i+=1
    if i < 7:
        cv2.imwrite(f"{img_dir}/frame{frame_n}_{i}.jpg", frame)

def tag_video(videofile):
    cap = cv2.VideoCapture(videofile)
    vidname = os.path.basename(videofile).split(".")[0]
    if not os.path.exists(vidname):
        os.mkdir(vidname)
    # Check if camera opened successfully
    if (cap.isOpened() == False): 
      print("Unable to read camera feed")
      sys.exit()

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    row = 0
    velocity = 100
    for i, posture in enumerate(id_to_posture):
        print(f"{i}: {posture}")
    while(True):
        ret, frame = cap.read()
        if ret == True: 
            # Display the resulting frame    
            cv2.imshow(vidname,frame)
            # Press Q on keyboard to stop recording

            keypressed = cv2.waitKey(velocity) & 0xFF
            if keypressed == ord('p'):
                tag_image(frame, row, vidname)
            elif keypressed == ord('+'):
                velocity -= 20
                print("Increasing velocity", velocity)
            elif keypressed == ord('-'):
                velocity += 20
                print("Decreasing velocity", velocity)
            elif keypressed == ord('q'):
                break
            row += 1
        else:
            break 
 
    # When everything done, release the video capture and video write objects
    cap.release()
 
    # Closes all the frames
    cv2.destroyAllWindows() 

if len(sys.argv) < 2:
    print("Use: python tagging_video.py videofile")
videofile = sys.argv[1]
tag_video(videofile)