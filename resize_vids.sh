#Resize and remove audio
vids=$(ls /c/Users/gabof/Downloads/rap_videos/train_videos/*mp4)
for video in $vids
do 
    directory=$(echo $video | cut -d "_" -f 2)
    # nname=$(echo ${video::-8})
    # echo $nname
    /c/Users/gabof/Downloads/ffmpeg/bin/ffmpeg.exe -i $video -s 1280x960 -c:a copy -an "${video}_res.mp4"
done