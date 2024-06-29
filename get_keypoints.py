import torch
import os
from huggingface_hub import HfApi
from pathlib import Path
from diffusers.utils import load_image
from PIL import Image
import numpy as np
# from controlnet_aux import OpenposeDetector
from external_libraries.controlnet_aux import OpenposeDetector

from diffusers import (
    ControlNetModel,
    StableDiffusionControlNetPipeline,
    UniPCMultistepScheduler,
)
    

# checkpoint = "lllyasviel/control_v11p_sd15_openpose"
# processor = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')



#     image = load_image(os.path.join(folder, i))
#     control_image = processor(image, hand_and_face=True)
#     control_image.save(os.path.join(output_folder, i))
    
    
class Openpose_detector_class:
    def __init__(self, checkpoint="lllyasviel/control_v11p_sd15_openpose"):
        self.processor = OpenposeDetector.from_pretrained(checkpoint)
        
    def __call__(self, image_path, hand_and_face=True, save_path=None):
        image = load_image(image_path)
        control_image = self.processor(image, hand_and_face=True)
        if save_path is not None:
            control_image.save(save_path)
        return control_image
    def get_keypoints_dir(self, folder, output_folder):
        for i in os.listdir(folder):
            image = load_image(os.path.join(folder, i))
            control_image = self.processor(image, hand_and_face=True)
            control_image.save(os.path.join(output_folder, i))
            
        