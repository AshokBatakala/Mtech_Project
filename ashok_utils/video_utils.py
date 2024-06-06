import os


def image_to_video(image_path, video_path, time=0.5):
    # os.system("ffmpeg -loop 1 -i {} -c:v libx264 -t {} -pix_fmt yuv420p {}".format(image_path, time, video_path))
    # Unknown encoder 'libx264'; so use some other encoder
    os.system("ffmpeg -loop 1 -i {} -c:v mpeg4 -t {} -pix_fmt yuv420p {}".format(image_path, time, video_path))



def extract_frames(video_path, output_folder):
    os.system("mkdir -p {}".format(output_folder))
    os.system("ffmpeg -i {} -vf fps=1 {}/%04d.png".format(video_path, output_folder))
    print("Frames extracted to {}".format(output_folder))
    