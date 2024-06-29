import os


def image_to_video(image_path, video_path, time=0.5):
    # os.system("ffmpeg -loop 1 -i {} -c:v libx264 -t {} -pix_fmt yuv420p {}".format(image_path, time, video_path))
    # Unknown encoder 'libx264'; so use some other encoder
    
    #if video_path exists throw error
    if os.path.exists(video_path):
        # raise ValueError("Video path already exists")
        #delete it 
        print("Video path already exists, deleting it")
        os.system("rm {}".format(video_path))
    
    # os.system("ffmpeg -loop 1 -i {} -c:v mpeg4 -t {} -pix_fmt yuv420p {}".format(image_path, time, video_path))
    
    # output_size should be 512x512
    os.system("ffmpeg -loop 1 -i {} -c:v mpeg4 -t {} -vf scale=512:512 -pix_fmt yuv420p {}".format(image_path, time, video_path))


def image_to_video_folder(images_folder,videos_folder, time=0.5):
    os.system("mkdir -p {}".format(videos_folder))
    for image in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image)
        video_path = os.path.join(videos_folder, image.split(".")[0]+".mp4")
        image_to_video(image_path, video_path, time)
    print("Videos created in {}".format(videos_folder))
    
def extract_frames(video_path, output_folder, fps=25):

    os.system("mkdir -p {}".format(output_folder))
    # os.system("ffmpeg -i {} -vf fps=1 {}/%04d.png".format(video_path, output_folder))
    os.system("ffmpeg -i {} -vf fps={} {}/%04d.png".format(video_path, fps, output_folder))
    print("Frames extracted to {}".format(output_folder), "with fps", fps)
    
def images2video(images_folder, video_path, fps=25):
    # os.system("ffmpeg -framerate {} -i {}/%04d.png -c:v mpeg4 -vf scale=512:512 -pix_fmt yuv420p {}".format(fps, images_folder, video_path))
    # [image2 @ 0x562257fae780] Could find no file with path '/media/test/D/Ashok_Batakala_folder/Ashok_temp_data/tiktok_d/seg_fat_n08/%04d.png' and index in the range 0-4

    # images are not named from 0000.png, so use globbing
    os.system("ffmpeg -framerate {} -pattern_type glob -i '{}/*.png' -c:v mpeg4 -vf scale=512:512 -pix_fmt yuv420p {}".format(fps, images_folder, video_path))
    
    
    print("Video created at", video_path, "with fps", fps)