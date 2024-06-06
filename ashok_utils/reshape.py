# Description: This file contains functions to reshape the images to 512x512 with padding
import cv2
import numpy as np
import os
from PIL import Image

IMAGE_SIZE = 512

def check_shape(img_path):
    img = cv2.imread(img_path)
    print(img.shape)
    return img.shape
    

def preprocess_image(image_path,
                     save_path = None,
                     padding_color = "white"):
    """ preprocesses the image to 512x512 with padding"""
    # read the image
    image = cv2.imread(image_path)
    H, W, _ = image.shape
    # resize the image keeping the max dimension to 512
    is_H_max = H > W
    if is_H_max:
        new_H = 512
        new_W = int(W * 512 / H)
    else:
        new_W = 512
        new_H = int(H * 512 / W)
    image = cv2.resize(image, (new_W, new_H))
    # pad the image to 512x512
    pad_H = (512 - new_H) // 2
    pad_W = (512 - new_W) // 2
    # image = cv2.copyMakeBorder(image, pad_H, pad_H, pad_W, pad_W, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    if padding_color == "black":
        padding_color = [0, 0, 0]
    elif padding_color == "white":
        padding_color = [255, 255, 255]
    else:
        print("Invalid padding color. Using white padding")
        padding_color = [255, 255, 255]
    image = cv2.copyMakeBorder(image, pad_H, pad_H, pad_W, pad_W, cv2.BORDER_CONSTANT, value=padding_color)
    
    # save the image
    if save_path is not None:
        cv2.imwrite(save_path, image)
    return image

def preprocess_image_using_pil(image_path,
                               save_path = None):
    """ preprocesses the image to 512x512 with padding using PIL"""
    import PIL.ImageOps as ImageOps
    image = Image.open(image_path)
    # check if the image is square
    H, W = image.size
    if H == W:
        image = image.resize((512, 512))
    else:
        # resize the image keeping the max dimension to 512
        is_H_max = H > W
        if is_H_max:
            new_H = 512
            new_W = int(W * 512 / H)
        else:
            new_W = 512
            new_H = int(H * 512 / W)
        image = image.resize((new_W, new_H))
        # pad the image to 512x512
        pad_H = (512 - new_H) // 2
        pad_W = (512 - new_W) // 2
        image = ImageOps.expand(image, border=(pad_W, pad_H, pad_W, pad_H), fill='black')
    # resize to 512x512
    
    image = image.resize((512, 512))
    image = np.array(image)
    # save using PIL
    if save_path is not None:
        image = Image.fromarray(image)
        image.save(save_path)
    return image
                    
                    
def preprocess_image_using_ffmpeg(image_path,
                                  save_path = None):
    """ saves the image to 512x512 with padding using ffmpeg"""
    # read the image
    image = cv2.imread(image_path)
    H, W, _ = image.shape
    # resize the image keeping the max dimension to 512
    is_H_max = H > W
    if is_H_max:
        new_H = 512
        new_W = int(W * 512 / H)
    else:
        new_W = 512
        new_H = int(H * 512 / W)
    
    temp_path = image_path.replace(".", "_temp.")

    
    os.system("ffmpeg -i {} -vf scale={}:{} {}".format(image_path, new_W, new_H, temp_path))
    #save using padding
    os.system("ffmpeg -i {} -vf scale=512:512 -vf pad=512:512:0:0:black {}".format(temp_path, save_path))
    os.system("rm {}".format(temp_path))
    

def apply_to_dir(function,
                 input_dir,
                 output_dir):
    """ applies the function to all the images in the input_dir and saves the images in the output_dir"""
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        extensions = ["jpg", "jpeg", "png"]
        if file.endswith(tuple(extensions)):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file)
            function(input_path, output_path)
            print("Processed: ", input_path)
        else:
            print("Skipped: ", file)
    print("All images processed")
    